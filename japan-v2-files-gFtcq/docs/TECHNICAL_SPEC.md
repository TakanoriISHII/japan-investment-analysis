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
us-investment-analysis/
├── CLAUDE.md                           # エントリーポイント（クイックリファレンス）
├── README.md                           # プロジェクト概要
│
├── docs/                               # ドキュメント（分割）
│   ├── STRATEGY.md                     # 戦略・理念（Why）
│   ├── METHODOLOGY.md                  # 評価フレームワーク（What）
│   ├── OPERATIONS.md                   # 実行プロトコル（How）
│   └── TECHNICAL_SPEC.md               # 技術仕様（この文書）
│
├── prompts/                            # LLM別最適化プロンプト（初期収集用）
│   ├── README.md                       # プロンプト概要
│   ├── shared/                         # 共通定義
│   │   └── definitions.md              # ドメイン、カテゴリ定義
│   ├── grok/                           # Grok用（速度重視）- 初期収集専用
│   │   ├── README.md
│   │   ├── broad_info.md               # 広域情報収集
│   │   └── company_scan.md             # 企業スキャン
│   ├── gemini/                         # Gemini用（深さ重視）- 初期収集専用
│   │   ├── README.md
│   │   ├── company_deep.md             # 企業深掘り
│   │   └── broad_info.md               # 広域情報（詳細）
│   ├── claude/                         # Claude用（検証重視）
│   │   ├── README.md
│   │   ├── contradiction_resolver.md   # 矛盾解消
│   │   ├── primary_source_verifier.md  # 一次情報源確認
│   │   ├── high_asymmetry_verifier.md  # 高非対称性確認
│   │   └── top30_reinforcement.md      # Top 30補強
│   └── external/                       # 旧プロンプト（参考用）
│       ├── README.md
│       ├── prompt_company_info.md
│       └── prompt_broad_info.md
│   # ※補強調査プロンプトは reinforcement/prompts/ に配置（ルートレベル）
│
├── data/
│   ├── state.json                      # 分析状態管理
│   ├── events.json                     # イベント記録
│   ├── information_quality.json        # 品質アラート
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
│   │   │   │   ├── grok.md             # Grok: 高速・広範囲スキャン
│   │   │   │   ├── gemini.md           # Gemini: 包括的分析
│   │   │   │   └── claude.md           # Claude: 自動・独自視点
│   │   │   └── broad_info/             # 市場/政策/トレンド
│   │   │       ├── grok.md             # Grok: リアルタイム情報
│   │   │       ├── gemini.md           # Gemini: メガトレンド
│   │   │       └── claude.md           # Claude: 自動・独自視点
│   │   │
│   │   ├── stable/                     # 蓄積情報（変化頻度別）
│   │   │   ├── permanent/              # 永続情報（年次確認）
│   │   │   │   ├── certifications.json
│   │   │   │   ├── moats.json
│   │   │   │   └── market_structure.json
│   │   │   ├── quarterly/              # 安定情報（四半期更新）
│   │   │   │   ├── market_share.json
│   │   │   │   ├── financials.json
│   │   │   │   └── policy_framework.json
│   │   │   └── monthly/                # 動的情報（月次更新）
│   │   │       ├── contracts.json
│   │   │       ├── investments.json
│   │   │       └── project_progress.json
│   │   │
│   │   ├── claude_supplemental.md      # Claude補足調査結果
│   │   ├── consolidated_companies.json # 統合企業情報
│   │   └── consolidated_broad.json     # 統合広域情報
│   │
│   ├── discovery/                      # 発見記録
│   │
│   ├── snapshots/
│   │   ├── monopoly_map.json
│   │   └── market_state.json
│   │
│   ├── analysis/
│   │   ├── contradictions.json         # 矛盾検出結果
│   │   ├── gaps.json                   # ギャップ検出結果
│   │   ├── gap_analysis.json
│   │   ├── market_risk.json
│   │   └── top30.json
│   │
│   └── performance/                    # パフォーマンス検証（新規）
│       ├── predictions/                # 予測記録
│       │   └── [YYYY-MM-DD]/
│       │       ├── top30_snapshot.json
│       │       ├── catalysts.json
│       │       └── market_risk.json
│       ├── actuals/                    # 実績記録
│       │   └── [YYYY-MM-DD]/
│       │       ├── price_performance.json
│       │       ├── catalyst_outcomes.json
│       │       └── events_occurred.json
│       └── analysis/                   # 検証分析
│           ├── monthly_review.json
│           ├── quarterly_review.json
│           └── annual_review.json
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
│   ├── learnings/                      # 学習記録（Phase 8で必須生成）
│   │   └── [YYYY-MM-DD].json           # 日次学習ファイル（精度、遅延、改善）
│   ├── prompts/                        # LLM別プロンプト（次回手動実行用）
│   │   ├── grok/                       # Grok用: カバレッジ、大量タスク
│   │   │   └── [YYYY-MM-DD]_tasks.md
│   │   └── gemini/                     # Gemini用: 企業深掘り、技術分析
│   │       └── [YYYY-MM-DD]_tasks.md
│   └── results/                        # LLM別結果
│       ├── claude_auto/                # Claude自動補強結果（必須）
│       │   └── [YYYY-MM-DD].md
│       ├── grok/                       # Grok結果（手動実行後）
│       │   └── [YYYY-MM-DD].md
│       └── gemini/                     # Gemini結果（手動実行後）
│           └── [YYYY-MM-DD].md
│
└── templates/
    └── quadrant_chart_template.html
