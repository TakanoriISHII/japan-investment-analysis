# セットアップ手順

## 前提条件

- GitHubアカウント
- Claude Code（`claude` コマンド）がインストール済み
- Git設定済み

---

## Step 1: GitHubでリポジトリを作成

1. https://github.com にアクセス
2. 「New repository」をクリック
3. 設定：
   - Repository name: `japan-investment-analysis`
   - Visibility: **Private**（推奨）
   - Initialize: チェックなし
4. 「Create repository」をクリック

---

## Step 2: ローカルにクローン

```bash
cd ~/projects  # または任意のディレクトリ
git clone https://github.com/[your-username]/japan-investment-analysis.git
cd japan-investment-analysis
```

---

## Step 3: ファイルを配置

ダウンロードしたファイルを以下のように配置：

```
japan-investment-analysis/
├── CLAUDE.md                    ← ルート
├── README.md                    ← ルート
├── SETUP.md                     ← ルート
├── prompts/                     ← フォルダ作成
│   ├── step0_collect_information.md     ← 広域情報収集（7カテゴリ）★情報が先
│   ├── step0_5_discover_opportunities.md ← 企業発掘（情報から発見）
│   ├── step1_collect_events.md
│   ├── step1_5_quality_check.md
│   ├── step2_update_monopoly_map.md
│   ├── step3_update_market_state.md
│   ├── step4_analyze_market_risk.md
│   ├── step5_analyze_top30.md
│   └── step6_generate_report.md
├── templates/                   ← フォルダ作成
│   └── quadrant_chart_template.html
├── data/                        ← フォルダ作成
│   ├── state.json
│   ├── events.json
│   ├── information_quality.json
│   ├── asymmetry_tracker.json
│   ├── sources/                 ← サブフォルダ作成（情報源マスター）
│   │   ├── primary_sources.json
│   │   ├── discovery_queries.json
│   │   └── verification_protocols.json
│   ├── intelligence/            ← サブフォルダ作成（広域情報）
│   │   └── broad_intelligence_YYYYMMDD.json
│   ├── discovery/               ← サブフォルダ作成（発掘結果）
│   │   └── discovery_result_YYYYMMDD.json
│   ├── snapshots/               ← サブフォルダ作成
│   │   ├── monopoly_map.json
│   │   └── market_state.json
│   └── analysis/                ← サブフォルダ作成
│       ├── market_risk.json
│       └── top30.json
├── reports/                     ← 空フォルダ作成
└── latest/                      ← 空フォルダ作成
```

---

## Step 4: 初回コミット

```bash
git add .
git commit -m "Initial setup: 情報戦略分析システム"
git push -u origin main
```

---

## Step 5: Claude Codeで開く

```bash
claude
```

CLAUDE.mdが自動的に読み込まれます。

---

## Step 6: 初回分析を実行

```
フル分析を実行
```

初回は全てのデータを収集するため、15-30分程度かかります。

---

## ファイル配置チェックリスト

| ファイル | 配置先 |
|----------|--------|
| CLAUDE.md | `/` (ルート) |
| README.md | `/` (ルート) |
| SETUP.md | `/` (ルート) |
| step0_collect_information.md | `/prompts/` |
| step0_5_discover_opportunities.md | `/prompts/` |
| step1_collect_events.md | `/prompts/` |
| step1_5_quality_check.md | `/prompts/` |
| step2_update_monopoly_map.md | `/prompts/` |
| step3_update_market_state.md | `/prompts/` |
| step4_analyze_market_risk.md | `/prompts/` |
| step5_analyze_top30.md | `/prompts/` |
| step6_generate_report.md | `/prompts/` |
| quadrant_chart_template.html | `/templates/` |
| state.json | `/data/` |
| events.json | `/data/` |
| information_quality.json | `/data/` |
| asymmetry_tracker.json | `/data/` |
| primary_sources.json | `/data/sources/` |
| discovery_queries.json | `/data/sources/` |
| verification_protocols.json | `/data/sources/` |
| broad_intelligence_*.json | `/data/intelligence/` |
| discovery_result_*.json | `/data/discovery/` |
| monopoly_map.json | `/data/snapshots/` |
| market_state.json | `/data/snapshots/` |
| market_risk.json | `/data/analysis/` |
| top30.json | `/data/analysis/` |

---

## トラブルシューティング

### Q: データが壊れた
```bash
git checkout HEAD -- data/
```

### Q: 強制的にゼロから実行したい
```
強制フル更新
```

### Q: 情報品質に問題がある
```
情報品質を確認
```
未検証・矛盾・陳腐化のアラートが表示されます。
