import asyncio
import re
import subprocess
import time
from dataclasses import replace
from pathlib import Path
from typing import Any, AsyncIterator, Optional, Set
from uuid import uuid4 as uuid

import aiodocker
import pytest
from yarl import URL

from neuro_sdk import CONFIG_ENV_NAME, DEFAULT_CONFIG_PATH, JobStatus

from tests.e2e import Helper


def parse_docker_ls_output(docker_ls_output: Any) -> Set[str]:
    return {
        repo_tag
        for info in docker_ls_output
        if info["RepoTags"] is not None
        for repo_tag in info["RepoTags"]
        if repo_tag
    }


@pytest.fixture()
def tag() -> str:
    return str(uuid())


async def generate_image(
    docker: aiodocker.Docker, tag: str, name: Optional[str] = None
) -> str:
    if name is None:
        name = f"e2e-cli-{uuid()}"
    image_archive = Path(__file__).parent / "assets/echo-tag.tar"
    # TODO use random image name here
    image_name = f"{name}:{tag}"
    with image_archive.open(mode="r+b") as fileobj:
        await docker.images.build(
            fileobj=fileobj, tag=image_name, buildargs={"TAG": tag}, encoding="identity"
        )

    return image_name


@pytest.fixture()
async def image(
    loop: asyncio.AbstractEventLoop, docker: aiodocker.Docker, tag: str
) -> AsyncIterator[str]:
    image = await generate_image(docker, tag)
    yield image
    await docker.images.delete(image, force=True)


@pytest.mark.e2e
def test_images_complete_lifecycle(
    helper: Helper,
    image: str,
    tag: str,
    loop: asyncio.AbstractEventLoop,
    docker: aiodocker.Docker,
) -> None:
    # Let`s push image
    captured = helper.run_cli(["image", "push", image])

    # stderr has "Used image ..." lines
    # assert not captured.err

    image_full_str = f"image://{helper.cluster_name}/{helper.username}/{image}"
    assert captured.out.endswith(image_full_str)
    image_url = URL(image_full_str)

    # Check if image available on registry
    captured = helper.run_cli(["image", "ls", "--full-uri"])

    image_urls = [URL(line.strip()) for line in captured.out.splitlines()[2:] if line]
    for url in image_urls:
        assert url.scheme == "image", url
    image_url_without_tag = image_url.with_path(image_url.path.replace(f":{tag}", ""))
    assert image_url_without_tag in image_urls

    # delete local
    loop.run_until_complete(docker.images.delete(image, force=True))
    docker_ls_output = loop.run_until_complete(docker.images.list())
    local_images = parse_docker_ls_output(docker_ls_output)
    assert image not in local_images

    # Pull image as with another tag
    captured = helper.run_cli(["image", "pull", f"image:{image}"])
    # stderr has "Used image ..." lines
    # assert not captured.err
    assert captured.out.endswith(image)

    # check pulled locally, delete for cleanup
    docker_ls_output = loop.run_until_complete(docker.images.list())
    local_images = parse_docker_ls_output(docker_ls_output)
    assert image in local_images

    # Execute image and check result
    captured = helper.run_cli(["-q", "run", "--no-wait-start", str(image_url)])
    assert not captured.err
    job_id = captured.out
    assert job_id.startswith("job-")
    helper.wait_job_change_state_to(job_id, JobStatus.SUCCEEDED, JobStatus.FAILED)

    helper.check_job_output(job_id, re.escape(tag))


@pytest.mark.e2e
def test_image_tags(helper: Helper, image: str, tag: str) -> None:
    # push image
    captured = helper.run_cli(["image", "push", image])

    image_full_str = f"image://{helper.cluster_name}/{helper.username}/{image}"
    assert captured.out.endswith(image_full_str)

    image_full_str_no_tag = image_full_str.replace(f":{tag}", "")

    delay = 0
    t0 = time.time()

    while time.time() - t0 < 600:
        time.sleep(delay)
        # check the tag is present now
        try:
            captured = helper.run_cli(
                ["image", "tags", image_full_str_no_tag], timeout=300
            )
        except subprocess.TimeoutExpired:
            continue
        if tag in map(lambda s: s.strip(), captured.out.splitlines()):
            break
        # Give a chance to sync remote registries
        delay = min(delay * 2 + 1, 15)
    else:
        raise AssertionError(
            f"Delay is reached on waiting for tag {tag} in {captured.out}"
        )

    cmd = f"neuro image tags {image_full_str}"
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    assertion_msg = f"Command {cmd} should fail: {result.stdout!r} {result.stderr!r}"
    assert result.returncode, assertion_msg

    image_full_str_latest_tag = image_full_str.replace(f":{tag}", ":latest")
    cmd = f"neuro image tags {image_full_str_latest_tag}"
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    assertion_msg = f"Command {cmd} should fail: {result.stdout!r} {result.stderr!r}"
    assert result.returncode, assertion_msg


