# stable/ - 蓄積情報ストレージ

> **目的**: 過去の情報をクリーニング・整理し、変化の速度に応じて階層化。次回以降の分析で再利用・更新する。

---

## 重要: stable/の役割と限界

### stable/は「ベースライン」であり「絶対優先」ではない

```
┌─────────────────────────────────────────────────────────────────────┐
│                    stable/の正しい使い方                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  stable/の役割:                                                      │
│  ✓ 過去の検証済み情報の保存                                          │
│  ✓ 次回分析の「ベースライン」として使用                              │
│  ✓ LLM収集との「差異検知」のための比較対象                           │
│                                                                     │
│  stable/の限界（注意点）:                                            │
│  ✗ 「固定化」すると変化を見逃す                                      │
│  ✗ 新しいLLM収集より常に優先すべきではない                           │
│  ✗ ランキングの硬直化を招く可能性                                    │
│                                                                     │
│  【解決策: 静的/動的情報の分離】                                      │
│                                                                     │
│  静的情報（stable/優先）:                                            │
│  - 認証（防衛省認定、原子力規制委員会許可等）                         │
│  - 参入障壁の構造的要因                                              │
│  - 法的・規制的独占（唯一の認定製造者等）                             │
│                                                                     │
│  動的情報（LLM収集を優先、stable/は参照値）:                          │
│  - 市場シェア（競合動向で変動）                                      │
│  - モートの強度（技術優位性は変動可能）                              │
│  - 受注残・契約金額（常に最新を優先）                                │
│  - 財務指標（四半期で変動）                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5軸スコアへの影響

| 軸 | 配点 | stable/依存度 | 変動要因 |
|----|------|--------------|---------|
| 技術ボトルネック度 | 40 | **混在** | 認証=静的、市場シェア=動的 |
| 競争優位持続性 | 25 | 中 | 技術優位は比較的静的だが追い上げリスクあり |
| 収斂加速性 | 20 | 中 | ドメイン構造は比較的静的 |
| 資本効率 | 10 | 低 | 四半期財務で変動 |
| 非対称性 | 5 | 低 | 市場認識は常に動的 |

→ **技術ボトルネック度（40点）が最も固定化リスクあり。市場シェアは毎回LLM収集で検証すること。**

---

## ディレクトリ構造

```
stable/
├── README.md              # このファイル
├── permanent/             # 永続情報（年単位で変化）
│   ├── companies.json     # 企業基礎情報（認証、モート、競争構造）
│   └── domains.json       # ドメイン基礎情報（技術基盤、規制環境）
├── quarterly/             # 四半期情報（3ヶ月で変化）
│   ├── financials.json    # 財務情報（売上、利益、ガイダンス）
│   └── market_share.json  # 市場シェア
└── monthly/               # 月次情報（月単位で変化）
    ├── contracts.json     # 契約・受注情報
    └── investments.json   # 投資・M&A情報
