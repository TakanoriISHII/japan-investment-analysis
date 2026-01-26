# マクロパルス × マルチドメイン・コンバージェンス分析

日本企業のグローバル競争優位を分析し、投資判断に資するレポートを自動生成するステートフル分析システム。

## 設計思想

**「情報は蓄積し、変化を追跡し、差分で判断する」**

- 過去のイベントは永続的に保存（削除禁止）
- 静的情報と動的情報を明確に分離
- 毎回の分析で「何が変わったか」を明示

## 情報の分類

| 分類 | 例 | 更新頻度 |
|------|-----|----------|
| **完全静的** | 過去のイベント、発言、確定数字 | 追記のみ、削除禁止 |
| **準静的** | 世界シェア、認証、バックログ | トリガーイベント時のみ |
| **動的** | 株価、為替、需給 | 毎回取得 |

## クイックスタート

### 1. リポジトリをクローン
```bash
git clone https://github.com/[your-username]/japan-investment-analysis.git
cd japan-investment-analysis
```

### 2. Claude Codeで開く
```bash
claude
```

### 3. 分析を実行
```
フル分析を実行
```

## 分析フロー

```
Step 1: イベント収集（append-only）
    ↓
Step 2: 独占マップ更新（トリガーがあれば）
    ↓
Step 3: 市場状態取得（毎回）
    ↓
Step 4: 市場危険度分析
    ↓
Step 5: Top30スコアリング + HTML生成
    ↓
Step 6: 最終レポート生成
```

## コマンド一覧

| コマンド | 動作 |
|----------|------|
| `フル分析を実行` | 状態を確認し、必要な部分のみ更新 |
| `強制フル更新` | 全てをゼロから再実行 |
| `差分レポート` | 前回からの変化点のみ表示 |
| `独占マップを更新` | 独占マップを強制更新 |
| `状態を確認` | 各コンポーネントの状態を表示 |

## ディレクトリ構造

```
japan-investment-analysis/
├── CLAUDE.md              # マスタープロンプト
├── data/                  # ★永続データ層
│   ├── state.json         # 実行状態
│   ├── events.json        # イベントログ（append-only）
│   ├── snapshots/
│   │   ├── monopoly_map.json  # 独占マップ
│   │   └── market_state.json  # 市場状態
│   └── analysis/
│       ├── market_risk.json   # 市場危険度
│       └── top30.json         # Top30分析
├── reports/               # 日付別レポート
│   └── YYYY-MM-DD/
│       ├── final_report.md
│       ├── changelog.md
│       └── quadrant_chart.html
└── latest/                # 最新レポート
```

## 可視化の確認

```bash
open latest/quadrant_chart.html
```

## ライセンス

Private - 個人利用のみ
