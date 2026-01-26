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

ダウンロードしたファイルをリポジトリに配置：

```
japan-investment-analysis/
├── CLAUDE.md
├── README.md
├── SETUP.md
├── .gitignore
├── prompts/
│   ├── step1_collect_events.md
│   ├── step2_update_monopoly_map.md
│   ├── step3_update_market_state.md
│   ├── step4_analyze_market_risk.md
│   ├── step5_analyze_top30.md
│   └── step6_generate_report.md
├── templates/
│   └── quadrant_chart_template.html
├── data/
│   ├── state.json
│   ├── events.json
│   ├── snapshots/
│   │   ├── monopoly_map.json
│   │   └── market_state.json
│   └── analysis/
│       ├── market_risk.json
│       └── top30.json
├── reports/
└── latest/
```

---

## Step 4: 初回コミット

```bash
git add .
git commit -m "Initial setup: ステートフル分析システム"
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

## Step 7: 完了確認

### Git履歴の確認
```bash
git log --oneline -15
```

期待される出力：
```
abc1234 分析完了: 2025-01-26
def5678 実行状態更新
ghi9012 最終レポート生成: 2025-01-26
jkl3456 4象限チャートHTML生成
mno7890 Top30スコアリング完了
pqr1234 市場危険度分析完了: 48/100
stu5678 市場状態更新
vwx9012 独占マップ更新: 初回構築
yz01234 イベント収集完了: 25件追加
abc5678 Initial setup: ステートフル分析システム
```

### 可視化の確認
```bash
open latest/quadrant_chart.html  # macOS
xdg-open latest/quadrant_chart.html  # Linux
```

### データの確認
```bash
cat data/state.json
```

---

## 2回目以降の実行

2回目以降は、システムが自動的に判断します：

```
フル分析を実行
```

- イベント収集: 前回以降の新規イベントのみ
- 独占マップ: トリガーイベントがなければスキップ
- 市場状態: 毎回取得
- 分析: 最新データで再計算

---

## トラブルシューティング

### Q: データが壊れた
```bash
# 特定ファイルを初期状態に戻す
git checkout HEAD -- data/events.json

# 全データを初期状態に戻す
git checkout HEAD -- data/
```

### Q: 強制的にゼロから実行したい
```
強制フル更新
```

### Q: 特定のステップだけ再実行したい
```
独占マップを更新
```
または
```
市場危険度を再計算
```

---

## 定期実行の設定（オプション）

### macOS/Linux: cronで週次実行

```bash
crontab -e
```

以下を追加（毎週月曜9:00に実行）：
```
0 9 * * 1 cd ~/projects/japan-investment-analysis && claude --prompt "フル分析を実行" --auto
```

---

## 次のステップ

1. **初回フル分析を実行**
2. **レポートを確認** — `reports/YYYY-MM-DD/final_report.md`
3. **可視化を確認** — `latest/quadrant_chart.html`
4. **定期更新を設定** — 週次でフル分析を実行
