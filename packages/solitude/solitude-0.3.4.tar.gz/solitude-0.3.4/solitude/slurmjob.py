from typing import Dict, Optional, Type

import logging
import time
import re

from solitude.cache import CacheData
from solitude.utils.ssh import SSHClient


SLURM_JOBINFO_QUERY = (
    '/opt/slurm/bin/squeue -j {jobid} -o "%.18i %.9P %.8j %.10T %.10M %R" -h'
)
SLURM_JOBINFO_PATTERN = re.compile(
    r"\s+(?P<jobid>\d+)\s+dlc-(?P<priority>\S+)\s+(?P<user>\S+)"
    r"\s+(?P<status>\S+)\s+(?P<runtime>\S+)\s+(?P<machine>\S+)\s+"
)
logger = logging.getLogger("SlurmJob")


class SlurmJob(CacheData):
    def __init__(
        self,
        jobid: int,
        user: Optional[str] = None,
        priority: Optional[str] = None,
        timestamp: Optional[int] = None,
        ssh_client: Optional[SSHClient] = None,
    ):
        super(SlurmJob, self).__init__(timestamp=timestamp)
        self.id: int = jobid
        self.user: Optional[str] = user
        self.priority: Optional[str] = priority
        self._status: Optional[str] = None
        self._ssh_client: Optional[SSHClient] = ssh_client

    def update(self):
        if self._ssh_client is None:
            raise ValueError("update - ssh_client was not set")
        result, _ = self._ssh_client.exec_command(
            cmd_to_execute=SLURM_JOBINFO_QUERY.format(jobid=self.id)
        )
        match_result = re.match(SLURM_JOBINFO_PATTERN, result)
        if match_result:
            info = match_result.groupdict()
        else:
            self._status = "IDLE"
            self.user = None
            self.priority = None
            return
        assert self.id == int(info["jobid"])
        self.id = int(info["jobid"])
        self.user = info["user"]
        self.priority = info["priority"]
        self._status = info["status"]

    def is_running(self) -> bool:
        return self._status in ("RUNNING", "PENDING")

    def is_pending(self) -> bool:
        return self._status == "PENDING"

    def is_timeout(self) -> bool:
        return self._status == "TIMEOUT"

    def get_log_text(self, active_polling: bool = False) -> str:
        if self._ssh_client is None:
            raise ValueError("get_log_text - ssh_client was not set")
        result = self._ssh_client.exec_command(
            cmd_to_execute=f"{'cat' if not active_polling else 'tail -f'} /mnt/cluster_storage/logfiles/slurm-{self.id}.out",
            active_polling=active_polling,
        )
        assert result is not None
        return result[0]

    def to_dict(self) -> Dict:
        return dict(
            id=self.id,
            user=self.user,
            priority=self.priority,
            timestamp=self.timestamp,
        )

    def exists(self) -> bool:
        if self._ssh_client is None:
            raise ValueError("exists - ssh_client was not set")
        return SlurmJob.check_if_job_exists(
            ssh_client=self._ssh_client, jobid=self.id
        )

    @staticmethod
    def check_if_job_exists(ssh_client: SSHClient, jobid: int) -> bool:
        result = ssh_client.exec_command(
            cmd_to_execute=SLURM_JOBINFO_QUERY.format(jobid=jobid)
        )
        assert result is not None
        return re.match(SLURM_JOBINFO_PATTERN, result[0]) is not None

    @classmethod
    def from_dict(cls: Type, dic: Dict) -> "SlurmJob":
        return SlurmJob(
            jobid=dic["id"],
            user=dic["user"],
            priority=dic["priority"],
            timestamp=dic.get("timestamp", int(time.time())),
        )
