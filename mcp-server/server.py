import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

from mcp.server.fastmcp import FastMCP
from tools.request_access import request_access
from tools.check_access import check_access
from tools.approve_access import approve_access
from tools.send_notification import send_notification

mcp = FastMCP("accessguard")
mcp.add_tool(request_access)
mcp.add_tool(check_access)
mcp.add_tool(approve_access)
mcp.add_tool(send_notification)

if __name__ == "__main__":
    mcp.run()