```

---

## 鮮度分類の基準

| 分類 | 変化頻度 | 収集タイミング | 更新トリガー |
|------|---------|---------------|-------------|
| **permanent** | 年次以下 | 初回収集 + 年次確認 | 認証取得/喪失、M&A、大規模組織変更 |
| **quarterly** | 四半期 | 決算発表後 | 決算発表、市場調査レポート更新 |
| **monthly** | 月次 | 月次分析時 | 契約発表、投資発表、プロジェクト進捗 |

---

## 各ファイルの詳細

### permanent/companies.json - 企業基礎情報

```json
{
  "metadata": {
    "last_updated": "2026-01-28",
    "update_reason": "初回収集",
    "next_review": "2027-01-28"
  },
  "companies": {
    "6501": {
      "name": "日立製作所",
      "ticker": "6501",
      "domains": ["エネルギー", "AI", "ロボティクス"],
      "moat": {
        "type": "技術独占",
        "description": "BWRX-300（GE日立）、送配電システム、Lumada",
        "durability": "high",
        "source": "有価証券報告書 2025年度",
        "last_verified": "2026-01-28"
      },
      "certifications": [
        {
          "name": "原子力規制委員会認定",
          "status": "active",
          "expiry": null,
          "source": "原子力規制委員会公開資料"
        }
      ],
      "competitive_structure": {
        "position": "dominant",
        "competitors": ["東芝", "三菱重工"],
        "barriers_to_entry": ["原子力認証", "長期顧客関係", "技術蓄積"],
        "source": "業界分析 2025"
      }
    }
  }
}
```

### permanent/domains.json - ドメイン基礎情報

```json
{
  "metadata": {
    "last_updated": "2026-01-28",
    "next_review": "2027-01-28"
  },
  "domains": {
    "エネルギー": {
      "regulatory_environment": {
        "key_regulations": ["原子力規制委員会規則", "電気事業法", "GX推進法"],
        "trend": "緩和（原発再稼働推進）",
        "source": "経済産業省"
      },
      "technology_base": {
        "key_technologies": ["BWRX-300", "変圧器", "パワー半導体"],
        "maturity": "成熟→成長（原発回帰）",
        "source": "業界レポート"
      },
      "supply_chain_structure": {
        "critical_nodes": ["日本製鋼所（圧力容器）", "三菱重工（原子炉）"],
        "vulnerabilities": ["熟練工不足", "サプライチェーン老朽化"],
        "source": "サプライチェーン分析"
      }
    }
  }
}
```

### quarterly/financials.json - 財務情報

```json
{
  "metadata": {
    "last_updated": "2026-01-28",
    "quarter": "Q3 FY2025",
    "next_update": "2026-02-15"
  },
  "companies": {
    "6501": {
      "revenue": {
        "value": 3200000000000,
        "currency": "JPY",
        "period": "Q3 FY2025",
        "yoy_growth": 0.08,
        "source": "日立 決算短信 Q3 FY2025"
      },
      "segment_breakdown": {
        "デジタルシステム&サービス": {
          "value": 800000000000,
          "pct_of_total": 0.25
        },
        "グリーンエナジー&モビリティ": {
          "value": 600000000000,
          "pct_of_total": 0.19
        }
      },
      "guidance": {
        "full_year_revenue": 9500000000000,
        "confidence": "high",
        "source": "決算説明会"
      }
    }
  }
}
```

### quarterly/market_share.json - 市場シェア

```json
{
  "metadata": {
    "last_updated": "2026-01-28",
    "sources": ["富士経済", "矢野経済研究所", "業界レポート"]
  },
  "markets": {
    "産業用ロボット": {
      "total_market_size": 2500000000000,
      "currency": "JPY",
      "year": 2025,
      "shares": {
        "6954": { "company": "ファナック", "pct": 0.25, "source": "矢野経済 2025" },
        "6506": { "company": "安川電機", "pct": 0.15, "source": "矢野経済 2025" },
        "6861": { "company": "キーエンス", "pct": 0.10, "source": "矢野経済 2025" }
      }
    }
  }
}
```

### monthly/contracts.json - 契約・受注情報

```json
{
  "metadata": {
    "last_updated": "2026-01-28",
    "next_update": "2026-02-28"
  },
  "contracts": [
    {
      "id": "contract_20260115_001",
      "company": "三菱重工業",
      "ticker": "7011",
      "type": "defense",
      "value": 500000000000,
      "currency": "JPY",
      "customer": "防衛省",
      "description": "次期戦闘機開発（GCAP）",
      "announced_date": "2026-01-15",
      "duration_months": 120,
      "source": "防衛省報道発表",
      "source_url": "https://www.mod.go.jp/...",
      "domains": ["防衛", "宇宙"],
      "certainty": 95
    }
  ]
}
```

### monthly/investments.json - 投資・M&A情報

```json
{
  "metadata": {
    "last_updated": "2026-01-28",
    "next_update": "2026-02-28"
  },
  "investments": [
    {
      "id": "inv_20260120_001",
      "type": "capex",
      "company": "ソニーグループ",
      "ticker": "6758",
      "value": 300000000000,
      "currency": "JPY",
      "description": "CMOSイメージセンサー増産投資",
      "announced_date": "2026-01-20",
      "source": "決算説明会資料",
      "domains": ["AI", "ロボティクス"],
      "beneficiaries": ["東京エレクトロン", "SCREENホールディングス"],
      "certainty": 90
    }
  ]
}
```

---

## 更新・クリーニングルール

### 更新タイミング

| 分類 | 更新タイミング | 担当 |
|------|---------------|------|
| permanent | 年次レビュー、または重大イベント発生時 | Gemini（深掘り） |
| quarterly | 決算発表後1週間以内 | Gemini（財務分析） |
| monthly | フル分析時（Phase 5） | Grok（広域）+ Claude（検証） |

### クリーニングルール

1. **重複排除**: 同一情報は最新のソースで上書き
2. **確度チェック**: 確度50%未満の情報は削除または要検証フラグ
3. **鮮度チェック**:
   - permanent: 2年超で要レビュー
   - quarterly: 6ヶ月超で削除
   - monthly: 3ヶ月超で削除（契約完了等は permanent へ昇格）
4. **情報昇格**:
   - monthly → quarterly: 四半期で安定した情報
   - quarterly → permanent: 年単位で安定した情報

### 統合ルール（Phase 5）- 改訂版

```
【重要】静的/動的情報で優先順位が異なる

┌─────────────────────────────────────────────────────────────────────┐
│  静的情報（認証、参入障壁）                                          │
│  優先順位: 一次情報源 > stable/permanent > LLM収集                   │
│  → stable/を優先、LLMで「取消・変更」報告時のみ検証                 │
├─────────────────────────────────────────────────────────────────────┤
│  動的情報（市場シェア、モート強度、契約、財務）                      │
│  優先順位: 一次情報源 > LLM収集（4LLM一致）> stable/ > LLM（3LLM）   │
│  → LLM収集を優先、stable/は「比較ベースライン」                     │
│  → 差異がある場合は「変化アラート」を生成                           │
└─────────────────────────────────────────────────────────────────────┘

全体優先順位（高い順）:
1. 一次情報源で確認済み（EDINET, 経産省, 防衛省, 原子力規制委員会）
2. 今回のLLM収集結果（4LLM一致）← 高確度の新規情報
3. stable/permanent（認証・参入障壁等の静的情報のみ）
4. 今回のLLM収集結果（3LLM一致）
5. stable/quarterly（四半期情報）
6. stable/monthly（月次情報）
7. 今回のLLM収集結果（2LLM以下）
8. reinforcement/results/（補強調査結果）
```

---

## 次回分析への引き継ぎ

Phase 9（完了）で以下を更新:

1. **新規収集情報の分類**:
   - 認証・モート情報 → permanent/companies.json
   - 財務・市場シェア → quarterly/
   - 契約・投資 → monthly/

2. **陳腐化情報のクリーニング**:
   - 鮮度切れ情報を削除
   - 更新された情報で上書き

3. **state.json への記録**:
   ```json
   "stable_update": {
     "last_update": "2026-01-28",
     "permanent_companies": 45,
     "quarterly_financials": 30,
     "monthly_contracts": 25,
     "next_review": {
       "permanent": "2027-01-28",
       "quarterly": "2026-04-28",
       "monthly": "2026-02-28"
     }
   }
   ```
