import collections
import copy
import getpass
import json
import logging
import pprint
import re
from pathlib import Path
from typing import Any, Dict, List

import click

import solitude.core
from solitude.core import log_setup, get_connected_ssh_client_from_config
from solitude.config import Config
from solitude.cache import json_write_atomic
from solitude import TOOL_NAME, __version__
from solitude.slurmjob import SlurmJob
from solitude.utils.ssh import SSHClient


DEFAULT_SSH_SERVER = "dlc-umbriel.umcn.nl"
DEFAULT_CONFIG = Config()


def resolve_jobids(
    ctx: click.core.Context, param: click.core.Option, value: Any
) -> List[int]:
    # split values out on " " and ","
    substrs = [
        v3
        for v in value
        for v2 in v.strip().split(" ")
        for v3 in v2.strip().split(",")
    ]
    indices = []
    for entry in substrs:
        res = re.match(r"(\d+)(?=-(\d+))?", entry)
        if not res:
            click.echo(
                "Indices should be specified using numbers, "
                "ranges (a-b) or as a list of comma separated indices"
            )
            ctx.exit()
        grps = res.groups()
        if grps[1] is None:
            # parse number
            indices.append(int(grps[0]))
        else:
            # parse range
            a, b = int(grps[0]), int(grps[1])
            if a > b:
                click.echo(
                    "The second value (b) in a range should "
                    "be greater or equal to the first value (a) (b >= a)"
                )
                ctx.exit()
            indices = indices + [e for e in range(a, b + 1)]
    indices = [e for e in sorted(set(indices))]
    if not all(map(lambda x: x > 0, indices)):
        click.echo("Jobids should be greater than 0")
        ctx.exit()
    return indices


def is_config_valid() -> bool:
    if not DEFAULT_CONFIG.is_config_present():
        click.echo(
            "Configuration file could not be found. "
            "Generate one using `solitude config create`"
        )
        return False
    if not DEFAULT_CONFIG.is_ssh_configured():
        click.echo(
            f"Configuration file was found at {DEFAULT_CONFIG.config_path}. "
            f"However ssh was not properly configured. "
            "Generate new settings using `solitude config create`"
        )
        return False
    return True


def print_version(
    ctx: click.core.Context, param: click.core.Option, value: Any
):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"{TOOL_NAME} {__version__}")
    ctx.exit()


def set_verbose_logging(
    ctx: click.core.Context, param: click.core.Option, value: Any
):
    if not value or ctx.resilient_parsing:
        return
    logger = logging.getLogger(f"{TOOL_NAME}")
    logger.setLevel(logging.DEBUG)
    logging.getLogger("Cache").setLevel(logging.DEBUG)


class ClickPath(click.Path):
    """A Click path argument that returns a pathlib Path, not a string"""

    def convert(self, value, param, ctx):
        return Path(super().convert(value, param, ctx))


class BaseGroup(click.core.Group):
    def __init__(self, name=None, commands=None, **kwargs):
        commands = commands or collections.OrderedDict()
        super().__init__(name, commands, **kwargs)
        self.params.insert(
            200,
            click.core.Option(
                param_decls=("--version",),
                is_flag=True,
                is_eager=True,
                expose_value=False,
                callback=print_version,
                help="Show the version and exit.",
            ),
        )

    def list_commands(
        self, ctx: click.core.Context
    ) -> Dict[str, click.core.Command]:
        return self.commands


