#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto-sync cibo.hk public docs into this repo.

Fetches the authoritative sources from cibo.hk and regenerates:
  - llms.txt     (verbatim mirror of https://cibo.hk/llms.txt)
  - openapi.json (verbatim mirror of https://cibo.hk/api/openapi.json)
  - README.md    (intro + llms.txt mirror + live MCP tool list + disclaimer)

Runs in GitHub Actions on a schedule. Uses only the Python stdlib so the
workflow has no pip dependencies.
"""
import json
import re
import sys
import urllib.request

LLMS_URL = "https://cibo.hk/llms.txt"
OPENAPI_URL = "https://cibo.hk/api/openapi.json"
MCP_URL = "https://cibo.hk/mcp/"

# Request timeout (seconds).
TIMEOUT = 30


def _get(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8")


def fetch_llms_txt() -> str:
    return _get(LLMS_URL)


def fetch_openapi_json() -> str:
    return _get(OPENAPI_URL)


def fetch_mcp_tools():
    """Return (tool_count, tools) where tools is a list of {name, description}.

    The Streamable HTTP MCP endpoint returns SSE: `event: message` then
    `data: {json}` per message. We parse every `data:` line and pick the one
    carrying the tools/list result.
    """
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    raw = _get(MCP_URL, data=body.encode("utf-8"), headers=headers)

    tools = []
    for line in raw.splitlines():
        if not line.startswith("data:"):
            continue
        payload = line[len("data:"):].strip()
        if not payload:
            continue
        try:
            obj = json.loads(payload)
        except json.JSONDecodeError:
            continue
        result = obj.get("result") or {}
        if isinstance(result, dict) and "tools" in result:
            tools = result["tools"]
            break

    normalized = []
    for t in tools:
        name = t.get("name", "")
        desc = t.get("description", "") or ""
        # Collapse multi-line docstrings into one line.
        desc = re.sub(r"\s+", " ", desc).strip()
        normalized.append({"name": name, "description": desc})

    normalized.sort(key=lambda t: t["name"])
    return len(normalized), normalized


def render_readme(llms_text: str, tool_count: int, tools: list) -> str:
    lines = []
    lines.append("# cibo.hk — HK IPO Allotment API & MCP Server")
    lines.append("")
    lines.append("面向 AI Agent 与开发者的**港股 IPO 中签分析**数据服务。提供两种接入方式：")
    lines.append("**REST API**（公开 JSON 端点）与 **MCP Server**（远程 Streamable HTTP，免安装）。")
    lines.append("")
    lines.append("- 网站：https://cibo.hk")
    lines.append("- 权威文档：https://cibo.hk/llms.txt （本 README 是其镜像，以 llms.txt 为准）")
    lines.append("- API 清单：https://cibo.hk/api/")
    lines.append("- OpenAPI Schema：https://cibo.hk/api/openapi.json")
    lines.append("- MCP 端点：https://cibo.hk/mcp")
    lines.append("")
    lines.append("> 由熊猫证券 CEO JW 用 AI 辅助编程构建。预测港股 IPO 中签率（可调申购倍数与 α 分配系数），")
    lines.append("> 并从过户处 ID 数据推断中签者画像（地区 / 国籍 / 性别 / 年龄），含港股通纳入分析、配发结果、")
    lines.append("> 国际配售、基石、全市场财务等。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 完整文档（权威镜像）")
    lines.append("")
    lines.append("以下内容逐字镜像自 https://cibo.hk/llms.txt：")
    lines.append("")
    lines.append(llms_text.rstrip("\n"))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"## MCP 工具清单（{tool_count} 个）")
    lines.append("")
    lines.append("工具清单由 MCP `tools/list` 实时生成。")
    lines.append("")
    lines.append("| 工具 | 说明 |")
    lines.append("|------|------|")
    for t in tools:
        name = t["name"]
        desc = t["description"] or ""
        lines.append(f"| `{name}` | {desc} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 免责声明")
    lines.append("")
    lines.append("本服务输出为统计模型结果，仅供参考，不构成投资建议。")
    lines.append("")
    return "\n".join(lines)


def main():
    llms_text = fetch_llms_txt()
    try:
        openapi_text = fetch_openapi_json()
    except Exception as e:
        print(f"WARNING: openapi.json fetch failed ({e}); keeping existing snapshot",
              file=sys.stderr)
        openapi_text = None
    tool_count, tools = fetch_mcp_tools()
    if tool_count == 0:
        print("WARNING: tools/list returned 0 tools; README tool list will be empty",
              file=sys.stderr)

    readme = render_readme(llms_text, tool_count, tools)

    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write(llms_text)
    if openapi_text is not None:
        with open("openapi.json", "w", encoding="utf-8") as f:
            f.write(openapi_text)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"llms.txt: {len(llms_text)} bytes")
    if openapi_text is not None:
        print(f"openapi.json: {len(openapi_text)} bytes")
    print(f"README.md: {len(readme)} bytes, {tool_count} tools")


if __name__ == "__main__":
    main()
