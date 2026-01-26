# 情報統合ガイド（Claude + 外部LLM）

## このファイルの目的

このファイルは、Claude自身および外部LLMから収集した情報を統合・処理する際の手順を定義します。

**重要**: Claudeも外部LLMも**同じフォーマット**で出力し、同じ統合プロセスで処理されます。

---

## 統合の全体フロー

```
┌─────────────────────────────────────────────────────────┐
│              情報収集フェーズ（並列実行可能）              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Claude                    外部LLM                      │
│  「企業発掘を収集」         Gemini/GPT-4/Perplexity      │
│  「広域情報を収集」                                      │
│  「独占情報を収集」                                      │
│  「財務情報を収集」                                      │
│         ↓                        ↓                     │
│  claude_YYYYMMDD.md        [llm名]_YYYYMMDD.md         │
│         ↓                        ↓                     │
│         └────────────┬───────────┘                     │
│                      ↓                                  │
│            data/intelligence/raw/                       │
└─────────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│              統合フェーズ（「情報を統合」コマンド）        │
├─────────────────────────────────────────────────────────┤
│  1. 全ファイル読み込み（Claude + 外部LLM）               │
│  2. 品質チェック                                        │
│  3. 重複排除・矛盾解決                                   │
│  4. 検証度昇格（複数ソース→multi_source）                │
│  5. consolidated_*.json 生成                            │
└─────────────────────────────────────────────────────────┘
```

---

## ファイル配置

### 入力（Claude + 外部LLM出力）

```
data/intelligence/raw/
├── company_discovery/
│   ├── claude_20250126.md      ★Claude出力
│   ├── gemini_20250126.md      外部LLM出力
│   ├── gpt4_20250126.md
│   └── perplexity_20250126.md
├── broad_intelligence/
│   ├── claude_20250126.md      ★Claude出力
│   ├── gemini_20250126.md
│   └── gpt4_20250126.md
├── monopoly_info/
│   ├── claude_20250126.md      ★Claude出力
│   ├── gemini_20250126.md
│   └── gpt4_20250126.md
└── financial_management/
    ├── claude_20250126.md      ★Claude出力
    ├── gemini_20250126.md
    └── gpt4_20250126.md
```

### 出力（統合済み）

```
data/intelligence/
├── consolidated_companies_YYYYMMDD.json
├── consolidated_intelligence_YYYYMMDD.json
├── consolidated_monopoly_YYYYMMDD.json
└── consolidated_financial_YYYYMMDD.json
```

---

## Claude情報収集の実行手順

### 「企業発掘を収集」コマンド実行時

```
1. prompts/external/00_common_instructions.md を読み込み
2. prompts/external/01_company_discovery.md を読み込み
3. Web検索を活用して50社を発掘
4. 統一フォーマット（Markdownテンプレート）で出力
5. data/intelligence/raw/company_discovery/claude_YYYYMMDD.md に保存
```

### 「広域情報を収集」コマンド実行時

```
1. prompts/external/00_common_instructions.md を読み込み
2. prompts/external/02_broad_intelligence.md を読み込み
3. Web検索を活用して7カテゴリの情報を収集
4. 統一フォーマットで出力
5. data/intelligence/raw/broad_intelligence/claude_YYYYMMDD.md に保存
```

### 「独占情報を収集」コマンド実行時

```
1. prompts/external/00_common_instructions.md を読み込み
2. prompts/external/03_monopoly_info.md を読み込み
3. Web検索を活用してシェア・参入障壁情報を収集
4. 統一フォーマットで出力
5. data/intelligence/raw/monopoly_info/claude_YYYYMMDD.md に保存
```

### 「財務情報を収集」コマンド実行時

```
1. prompts/external/00_common_instructions.md を読み込み
2. prompts/external/04_financial_management.md を読み込み
3. Web検索を活用してROE/FCF/経営評価を収集
4. 統一フォーマットで出力
5. data/intelligence/raw/financial_management/claude_YYYYMMDD.md に保存
```

---

## 統合処理の詳細

### Step 1: 品質チェック

各ファイルを読み込み、以下を確認：