class BaseCommand(click.core.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.insert(
            199,
            click.core.Option(
                param_decls=("-v", "--verbose"),
                is_flag=True,
                is_eager=True,
                expose_value=False,
                callback=set_verbose_logging,
                help="Enable verbose messages.",
            ),
        )
        self.params.insert(
            200,
            click.core.Option(
                param_decls=("--version",),
                is_flag=True,
                is_eager=True,
                expose_value=False,
                callback=print_version,
                help="Show the version and exit.",
            ),
        )


class SharedCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.insert(
            0,
            click.core.Option(
                param_decls=("-f", "--cmd-files"),
                multiple=True,
                required=True,
                type=ClickPath(dir_okay=True, exists=True),
                default=DEFAULT_CONFIG.defaults.cmdfiles,
                help=f"File(s) containing a list of commands. Default: {DEFAULT_CONFIG.defaults.cmdfiles}",
            ),
        )
        self.params.insert(
            1,
            click.core.Option(
                param_decls=("-i", "--jobids"),
                multiple=True,
                type=str,
                callback=resolve_jobids,
                help="Select specific jobids. E.g.: 1-5,7,9",
            ),
        )
        self.params.insert(
            2,
            click.core.Option(
                param_decls=("-w", "--workers"),
                default=DEFAULT_CONFIG.defaults.workers,
                help=f"Workers to use for scheduling. Default: {DEFAULT_CONFIG.defaults.workers}",
            ),
        )


@click.group(
    cls=BaseGroup,
    help="A tool for running and managing commands on the DIAG SOL cluster",
)
def cli():
    pass


def are_jobids_specified(jobids: List[int]) -> bool:
    are_specified = len(jobids) > 0
    if not are_specified:
        click.echo(
            "This operation requires specification of jobids with -i or --jobids"
        )
    return are_specified


@click.command(cls=SharedCommand, help="Run jobs")
@click.option(
    "-u",
    "--user",
    default=DEFAULT_CONFIG.defaults.username,
    help="Run command job(s) for the given user.",
)
@click.option(
    "-p",
    "--priority",
    default=DEFAULT_CONFIG.defaults.priority,
    type=click.Choice(["idle", "low", "high"], case_sensitive=False),
    help="Run command job(s) with priority level (idle|low|high)",
)
@click.option(
    "-r",
    "--reservation",
    default=None,
    help="Run command job(s) for the given reservation.",
)
@click.option(
    "-d",
    "--duration",
    default=None,
    type=int,
    help="Run command job(s) for the given duration.",
)
@click.option(
    "-x",
    "--ignore-errors",
    default=False,
    flag_value=True,
    help="Run command job(s) despite reported errors.",
)
def run(
    cmd_files: List[Path],
    jobids: List[int],
    workers: int,
    user: str,
    priority: str,
    reservation: str,
    duration: int,
    ignore_errors: bool,
):
    if are_jobids_specified(jobids=jobids) and is_config_valid():
        solitude.core.run(
            cmd_files=cmd_files,
            jobids=jobids,
            workers=workers,
            user=user,
            priority=priority,
            reservation=reservation,
            duration=duration,
            ignore_errors=ignore_errors,
            cfg=DEFAULT_CONFIG,
        )


@click.command(cls=SharedCommand, help="Extend running jobs")
def extend(cmd_files: List[Path], jobids: List[int], workers: int):
    if are_jobids_specified(jobids=jobids) and is_config_valid():
        solitude.core.extend(
            cmd_files=cmd_files,
            jobids=jobids,
            workers=workers,
            cfg=DEFAULT_CONFIG,
        )


@click.command(cls=SharedCommand, help="Stop running jobs")
def stop(cmd_files: List[Path], jobids: List[int], workers: int):
    if are_jobids_specified(jobids=jobids) and is_config_valid():
        solitude.core.stop(
            cmd_files=cmd_files,
            jobids=jobids,
            workers=workers,
            cfg=DEFAULT_CONFIG,
        )


@click.command(cls=SharedCommand, help="Link jobs to existing slurm job")
@click.option(
    "-s",
    "--slurm-jobid",
    "slurm_jobid",
    required=True,
    type=int,
    help="Slurm job id to link the jobs to.",
)
def link(
    cmd_files: List[Path], jobids: List[int], workers: int, slurm_jobid: int
):
    if are_jobids_specified(jobids=jobids) and is_config_valid():
        cfg = DEFAULT_CONFIG
        ssh_client = get_connected_ssh_client_from_config(
            cfg=cfg, verbose=False
        )
        if SlurmJob.check_if_job_exists(
            ssh_client=ssh_client, jobid=slurm_jobid
        ):
            for jobid in jobids:
                success = solitude.core.link(
                    cmd_files=cmd_files,
                    jobid=jobid,
                    slurm_jobid=slurm_jobid,
                    cfg=cfg,
                )
                click.echo(
                    f"Linked job id {jobid} to slurm job: {slurm_jobid} {'succeeded' if success else 'failed'}"
                )
        else:
            click.echo(f"Slurm job id: {slurm_jobid} does not exists...")


@click.command(cls=SharedCommand, help="Unlink jobs from slurm job")
def unlink(cmd_files: List[Path], jobids: List[int], workers: int):
    if are_jobids_specified(jobids=jobids) and is_config_valid():
        for jobid in jobids:
            success = solitude.core.unlink(
                cmd_files=cmd_files, jobid=jobid, cfg=DEFAULT_CONFIG
            )
            if success:
                click.echo(f"Unlinked job id {jobid} from slurm jobs.")
            else:
                click.echo(
                    f"Job id {jobid} has no slurm job associated with it."
                )


@click.command(cls=SharedCommand, help="Get log file for slurm job")
@click.option(
    "-p",
    "--poll",
    "active_polling",
    flag_value=True,
    default=False,
    help="Use this flag to enable active polling of the specified jobs. Default=No",
)
def getlog(
    cmd_files: List[Path],
    jobids: List[int],
    workers: int,
    active_polling: bool,
):
    if are_jobids_specified(jobids=jobids) and is_config_valid():
        for jobid in jobids:
            log_output = solitude.core.get_log(
                cmd_files=cmd_files,
                jobid=jobid,
                cfg=DEFAULT_CONFIG,
                active_polling=active_polling,
            )
            if log_output:
                if not active_polling:
                    click.echo(log_output)
            else:
                click.echo(
                    f"Job id {jobid} has no log file associated with it."
                )


@click.command(name="list", cls=SharedCommand, help="List jobs")
@click.option(
    "-s",
    "--selected-only",
    "selected_only",
    flag_value=True,
    default=False,
    help="Only display the jobs indicated by jobids. Default=No",
)
@click.option(
    "-np",
    "--no-progress",
    "show_progress_bar",
    flag_value=False,
    default=True,
    help="Hide progress bar while loading the list. Default=No",
)
def list_jobs(
    cmd_files: List[Path],
    jobids: List[int],
    workers: int,
    selected_only: bool,
    show_progress_bar: bool,
):
    if is_config_valid():
        solitude.core.list_jobs(
            cmd_files=cmd_files,
            jobids=jobids,
            workers=workers,
            selected_only=selected_only,
            show_progress_bar=show_progress_bar,
            cfg=DEFAULT_CONFIG,
        )


@click.group(cls=BaseGroup, help="Job operations")
def job():
    pass


@click.group(cls=BaseGroup, help="Configuration operations")
def config():
    pass


@click.command(cls=BaseCommand, help="Show status of the configuration")
def status():
    is_config_valid()
    if DEFAULT_CONFIG.is_config_present():
        click.echo(
            f"Configuration file found at: {DEFAULT_CONFIG.config_path}"
        )
        with open(DEFAULT_CONFIG.config_path, "r") as f:
            cfg = json.load(f)
        display_configuration(cfg=cfg)


@click.command(cls=BaseCommand, help="Create or refresh the configuration")
@click.option(
    "--user",
    prompt="Default username for running jobs using SOL",
    type=str,
    required=True,
    default=getpass.getuser(),
    help="Set default user to run jobs on SOL.",
)
@click.option(
    "--workers",
    type=int,
    default=8,
    help="Set default number of workers for issuing jobs on the server.",
)
@click.option(
    "--priority",
    type=click.Choice(["idle", "low", "high"]),
    default="low",
    help="Set default priority to run jobs with.",
)
@click.option(
    "--cmd-files",
    type=ClickPath(exists=True, dir_okay=False),
    multiple=True,
    default=(),
    help="Set default command file(s) to use.",
)
@click.option(
    "--ssh-server",
    prompt="Default ssh DIAG deep learning server to use",
    type=str,
    default=DEFAULT_SSH_SERVER,
    required=True,
    help="Set default ssh DIAG deep learning server. Any of: `dlc-{MACHINE}.umcn.nl`.",
)
@click.option(
    "--ssh-user",
    prompt="Default ssh username to use",
    type=str,
    default="diag",
    required=True,
    help="Set default ssh username.",
)
@click.option(
    "--ssh-pass",
    prompt="Default ssh password to use",
    type=str,
    required=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Set default ssh password.",
)
@click.option(
    "-i",
    "--ignore-test",
    default=False,
    flag_value=True,
    help="Ignore ssh connectivity test.",
)
@click.option(
    "-f",
    "--force",
    default=False,
    flag_value=True,
    help="Overwrite previous configuration file if it exists.",
)
def create(
    user: str,
    workers: int,
    priority: str,
    cmd_files: List[Path],
    ssh_server: str,
    ssh_user: str,
    ssh_pass: str,
    ignore_test: bool,
    force: bool,
):
    ssh_creds = {
        "server": ssh_server,
        "username": ssh_user,
        "password": ssh_pass,
    }
    cfgnew = {
        "defaults": {
            "username": user,
            "workers": workers,
            "priority": priority,
            "cmdfiles": list(map(str, cmd_files)),
        },
        "ssh": ssh_creds,
        "plugins": [],
    }
    if not ignore_test:
        connected = test_ssh_credentials(**ssh_creds)
        if not connected and not click.confirm(
            f"SSH connection failed using provided credentials. Do you want to keep these settings anyway?",
            default=False,
        ):
            return
    else:
        click.echo(f"TEST: CONNECT to server ({ssh_server}): SKIPPED...")

    if (
        not DEFAULT_CONFIG.is_config_present()
        or force
        or click.confirm(
            f"There already is a configuration file at: {DEFAULT_CONFIG.config_path}"
            f", Do you want to overwrite this file?",
            default=False,
        )
    ):
        click.echo(f"Writing configuration to: {DEFAULT_CONFIG.config_path}")
        DEFAULT_CONFIG.config_path.parent.mkdir(parents=True, exist_ok=True)
        json_write_atomic(fname=DEFAULT_CONFIG.config_path, data=cfgnew)
        display_configuration(cfg=cfgnew)


@click.command(
    name="test",
    cls=BaseCommand,
    help="Test the configuration's ssh credentials",
)
def test_config():
    if not DEFAULT_CONFIG.is_config_present():
        click.echo(
            "There is no configuration file present. Create one with: solitude config create"
        )
    else:
        test_ssh_credentials(*DEFAULT_CONFIG.ssh)


def test_ssh_credentials(server: str, username: str, password: str) -> bool:
    connected = SSHClient(exit_on_fail=False).connect(
        server, username, password
    )
    click.echo(
        f"TEST: CONNECT to server ({server}): {'SUCCESS' if connected else 'FAILED!'}"
    )
    if not connected:
        click.echo(
            f"Are you connected to the SOL network (VPN)?\n"
            f"Are the provided ssh credentials correct?\n"
        )
    return connected


def display_configuration(cfg: Dict):
    """Display configuration, but obscure the ssh password"""
    cfgcopy = copy.deepcopy(cfg)
    if "ssh" in cfgcopy and "password" in cfgcopy["ssh"]:
        cfgcopy["ssh"]["password"] = "********"
    click.echo("Configuration dump:")
    pprint.pprint(cfgcopy)


job.add_command(list_jobs)
job.add_command(run)
job.add_command(extend)
job.add_command(stop)
job.add_command(link)
job.add_command(unlink)
job.add_command(getlog)
cli.add_command(job)

config.add_command(status)
config.add_command(create)
config.add_command(test_config)
cli.add_command(config)


def main():
    logger = log_setup()
    logger.setLevel(logging.INFO)
    cli()


if __name__ == "__main__":
    main()
