# MCP（Model Context Protocol）拡張ガイド

## 概要

このドキュメントでは、japan-investment-analysisプロジェクトの情報収集能力を強化するためのMCP設定を説明します。

---

## 現在の制約

| 方法 | 状態 | 問題 |
|------|------|------|
| WebFetch | ❌ | 多くのサイトで403エラー |
| WebSearch | ✅ | 間接的な情報取得のみ |

---

## MCP拡張による解決

### Phase 1: 基本拡張（Fetch Server）

**.mcp.json（現在の設定）:**

```json
{
  "mcpServers": {
    "fetch": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "description": "Web content fetching - converts HTML to markdown"
    }
  }
}
```

**セットアップ手順:**

```bash
# 1. uvx（Python パッケージランナー）の確認
uvx --version

# 2. mcp-server-fetchの動作確認
uvx mcp-server-fetch --help

# 3. Claude Code再起動後、MCPツールが利用可能に
/mcp
```

**利用可能なオプション:**
- `--user-agent USER_AGENT`: カスタムUser-Agent文字列
- `--ignore-robots-txt`: robots.txt制限を無視
- `--proxy-url PROXY_URL`: プロキシURL指定

---

### Phase 2: ブラウザ自動化（Puppeteer）

**目的**: JavaScript動的サイト（EDINET、政府サイト等）へのアクセス

**.mcp.json に追加:**

```json
{
  "mcpServers": {
    "puppeteer": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-puppeteer"]
    }
  }
}
```

**セットアップ手順:**

```bash
# Chromiumの依存関係（Linux）
sudo apt-get install -y chromium-browser

# または
npx puppeteer browsers install chrome
```

**利用例:**

```
# Claude Code内で
> puppeteer_navigate to https://disclosure.edinet-fsa.go.jp/
> puppeteer_screenshot
> puppeteer_evaluate "document.querySelector('table').innerText"
```

---

### Phase 3: カスタムAPIサーバー

**目的**: EDINET API等の専用接続

**ファイル: `scripts/mcp_servers/edinet_server.py`**

```python
#!/usr/bin/env python3
"""
EDINET API専用MCPサーバー
日本企業の開示情報を自動取得
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Any

import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

# サーバー初期化
server = Server("edinet-api")

EDINET_BASE_URL = "https://disclosure.edinet-fsa.go.jp/api/v2"

@server.tool()
async def fetch_today_documents() -> dict:
    """本日の開示書類一覧を取得"""
    today = datetime.now().strftime("%Y-%m-%d")
    return await _fetch_documents(today)

@server.tool()
async def fetch_documents_by_date(date: str) -> dict:
    """指定日の開示書類を取得（形式: YYYY-MM-DD）"""
    return await _fetch_documents(date)

@server.tool()
async def fetch_recent_documents(days: int = 7) -> list:
    """直近N日間の開示書類を取得"""
    results = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        docs = await _fetch_documents(date)
        results.extend(docs.get("results", []))
    return results

@server.tool()
async def search_company_documents(edinetCode: str) -> list:
    """企業コードで開示書類を検索"""
    # 直近30日を検索
    all_docs = await fetch_recent_documents(30)
    return [d for d in all_docs if d.get("edinetCode") == edinetCode]

async def _fetch_documents(date: str) -> dict:
    """EDINET APIから書類取得"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{EDINET_BASE_URL}/documents.json",
            params={"date": date, "type": 2}
        )
        return response.json()

if __name__ == "__main__":
    import mcp
    mcp.run(server)
```

**セットアップ:**

```bash
# 依存関係インストール
pip install mcp httpx

# .mcp.jsonに追加
{
  "mcpServers": {
    "edinet": {
      "type": "stdio",
      "command": "python",
      "args": ["scripts/mcp_servers/edinet_server.py"]
    }
  }
}
```

---

## 情報収集フローの変化

### Before（現在）

```
WebSearch → 検索結果 → 手動でデータ抽出 → events.json
```

### After（MCP拡張後）

```
┌─────────────────────────────────────────────────┐
│ 自動収集パイプライン                              │
├─────────────────────────────────────────────────┤
│                                                 │
│  EDINET MCP ─┬→ 開示書類 ─┐                     │
│              │            │                     │
│  Puppeteer ──┼→ 政府サイト ┼→ 4次元評価 → JSON   │
│              │            │                     │
│  WebSearch ──┴→ ニュース ─┘                     │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## トラブルシューティング

### MCPサーバーが認識されない

```bash
# キャッシュクリア
claude mcp reset-project-choices

# 再読み込み
claude mcp list
```

### npmパッケージエラー

```bash
# キャッシュクリア
npm cache clean --force

# 直接インストール
npm install -g @anthropic/mcp-server-fetch
```

### 権限エラー

```bash
# .mcp.jsonの権限確認
chmod 644 .mcp.json
```

---

## 次のステップ

1. **Phase 1テスト**: fetch MCPサーバーで403回避を確認
2. **Phase 2導入**: Puppeteerで動的サイト対応
3. **Phase 3開発**: EDINET専用サーバーの実装

---

## 参考リンク

- [MCP公式ドキュメント](https://modelcontextprotocol.io/)
- [Claude Code MCP設定](https://docs.anthropic.com/claude-code/mcp)
- [EDINET API仕様](https://disclosure.edinet-fsa.go.jp/EKW0EZ0015.html)
