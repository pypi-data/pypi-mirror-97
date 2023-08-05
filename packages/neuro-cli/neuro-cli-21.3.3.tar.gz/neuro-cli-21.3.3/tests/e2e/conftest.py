import asyncio
import asyncio.subprocess
import errno
import hashlib
import logging
import os
import re
import shlex
import subprocess
import sys
from collections import namedtuple
from contextlib import contextmanager, suppress
from hashlib import sha1
from os.path import join
from pathlib import Path
from time import time
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    ContextManager,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
)
from uuid import uuid4 as uuid

import aiodocker
import aiohttp
import click
import pexpect
import pytest
import toml
from typing_extensions import Final
from yarl import URL

from neuro_sdk import (
    Action,
    AuthorizationError,
    Client,
    Config,
    Container,
    FileStatusType,
    IllegalArgumentError,
    JobDescription,
    JobStatus,
    ResourceNotFound,
    Resources,
)
from neuro_sdk import get as api_get
from neuro_sdk import login_with_token

if sys.version_info >= (3, 7):  # pragma: no cover
    from contextlib import asynccontextmanager
else:
    from async_generator import asynccontextmanager

from neuro_cli.asyncio_utils import run
from neuro_cli.utils import resolve_job

from tests.e2e.utils import FILE_SIZE_B, NGINX_IMAGE_NAME, JobWaitStateStopReached

JOB_TIMEOUT = 5 * 60
JOB_WAIT_SLEEP_SECONDS = 2
JOB_OUTPUT_TIMEOUT = 5 * 60
JOB_OUTPUT_SLEEP_SECONDS = 2
CLI_MAX_WAIT = 5 * 60
NETWORK_TIMEOUT = 3 * 60.0
CLIENT_TIMEOUT = aiohttp.ClientTimeout(None, None, NETWORK_TIMEOUT, NETWORK_TIMEOUT)

log = logging.getLogger(__name__)

JOB_ID_PATTERN: Final = re.compile(
    # pattern for UUID v4 taken here: https://stackoverflow.com/a/38191078
    r"(job-[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})",
    re.IGNORECASE,
)


@pytest.fixture
def loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()


SysCap = namedtuple("SysCap", "out err")


async def _run_async(
    coro: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any
) -> Any:
    try:
        return await coro(*args, **kwargs)
    finally:
        if sys.platform == "win32":
            await asyncio.sleep(0.2)
        else:
            await asyncio.sleep(0.05)


def run_async(coro: Any) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return run(_run_async(coro, *args, **kwargs))

    return wrapper


