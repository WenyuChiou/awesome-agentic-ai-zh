"""Manual Docker smoke test for Smolagents' host control channel.

Run this only after ``docker version`` succeeds. It builds/starts the official
Jupyter executor, proves the host can execute one tiny statement, and confirms
the control port is published only on loopback. The normal offline tests do not call it.
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from smolagents import DockerExecutor
from smolagents.monitoring import AgentLogger, LogLevel

from starter import codeact_executor_config


def test_docker_control_channel() -> None:
    config = codeact_executor_config()
    executor = None
    try:
        executor = DockerExecutor(
            additional_imports=[],
            logger=AgentLogger(level=LogLevel.ERROR),
            build_new_image=True,
            **config,
        )
        output = executor.run_code_raise_errors("print(2 + 2)")
        assert "4" in output.logs
        executor.container.reload()
        bindings = executor.container.attrs["NetworkSettings"]["Ports"]["8888/tcp"]
        assert bindings
        assert all(binding["HostIp"] == "127.0.0.1" for binding in bindings)
    finally:
        if executor is not None:
            executor.cleanup()


if __name__ == "__main__":
    test_docker_control_channel()
    print("docker smoke pass")
