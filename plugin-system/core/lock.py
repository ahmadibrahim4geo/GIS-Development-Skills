"""Atomic project lock with bounded wait timeout and stale-lock recovery."""

from __future__ import annotations

import json
import os
import socket
import time
from pathlib import Path

from .models import LockTimeoutError


class ProjectLock:
    """File-based cooperative lock supporting timeout and stale lock recovery."""

    def __init__(self, lock_path: Path, *, timeout_seconds: float = 30.0, stale_seconds: float = 600.0):
        self.lock_path = Path(lock_path)
        self.timeout_seconds = float(timeout_seconds)
        self.stale_seconds = float(stale_seconds)
        self._acquired = False

    def _is_stale(self) -> bool:
        try:
            data = json.loads(self.lock_path.read_text(encoding="utf-8"))
            acquired_at = float(data.get("acquired_at_epoch", 0))
            return (time.time() - acquired_at) >= self.stale_seconds
        except (OSError, ValueError, TypeError):
            try:
                age = time.time() - self.lock_path.stat().st_mtime
                return age >= self.stale_seconds
            except OSError:
                return False

    def acquire(self) -> None:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.timeout_seconds
        payload = json.dumps(
            {
                "pid": os.getpid(),
                "host": socket.gethostname(),
                "acquired_at_epoch": time.time(),
            },
            indent=2,
        ).encode("utf-8")

        while True:
            try:
                fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                try:
                    os.write(fd, payload)
                finally:
                    os.close(fd)
                self._acquired = True
                return
            except FileExistsError:
                if self._is_stale():
                    try:
                        self.lock_path.unlink(missing_ok=True)
                        continue
                    except OSError:
                        pass
                if time.monotonic() >= deadline:
                    raise LockTimeoutError(
                        f"Project lock held at {self.lock_path}; timed out after {self.timeout_seconds}s"
                    )
                time.sleep(0.05)

    def release(self) -> None:
        if self._acquired:
            try:
                self.lock_path.unlink(missing_ok=True)
            finally:
                self._acquired = False

    def __enter__(self) -> "ProjectLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()
