#!/usr/bin/env python3
"""
EDINET API専用MCPサーバー
日本企業の開示情報を自動取得

使用方法:
1. pip install mcp httpx
2. .mcp.jsonに以下を追加:
   {
     "mcpServers": {
       "edinet": {
         "type": "stdio",
         "command": "python",
         "args": ["scripts/mcp_servers/edinet_server.py"]
       }
     }
   }
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Any, Optional
import sys

try:
    import httpx
except ImportError:
    print("Error: httpx not installed. Run: pip install httpx", file=sys.stderr)
    sys.exit(1)

# EDINET API設定
EDINET_BASE_URL = "https://disclosure.edinet-fsa.go.jp/api/v2"

# 対象とする書類タイプ
DOC_TYPES = {
    "120": "有価証券報告書",
    "130": "四半期報告書",
    "140": "半期報告書",
    "150": "臨時報告書",
    "160": "有価証券届出書",
    "170": "発行登録書",
    "350": "大量保有報告書"
}


async def fetch_documents(date: str, doc_type: int = 2) -> dict:
    """
    EDINET APIから開示書類を取得

    Args:
        date: 日付（YYYY-MM-DD形式）
        doc_type: 書類種別（1:メタデータのみ, 2:詳細情報含む）

    Returns:
        APIレスポンス（JSON）
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{EDINET_BASE_URL}/documents.json",
                params={"date": date, "type": doc_type}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e), "results": []}


async def fetch_recent_documents(days: int = 7) -> list:
    """
    直近N日間の開示書類を取得

    Args:
        days: 取得日数

    Returns:
        開示書類のリスト
    """
    results = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        data = await fetch_documents(date)
        if "results" in data:
            results.extend(data["results"])
    return results


def filter_by_company(documents: list, company_name: str) -> list:
    """企業名でフィルタ"""
    return [
        d for d in documents
        if company_name.lower() in d.get("filerName", "").lower()
    ]


def filter_by_doc_type(documents: list, doc_type_codes: list) -> list:
    """書類タイプでフィルタ"""
    return [
        d for d in documents
        if d.get("docTypeCode") in doc_type_codes
    ]


def extract_key_info(document: dict) -> dict:
    """
    書類から重要情報を抽出

    Returns:
        簡略化された書類情報
    """
    return {
        "docID": document.get("docID"),
        "edinetCode": document.get("edinetCode"),
        "secCode": document.get("secCode"),  # 証券コード
        "filerName": document.get("filerName"),
        "docTypeCode": document.get("docTypeCode"),
        "docTypeName": DOC_TYPES.get(document.get("docTypeCode"), "その他"),
        "submitDateTime": document.get("submitDateTime"),
        "docDescription": document.get("docDescription"),
        "pdfFlag": document.get("pdfFlag"),
        "attachDocFlag": document.get("attachDocFlag")
    }


# =============================================================================
# メイン処理（スタンドアロンテスト用）
# =============================================================================

async def main():
    """テスト実行"""
    print("EDINET API テスト")
    print("=" * 50)

    # 本日の書類を取得
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n{today} の開示書類を取得中...")

    data = await fetch_documents(today)

    if "results" in data:
        docs = data["results"]
        print(f"取得件数: {len(docs)}件")

        # 有価証券報告書のみ抽出
        yuho = filter_by_doc_type(docs, ["120"])
        print(f"有価証券報告書: {len(yuho)}件")

        # 最初の5件を表示
        for doc in docs[:5]:
            info = extract_key_info(doc)
            print(f"\n  [{info['secCode']}] {info['filerName']}")
            print(f"  → {info['docTypeName']}: {info['docDescription']}")
    else:
        print(f"エラー: {data.get('error', '不明なエラー')}")


if __name__ == "__main__":
    asyncio.run(main())
