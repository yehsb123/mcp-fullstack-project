"""
AccessGuard Agent 그래프 시각화 스크립트
사용법: python scripts/visualize_graph.py
출력: scripts/agent_graph.md (Mermaid 코드) + 콘솔 출력
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from agent.graph import build_graph


def main():
    graph = build_graph()
    mermaid = graph.get_graph().draw_mermaid()

    out_path = os.path.join(os.path.dirname(__file__), "agent_graph.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("```mermaid\n")
        f.write(mermaid)
        f.write("\n```\n")

    print("=== AccessGuard Agent Graph (Mermaid) ===\n")
    print(mermaid)
    print(f"\nSaved to: {out_path}")
    print("mermaid.live 에 붙여넣으면 PNG/SVG 다운로드 가능")


if __name__ == "__main__":
    main()
