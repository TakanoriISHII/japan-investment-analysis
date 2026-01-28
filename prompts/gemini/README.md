# Gemini用プロンプト

## Geminiの特性

| 項目 | 評価 |
|------|------|
| 速度 | ★★★☆☆ やや遅い |
| 長文処理 | ★★★★★ 優秀 |
| 包括的分析 | ★★★★★ 優秀 |
| 深い調査 | ★★★★☆ 良好 |

## 最適なタスク

1. **企業深掘り分析** - 財務、独占ポジション、シナジーの詳細分析
2. **詳細な情報収集** - 長文レポート、複雑な情報の整理
3. **クロスチェック用** - Grok結果の検証・補完

## プロンプト一覧

| ファイル | 用途 | 実行頻度 |
|---------|------|---------|
| `company_deep.md` | 企業深掘り分析 | 週次 |
| `broad_info.md` | 広域情報（詳細版） | 週次 |

> **補強調査**: `reinforcement/prompts/gemini/` を参照

## 使用方法

1. プロンプトをコピー
2. Gemini (DeepResearch) に貼り付け
3. 出力を `data/intelligence/raw/gemini/` に保存

## 出力ディレクトリ

```
data/intelligence/raw/gemini/
├── company_deep_YYYYMMDD.md
└── broad_info_YYYYMMDD.md
```