| チェック項目 | 対応 |
|-------------|------|
| メタデータがあるか | なければ警告、ファイル名からLLM名・日付を推定 |
| 4次元評価があるか | なければ該当情報を除外または低スコア付与 |
| ソースが明記されているか | なければ検証度を single_unverified に |
| フォーマットが正しいか | パースエラーは警告、可能な範囲で処理 |

### Step 2: 重複排除

**企業発掘の場合**:
```
1. 証券コードで重複を検出
2. 同一企業が複数ソース（Claude含む）から発掘された場合:
   - 4次元評価の高い方を採用
   - 両方の情報をマージ
   - discovered_by に全ソースを記録
   - 検証度を multi_source に昇格
```

**情報の場合**:
```
1. タイトル・内容の類似度で重複を検出
2. 同一情報が複数ソースから報告された場合:
   - 検証度を multi_source に昇格
   - より詳細な方を採用
   - ソースをマージ
```

### Step 3: 矛盾解決

**シェア情報の矛盾**:
```
ソースA: 「A社のシェアは91%」
ソースB: 「A社のシェアは85%」

解決手順:
1. 各ソースの出典を確認
2. 一次資料（SEMI、Gartner等）を優先
3. 一次資料がない場合、範囲として記録（85-91%）
4. conflictフラグを付与、追加調査を推奨
```

**評価スコアの矛盾**:
```
ソースA: 確度 score: 80
ソースB: 確度 score: 50

解決手順:
1. 各ソースの根拠を確認
2. ソースの信頼性で判断
3. 中間値は取らない（根拠のある方を採用）
```

### Step 4: 4次元評価の統一

**統合時の評価ルール**:

| 項目 | 統合ルール |
|------|-----------|
| 確度 | 一次資料ありの方を優先。なければソースの信頼性で判断 |
| 検証度 | 複数ソース（Claude+外部LLM）で同一情報→ multi_source に昇格 |
| 非対称性 | 保守的に評価（低い方を採用、ただし根拠を確認） |
| 鮮度 | 最新の情報を優先、valid_until は短い方を採用 |

---

## 統合済みデータのフォーマット

### consolidated_companies_YYYYMMDD.json

```json
{
  "metadata": {
    "consolidated_date": "YYYY-MM-DD",
    "source_files": [
      {"llm": "claude", "file": "claude_20250126.md", "companies": 50},
      {"llm": "gemini", "file": "gemini_20250126.md", "companies": 50},
      {"llm": "gpt4", "file": "gpt4_20250126.md", "companies": 50}
    ],
    "total_before_dedup": 150,
    "total_after_dedup": 85,
    "multi_source_discovered": 35
  },
  "companies": [
    {
      "ticker": "8035",
      "name": "東京エレクトロン",
      "discovered_by": ["claude", "gemini", "gpt4"],
      "discovery_method": "SC逆引き法",
      "domains": ["AI"],
      "monopoly_position": {
        "product": "コータ/デベロッパ",
        "share": 91,
        "source": "SEMI"
      },
      "certainty": {"stage": "official_announcement", "score": 85},
      "verification": {"level": "multi_source"},
      "asymmetry": {"score": 8},
      "freshness": {"valid_until": "2025-06-30"},
      "consolidation_note": "3ソースで発見。シェア情報一致。"
    }
  ]
}
```

### consolidated_intelligence_YYYYMMDD.json

```json
{
  "metadata": {
    "consolidated_date": "YYYY-MM-DD",
    "source_files": [...],
    "total_items": 120,
    "by_category": {
      "A_international": 18,
      "B_market_signals": 15,
      "C_megatrends": 22,
      "D_domain_growth": 25,
      "E_large_investments": 20,
      "F_overlooked_scan": 12,
      "G_others": 8
    }
  },
  "items": [
    {
      "id": "intel_A_001",
      "category": "A_international",
      "title": "米中半導体規制強化",
      "detail": "...",
      "reported_by": ["claude", "gemini"],
      "certainty": {"stage": "official_announcement", "score": 85},
      "verification": {"level": "multi_source"},
      "asymmetry": {"score": 8},
      "freshness": {"valid_until": "2025-06-30"},
      "sources": [...],
      "consolidation_note": "2ソースで報告。詳細はclaude版を採用。"
    }
  ]
}
```

