# 外部LLM出力の統合ガイド（Claude用）

## このファイルの目的

このファイルは、外部LLMから収集した情報をClaudeが統合・処理する際の手順を定義します。

---

## 統合の全体フロー

```
外部LLM出力（4タイプ）
    ↓
data/intelligence/raw/ に保存
    ↓
Claude: 品質チェック
    ↓
Claude: 重複排除・矛盾解決
    ↓
Claude: 4次元評価の統一
    ↓
統合済みデータの保存
    ↓
既存フローへの統合
```

---

## ファイル配置

### 入力（外部LLM出力）

```
data/intelligence/raw/
├── company_discovery/
│   ├── gemini_20250126.md
│   ├── gpt4_20250126.md
│   └── perplexity_20250126.md
├── broad_intelligence/
│   ├── gemini_20250126.md
│   └── gpt4_20250126.md
├── monopoly_info/
│   ├── gemini_20250126.md
│   └── gpt4_20250126.md
└── financial_management/
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

## 統合処理の詳細

### Step 1: 品質チェック

各ファイルを読み込み、以下を確認：

| チェック項目 | 対応 |
|-------------|------|
| メタデータがあるか | なければ警告、手動補完 |
| 4次元評価があるか | なければ該当情報を除外または低スコア付与 |
| ソースが明記されているか | なければ検証度を single_unverified に |
| フォーマットが正しいか | パースエラーは手動修正を要求 |

### Step 2: 重複排除

**企業発掘の場合**:
```
1. 証券コードで重複を検出
2. 同一企業が複数LLMから発掘された場合:
   - 4次元評価の高い方を採用
   - 両方の情報をマージ
   - 「複数LLMで発見」フラグを付与
```

**情報の場合**:
```
1. タイトル・内容の類似度で重複を検出
2. 同一情報が複数LLMから報告された場合:
   - 検証度を multi_source に昇格
   - より詳細な方を採用
   - ソースをマージ
```

### Step 3: 矛盾解決

**シェア情報の矛盾**:
```
LLM-A: 「A社のシェアは91%」
LLM-B: 「A社のシェアは85%」

解決手順:
1. 各LLMのソースを確認
2. 一次資料を優先
3. 一次資料がない場合、範囲として記録（85-91%）
4. conflictフラグを付与、追加調査を推奨
```

**評価スコアの矛盾**:
```
LLM-A: 確度 score: 80
LLM-B: 確度 score: 50

解決手順:
1. 各LLMの根拠を確認
2. ソースの信頼性で判断
3. 中間値は取らない（根拠のある方を採用）
```

### Step 4: 4次元評価の統一

**統合時の評価ルール**:

| 項目 | 統合ルール |
|------|-----------|
| 確度 | 一次資料ありの方を優先。なければソースの信頼性で判断 |
| 検証度 | 複数LLMで同一情報→ multi_source に昇格 |
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
      {"llm": "gemini", "file": "gemini_20250126.md", "companies": 50},
      {"llm": "gpt4", "file": "gpt4_20250126.md", "companies": 50}
    ],
    "total_before_dedup": 100,
    "total_after_dedup": 75,
    "multi_llm_discovered": 25
  },
  "companies": [
    {
      "ticker": "8035",
      "name": "東京エレクトロン",
      "discovered_by": ["gemini", "gpt4"],
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
      "consolidation_note": "2LLMで発見。シェア情報一致。"
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
    "total_items": 80,
    "by_category": {
      "A_international": 12,
      "B_market_signals": 10,
      "C_megatrends": 15,
      "D_domain_growth": 18,
      "E_large_investments": 12,
      "F_overlooked_scan": 8,
      "G_others": 5
    }
  },
  "items": [
    {
      "id": "intel_A_001",
      "category": "A_international",
      "title": "米中半導体規制強化",
      "detail": "...",
      "reported_by": ["gemini", "gpt4"],
      "certainty": {"stage": "official_announcement", "score": 85},
      "verification": {"level": "multi_source"},
      "asymmetry": {"score": 8},
      "freshness": {"valid_until": "2025-06-30"},
      "sources": [...],
      "consolidation_note": "2LLMで報告。詳細はgemini版を採用。"
    }
  ]
}
```

---

## 既存フローへの統合

### 統合データの活用先

| 統合データ | 活用先Step | 活用方法 |
|-----------|-----------|----------|
| consolidated_companies | Step 0.5 | 候補プール50社の選定に使用 |
| consolidated_intelligence | Step 0, Step 1 | 広域情報として使用、イベント収集の補完 |
| consolidated_monopoly | Step 2 | 独占マップの更新データとして使用 |
| consolidated_financial | Step 5 | 資本効率評価に使用 |

### Step 0での活用

```
通常のStep 0（広域情報収集）実行時:
1. data/intelligence/raw/ に外部LLM出力があるか確認
2. あれば統合処理を実行
3. consolidated_*.json を生成
4. Step 0の出力（broad_intelligence_*.json）と統合
```

### Step 0.5での活用

```
通常のStep 0.5（企業発掘）実行時:
1. consolidated_companies_*.json があるか確認
2. あれば外部LLM発見企業を候補に含める
3. Claude独自発掘と統合
4. 重複排除→70-100社→スクリーニング→50社
```

---

## コマンド

| コマンド | 動作 |
|----------|------|
| `外部情報を統合` | data/intelligence/raw/配下を処理し、統合済みデータを生成 |
| `統合状態を確認` | 外部LLM出力の有無と統合状況を表示 |

---

## 統合時の警告・エラー

| 状況 | 対応 |
|------|------|
| メタデータなし | 警告を出力、手動でLLM名・日付を確認 |
| 4次元評価なし | 該当情報をスキップ、または低スコア（30）を付与 |
| フォーマットエラー | エラー箇所を特定、手動修正を要求 |
| 重大な矛盾 | 両方の情報を保持、conflictフラグ付与 |
| ソースなし | 検証度を single_unverified に設定 |

---

## 品質レポート

統合完了時に以下を出力：

```markdown
## 外部情報統合レポート

### 処理サマリー
- 処理ファイル数: X件
- 処理LLM: [gemini, gpt4, perplexity]
- 処理日時: YYYY-MM-DD HH:MM

### 企業発掘
- 統合前: XXX社（重複含む）
- 統合後: XX社
- 複数LLMで発見: XX社
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
- 資本効率スコア平均: XX点

### 警告
- [警告リスト]

### 次のアクション
1. [矛盾解決が必要な項目]
2. [追加調査が必要な項目]
```
