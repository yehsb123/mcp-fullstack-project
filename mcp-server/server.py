# MCP Server 엔트리포인트
# 2주차에 구현

# TODO: MCP Server 초기화
# TODO: 4개 Tool 등록
# TODO: 서버 실행

import os
import sys

# backend/ 아래 app 패키지(services 등)를 import할 수 있도록 경로 추가
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
