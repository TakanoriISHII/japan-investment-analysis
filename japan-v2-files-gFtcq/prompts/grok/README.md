# Grok用プロンプト

## Grokの特性

| 項目 | 評価 |
|------|------|
| 速度 | ★★★★★ 最速 |
| リアルタイム情報 | ★★★★★ X/Twitter統合 |
| 広域スキャン | ★★★★☆ 良好 |
| 深い分析 | ★★☆☆☆ やや弱い |

## 最適なタスク

1. **広域情報収集** - 7カテゴリの速報・トレンド
2. **市場センチメント** - X/Twitterからのリアルタイム情報
3. **大量企業スキャン** - 50社以上の初期スクリーニング

## プロンプト一覧

| ファイル | 用途 | 実行頻度 |
|---------|------|---------|
| `broad_info.md` | 広域情報収集 | 週次/イベント時 |
| `company_scan.md` | 企業スキャン | 週次 |

> **補強調査**: `reinforcement/prompts/grok/` を参照

## 使用方法

1. プロンプトをコピー
2. Grok (DeepSearch) に貼り付け
3. 出力を `data/intelligence/raw/grok/` に保存

## 出力ディレクトリ

```
data/intelligence/raw/grok/
├── broad_info_YYYYMMDD.md
└── company_scan_YYYYMMDD.md
```