```

---

## データファイル仕様

> **Single Source of Truth**: `state.json` が分析状態の唯一の正式なソース。
> `events.json` と `information_quality.json` は詳細ログ用（オプション）。

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
      "top_conviction": "NVDA",
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
    "evaluation_system": "5軸評価（100点満点）",
    "axes": {
      "monopoly": {"max": 30, "description": "物理的独占力"},
      "resilience": {"max": 20, "description": "政策耐性"},
      "synergy": {"max": 25, "description": "クロスドメイン・シナジー"},
      "asymmetry": {"max": 15, "description": "情報非対称性"},
      "capital": {"max": 10, "description": "資本効率"}
    },
    "market_risk_score": 45,
    "attack_defense_stance": "balanced"
  },
  "top30": [
    {
      "rank": 1,
      "ticker": "XXXX",
      "name": "企業名",
      "core_technology": "主要技術/製品",
      "total": 85,
      "monopoly": 28,
      "resilience": 18,
      "synergy": 20,
      "asymmetry": 12,
      "capital": 7,
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
        "llm_agreement": 3
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
      "policy_pivot": {
        "score": 12,
        "max": 20,
        "detail": "FRB据え置き、やや転換リスク",
        "indicators": ["Fed dot plot", "CPI trend"]
      },
      "valuation": {
        "score": 10,
        "max": 15,
        "detail": "CAPE 32、高いが極端ではない",
        "indicators": ["CAPE ratio", "Forward P/E"]
      }
    },
    "tier2": {
      "concentration": {
        "score": 8,
        "max": 12,
        "detail": "トップ10がS&P 500の35%",
        "indicators": ["Top 10 weight", "HHI"]
      },
      "leverage": {
        "score": 4,
        "max": 12,
        "detail": "信用取引残は中程度",
        "indicators": ["Margin debt", "HY spreads"]
      },
      "sentiment": {
        "score": 5,
        "max": 10,
        "detail": "VIX低、強気だが陶酔ではない",
        "indicators": ["VIX", "Bull/Bear ratio", "IPO volume"]
      }
    },
    "tier3": {
      "external": {
        "score": 7,
        "max": 11,
        "detail": "台湾リスク上昇",
        "indicators": ["Taiwan Strait activity", "Sanctions news"]
      },
      "liquidity": {
        "score": 3,
        "max": 10,
        "detail": "市場は正常に機能",
        "indicators": ["Repo rates", "Bid-ask spreads"]
      },
      "earnings_divergence": {
        "score": 5,
        "max": 10,
        "detail": "株価対EPSのギャップは控えめ",
        "indicators": ["Price vs EPS growth", "Revision ratio"]
      }
    }
  },
  "historical_analog": "現在明確な歴史的類似なし",
  "key_watchpoints": [
    "FRBコミュニケーションの転換シグナル",
    "台湾海峡の軍事活動",
    "企業業績予想の改定"
  ],
  "scenario_triggers": {
    "risk_increase": ["Fed hawkish pivot", "China-Taiwan escalation"],
    "risk_decrease": ["Inflation cooling", "Geopolitical de-escalation"]
  }
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
      "type": "policy|earnings|contract|market|geopolitics",
      "category": "A|B|C|D|E|F|G",
      "content": {
        "title": "イベントタイトル",
        "detail": "詳細説明",
        "affected_tickers": ["XXXX", "YYYY"],
        "affected_domains": ["AI", "エネルギー"]
      },
      "certainty": {
        "stage": "official_announcement",
        "score": 75,
        "rationale": "DoDプレスリリースで確認",
        "upgrade_trigger": "契約締結で90に上昇"
      },
      "verification": {
        "level": "primary_confirmed",
        "sources": [
          {"type": "primary", "name": "DoD", "url": "https://..."},
          {"type": "secondary", "name": "Defense News", "date": "2025-01-26"}
        ]
      },
      "asymmetry": {
        "score": 15,
        "known_by": ["防衛セクターアナリスト"],
        "unknown_to": ["ジェネラリスト投資家"],
        "resolution_trigger": "決算説明会での言及"
      },
      "freshness": {
        "event_date": "2025-01-26",
        "recorded_at": "2025-01-26T10:30:00Z",
        "decay_rate": "medium",
        "valid_until": "2025-06-30"
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
      "llm_outputs": 6,
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
      "ticker": "XXXX",
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
          "value": ["ITAR", "DoD Secret"],
          "confidence": "high",
          "source": "stable/permanent",
          "last_verified": "2025-12-01"
        },
        "recent_contracts": [
          {
            "value": "$500M DoD contract",
            "confidence": "high",
            "source": "SAM.gov",
            "date": "2026-01-20"
          }
        ],
        "financials": {
          "revenue_ttm": "$2.5B",
          "fcf_ttm": "$300M",
          "debt_ebitda": 1.5,
          "confidence": "high",
          "source": "10-K",
          "as_of": "2025-12-31"
        }
      },
      "llm_mentions": {
        "grok": true,
        "gemini": true,
        "claude": true
      },
      "contradictions": [],
      "gaps": ["競合詳細情報が不足"]
    }
  ]
}
```