### consolidated_monopoly_YYYYMMDD.json

```json
{
  "metadata": {
    "consolidated_date": "YYYY-MM-DD",
    "source_files": [...],
    "total_products": 60,
    "primary_source_ratio": 0.72,
    "conflicts_count": 3
  },
  "products": [
    {
      "id": "monopoly_semi_001",
      "category": "semiconductor_equipment",
      "product_name": "コータ/デベロッパ",
      "top_company": {
        "ticker": "8035",
        "name": "東京エレクトロン",
        "share": 91,
        "share_range": null
      },
      "competitors": [...],
      "entry_barrier": {
        "years": 10,
        "strength": "極めて強い"
      },
      "reported_by": ["claude", "gemini"],
      "certainty": {...},
      "verification": {"level": "multi_source"},
      "sources": [...]
    }
  ]
}
```

### consolidated_financial_YYYYMMDD.json

```json
{
  "metadata": {
    "consolidated_date": "YYYY-MM-DD",
    "source_files": [...],
    "total_companies": 50,
    "data_as_of": "2024-12",
    "average_capital_efficiency_score": 14.2
  },
  "companies": [
    {
      "ticker": "8035",
      "name": "東京エレクトロン",
      "financial_data": {
        "roe": {"value": 22.5, "trend": "安定", "score": 8},
        "debt_ratio": {"value": 18.3, "trend": "改善", "score": 6},
        "fcf": {"5year_positive": true, "trend": "成長", "score": 6}
      },
      "capital_efficiency_score": 20,
      "management_evaluation": {
        "mid_term_plan_achievement": "高",
        "shareholder_return": "積極的"
      },
      "reported_by": ["claude", "gemini"],
      "certainty": {"stage": "executed", "score": 95},
      "verification": {"level": "primary_confirmed"},
      "sources": [...]
    }
  ]
}
```

---

## 統合データの活用先

| 統合データ | 活用先Phase | 活用方法 |
|-----------|------------|----------|
| consolidated_companies | Phase 4: 候補プール作成 | 50社候補プールの選定に使用 |
| consolidated_intelligence | Phase 4: 市場危険度分析 | 広域情報として使用 |
| consolidated_monopoly | Phase 4: 独占マップ更新 | 独占マップの更新データとして使用 |
| consolidated_financial | Phase 4: Top30スコアリング | 資本効率評価に使用 |

---

## コマンド

| コマンド | 動作 |
|----------|------|
| `情報を統合` | data/intelligence/raw/配下の全ファイル（Claude+外部LLM）を統合 |
| `統合状態を確認` | raw/配下の出力状況と統合状況を表示 |

---

## 統合時の警告・エラー

| 状況 | 対応 |
|------|------|
| メタデータなし | 警告を出力、ファイル名から推定 |
| 4次元評価なし | 該当情報をスキップ、または低スコア（30）を付与 |
| フォーマットエラー | エラー箇所を特定、可能な範囲で処理 |
| 重大な矛盾 | 両方の情報を保持、conflictフラグ付与 |
| ソースなし | 検証度を single_unverified に設定 |

---

## 品質レポート

統合完了時に以下を出力：

```markdown
## 情報統合レポート

### 処理サマリー
- 処理ファイル数: X件
- 処理ソース: [claude, gemini, gpt4, perplexity]
- 処理日時: YYYY-MM-DD HH:MM

### 企業発掘
- 統合前: XXX社（重複含む）
- 統合後: XX社
- 複数ソースで発見: XX社（検証度昇格）
- 矛盾解決: X件

### 広域情報
- 統合前: XXX件
- 統合後: XX件
- 検証度昇格: X件

### 独占マップ情報
- 製品数: XX件
- 一次資料比率: XX%
- 矛盾あり: X件

### 財務情報
- 企業数: XX社
- 資本効率スコア平均: XX点/20点

### 警告
- [警告リスト]

### 次のアクション
1. [矛盾解決が必要な項目]
2. [追加調査が必要な項目]
```
