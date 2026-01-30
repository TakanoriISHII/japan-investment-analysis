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
│  - NRC/FAA/DoD認証（取消されるまで有効）                             │
│  - 参入障壁の構造的要因                                              │
│  - 法的・規制的独占（認定製造者等）                                   │
│                                                                     │
│  動的情報（LLM収集を優先、stable/は参照値）:                          │
│  - 市場シェア（競合動向で変動）                                      │
│  - モートの強度（技術優位性は変動可能）                              │
│  - 受注残・契約金額（常に最新を優先）                                │
│  - 財務指標（四半期で変動）                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5軸スコアへの影響（Graham分類体系統合版）

| 分類 | 軸 | 配点 | stable/依存度 | 変動要因 |
|------|-----|------|--------------|---------|
| B.投資的 | 構造的優位性 | 20 | **混在** | 認証=静的、市場シェア=動的 |
| B.投資的 | 本質的価値 | 20 | 低 | 四半期財務・バリュエーションで変動 |
| A.投機的 | 将来の価値 | 25 | 中 | ドメイン構造は比較的静的 |
| A.投機的 | 情報非対称性 | 20 | 低 | 市場認識は常に動的 |
| A.投機的 | 政策・触媒 | 15 | 低 | 政策変更・カタリストは動的 |

→ **構造的優位性（20点）が最も固定化リスクあり。市場シェアは毎回LLM収集で検証すること。**

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
    "NVDA": {
      "name": "NVIDIA Corporation",
      "ticker": "NVDA",
      "domains": ["AI", "ロボティクス", "防衛"],
      "moat": {
        "type": "技術独占",
        "description": "CUDA ecosystem、学習済みモデル最適化",
        "durability": "high",
        "source": "10-K FY2025",
        "last_verified": "2026-01-28"
      },
      "certifications": [
        {
          "name": "ITAR",
          "status": "active",
          "expiry": null,
          "source": "DoD Contractor List"
        }
      ],
      "competitive_structure": {
        "position": "dominant",
        "competitors": ["AMD", "Intel"],
        "barriers_to_entry": ["CUDA lock-in", "ソフトウェアエコシステム"],
        "source": "Industry analysis 2025"
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
    "AI": {
      "regulatory_environment": {
        "key_regulations": ["AI Act (EU)", "Executive Order 14110"],
        "trend": "strengthening",
        "source": "Federal Register"
      },
      "technology_base": {
        "key_technologies": ["Transformer", "GPU computing", "HBM"],
        "maturity": "growth",
        "source": "Industry reports"
      },
      "supply_chain_structure": {
        "critical_nodes": ["TSMC (fabrication)", "SK Hynix (HBM)"],
        "vulnerabilities": ["台湾集中リスク"],
        "source": "Supply chain analysis"
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
    "quarter": "Q3 FY2026",
    "next_update": "2026-02-15"
  },
  "companies": {
    "NVDA": {
      "revenue": {
        "value": 57000000000,
        "currency": "USD",
        "period": "Q3 FY2026",
        "yoy_growth": 0.94,
        "source": "NVDA 10-Q Q3 FY2026"
      },
      "segment_breakdown": {
        "data_center": {
          "value": 51200000000,
          "pct_of_total": 0.898
        },
        "gaming": {
          "value": 3200000000,
          "pct_of_total": 0.056
        }
      },
      "guidance": {
        "next_quarter_revenue": 60000000000,
        "confidence": "high",
        "source": "Earnings call"
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
    "sources": ["Gartner", "IDC", "Industry reports"]
  },
  "markets": {
    "data_center_gpu": {
      "total_market_size": 100000000000,
      "currency": "USD",
      "year": 2025,
      "shares": {
        "NVDA": { "pct": 0.88, "source": "IDC Q3 2025" },
        "AMD": { "pct": 0.10, "source": "IDC Q3 2025" },
        "Intel": { "pct": 0.02, "source": "IDC Q3 2025" }
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
      "company": "BWXT",
      "ticker": "BWXT",
      "type": "defense",
      "value": 2600000000,
      "currency": "USD",
      "customer": "US Navy",
      "description": "海軍原子力推進システム",
      "announced_date": "2026-01-15",
      "duration_months": 60,
      "source": "SAM.gov",
      "source_url": "https://sam.gov/...",
      "domains": ["エネルギー", "防衛"],
      "certainty": 99
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
      "company": "META",
      "ticker": "META",
      "value": 65000000000,
      "currency": "USD",
      "description": "2025年AI設備投資計画",
      "announced_date": "2026-01-20",
      "source": "Earnings call Q4 2024",
      "domains": ["AI"],
      "beneficiaries": ["NVDA", "VRT", "EATON"],
      "certainty": 95
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
│  優先順位: 一次情報源 > LLM収集（3LLM一致）> stable/ > LLM（2LLM）   │
│  → LLM収集を優先、stable/は「比較ベースライン」                     │
│  → 差異がある場合は「変化アラート」を生成                           │
└─────────────────────────────────────────────────────────────────────┘

全体優先順位（高い順）:
1. 一次情報源で確認済み（SEC, SAM.gov, DoD）
2. 今回のLLM収集結果（3LLM一致）← 高確度の新規情報
3. stable/permanent（認証・参入障壁等の静的情報のみ）
4. 今回のLLM収集結果（2LLM一致）
5. stable/quarterly（四半期情報）
6. stable/monthly（月次情報）
7. 今回のLLM収集結果（単一）
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
