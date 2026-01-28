# TECHNICAL_SPEC.md - 技術仕様

> **対象読者**: エンジニア、システム管理者
> **目的**: データ構造、ファイル仕様、ディレクトリ構成を定義する

---

## 目次

1. [ディレクトリ構造](#ディレクトリ構造)
2. [データファイル仕様](#データファイル仕様)
3. [差分追跡仕様](#差分追跡仕様)
4. [アラートシステム](#アラートシステム)
5. [用語集](#用語集)

---

## ディレクトリ構造

```
japan-investment-analysis/
├── CLAUDE.md                           # エントリーポイント（クイックリファレンス）
├── README.md                           # プロジェクト概要
├── SETUP.md                            # セットアップ手順
│
├── docs/                               # ドキュメント（分割）
│   ├── STRATEGY.md                     # 戦略・理念（Why）
│   ├── METHODOLOGY.md                  # 評価フレームワーク（What）
│   ├── OPERATIONS.md                   # 実行プロトコル（How）
│   ├── TECHNICAL_SPEC.md               # 技術仕様（この文書）
│   └── MCP_SETUP.md                    # MCP設定
│
├── prompts/                            # LLM別最適化プロンプト（初期収集用）
│   ├── external/                       # 外部LLM用プロンプト
│   │   ├── prompt_company_info.md      # 企業・独占・財務情報
│   │   └── prompt_broad_info.md        # 広域情報（市場・政策）
│   ├── step0_collect_information.md    # 広域情報収集
│   ├── step0_5_discover_opportunities.md # 企業発掘
│   ├── step1_collect_events.md         # イベント収集
│   ├── step1_5_quality_check.md        # 品質チェック
│   ├── step2_update_monopoly_map.md    # 独占マップ更新
│   ├── step3_update_market_state.md    # 市場状態更新
│   ├── step4_analyze_market_risk.md    # 市場リスク分析
│   ├── step5_analyze_top30.md          # Top30分析
│   └── step6_generate_report.md        # レポート生成
│
├── data/
│   ├── state.json                      # 分析状態管理
│   ├── events.json                     # イベント記録
│   │
│   ├── checkpoints/                    # フェーズ完了チェックポイント
│   │   └── checkpoint_phaseN_YYYYMMDD.json
│   │
│   ├── diff/                           # 差分追跡
│   │   ├── latest_diff.json            # 最新の差分
│   │   └── history/                    # 差分履歴
│   │       └── diff_YYYYMMDD.json
│   │
│   ├── sources/
│   │   ├── primary_sources.json        # 一次情報源リスト
│   │   └── verification_protocols.json # 検証プロトコル
│   │
│   ├── intelligence/
│   │   ├── raw/                        # リアルタイム情報（毎回収集）
│   │   │   ├── company_info/           # 企業/独占/財務情報
│   │   │   │   ├── grok_cd.md          # Grok: 高速・広範囲スキャン
│   │   │   │   ├── gemini_cd.md        # Gemini: 包括的分析
│   │   │   │   ├── gpt_cd.md           # ChatGPT: 深い分析
│   │   │   │   └── claude_cd.md        # Claude: 自動・独自視点
│   │   │   └── broad_info/             # 市場/政策/トレンド
│   │   │       ├── grok_mi.md          # Grok: リアルタイム情報
│   │   │       ├── gemini_mi.md        # Gemini: メガトレンド
│   │   │       ├── chatgpt_mi.md       # ChatGPT: 深い分析
│   │   │       └── claude_mi.md        # Claude: 自動・独自視点
│   │   │
│   │   ├── stable/                     # 蓄積情報（変化頻度別）
│   │   │   ├── README.md               # stable/の使い方
│   │   │   ├── permanent/              # 永続情報（年次確認）
│   │   │   │   ├── companies.json      # 企業基礎（認証、モート）
│   │   │   │   └── domains.json        # ドメイン基礎
│   │   │   ├── quarterly/              # 安定情報（四半期更新）
│   │   │   │   ├── market_share.json   # 市場シェア
│   │   │   │   └── financials.json     # 財務情報
│   │   │   └── monthly/                # 動的情報（月次更新）
│   │   │       ├── contracts.json      # 契約・受注
│   │   │       └── investments.json    # 投資・M&A
│   │   │
│   │   ├── claude_supplemental.md      # Claude補足調査結果
│   │   ├── consolidated_companies.json # 統合企業情報
│   │   └── consolidated_broad.json     # 統合広域情報
│   │
│   ├── snapshots/
│   │   ├── monopoly_map.json           # 独占マップ
│   │   └── market_state.json           # 市場状態
│   │
│   ├── analysis/
│   │   ├── contradictions.json         # 矛盾検出結果
│   │   ├── gaps.json                   # ギャップ検出結果
│   │   ├── market_risk.json            # 市場リスク
│   │   └── top30.json                  # Top 30評価
│   │
│   └── performance/                    # パフォーマンス検証
│       ├── predictions/                # 予測記録
│       ├── actuals/                    # 実績記録
│       └── analysis/                   # 検証分析
│
├── reports/
│   └── [YYYY-MM-DD]/
│       ├── final_report.md
│       ├── executive_summary.md
│       ├── information_quality_report.md
│       └── quadrant_chart.html
│
├── latest/                             # 最新レポートへのシンボリックリンク
│   └── → reports/[YYYY-MM-DD]/
│
├── reinforcement/                      # 補強調査（継続的改善）
│   ├── pending_tasks.json              # 未実施タスクリスト
│   ├── learnings/                      # 学習記録
│   │   └── [YYYY-MM-DD].json           # 日次学習ファイル
│   ├── prompts/                        # LLM別プロンプト
│   │   ├── grok/                       # Grok用
│   │   │   └── [YYYY-MM-DD]_tasks.md
│   │   └── gemini/                     # Gemini用
│   │       └── [YYYY-MM-DD]_tasks.md
│   └── results/                        # LLM別結果
│       ├── claude_auto/                # Claude自動補強結果
│       │   └── [YYYY-MM-DD].md
│       ├── grok/                       # Grok結果
│       │   └── [YYYY-MM-DD].md
│       └── gemini/                     # Gemini結果
│           └── [YYYY-MM-DD].md
│
├── templates/
│   └── sample_report.md
│
└── scripts/                            # スクリプト
```

---

## データファイル仕様

> **Single Source of Truth**: `state.json` が分析状態の唯一の正式なソース。

### state.json

分析の状態を管理する。**全フェーズ完了時に更新必須。**

```json
{
  "last_execution": "2026-01-28T12:00:00Z",
  "analysis": {
    "market_risk": {
      "last_update": "2026-01-28",
      "last_score": 65,
      "previous_score": 62,
      "delta": "+3"
    },
    "top30": {
      "last_update": "2026-01-28",
      "top_conviction": "6857",
      "thesis_updates": 8
    }
  },
  "information_quality": {
    "last_check": "2026-01-28",
    "quality_score": 91,
    "active_alerts": 0
  },
  "gap_analysis": {
    "last_check": "2026-01-28",
    "gaps_filled": 9,
    "gaps_pending": 3
  },
  "contradictions": {
    "total_found": 7,
    "resolved": 7,
    "pending": 0
  },
  "critical_findings": [
    "重要な発見事項をここに記録"
  ]
}
```

---

### top30.json

Top 30企業の評価結果。

```json
{
  "metadata": {
    "date": "YYYY-MM-DD",
    "evaluation_system": "ボトルネック独占評価（100点満点）",
    "axes": {
      "bottleneck": {"max": 40, "description": "技術ボトルネック度"},
      "durability": {"max": 25, "description": "競争優位持続性"},
      "convergence": {"max": 20, "description": "収斂加速性"},
      "capital": {"max": 10, "description": "資本効率"},
      "asymmetry": {"max": 5, "description": "非対称性"}
    },
    "market_risk_score": 45,
    "attack_defense_stance": "balanced"
  },
  "top30": [
    {
      "rank": 1,
      "ticker": "6857",
      "name": "企業名",
      "core_technology": "主要技術/製品",
      "total": 85,
      "bottleneck": 38,
      "durability": 22,
      "convergence": 14,
      "capital": 8,
      "asymmetry": 3,
      "certainty": 88,
      "upside": 82,
      "quadrant": "prime",
      "thesis": "1-2文の投資テーゼ",
      "domains_impacted": ["AI", "エネルギー", "防衛"],
      "key_catalyst": "次のカタリストイベント",
      "catalyst_date": "2026-Q2",
      "risk": "主要リスク要因",
      "information_quality": {
        "confidence": "high",
        "sources_count": 5,
        "llm_agreement": 4
      }
    }
  ],
  "watchlist": [
    {
      "rank": 31,
      "ticker": "YYYY",
      "name": "企業",
      "total": 65,
      "thesis": "簡潔なテーゼ",
      "watch_reason": "確度上昇待ち"
    }
  ]
}
```

---

### market_risk.json

市場リスク分析結果。

```json
{
  "date": "YYYY-MM-DD",
  "total_score": 45,
  "risk_level": "medium",
  "recommended_stance": "balanced",
  "categories": {
    "tier1": {
      "monetary_policy": {
        "score": 8,
        "max": 15,
        "detail": "日銀据え置き、やや転換リスク",
        "indicators": ["日銀政策決定会合", "CPI"]
      },
      "leverage": {
        "score": 7,
        "max": 15,
        "detail": "円キャリーポジション中程度",
        "indicators": ["円キャリー残高", "信用取引残"]
      }
    },
    "tier2": {
      "valuation": {
        "score": 6,
        "max": 10,
        "detail": "PER適正水準",
        "indicators": ["日経平均PER", "PBR"]
      },
      "volatility": {
        "score": 4,
        "max": 10,
        "detail": "VIX低位安定",
        "indicators": ["VIX", "日経VI"]
      },
      "foreign_flows": {
        "score": 5,
        "max": 10,
        "detail": "外国人売買動向中立",
        "indicators": ["外国人売買動向"]
      }
    },
    "tier3": {
      "china_risk": {
        "score": 5,
        "max": 10,
        "detail": "中国減速懸念継続",
        "indicators": ["中国PMI", "不動産指標"]
      },
      "geopolitics": {
        "score": 6,
        "max": 10,
        "detail": "台湾リスクやや上昇",
        "indicators": ["台湾海峡動向"]
      },
      "liquidity": {
        "score": 2,
        "max": 10,
        "detail": "市場流動性正常",
        "indicators": ["出来高", "スプレッド"]
      },
      "fx_risk": {
        "score": 4,
        "max": 10,
        "detail": "円安基調継続",
        "indicators": ["ドル円", "実質実効為替レート"]
      }
    }
  },
  "historical_analog": "現在明確な歴史的類似なし",
  "key_watchpoints": [
    "日銀政策決定会合のシグナル",
    "台湾海峡の軍事活動",
    "企業業績予想の改定"
  ]
}
```

---

### events.json

イベント記録（4次元評価付き）。

```json
{
  "events": [
    {
      "id": "evt_YYYYMMDD_NNN",
      "date": "YYYY-MM-DD",
      "type": "policy|earnings|ma|contract|market_data|geopolitics",
      "category": "A|B|C|D|E|F|G",
      "content": {
        "title": "イベントタイトル",
        "detail": "詳細説明",
        "affected_tickers": ["8035", "6857"],
        "affected_domains": ["AI", "エネルギー"]
      },
      "certainty": {
        "stage": "official_announcement",
        "score": 75,
        "rationale": "経産省プレスリリースで確認",
        "upgrade_trigger": "契約締結で90に上昇"
      },
      "verification": {
        "level": "primary_confirmed",
        "sources": [
          {"type": "primary", "name": "経産省", "url": "https://..."},
          {"type": "secondary", "name": "日経", "date": "2026-01-26"}
        ]
      },
      "asymmetry": {
        "score": 18,
        "sources": {
          "language_barrier": true,
          "supply_chain_depth": false,
          "certification_barrier": false
        },
        "known_by": ["日本機関投資家"],
        "unknown_to": ["グローバルマクロファンド"],
        "resolution_trigger": "英語メディア報道"
      },
      "freshness": {
        "event_date": "2026-01-26",
        "recorded_at": "2026-01-26T10:30:00Z",
        "decay_rate": "slow",
        "valid_until": "2026-03-31"
      }
    }
  ]
}
```

---

### consolidated_companies.json

統合企業情報。

```json
{
  "metadata": {
    "generated_at": "2026-01-27T12:00:00Z",
    "sources": {
      "llm_outputs": 8,
      "stable_data": 9,
      "reinforcement": 3
    },
    "total_companies": 87,
    "quality_summary": {
      "high_confidence": 45,
      "medium_confidence": 30,
      "low_confidence": 12
    }
  },
  "companies": [
    {
      "ticker": "6857",
      "name": "企業名",
      "domains": ["AI", "エネルギー"],
      "core_technology": "主要技術",
      "data": {
        "market_share": {
          "value": "45%",
          "confidence": "high",
          "source": "primary_confirmed",
          "last_updated": "2026-01-15"
        },
        "certifications": {
          "value": ["防衛調達認定", "原子力規制適合"],
          "confidence": "high",
          "source": "stable/permanent",
          "last_verified": "2025-12-01"
        },
        "recent_contracts": [
          {
            "value": "500億円 防衛省契約",
            "confidence": "high",
            "source": "防衛省発表",
            "date": "2026-01-20"
          }
        ],
        "financials": {
          "revenue_ttm": "2500億円",
          "fcf_ttm": "300億円",
          "debt_ebitda": 1.5,
          "confidence": "high",
          "source": "有価証券報告書",
          "as_of": "2025-12-31"
        }
      },
      "llm_mentions": {
        "grok": true,
        "gemini": true,
        "chatgpt": true,
        "claude": true
      },
      "contradictions": [],
      "gaps": ["競合詳細情報が不足"]
    }
  ]
}
```

---

### pending_tasks.json

未実施の補強タスク（LLM割り当て情報を含む）。

```json
{
  "generated_at": "2026-01-27T12:00:00Z",
  "claude_auto_completed": [
    {
      "id": "task_001",
      "type": "verification",
      "target": "XXXX市場シェア",
      "reason": "一次情報源で検証",
      "result_file": "results/claude_auto/2026-01-27.md",
      "status": "completed",
      "completed_at": "2026-01-27T12:30:00Z"
    }
  ],
  "grok_tasks": [
    {
      "id": "task_002",
      "type": "coverage",
      "priority": 2,
      "target": "宇宙ドメイン",
      "reason": "候補企業が3社のみ",
      "prompt_file": "prompts/grok/space_coverage_20260127.md",
      "status": "pending",
      "created_at": "2026-01-27T12:00:00Z"
    }
  ],
  "gemini_tasks": [
    {
      "id": "task_004",
      "type": "deep_dive",
      "priority": 2,
      "target": "YYYY企業詳細",
      "reason": "財務・競争構造の深掘り",
      "prompt_file": "prompts/gemini/yyyy_deep_dive_20260127.md",
      "status": "pending",
      "created_at": "2026-01-27T12:00:00Z"
    }
  ],
  "summary": {
    "claude_auto_completed": 1,
    "grok_pending": 1,
    "gemini_pending": 1,
    "total_pending": 2
  }
}
```

---

## stable/ - 蓄積情報ストレージ

### 目的

過去の情報をクリーニング・整理し、変化の速度に応じて階層化。次回以降の分析で再利用・更新する。

### ディレクトリ構造

```
stable/
├── README.md              # 使い方
├── permanent/             # 永続情報（年単位で変化）
│   ├── companies.json     # 企業基礎情報（認証、モート、競争構造）
│   └── domains.json       # ドメイン基礎情報
├── quarterly/             # 四半期情報（3ヶ月で変化）
│   ├── financials.json    # 財務情報
│   └── market_share.json  # 市場シェア
└── monthly/               # 月次情報（月単位で変化）
    ├── contracts.json     # 契約・受注情報
    └── investments.json   # 投資・M&A情報
```

### 重要: stable/の役割と限界

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
│  - 防衛調達認定、原子力規制適合等の認証                               │
│  - 参入障壁の構造的要因                                              │
│                                                                     │
│  動的情報（LLM収集を優先、stable/は参照値）:                          │
│  - 市場シェア（競合動向で変動）                                      │
│  - モートの強度（技術優位性は変動可能）                              │
│  - 受注残・契約金額（常に最新を優先）                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 更新・クリーニングルール

| 分類 | 更新タイミング | 保持期間 |
|------|---------------|---------|
| permanent | 年次レビュー、または重大イベント発生時 | 2年（超過で要レビュー） |
| quarterly | 決算発表後1週間以内 | 6ヶ月 |
| monthly | フル分析時（Phase 5） | 3ヶ月 |

---

## 差分追跡仕様

### 差分検出ルール

| 変動タイプ | 検出条件 | アクション |
|-----------|---------|-----------|
| Top 30追加 | 新規企業がTop 30に入った | diff_report.added に記録 |
| Top 30除外 | 企業がTop 30から外れた | diff_report.removed に記録 |
| スコア変動 | スコアが±3以上変動 | diff_report.score_changes に記録 |
| 順位変動 | Top 10内で順位が±2以上変動 | diff_report.rank_changes に記録 |
| 市場リスク変動 | 市場リスクスコアが±5以上変動 | diff_report.market_risk_change に記録 |

---

## アラートシステム

### アラートレベル定義

| レベル | 説明 | 通知方法 |
|--------|------|---------|
| critical | 即時対応が必要 | レポート冒頭に表示、即時通知 |
| high | 重要な変動 | レポートのアラートセクションに表示 |
| medium | 注目すべき変動 | レポート内に記載 |
| low | 情報提供 | ログに記録のみ |

### アラートトリガー

| トリガー条件 | アラートレベル | メッセージ例 |
|-------------|---------------|-------------|
| 市場リスク 76+ | critical | 市場リスク極高: ディフェンシブ推奨 |
| 市場リスク ±10以上変動 | high | 市場リスク急変: 42→58 (+16) |
| Top 10 スコア±5以上 | high | 6857 スコア急変: 92→86 (-6) |
| Top 30 入れ替え | medium | Top30: +XXXX, -YYYY |
| 重大矛盾検出 | high | 矛盾検出: XXXX売上（1800億円 vs 1400億円） |
| 情報鮮度切れ | medium | 鮮度警告: XXXX市場シェア（180日超） |
| 一次情報源未確認 | low | 確認待ち: YYYY契約（単一ソース） |

---

## 用語集

### サプライチェーン用語

| 用語 | 定義 | 非対称性レベル |
|------|------|---------------|
| Tier 1 | 最終製品メーカーに直接納入 | 低（可視性高い） |
| Tier 2 | Tier 1に納入 | 中 |
| Tier 3 | Tier 2に納入 | 高（ほぼ不可視） |

### 日本市場用語

| 用語 | 定義 |
|------|------|
| EDINET | 有価証券報告書等の電子開示システム |
| 適時開示 | 東証への重要事実の開示 |
| 決算短信 | 四半期/通期決算の速報 |
| 有価証券報告書 | 年次の詳細な財務・事業報告 |

### 評価用語

| 用語 | 定義 |
|------|------|
| ボトルネック | 代替が困難で、複数の産業が依存する技術・企業 |
| モート | 持続可能な競争優位性（参入障壁） |
| カタリスト | 株価認識のトリガーとなるイベント |
| FCF | フリーキャッシュフロー |
| PER | 株価収益率 |
| PBR | 株価純資産倍率 |

### 情報品質用語

| 用語 | 定義 |
|------|------|
| 一次情報源 | 政府、EDINET、公式発表など直接的な情報源 |
| 二次情報源 | 通信社、業界メディアなど一次を引用する情報源 |
| LLM一致 | 複数のLLMが同一の情報を報告 |
| 確度重み | 情報の信頼性に基づく評価への重み付け係数 |

---

## 関連ドキュメント

- [STRATEGY.md](./STRATEGY.md) - 戦略・理念
- [METHODOLOGY.md](./METHODOLOGY.md) - 評価フレームワーク
- [OPERATIONS.md](./OPERATIONS.md) - 実行プロトコル
