# CLAUDE.md - 日本マルチドメイン・コンバージェンス分析

> **このファイルはエントリーポイントです。詳細は `docs/` 配下の各ドキュメントを参照してください。**

---

## クイックリファレンス

| やりたいこと | コマンド | 詳細ドキュメント |
|-------------|---------|-----------------|
| フル分析を実行 | `run analysis` | [OPERATIONS.md](./docs/OPERATIONS.md#フル分析プロトコル) |
| 特定フェーズから再開 | `run analysis --from [N]` | [OPERATIONS.md](./docs/OPERATIONS.md#フェーズ独立性と部分再実行) |
| 状態を確認 | `check status` | - |
| 前回との差分を確認 | `diff report` | [OPERATIONS.md](./docs/OPERATIONS.md#差分追跡) |
| 企業をスコアリング | `score companies` | [METHODOLOGY.md](./docs/METHODOLOGY.md#企業評価-5軸フレームワーク) |
| 市場環境を判断 | `analyze market risk` | [METHODOLOGY.md](./docs/METHODOLOGY.md#市場リスク分析) |

---

## ドキュメント構成

| ファイル | 内容 | 読むタイミング |
|---------|------|---------------|
| [STRATEGY.md](./docs/STRATEGY.md) | **Why**: 理念、ミッション、6ドメイン定義 | 全体方針を理解したい時 |
| [METHODOLOGY.md](./docs/METHODOLOGY.md) | **What**: 市場リスク分析、5軸評価、情報品質 | 評価方法を確認したい時 |
| [OPERATIONS.md](./docs/OPERATIONS.md) | **How**: 9フェーズ実行、継続的改善 | 分析を実行する時 |
| [TECHNICAL_SPEC.md](./docs/TECHNICAL_SPEC.md) | **仕様**: ディレクトリ構造、JSON仕様 | データ構造を確認したい時 |

---

## 基本理念

**情報は不確実性を減少させる。**

1. **情報精度の最大化** — 噂と事実を区別し、一次情報源で検証する
2. **情報の非対称性を活用** — 他者が持たない知識で優位性を得る
3. **情報の鮮度を管理** — 古いデータに基づく意思決定を排除する

→ 詳細: [STRATEGY.md](./docs/STRATEGY.md)

---

## ミッション

**マルチドメイン・コンバージェンスにおける情報の非対称性を活用する** — 市場が単一ドメインに焦点を当てることで過小評価している、6ドメインの収束点で構造的優位性を持つ日本企業を特定する。

### 6つのドメイン

| # | ドメイン | 主要領域 |
|---|---------|---------|
| 1 | **エネルギー** | 原子力（SMR、HALEU）、グリッド、変圧器、蓄電 |
| 2 | **防衛** | ミサイル、航空機、艦船、弾薬、防衛エレクトロニクス |
| 3 | **AI** | コンピュートインフラ、半導体、データセンター |
| 4 | **ロボティクス** | 産業用、ドローン、UUV、ヒューマノイド |
| 5 | **宇宙** | 打上げ、衛星、月面、ISR |
| 6 | **サイバー** | 暗号化、電子戦、ISR融合 |

→ 詳細: [STRATEGY.md - 6つのドメイン](./docs/STRATEGY.md#6つのドメイン)

---

## 評価フレームワーク概要

```
1. 市場リスク分析（100点） → 今は投資すべきタイミングか？
2. 企業評価（5軸/100点）   → どの企業が最も優位か？【相対評価】
3. 4象限配置              → 確実性 × アップサイドでポジション決定
```

### 5軸評価の原則（Graham分類体系統合版）

5軸は**投資的要因**と**投機的要因**に分類し、**相対的**に評価する:

| 分類 | 軸 | 配点 |
|------|-----|------|
| B. 投資的要因(40) | 構造的優位性 / 本質的価値 | 20 + 20 |
| A. 投機的要因(60) | 将来の価値 / 情報非対称性 / 政策・触媒 | 25 + 20 + 15 |

**評価手順**: ベーススコア → 相対調整 → 情報確度(A-E)適用 → 最終スコア

| 評価 | 詳細 |
|------|------|
| 市場リスク分析 | [METHODOLOGY.md - 市場リスク分析](./docs/METHODOLOGY.md#市場リスク分析) |
| 5軸評価 | [METHODOLOGY.md - 企業評価](./docs/METHODOLOGY.md#企業評価-5軸フレームワークgraham分類体系統合版) |
| 4象限マトリックス | [METHODOLOGY.md - 4象限マトリックス](./docs/METHODOLOGY.md#4象限マトリックス) |

---

## 実行プロトコル概要

### フル分析の9フェーズ

| Phase | 内容 | 出力 |
|-------|------|------|
| 1 | 状態確認 | - |
| 2 | インテリジェンス収集（3LLM） | `data/intelligence/raw/` |
| 3 | 比較分析 | `contradictions.json`, `gaps.json` |
| 4 | 補足調査 | `claude_supplemental.md` |
| 5 | 統合・確度整理・stable更新 | `consolidated_*.json`, `stable/*` |
| 6 | 分析・評価 | `market_risk.json`, `top30.json` |
| 7 | レポート生成 | `reports/[DATE]/` |
| 8 | 継続的改善 | `reinforcement/` |
| 9 | 完了 | `state.json` 更新 |

→ 詳細: [OPERATIONS.md - フル分析プロトコル](./docs/OPERATIONS.md#フル分析プロトコル)

### フェーズ実行ルール【必須】

**各フェーズ開始時、以下の手順を必ず実行すること:**

1. **チェックリスト読み込み**: OPERATIONS.mdの該当フェーズのチェックリストを読む
2. **Todo展開**: TodoWriteで全チェック項目をTodoとして展開する
3. **逐次完了**: 各項目完了時にTodoを「completed」に更新する
4. **完了確認**: 全項目が完了するまで次フェーズに進まない

```
例: Phase 8開始時
1. Read: docs/OPERATIONS.md（Phase 8チェックリスト部分）
2. TodoWrite: [
     {"content": "8-1: Claude自動補強実行", "status": "pending"},
     {"content": "8-2: learnings/[DATE].json作成", "status": "pending"},
     {"content": "8-3: 収集プロンプト改善検討", "status": "pending"},
     ...
   ]
3. 各項目を順次実行し、完了時にTodoを更新
```

> **警告**: チェックリストをスキップすると、補強プロンプト未生成などの重要な漏れが発生する。

### stable/による情報蓄積

情報を鮮度別に分類し、次回以降の分析で再利用:

| ディレクトリ | 変化頻度 | 内容 |
|------------|---------|------|
| `stable/permanent/` | 年次以下 | 認証、モート、競争構造 |
| `stable/quarterly/` | 四半期 | 財務、市場シェア |
| `stable/monthly/` | 月次 | 契約、投資 |

→ 詳細: [stable/README.md](./data/intelligence/stable/README.md)

---

## フェーズ完了検証

→ 詳細: [OPERATIONS.md](./docs/OPERATIONS.md#フル分析プロトコル)

### Phase 1 フレームワーク整合性検証ゲート【v2.0.0〜】
- `state.json` の `framework.version` が "2.0.0" であること
- METHODOLOGY.md / OPERATIONS.md / TECHNICAL_SPEC.md に新5軸名が存在すること
- 収集プロンプト（Grok/Gemini）に Graham-Buffett指標セクションが存在すること
- 旧軸名（"物理的独占力", "資本効率"等）がスコア定義として残留していないこと
- → HALT / WARN / PASS を判定

### Phase 5 必須検証ゲート
- `stable/permanent/domains.json` の6ドメイン × 3項目にnullが残っていないこと
- `stable/quarterly/financials.json` にTop 30全社が登録されていること
- Top 30全社にバリュエーション項目（PER, EPS, 52週レンジ等）があること

### Phase 6 スキーマ検証ゲート【v2.0.0〜】
- `top30.json` のメタデータに Graham分類体系統合版の5軸定義が存在すること
- 旧フィールド（monopoly, resilience, synergy, asymmetry, capital）が不在であること
- 全Top 30社に: 5軸スコア、investment_factors、speculative_factors、confidence（5軸+サマリー）、graham_buffett_note が存在すること
- 配点整合性: 各軸≤上限、投資的=軸1+軸2、投機的=軸3+軸4+軸5、合計=投資的+投機的
- → FAIL の場合 Phase 7 に進まない

### Phase 7 必須出力
- `reports/[DATE]/executive_summary.md`
- `reports/[DATE]/final_report.md`
- `reports/[DATE]/information_quality_report.md`
- `reports/[DATE]/quadrant_chart.html`

### Phase 8 必須出力
- `reinforcement/pending_tasks.json`
- `reinforcement/results/claude_auto/[DATE].md`
- `reinforcement/prompts/grok/[DATE]_tasks.md`（未完了Grokタスクがあれば）
- `reinforcement/prompts/gemini/[DATE]_tasks.md`（未完了Geminiタスクがあれば）
- **情報範囲拡大タスク**（domains.json null検査、financials.json全社登録検査）

### Phase 9 フレームワーク移行完了【v2.0.0〜】
- `framework.migration_status` を `"completed"` に更新
- `monopoly_map` → `structural_advantage_map` のリネーム（初回のみ）
- `framework.last_validated` を更新

---

## コマンド一覧

→ 詳細: [OPERATIONS.md - コマンド一覧](./docs/OPERATIONS.md#コマンド一覧)

| カテゴリ | 主要コマンド |
|---------|-------------|
| 基本 | `run analysis`, `check status`, `diff report` |
| 分析 | `score companies`, `analyze market risk`, `generate report` |
| 改善 | `show quality issues`, `run reinforcement`, `show pending tasks` |
| 検証 | `record predictions`, `verify performance` |

---

## ディレクトリ構造

→ 詳細: [TECHNICAL_SPEC.md - ディレクトリ構造](./docs/TECHNICAL_SPEC.md#ディレクトリ構造)

```
japan-investment-analysis/
├── CLAUDE.md                    # このファイル（エントリーポイント）
├── docs/                        # ドキュメント（STRATEGY/METHODOLOGY/OPERATIONS/TECHNICAL_SPEC）
├── prompts/                     # LLM別最適化プロンプト（grok/gemini/claude）
├── data/
│   ├── intelligence/
│   │   ├── raw/                 # LLM収集結果
│   │   ├── stable/              # 蓄積情報（permanent/quarterly/monthly）
│   │   └── consolidated_*.json  # 統合結果
│   └── analysis/                # 分析結果
├── reinforcement/               # 継続的改善
├── reports/                     # レポート
└── latest/                      # 最新レポート（シンボリックリンク）
```

---

## 意思決定マトリックス

→ 詳細: [STRATEGY.md - 意思決定マトリックス](./docs/STRATEGY.md#意思決定マトリックス)

| 決定事項 | AI | 人間 |
|---------|:--:|:----:|
| 候補企業の発掘 | 自動 | - |
| 5軸スコアリング | 自動 | レビュー |
| Top 30選定 | - | **承認** |
| ポジションサイズ・売買タイミング | - | **最終判断** |