---

### pending.json

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
    },
    {
      "id": "task_003",
      "type": "realtime",
      "priority": 1,
      "target": "地政学リスク更新",
      "reason": "台湾情勢の最新情報",
      "prompt_file": "prompts/grok/geopolitics_update_20260127.md",
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
  "chatgpt_tasks": [],
  "summary": {
    "claude_auto_completed": 1,
    "grok_pending": 2,
    "gemini_pending": 1,
    "chatgpt_pending": 0,
    "total_pending": 3
  }
}
```

---

### checkpoint_phaseN_YYYYMMDD.json

フェーズ完了時のチェックポイント。

```json
{
  "phase": 5,
  "timestamp": "2026-01-27T15:30:00Z",
  "status": "completed",
  "outputs": {
    "consolidated_companies": {
      "path": "data/intelligence/consolidated_companies.json",
      "hash": "sha256:abc123..."
    },
    "consolidated_broad": {
      "path": "data/intelligence/consolidated_broad.json",
      "hash": "sha256:def456..."
    }
  },
  "input_hashes": {
    "raw/company_info/grok.md": "sha256:111...",
    "raw/company_info/gemini.md": "sha256:222...",
    "raw/broad_info/grok.md": "sha256:333..."
  },
  "metrics": {
    "companies_processed": 87,
    "high_confidence_count": 45,
    "contradictions_resolved": 12
  }
}
```

---

### diff_YYYYMMDD.json

前回分析との差分記録。

```json
{
  "comparison": {
    "current_date": "2026-01-27",
    "previous_date": "2026-01-20"
  },
  "top30_changes": {
    "added": [
      {
        "ticker": "XYZ",
        "rank": 12,
        "score": 78,
        "reason": "新規防衛契約$500M獲得"
      }
    ],
    "removed": [
      {
        "ticker": "ABC",
        "previous_rank": 28,
        "reason": "政策リスク増加によりスコア低下"
      }
    ],
    "score_changes": [
      {
        "ticker": "NVDA",
        "previous_score": 92,
        "current_score": 94,
        "change": 2,
        "reason": "データセンター売上予想上方修正"
      }
    ],
    "rank_changes": [
      {
        "ticker": "DEF",
        "previous_rank": 5,
        "current_rank": 3,
        "change": 2
      }
    ]
  },
  "market_risk_change": {
    "previous_score": 42,
    "current_score": 48,
    "change": 6,
    "level_change": null,
    "main_factors": ["バリュエーション上昇", "台湾リスクやや増加"]
  },
  "new_information": [
    {
      "type": "policy",
      "title": "Stargate第2フェーズ発表",
      "importance": "high",
      "affected_tickers": ["NVDA", "MSFT", "ORA"]
    },
    {
      "type": "geopolitics",
      "title": "台湾海峡緊張度やや低下",
      "importance": "medium",
      "affected_domains": ["AI", "防衛"]
    }
  ],
  "alerts_generated": [
    {
      "type": "score_change",
      "severity": "medium",
      "message": "NVDA スコア+2 (92→94)"
    }
  ]
}
```

---

### performance/predictions/[DATE]/top30_snapshot.json

パフォーマンス検証用の予測記録。

```json
{
  "snapshot_date": "2026-01-27",
  "market_risk_score": 45,
  "companies": [
    {
      "ticker": "XXXX",
      "rank": 1,
      "total_score": 85,
      "price_at_snapshot": 150.25,
      "predicted_catalysts": [
        {
          "event": "Q1決算発表",
          "expected_date": "2026-04-15",
          "expected_impact": "positive"
        }
      ],
      "asymmetry_score": 12,
      "certainty_score": 88
    }
  ]
}
```

---

### performance/analysis/quarterly_review.json

四半期検証レポート。

```json
{
  "period": "2026-Q1",
  "generated_at": "2026-04-01T10:00:00Z",
  "summary": {
    "top30_avg_return": 12.5,
    "benchmark_return": 8.2,
    "excess_return": 4.3,
    "catalyst_hit_rate": 0.65,
    "asymmetry_resolution_rate": 0.25
  },
  "axis_analysis": {
    "monopoly": {
      "top_decile_return": 15.2,
      "bottom_decile_return": 5.1,
      "correlation": 0.42,
      "assessment": "effective"
    },
    "resilience": {
      "top_decile_return": 11.8,
      "bottom_decile_return": 7.2,
      "correlation": 0.28,
      "assessment": "moderate"
    },
    "synergy": {
      "top_decile_return": 14.5,
      "bottom_decile_return": 6.8,
      "correlation": 0.38,
      "assessment": "effective"
    },
    "asymmetry": {
      "top_decile_return": 18.2,
      "bottom_decile_return": 8.5,
      "correlation": 0.51,
      "assessment": "highly_effective"
    },
    "capital": {
      "top_decile_return": 10.2,
      "bottom_decile_return": 9.1,
      "correlation": 0.12,
      "assessment": "review_needed"
    }
  },
  "quadrant_analysis": {
    "prime": {"count": 12, "avg_return": 16.5},
    "speculative": {"count": 8, "avg_return": 22.1},
    "stable": {"count": 10, "avg_return": 8.2}
  },
  "recommendations": [
    {
      "type": "weight_adjustment",
      "axis": "capital",
      "current_weight": 10,
      "proposed_weight": 8,
      "rationale": "相関が低く、予測力が弱い"
    }
  ]
}
```

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

### 差分計算フロー

```
前回 top30.json + market_risk.json
              ↓
        差分計算
              ↓
