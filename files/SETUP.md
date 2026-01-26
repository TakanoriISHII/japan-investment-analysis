# セットアップ手順

## 前提条件

- GitHubアカウント
- Claude Code（`claude` コマンド）がインストール済み
- Git設定済み（`git config --global user.name` / `user.email`）

---

## Step 1: GitHubでリポジトリを作成

### 1.1 GitHubにログイン
https://github.com にアクセス

### 1.2 新規リポジトリ作成
1. 右上の「+」→「New repository」
2. 設定：
   - Repository name: `japan-investment-analysis`
   - Description: `マクロパルス × マルチドメイン・コンバージェンス分析`
   - Visibility: **Private**（推奨）
   - Initialize: チェックなし（空のリポジトリ）
3. 「Create repository」をクリック

### 1.3 リポジトリURLをコピー
```
https://github.com/[your-username]/japan-investment-analysis.git
```

---

## Step 2: ローカルにクローン

### 2.1 作業ディレクトリに移動
```bash
cd ~/projects  # または任意のディレクトリ
```

### 2.2 クローン
```bash
git clone https://github.com/[your-username]/japan-investment-analysis.git
cd japan-investment-analysis
```

---

## Step 3: 初期ファイルをセットアップ

### 3.1 このリポジトリのファイルをコピー

Claude.aiからダウンロードしたファイルを配置：

```
japan-investment-analysis/
├── CLAUDE.md
├── README.md
├── SETUP.md
└── prompts/
    ├── phase1_market_risk.md
    ├── phase2_monopoly_map.md
    ├── phase3_macro_pulse.md
    ├── phase4_top30_scoring.md
    └── phase5_final_report.md
```

### 3.2 ディレクトリ作成
```bash
mkdir -p reports latest
```

### 3.3 .gitignoreを作成
```bash
cat > .gitignore << 'EOF'
# OS generated files
.DS_Store
Thumbs.db

# Editor files
*.swp
*.swo
*~

# Temporary files
*.tmp
*.temp
EOF
```

### 3.4 初回コミット＆プッシュ
```bash
git add .
git commit -m "Initial setup: Claude分析フレームワーク"
git push -u origin main
```

---

## Step 4: Claude Codeで開く

### 4.1 Claude Codeを起動
```bash
cd ~/projects/japan-investment-analysis
claude
```

### 4.2 CLAUDE.mdを確認
Claude Codeは自動的に`CLAUDE.md`を読み込みます。
読み込まれていない場合：
```
CLAUDE.mdを読み込んで
```

---

## Step 5: 初回分析を実行

### 5.1 フル分析を開始
Claude Codeのプロンプトで：
```
フル分析を実行
```

### 5.2 実行中の確認
- 各Phase完了時にコミットが作成される
- 全Phase完了後にプッシュされる
- 進捗はターミナルに表示

### 5.3 完了確認
```bash
git log --oneline -10
```

期待される出力：
```
abc1234 レポート完了: 2025-01-26
def5678 Phase 5: 最終レポート完了
ghi9012 Phase 4: Top30スコアリング完了
jkl3456 Phase 3: マクロパルス情報収集完了
mno7890 Phase 2: グローバル独占マップ完了
pqr1234 Phase 1: 市場危険度スコア完了
stu5678 Initial setup: Claude分析フレームワーク
```

---

## トラブルシューティング

### Q: Claude Codeが見つからない
```bash
# インストール確認
which claude

# インストールされていない場合
# https://docs.anthropic.com/claude-code を参照
```

### Q: GitHubにプッシュできない
```bash
# 認証確認
git remote -v

# HTTPS認証の場合、Personal Access Tokenが必要
# Settings → Developer settings → Personal access tokens → Generate new token
```

### Q: CLAUDE.mdが読み込まれない
```bash
# ファイル存在確認
ls -la CLAUDE.md

# Claude Codeで明示的に読み込み
# プロンプト: "CLAUDE.mdを読み込んで"
```

### Q: 検索が失敗する
- インターネット接続を確認
- Claude Codeのセッションを再起動
- 検索クエリを簡略化して再試行

---

## 定期実行の設定（オプション）

### macOS/Linux: cronで週次実行
```bash
crontab -e
```

以下を追加（毎週月曜9:00に実行）：
```
0 9 * * 1 cd ~/projects/japan-investment-analysis && claude --prompt "週次更新を実行" --auto
```

※ `--auto` フラグはClaude Codeのバージョンによって異なる場合があります

---

## 次のステップ

1. **初回フル分析を実行** — `フル分析を実行`
2. **レポートを確認** — `reports/YYYY-MM-DD/05_final_report.md`
3. **定期更新を設定** — 週次/月次のルーティン化