class Helper:
    def __init__(self, nmrc_path: Optional[Path], tmp_path: Path) -> None:
        self._nmrc_path = nmrc_path
        self._tmp = tmp_path
        self.tmpstoragename = f"test_e2e/{uuid()}"
        self._tmpstorage = f"storage:{self.tmpstoragename}/"
        self._closed = False
        self._executed_jobs: List[str] = []

    def close(self) -> None:
        if not self._closed:
            with suppress(Exception):
                self.rm("", recursive=True)
            self._closed = True
        if self._executed_jobs:
            for job in self._executed_jobs:
                self.kill_job(job, wait=False)

    @property
    def username(self) -> str:
        config = self.get_config()
        return config.username

    @property
    def cluster_name(self) -> str:
        config = self.get_config()
        return config.cluster_name

    @property
    def token(self) -> str:
        config = self.get_config()

        @run_async
        async def get_token() -> str:
            return await config.token()

        return get_token()

    @property
    def registry_url(self) -> URL:
        config = self.get_config()
        return config.registry_url

    @property
    def tmpstorage(self) -> str:
        return self._tmpstorage

    def make_uri(self, path: str, *, fromhome: bool = False) -> URL:
        if fromhome:
            return URL(f"storage://{self.cluster_name}/{self.username}/{path}")
        else:
            return URL(self.tmpstorage + path)

    @run_async
    async def get_config(self) -> Config:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            return client.config

    @run_async
    async def mkdir(self, path: str, **kwargs: bool) -> None:
        __tracebackhide__ = True
        url = URL(self.tmpstorage + path)
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            await client.storage.mkdir(url, **kwargs)

    @run_async
    async def rm(self, path: str, *, recursive: bool = False) -> None:
        __tracebackhide__ = True
        url = URL(self.tmpstorage + path)
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            await client.storage.rm(url, recursive=recursive)

    @run_async
    async def resolve_job_name_to_id(self, job_name: str) -> str:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            return await resolve_job(
                job_name,
                client=client,
                status=JobStatus.items(),
            )

    @run_async
    async def check_file_exists_on_storage(
        self, name: str, path: str, size: int, *, fromhome: bool = False
    ) -> None:
        __tracebackhide__ = True
        url = self.make_uri(path, fromhome=fromhome)
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            async for file in client.storage.ls(url):
                if (
                    file.type == FileStatusType.FILE
                    and file.name == name
                    and file.size == size
                ):
                    return
        raise AssertionError(f"File {name} with size {size} not found in {url}")

    @run_async
    async def check_dir_exists_on_storage(self, name: str, path: str) -> None:
        __tracebackhide__ = True
        url = URL(self.tmpstorage + path)
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            async for file in client.storage.ls(url):
                if file.type == FileStatusType.DIRECTORY and file.path == name:
                    return
        raise AssertionError(f"Dir {name} not found in {url}")

    @run_async
    async def check_dir_absent_on_storage(self, name: str, path: str) -> None:
        __tracebackhide__ = True
        url = URL(self.tmpstorage + path)
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            async for file in client.storage.ls(url):
                if file.type == FileStatusType.DIRECTORY and file.path == name:
                    raise AssertionError(f"Dir {name} found in {url}")

    @run_async
    async def check_file_absent_on_storage(self, name: str, path: str) -> None:
        __tracebackhide__ = True
        url = URL(self.tmpstorage + path)
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            async for file in client.storage.ls(url):
                if file.type == FileStatusType.FILE and file.path == name:
                    raise AssertionError(f"File {name} found in {url}")

    @run_async
    async def check_file_on_storage_checksum(
        self, name: str, path: str, checksum: str, tmpdir: str, tmpname: str
    ) -> None:
        __tracebackhide__ = True
        url = URL(self.tmpstorage + path)
        if tmpname:
            target = join(tmpdir, tmpname)
            target_file = target
        else:
            target = tmpdir
            target_file = join(tmpdir, name)
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            await client.storage.download_file(url / name, URL("file:" + target))
            assert (
                self.hash_hex(target_file) == checksum
            ), "checksum test failed for {url}"

    @run_async
    async def check_rm_file_on_storage(
        self, name: str, path: str, *, fromhome: bool = False
    ) -> None:
        __tracebackhide__ = True
        url = self.make_uri(path, fromhome=fromhome)
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            await client.storage.rm(url / name)

    @run_async
    async def check_upload_file_to_storage(
        self, name: str, path: str, local_file: str
    ) -> None:
        __tracebackhide__ = True
        url = URL(self.tmpstorage + path)
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            if name is None:
                await client.storage.upload_file(URL("file:" + local_file), url)
            else:
                await client.storage.upload_file(
                    URL("file:" + local_file), URL(f"{url}/{name}")
                )

    @run_async
    async def check_rename_file_on_storage(
        self, name_from: str, path_from: str, name_to: str, path_to: str
    ) -> None:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            await client.storage.mv(
                URL(f"{self.tmpstorage}{path_from}/{name_from}"),
                URL(f"{self.tmpstorage}{path_to}/{name_to}"),
            )
            names1 = {
                f.name
                async for f in client.storage.ls(URL(f"{self.tmpstorage}{path_from}"))
            }
            assert name_from not in names1

            names2 = {
                f.name
                async for f in client.storage.ls(URL(f"{self.tmpstorage}{path_to}"))
            }
            assert name_to in names2

    @run_async
    async def check_rename_directory_on_storage(
        self, path_from: str, path_to: str
    ) -> None:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            await client.storage.mv(
                URL(f"{self.tmpstorage}{path_from}"), URL(f"{self.tmpstorage}{path_to}")
            )

    def hash_hex(self, file: Union[str, Path]) -> str:
        __tracebackhide__ = True
        _hash = sha1()
        with open(file, "rb") as f:
            for block in iter(lambda: f.read(16 * 1024 * 1024), b""):
                _hash.update(block)

        return _hash.hexdigest()

    @run_async
    async def wait_job_change_state_from(
        self, job_id: str, wait_state: JobStatus, stop_state: Optional[JobStatus] = None
    ) -> None:
        __tracebackhide__ = True
        start_time = time()
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            job = await client.jobs.status(job_id)
            while job.status == wait_state and (int(time() - start_time) < JOB_TIMEOUT):
                if stop_state == job.status:
                    raise JobWaitStateStopReached(
                        f"failed running job {job_id}: {stop_state}"
                    )
                await asyncio.sleep(JOB_WAIT_SLEEP_SECONDS)
                job = await client.jobs.status(job_id)

    @run_async
    async def wait_job_change_state_to(
        self,
        job_id: str,
        target_state: JobStatus,
        stop_state: Optional[JobStatus] = None,
        timeout: float = JOB_TIMEOUT,
    ) -> None:
        __tracebackhide__ = True
        start_time = time()
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            job = await client.jobs.status(job_id)
            while target_state != job.status:
                if stop_state and stop_state == job.status:
                    raise JobWaitStateStopReached(
                        f"failed running job {job_id}: '{stop_state}'"
                    )
                if int(time() - start_time) > timeout:
                    raise AssertionError(
                        f"timeout exceeded, last output: '{job.status}'"
                    )
                await asyncio.sleep(JOB_WAIT_SLEEP_SECONDS)
                job = await client.jobs.status(job_id)

    @run_async
    async def assert_job_state(self, job_id: str, state: JobStatus) -> None:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            job = await client.jobs.status(job_id)
            assert job.status == state

    async def ajob_info(self, job_id: str, wait_start: bool = False) -> JobDescription:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            job = await client.jobs.status(job_id)
            start_time = time()
            while (
                wait_start
                and job.status == JobStatus.PENDING
                and time() - start_time < JOB_TIMEOUT
            ):
                job = await client.jobs.status(job_id)
            if int(time() - start_time) > JOB_TIMEOUT:
                raise AssertionError(f"timeout exceeded, last output: '{job.status}'")
            return job

    job_info = run_async(ajob_info)

    @run_async
    async def check_job_output(
        self, job_id: str, expected: str, flags: int = 0
    ) -> None:
        """
        Wait until job output satisfies given regexp
        """
        __tracebackhide__ = True

        async def _check_job_output() -> AsyncIterator[bytes]:
            async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
                async for chunk in client.jobs.monitor(job_id):
                    yield chunk

        started_at = time()
        while time() - started_at < JOB_OUTPUT_TIMEOUT:
            chunks = []
            async for chunk in _check_job_output():
                if not chunk:
                    break
                chunks.append(chunk.decode())
                if re.search(expected, "".join(chunks), flags):
                    return
                if time() - started_at < JOB_OUTPUT_TIMEOUT:
                    break
                await asyncio.sleep(JOB_OUTPUT_SLEEP_SECONDS)

        raise AssertionError(
            f"Output of job {job_id} does not satisfy to expected regexp: {expected}"
        )

    def _default_args(self, verbosity: int, network_timeout: float) -> List[str]:
        args = [
            "--show-traceback",
            "--disable-pypi-version-check",
            "--color=no",
            f"--network-timeout={network_timeout}",
            "--skip-stats",
        ]

        if verbosity < 0:
            args.append("-" + "q" * (-verbosity))
        if verbosity > 0:
            args.append("-" + "v" * verbosity)

        if self._nmrc_path:
            args.append(f"--neuromation-config={self._nmrc_path}")

        return args

    async def acli(
        self,
        arguments: List[str],
        *,
        verbosity: int = 0,
        network_timeout: float = NETWORK_TIMEOUT,
    ) -> asyncio.subprocess.Process:
        __tracebackhide__ = True

        log.info("Run 'neuro %s'", " ".join(arguments))

        # 5 min timeout is overkill
        proc = await asyncio.create_subprocess_exec(
            "neuro",
            *(self._default_args(verbosity, network_timeout) + arguments),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return proc

    def run_cli(
        self,
        arguments: List[str],
        *,
        verbosity: int = 0,
        network_timeout: float = NETWORK_TIMEOUT,
        input: Optional[str] = None,
        timeout: float = 300,
    ) -> SysCap:
        __tracebackhide__ = True

        log.info("Run 'neuro %s'", " ".join(arguments))

        # 5 min timeout is overkill
        proc = subprocess.run(
            ["neuro"] + self._default_args(verbosity, network_timeout) + arguments,
            timeout=timeout,
            encoding="utf8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            input=input,
        )
        try:
            proc.check_returncode()
        except subprocess.CalledProcessError:
            log.error(f"Last stdout: '{proc.stdout}'")
            log.error(f"Last stderr: '{proc.stderr}'")
            raise
        out = click.unstyle(proc.stdout)
        err = click.unstyle(proc.stderr)
        if any(run_cmd in arguments for run_cmd in ("submit", "run")):
            job_id = self.find_job_id(out)
            if job_id:
                self._executed_jobs.append(job_id)
        out = out.strip()
        err = err.strip()
        if verbosity > 3:
            print(f"neuro stdout: {out}")
            print(f"neuro stderr: {err}")
        return SysCap(out, err)

    def find_job_id(self, arg: str) -> Optional[str]:
        match = JOB_ID_PATTERN.search(arg)
        return match.group(1) if match else None

    def pexpect(
        self,
        arguments: List[str],
        *,
        verbosity: int = 0,
        network_timeout: float = NETWORK_TIMEOUT,
        encoding: str = "utf8",
        echo: bool = True,
    ) -> "pexpect.spawn":
        if not hasattr(pexpect, "spawn"):
            pytest.skip("TTY tests are not supported on Windows")
        return pexpect.spawn(
            "neuro",
            self._default_args(verbosity, network_timeout) + arguments,
            encoding=encoding,
            echo=echo,
        )

    def autocomplete(
        self,
        arguments: List[str],
        *,
        verbosity: int = 0,
        network_timeout: float = NETWORK_TIMEOUT,
        timeout: float = 30,
    ) -> str:
        __tracebackhide__ = True

        log.info("Run 'neuro %s'", " ".join(arguments))

        args = self._default_args(verbosity, network_timeout)
        env = dict(os.environ)
        env["_NEURO_COMPLETE"] = "complete_zsh"
        env["COMP_WORDS"] = " ".join(shlex.quote(arg) for arg in args + arguments)
        env["COMP_CWORD"] = str(len(args + arguments) - 1)
        env["NEURO_CLI_JOB_AUTOCOMPLETE_LIMIT"] = "500"

        proc = subprocess.run(
            "neuro",
            encoding="utf8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            timeout=timeout,
        )
        assert proc.returncode == 1
        assert not proc.stderr
        return proc.stdout

    async def arun_job_and_wait_state(
        self,
        image: str,
        command: str = "",
        *,
        description: Optional[str] = None,
        name: Optional[str] = None,
        tty: bool = False,
        env: Optional[Dict[str, str]] = None,
        wait_state: JobStatus = JobStatus.RUNNING,
        stop_state: JobStatus = JobStatus.FAILED,
    ) -> str:
        __tracebackhide__ = True
        if env is None:
            env = {}
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            preset = client.presets["cpu-micro"]
            resources = Resources(memory_mb=preset.memory_mb, cpu=preset.cpu)
            container = Container(
                image=client.parse.remote_image(image),
                command=command,
                resources=resources,
                tty=tty,
                env=env,
            )
            job = await client.jobs.run(
                container,
                scheduler_enabled=preset.scheduler_enabled,
                description=description,
                name=name,
            )

            start_time = time()
            while job.status != wait_state:
                if stop_state == job.status:
                    raise JobWaitStateStopReached(
                        f"failed running job {job.id}: {stop_state}"
                    )
                if int(time() - start_time) > JOB_TIMEOUT:
                    raise AssertionError(
                        f"timeout exceeded, last output: '{job.status}'"
                    )
                await asyncio.sleep(JOB_WAIT_SLEEP_SECONDS)
                job = await client.jobs.status(job.id)

            return job.id

    run_job_and_wait_state = run_async(arun_job_and_wait_state)

    @run_async
    async def check_http_get(self, url: Union[URL, str]) -> str:
        """
        Try to fetch given url few times.
        """
        __tracebackhide__ = True
        async with aiohttp.ClientSession() as session:
            for i in range(3):
                async with session.get(url) as resp:
                    if resp.status == 200:
                        return await resp.text()
                await asyncio.sleep(5)
            else:
                raise aiohttp.ClientResponseError(
                    status=resp.status,
                    message=f"Server return {resp.status}",
                    history=tuple(),
                    request_info=resp.request_info,
                )

    async def akill_job(self, id_or_name: str, *, wait: bool = True) -> None:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            id = await resolve_job(
                id_or_name, client=client, status=JobStatus.active_items()
            )
            with suppress(ResourceNotFound, IllegalArgumentError):
                await client.jobs.kill(id)
                if wait:
                    while True:
                        stat = await client.jobs.status(id)
                        if stat.status.is_finished:
                            break

    kill_job = run_async(akill_job)

    async def acreate_bucket(self, name: str, *, wait: bool = False) -> None:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            await client.blob_storage.create_bucket(name)
            if wait:
                t0 = time()
                delay = 1
                while time() - t0 < 30:
                    try:
                        await client.blob_storage.list_blobs(name, max_keys=10)
                        return
                    except ResourceNotFound:
                        delay = min(delay * 2, 15)
                        await asyncio.sleep(delay)
                raise RuntimeError(f"Bucket {name} doesn't exist after the creation")

    create_bucket = run_async(acreate_bucket)

    async def adelete_bucket(self, name: str) -> None:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            await client.blob_storage.delete_bucket(name)

    delete_bucket = run_async(adelete_bucket)

    async def acleanup_bucket(self, bucket_name: str) -> None:
        __tracebackhide__ = True
        # Each test needs a clean bucket state and we can't delete bucket until it's
        # cleaned
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            blobs, _ = await client.blob_storage.list_blobs(bucket_name, recursive=True)
            if not blobs:
                return

            # XXX: We do assume we will not have tests that run 10000 of objects. If we
            # do, please add a semaphore here.
            tasks = []
            for blob in blobs:
                log.info("Removing %s %s", bucket_name, blob.key)
                tasks.append(client.blob_storage.delete_blob(bucket_name, key=blob.key))
            await asyncio.gather(*tasks)

    cleanup_bucket = run_async(acleanup_bucket)

    @run_async
    async def drop_stale_buckets(self, bucket_prefix: str) -> None:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            buckets = await client.blob_storage.list_buckets()
            for bucket in buckets:
                if (
                    bucket.name.startswith(bucket_prefix)
                    and bucket.creation_time < time() - 3600 * 4
                    and bucket.permission in (Action.WRITE, Action.MANAGE)
                ):
                    with suppress(ResourceNotFound):
                        # bucket can be deleted by another parallel test run,
                        # ignore ResourceNotFound errors
                        await self.acleanup_bucket(bucket.name)
                        await self.adelete_bucket(bucket.name)

    @run_async
    async def upload_blob(self, bucket_name: str, key: str, file: Path) -> None:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            await client.blob_storage.upload_file(
                URL("file:" + str(file)), client.blob_storage.make_url(bucket_name, key)
            )

    @run_async
    async def check_blob_size(self, bucket_name: str, key: str, size: int) -> None:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            blob = await client.blob_storage.head_blob(bucket_name, key)
            assert blob.size == size

    @run_async
    async def check_blob_checksum(
        self, bucket_name: str, key: str, checksum: str, tmp_path: Path
    ) -> None:
        __tracebackhide__ = True
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            await client.blob_storage.download_file(
                client.blob_storage.make_url(bucket_name, key),
                URL("file:" + str(tmp_path)),
            )
            assert self.hash_hex(tmp_path) == checksum, "checksum test failed for {url}"

    @asynccontextmanager
    async def client(self) -> AsyncIterator[Client]:
        async with api_get(timeout=CLIENT_TIMEOUT, path=self._nmrc_path) as client:
            yield client


# Cache at the session level to reduce amount of relogins.
# Frequent relogins returns 500 Internal Server Error too often.
_nmrc_path_user = _nmrc_path_admin = None


@pytest.fixture
def nmrc_path(tmp_path_factory: Any, request: Any) -> Optional[Path]:
    global _nmrc_path_user
    global _nmrc_path_admin
    require_admin = request.keywords.get("require_admin", False)
    if require_admin:
        if _nmrc_path_admin is None:
            _nmrc_path_admin = _get_nmrc_path(tmp_path_factory, True)
        return _nmrc_path_admin
    else:
        if _nmrc_path_user is None:
            _nmrc_path_user = _get_nmrc_path(tmp_path_factory, False)
        return _nmrc_path_user


def _get_nmrc_path(tmp_path_factory: Any, require_admin: bool) -> Optional[Path]:
    if require_admin:
        token_env = "E2E_TOKEN"
    else:
        token_env = "E2E_USER_TOKEN"
    e2e_test_token = os.environ.get(token_env)
    if e2e_test_token:
        tmp_path = tmp_path_factory.mktemp("config")
        nmrc_path = tmp_path / "conftest.nmrc"
        run(
            login_with_token(
                e2e_test_token,
                url=URL("https://dev.neu.ro/api/v1"),
                path=nmrc_path,
                timeout=CLIENT_TIMEOUT,
            )
        )
        # Setup user config
        local_conf = nmrc_path / ".neuro.toml"
        local_conf.write_text(toml.dumps({"job": {"life-span": "10m"}}))
        return nmrc_path
    else:
        # By providing `None` we allow Helper to login using default configuration
        # in user's home folder. Tests will use current logged in user and current
        # cluster from neuro cli.
        return None


@pytest.fixture
def helper(tmp_path: Path, nmrc_path: Path) -> Iterator[Helper]:
    ret = Helper(nmrc_path=nmrc_path, tmp_path=tmp_path)
    yield ret
    with suppress(Exception):
        # ignore exceptions in helper closing
        # nothing to do here anyway
        ret.close()


def generate_random_file(path: Path, size: int) -> Tuple[str, str]:
    name = f"{uuid()}.tmp"
    path_and_name = path / name
    hasher = hashlib.sha1()
    with open(path_and_name, "wb") as file:
        generated = 0
        while generated < size:
            length = min(1024 * 1024, size - generated)
            data = os.urandom(length)
            file.write(data)
            hasher.update(data)
            generated += len(data)
    return str(path_and_name), hasher.hexdigest()


@pytest.fixture(scope="session")
def static_path(tmp_path_factory: Any) -> Path:
    return tmp_path_factory.mktemp("data")


@pytest.fixture(scope="session")
def data(static_path: Path) -> Tuple[str, str]:
    folder = static_path / "data"
    folder.mkdir()
    return generate_random_file(folder, FILE_SIZE_B)


@pytest.fixture(scope="session")
def data2(static_path: Path) -> Tuple[str, str]:
    folder = static_path / "data2"
    folder.mkdir()
    return generate_random_file(folder, FILE_SIZE_B // 3)


@pytest.fixture(scope="session")
def data3(static_path: Path) -> Tuple[str, str]:
    folder = static_path / "data3"
    folder.mkdir()
    return generate_random_file(folder, FILE_SIZE_B // 5)


@pytest.fixture(scope="session")
def nested_data(static_path: Path) -> Tuple[str, str, str]:
    root_dir = static_path / "neested_data" / "nested"
    nested_dir = root_dir / "directory" / "for" / "test"
    nested_dir.mkdir(parents=True, exist_ok=True)
    generated_file, hash = generate_random_file(nested_dir, FILE_SIZE_B // 3)
    return generated_file, hash, str(root_dir)


@pytest.fixture(scope="session")
def _tmp_bucket_create(
    tmp_path_factory: Any, request: Any
) -> Iterator[Tuple[str, Helper]]:
    tmp_path = tmp_path_factory.mktemp("tmp_bucket" + str(uuid()))
    tmpbucketname = f"neuro-e2e-{uuid()}"
    nmrc_path = _get_nmrc_path(tmp_path_factory, require_admin=True)

    helper = Helper(nmrc_path, tmp_path)

    try:
        helper.drop_stale_buckets("neuro-e2e-")
        helper.create_bucket(tmpbucketname, wait=True)
    except AuthorizationError:
        pytest.skip("No permission to create bucket for user E2E_TOKEN")
    yield tmpbucketname, helper
    helper.delete_bucket(tmpbucketname)
    helper.close()


@pytest.fixture
def tmp_bucket(_tmp_bucket_create: Tuple[str, Helper]) -> Iterator[str]:
    tmpbucketname, helper = _tmp_bucket_create
    yield tmpbucketname
    try:
        helper.cleanup_bucket(tmpbucketname)
    except aiohttp.ClientOSError as exc:
        if exc.errno == errno.ETIMEDOUT:
            # Try next time
            pass
        else:
            raise


@pytest.fixture
def secret_job(helper: Helper) -> Callable[[bool, bool, Optional[str]], Dict[str, Any]]:
    def go(
        http_port: bool, http_auth: bool = False, description: Optional[str] = None
    ) -> Dict[str, Any]:
        secret = str(uuid())
        # Run http job
        command = (
            f"bash -c \"echo -n '{secret}' > /usr/share/nginx/html/secret.txt; "
            f"timeout 15m /usr/sbin/nginx -g 'daemon off;'\""
        )
        args: List[str] = []
        if http_port:
            args += ["--http", "80"]
            if http_auth:
                args += ["--http-auth"]
            else:
                args += ["--no-http-auth"]
        if not description:
            description = "nginx with secret file"
            if http_port:
                description += " and forwarded http port"
                if http_auth:
                    description += " with authentication"
        args += ["-d", description]
        capture = helper.run_cli(
            ["-q", "job", "run", "--detach", *args, NGINX_IMAGE_NAME, command]
        )
        http_job_id = capture.out
        status: JobDescription = helper.job_info(http_job_id, wait_start=True)
        return {
            "id": http_job_id,
            "secret": secret,
            "ingress_url": status.http_url,
            "internal_hostname": status.internal_hostname,
        }

    return go


@pytest.fixture()
async def docker(loop: asyncio.AbstractEventLoop) -> AsyncIterator[aiodocker.Docker]:
    if sys.platform == "win32":
        pytest.skip(f"Skip tests for docker on windows")
    try:
        client = aiodocker.Docker()
    except Exception as e:
        pytest.skip(f"Could not connect to Docker: {e}")
    yield client
    await client.close()


@pytest.fixture
def disk_factory(helper: Helper) -> Callable[[str], ContextManager[str]]:
    @contextmanager
    def _make_disk(storage: str, name: Optional[str] = None) -> Iterator[str]:
        # Create disk
        args = ["disk", "create", storage]
        if name:
            args += ["--name", name]
        cap = helper.run_cli(args)
        assert cap.err == ""
        disk_id = cap.out.splitlines()[0].split()[1]
        yield disk_id

        # Remove disk
        cap = helper.run_cli(["disk", "rm", disk_id])
        assert cap.err == ""

    return _make_disk
