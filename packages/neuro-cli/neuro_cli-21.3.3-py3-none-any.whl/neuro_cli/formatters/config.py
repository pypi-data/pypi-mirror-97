import operator
from decimal import Decimal
from typing import Iterable, List, Mapping, Optional, Union

import click
from rich import box
from rich.console import RenderableType, RenderGroup
from rich.padding import Padding
from rich.table import Table
from rich.text import Text

from neuro_sdk import Cluster, Config, Preset
from neuro_sdk.admin import _Quota
from neuro_sdk.quota import _QuotaInfo

from neuro_cli.utils import format_size


class ConfigFormatter:
    def __call__(
        self, config: Config, available_jobs_counts: Mapping[str, int]
    ) -> RenderableType:
        table = Table(
            title="User Configuration:",
            title_justify="left",
            box=None,
            show_header=False,
            show_edge=False,
        )
        table.add_column()
        table.add_column(style="bold")
        table.add_row("User Name", config.username)
        table.add_row("Current Cluster", config.cluster_name)
        table.add_row("API URL", str(config.api_url))
        table.add_row("Docker Registry URL", str(config.registry_url))

        return RenderGroup(
            table, _format_presets(config.presets, available_jobs_counts)
        )


class QuotaInfoFormatter:
    QUOTA_NOT_SET = "infinity"

    def __call__(self, quota: _QuotaInfo) -> RenderableType:
        gpu_details = self._format_quota_details(
            quota.gpu_time_spent, quota.gpu_time_limit, quota.gpu_time_left
        )
        cpu_details = self._format_quota_details(
            quota.cpu_time_spent, quota.cpu_time_limit, quota.cpu_time_left
        )
        return RenderGroup(
            Text.assemble(Text("GPU", style="bold"), f": ", gpu_details),
            Text.assemble(Text("CPU", style="bold"), f": ", cpu_details),
        )

    def _format_quota_details(
        self, time_spent: float, time_limit: float, time_left: float
    ) -> str:
        spent_str = f"spent: {self._format_time(time_spent)}"
        quota_str = "quota: "
        if time_limit < float("inf"):
            assert time_left < float("inf")
            quota_str += self._format_time(time_limit)
            quota_str += f", left: {self._format_time(time_left)}"
        else:
            quota_str += self.QUOTA_NOT_SET
        return f"{spent_str} ({quota_str})"

    def _format_time(self, total_seconds: float) -> str:
        # Since API for `GET /stats/users/{name}` returns time in minutes,
        #  we need to display it in minutes as well.
        total_minutes = int(total_seconds // 60)
        hours, minutes = divmod(total_minutes, 60)
        return f"{hours:02d}h {minutes:02d}m"


class QuotaFormatter:
    QUOTA_NOT_SET = "infinity"

    def __call__(self, quota: _Quota) -> RenderableType:
        credits_details = self._format_quota_details(quota.credits, is_minutes=False)
        jobs_details = self._format_quota_details(
            quota.total_running_jobs, is_minutes=False
        )
        gpu_details = self._format_quota_details(quota.total_gpu_run_time_minutes)
        non_gpu_details = self._format_quota_details(
            quota.total_non_gpu_run_time_minutes
        )
        return RenderGroup(
            Text.assemble(Text("Credits", style="bold"), f": ", credits_details),
            Text.assemble(Text("Jobs", style="bold"), f": ", jobs_details),
            Text.assemble(Text("GPU", style="bold"), f": ", gpu_details),
            Text.assemble(Text("CPU", style="bold"), f": ", non_gpu_details),
        )

    def _format_quota_details(
        self, quota: Optional[Union[int, Decimal]], *, is_minutes: bool = True
    ) -> str:
        if quota is None:
            return self.QUOTA_NOT_SET
        elif is_minutes:
            return f"{quota}m"
        else:
            return str(quota)


class ClustersFormatter:
    def __call__(
        self, clusters: Iterable[Cluster], default_name: Optional[str]
    ) -> RenderableType:
        out: List[RenderableType] = [Text("Available clusters:", style="i")]
        for cluster in clusters:
            name: Union[str, Text] = cluster.name or ""
            pre = "  "
            if cluster.name == default_name:
                name = Text(cluster.name, style="u")
                pre = "* "
            out.append(Text.assemble(pre, Text("Name"), ": ", name))
            out.append(Padding.indent(_format_presets(cluster.presets, None), 2))
        return RenderGroup(*out)


def _format_presets(
    presets: Mapping[str, Preset],
    available_jobs_counts: Optional[Mapping[str, int]],
) -> Table:
    has_tpu = False
    for preset in presets.values():
        if preset.tpu_type:
            has_tpu = True
            break

    table = Table(
        title="Resource Presets:",
        title_justify="left",
        box=box.SIMPLE_HEAVY,
        show_edge=False,
    )
    table.add_column("Name", style="bold", justify="left")
    table.add_column("#CPU", justify="right")
    table.add_column("Memory", justify="right")
    table.add_column("Round Robin", justify="center")
    table.add_column("Preemptible Node", justify="center")
    table.add_column("GPU", justify="left")
    if available_jobs_counts:
        table.add_column("Jobs Avail", justify="right")
    if has_tpu:
        table.add_column("TPU", justify="left")
    table.add_column("Credits per hour", justify="left")

    for name, preset in presets.items():
        gpu = ""
        if preset.gpu:
            gpu = f"{preset.gpu} x {preset.gpu_model}"
        row = [
            name,
            str(preset.cpu),
            format_size(preset.memory_mb * 1024 ** 2),
            "√" if preset.scheduler_enabled else "×",
            "√" if preset.preemptible_node else "×",
            gpu,
        ]
        if has_tpu:
            tpu = (
                f"{preset.tpu_type}/{preset.tpu_software_version}"
                if preset.tpu_type
                else ""
            )
            row.append(tpu)
        if available_jobs_counts:
            if name in available_jobs_counts:
                row.append(str(available_jobs_counts[name]))
            else:
                row.append("")
        row.append(str(preset.credits_per_hour))
        table.add_row(*row)

    return table


class AliasesFormatter:
    def __call__(self, aliases: Iterable[click.Command]) -> Table:
        table = Table(box=box.MINIMAL_HEAVY_HEAD)
        table.add_column("Alias", style="bold")
        table.add_column("Description")
        for alias in sorted(aliases, key=operator.attrgetter("name")):
            table.add_row(alias.name, alias.get_short_help_str())
        return table