┌─────────────────────────────────┐
│ diff_YYYYMMDD.json              │
│ - added/removed 企業            │
│ - score_changes                 │
│ - rank_changes                  │
│ - market_risk_change            │
│ - new_information               │
│ - alerts_generated              │
└─────────────────────────────────┘
              ↓
        latest_diff.json にコピー
              ↓
        history/ に保存
```

### 差分レポート生成

`diff report` コマンド実行時:

1. `data/diff/latest_diff.json` を読み込み
2. マークダウン形式でレポートを生成
3. 重要な変動をハイライト
4. 必要に応じてアラートを発行

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
| Top 10 スコア±5以上 | high | NVDA スコア急変: 92→86 (-6) |
| Top 30 入れ替え | medium | Top30: +XYZ, -ABC |
| 重大矛盾検出 | high | 矛盾検出: NVDA売上（$18B vs $14B） |
| 情報鮮度切れ | medium | 鮮度警告: XXXX市場シェア（180日超） |
| 一次情報源未確認 | low | 確認待ち: YYYY契約（単一ソース） |

### アラート出力形式

```json
// data/alerts/alert_YYYYMMDD_NNN.json
{
  "id": "alert_20260127_001",
  "timestamp": "2026-01-27T10:30:00Z",
  "level": "high",
  "type": "market_risk_change",
  "title": "市場リスク急上昇",
  "message": "市場リスクスコアが42から58に上昇（+16）",
  "details": {
    "previous_value": 42,
    "current_value": 58,
    "change": 16,
    "main_factors": ["バリュエーション過熱", "地政学リスク増"]
  },
  "recommended_action": "ポジションサイズ見直しを推奨",
  "acknowledged": false,
  "acknowledged_at": null
}
```

### アラート集約レポート

```markdown
## アラートサマリー: 2026-01-27

