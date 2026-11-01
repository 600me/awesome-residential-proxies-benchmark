"""cloud-infra-tco-mcp — MCP server & CLI for 2026 cloud infrastructure TCO benchmarking.

Pure Python standard library. Author: CloudBench Research (MIT).
"""

from .server import TOOL_SPECS, dispatch_tool, main, run_self_test  # noqa: F401

__version__ = "1.0.0"
