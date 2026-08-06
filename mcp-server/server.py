import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "..", "backend")

sys.path.insert(0, BACKEND_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, ".env"))

import app.db.models.user
import app.db.models.access_request
import app.db.models.permission
import app.db.models.audit_log

from mcp.server.fastmcp import FastMCP
from tools.request_access import request_access
from tools.check_access import check_access
from tools.approve_access import approve_access
from tools.send_notification import send_notification
from tools.list_requests import list_requests
from tools.get_audit_logs import get_audit_logs
from tools.search_policy import search_policy

mcp = FastMCP("accessguard")
mcp.add_tool(request_access)
mcp.add_tool(check_access)
mcp.add_tool(approve_access)
mcp.add_tool(send_notification)
mcp.add_tool(list_requests)
mcp.add_tool(get_audit_logs)
mcp.add_tool(search_policy)

if __name__ == "__main__":
    mcp.run()