@pytest.mark.e2e
def test_image_ls(helper: Helper, image: str, tag: str) -> None:
    # push image
    captured = helper.run_cli(["image", "push", image])

    image_full_str = f"image://{helper.cluster_name}/{helper.username}/{image}"
    image_short_str = f"image:{image}"
    assert captured.out.endswith(image_full_str)

    image_full_str_no_tag = image_full_str.replace(f":{tag}", "")
    image_short_str_no_tag = image_short_str.replace(f":{tag}", "")

    # check ls short mode
    captured = helper.run_cli(["image", "ls"])
    assert image_short_str_no_tag in [
        line.strip() for line in captured.out.splitlines()
    ]

    captured = helper.run_cli(["image", "ls", "--full-uri"])
    assert image_full_str_no_tag in [line.strip() for line in captured.out.splitlines()]

    # check ls long mode
    captured = helper.run_cli(["image", "ls", "-l"])
    for line in captured.out.splitlines():
        if image_short_str_no_tag in line:
            break
    else:
        assert False, f"Not found {image_short_str_no_tag} in {captured.out}"


@pytest.mark.e2e
async def test_images_delete(
    helper: Helper,
    docker: aiodocker.Docker,
) -> None:
    name = f"test-{uuid()}"
    await generate_image(docker, name=name, tag="latest")
    img_name = f"image:{name}"

    helper.run_cli(["image", "push", name + ":latest"])

    captured = helper.run_cli(["-q", "image", "ls"])
    assert img_name in captured.out

    helper.run_cli(["image", "rm", img_name])

    for _ in range(10):
        captured = helper.run_cli(["-q", "image", "ls"])
        if img_name in captured.out:
            time.sleep(5)

    assert img_name not in captured.out


@pytest.mark.e2e
async def test_images_push_with_specified_name(
    helper: Helper,
    image: str,
    tag: str,
    loop: asyncio.AbstractEventLoop,
    docker: aiodocker.Docker,
) -> None:
    # Let`s push image
    image_no_tag = image.replace(f":{tag}", "")
    pushed_no_tag = f"{image_no_tag}-pushed"
    pulled_no_tag = f"{image_no_tag}-pulled"
    pulled = f"{pulled_no_tag}:{tag}"

    captured = helper.run_cli(["image", "push", image, f"image:{pushed_no_tag}:{tag}"])
    # stderr has "Used image ..." lines
    # assert not captured.err
    async with helper.client() as client:
        image_pushed_full_str = (
            f"image://{client.config.cluster_name}/"
            f"{client.config.username}/{pushed_no_tag}:{tag}"
        )
        assert captured.out.endswith(image_pushed_full_str)

    # Check if image available on registry
    docker_ls_output = await docker.images.list()
    local_images = parse_docker_ls_output(docker_ls_output)
    assert pulled not in local_images

    async with helper.client() as client:
        image_pushed_full = client.parse.remote_image(image_pushed_full_str)
        image_url_without_tag = replace(image_pushed_full, tag=None)
        imgs = await client.images.ls()
        assert image_url_without_tag in imgs

    # check locally
    docker_ls_output = await docker.images.list()
    local_images = parse_docker_ls_output(docker_ls_output)
    assert pulled not in local_images

    # Pull image as with another name
    captured = helper.run_cli(["image", "pull", f"image:{pushed_no_tag}:{tag}", pulled])
    # stderr has "Used image ..." lines
    # assert not captured.err
    assert captured.out.endswith(pulled)
    # check locally
    docker_ls_output = await docker.images.list()
    local_images = parse_docker_ls_output(docker_ls_output)
    assert pulled in local_images

    # TODO (A.Yushkovskiy): delete the pushed image in GCR
    # delete locally
    await docker.images.delete(pulled, force=True)


@pytest.mark.e2e
def test_docker_helper(
    helper: Helper, image: str, tag: str, nmrc_path: Path, monkeypatch: Any
) -> None:
    monkeypatch.setenv(CONFIG_ENV_NAME, str(nmrc_path or DEFAULT_CONFIG_PATH))
    helper.run_cli(["config", "docker"])
    registry = helper.registry_url.host
    username = helper.username
    full_tag = f"{registry}/{username}/{image}"
    tag_cmd = f"docker tag {image} {full_tag}"
    result = subprocess.run(
        tag_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    assert (
        not result.returncode
    ), f"Command {tag_cmd} failed: {result.stdout!r} {result.stderr!r} "
    push_cmd = f"docker push {full_tag}"
    result = subprocess.run(
        push_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    assert (
        not result.returncode
    ), f"Command {push_cmd} failed: {result.stdout!r} {result.stderr!r} "
    # Run image and check output
    image_url = f"image://{helper.cluster_name}/{username}/{image}"
    job_id = helper.run_job_and_wait_state(
        image_url, "", wait_state=JobStatus.SUCCEEDED, stop_state=JobStatus.FAILED
    )
    helper.check_job_output(job_id, re.escape(tag))