### Critical (0件)
なし

### High (2件)
1. [市場リスク] 42→58 (+16) - バリュエーション過熱
2. [スコア変動] NVDA 92→86 (-6) - 輸出規制リスク増

### Medium (3件)
1. [Top30変動] 新規: XYZ (Rank 12)
2. [鮮度警告] AAAA市場シェア - 180日超
3. [情報不足] BBBB契約 - 単一ソース

### 推奨アクション
- [ ] 市場リスク上昇への対応検討
- [ ] NVDA輸出規制影響の詳細分析
- [ ] AAAA市場シェアの更新調査
```

---

## 用語集

### サプライチェーン用語

| 用語 | 定義 | 非対称性レベル |
|------|------|---------------|
| プライムコントラクター | 政府との直接契約 | 低（可視） |
| Tier 1 | プライムに直接供給 | 低 |
| Tier 2 | Tier 1に供給 | 中 |
| Tier 3 | Tier 2に供給 | 高（しばしば不可視） |

### 政策用語

| 用語 | 定義 |
|------|------|
| NDAA | 国防権限法（年次防衛政策法案） |
| HALEU | 高濃縮低濃縮ウラン（先進炉向け5-20%濃縮） |
| SMR | 小型モジュール炉（300MW未満） |
| PPA | 電力購入契約 |
| SAM.gov | 連邦契約データベース（System for Award Management） |
| FPDS | 連邦調達データシステム |
| 13F | 機関投資家保有状況を示すSEC提出書類 |

### 評価用語

| 用語 | 定義 |
|------|------|
| Book-to-Bill | 受注 ÷ 売上（1.0超 = 受注残増加） |
| TAM | 総アドレス可能市場 |
| モート | 持続可能な競争優位性 |
| カタリスト | 株価認識のトリガーとなるイベント |
| SBC | 株式報酬（Stock-Based Compensation） |
| FCF | フリーキャッシュフロー |
| CAPE | 景気調整済みPER（Cyclically Adjusted P/E） |

### 情報品質用語

| 用語 | 定義 |
|------|------|
| 一次情報源 | 政府、SEC、公式発表など直接的な情報源 |
| 二次情報源 | 通信社、業界メディアなど一次を引用する情報源 |
| LLM一致 | 複数のLLMが同一の情報を報告 |
| 確度重み | 情報の信頼性に基づく評価への重み付け係数 |

---

## 関連ドキュメント

- [STRATEGY.md](./STRATEGY.md) - 戦略・理念
- [METHODOLOGY.md](./METHODOLOGY.md) - 評価フレームワーク
- [OPERATIONS.md](./OPERATIONS.md) - 実行プロトコル
