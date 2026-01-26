# CLAUDE.md - マクロパルス × マルチドメイン・コンバージェンス分析

## プロジェクト概要

日本企業のグローバル競争優位を分析し、投資判断に資するレポートを生成するステートフル分析システム。
**情報を蓄積し、変化を追跡し、差分で判断する**設計思想に基づく。

---

## コマンド一覧

| コマンド | 動作 |
|----------|------|
| `フル分析を実行` | state.jsonを確認し、必要な部分のみ更新して分析 |
| `強制フル更新` | 全てをゼロから再実行（キャッシュ無視） |
| `差分レポート` | 前回からの変化点のみを表示 |
| `独占マップを更新` | 独占マップを強制更新 |
| `状態を確認` | 各コンポーネントの最終更新日時を表示 |
| `イベントを追加` | 手動でイベントを追加 |

---

## 情報の分類と更新ルール

### 1. 完全静的（Immutable）— 削除・上書き禁止

| カテゴリ | 例 |
|----------|-----|
| 過去のイベント | 政策発表、決算発表、契約締結 |
| 過去の発言 | CEO発言、アナリスト見解 |
| 確定した数字 | 決算実績、契約金額 |

**→ events.jsonにappend-onlyで蓄積**

### 2. 準静的（Semi-static）— トリガーイベント時のみ更新

| カテゴリ | 変化トリガー |
|----------|--------------|
| 世界シェア | 調査機関レポート発表、M&A完了、大型失注/獲得 |
| 事業構成 | 事業売却/買収発表 |
| 認証・資格 | 防衛/宇宙/原子力の認定取得/失効 |
| バックログ | 四半期決算発表 |
| 政策・法律 | 法案成立、予算確定 |

**→ monopoly_map.jsonをトリガー検出時のみ更新**

### 3. 動的（Dynamic）— 毎回取得

| カテゴリ | 例 |
|----------|-----|
| バリュエーション | PER、PBR |
| 為替 | ドル円 |
| 需給 | 外国人売買動向、信用残高 |

**→ market_state.jsonを毎回上書き**

---

## 実行プロトコル

### 「フル分析を実行」と言われた場合

```
1. 状態確認
   - data/state.jsonを読み込み
   - 前回実行日時、各コンポーネントの状態を確認

2. イベント収集（Step 1）
   - prompts/step1_collect_events.mdを読み込み
   - 前回収集日以降の新規イベントを検索
   - data/events.jsonに追記（既存イベントは変更禁止）
   - トリガーイベント（シェア変動、M&A等）を検出
   - git commit "イベント収集完了: N件追加"

3. 独占マップ判定（Step 2）
   - prompts/step2_update_monopoly_map.mdを読み込み
   - if トリガーイベントあり OR 前回更新から30日超過:
       → 該当部分を更新
       → git commit "独占マップ更新: [理由]"
   - else:
       → スキップ
       → 「独占マップは[日付]更新済み、トリガーイベントなし」と通知

4. 市場状態取得（Step 3）
   - prompts/step3_update_market_state.mdを読み込み
   - 動的データ（為替、PER、外国人動向等）を取得
   - data/snapshots/market_state.jsonを上書き
   - git commit "市場状態更新"

5. 市場危険度分析（Step 4）
   - prompts/step4_analyze_market_risk.mdを読み込み
   - 入力: events.json + market_state.json
   - 8項目をスコアリング
   - 前回スコアとの差分を計算
   - data/analysis/market_risk.jsonを更新
   - git commit "市場危険度分析完了: [スコア]/100"

6. Top30スコアリング（Step 5）
   - prompts/step5_analyze_top30.mdを読み込み
   - 入力: monopoly_map.json + events.json + market_state.json + market_risk.json
   - スコアリング実行、4象限配置
   - 前回順位との変動を計算
   - data/analysis/top30.jsonを更新
   - git commit "Top30スコアリング完了"

7. HTML可視化生成（Step 5.5）
   - templates/quadrant_chart_template.htmlを読み込み
   - top30.jsonのデータでstockDataを生成
   - reports/[TODAY]/quadrant_chart.htmlに出力
   - git commit "4象限チャートHTML生成"

8. 最終レポート生成（Step 6）
   - prompts/step6_generate_report.mdを読み込み
   - 全データを統合
   - 変化点（changelog）を明記
   - reports/[TODAY]/final_report.mdに出力
   - git commit "最終レポート生成"

9. 完了処理
   - data/state.jsonを更新
   - latest/フォルダを更新
   - git commit "分析完了: [TODAY]"
   - git push origin main
   - サマリーを表示
```

---

## ディレクトリ構造

```
japan-investment-analysis/
├── CLAUDE.md                         # このファイル
├── README.md                         # プロジェクト説明
├── SETUP.md                          # セットアップ手順
├── prompts/                          # Step別プロンプト
│   ├── step1_collect_events.md
│   ├── step2_update_monopoly_map.md
│   ├── step3_update_market_state.md
│   ├── step4_analyze_market_risk.md
│   ├── step5_analyze_top30.md
│   └── step6_generate_report.md
├── templates/                        # HTMLテンプレート
│   └── quadrant_chart_template.html
├── data/                             # ★永続データ層
│   ├── state.json                    # 実行状態
│   ├── events.json                   # イベントログ（append-only）
│   ├── snapshots/
│   │   ├── monopoly_map.json         # 独占マップ（準静的）
│   │   ├── market_state.json         # 市場状態（動的）
│   │   └── forecasts.json            # 予測・見通し
│   └── analysis/
│       ├── market_risk.json          # 市場危険度（履歴保持）
│       └── top30.json                # Top30（履歴保持）
├── reports/                          # 日付別レポート
│   └── YYYY-MM-DD/
│       ├── final_report.md
│       ├── changelog.md              # 変化ログ
│       └── quadrant_chart.html
└── latest/                           # 最新レポートのコピー
```

---

## データファイル仕様

### events.json（イベントログ）

**絶対ルール: 既存イベントの削除・変更は禁止。追記のみ。**

```json
{
  "events": [
    {
      "id": "evt_YYYYMMDD_NNN",
      "date": "YYYY-MM-DD",
      "type": "policy|earnings|ma|contract|market_data|geopolitics|other",
      "category": "japan_policy|us_policy|company|share_update|...",
      "title": "イベントタイトル",
      "content": "詳細内容",
      "affected_tickers": ["8035", "6857"],
      "source": "ソース名",
      "source_url": "https://...",
      "reliability": "A|B+|B",
      "recorded_at": "ISO8601",
      "is_trigger_for": null | "monopoly_map"
    }
  ]
}
```

### monopoly_map.json（独占マップ）

```json
{
  "metadata": {
    "last_update": "YYYY-MM-DD",
    "update_reason": "更新理由",
    "update_trigger_event_id": "evt_...",
    "next_expected_triggers": ["2025-04 Gartner", "2025-06 SEMI"]
  },
  "companies": {
    "8035": {
      "name": "東京エレクトロン",
      "products": [
        {
          "name": "コータ/デベロッパ",
          "share": 91,
          "share_range": null,
          "share_source": "SEMI 2024",
          "share_as_of": "2024",
          "previous_share": 87,
          "competitors": [{"name": "ASML", "share": 5}],
          "entry_barrier_years": 10,
          "switching_cost": "極めて高い"
        }
      ],
      "domains": ["AI", "半導体"],
      "certifications": [],
      "china_revenue_pct": 25
    }
  }
}
```

### market_state.json（市場状態）

```json
{
  "as_of": "YYYY-MM-DD HH:MM:SS",
  "fx": {
    "usdjpy": 155.50,
    "source": "検索結果"
  },
  "indices": {
    "nikkei225": 39500,
    "nikkei225_per": 17.2,
    "nikkei225_pbr": 1.45,
    "topix": 2750
  },
  "sentiment": {
    "foreign_investor_flow_weekly": "+1500億円",
    "margin_buying_balance": "3.8兆円",
    "arbitrage_balance": "5000億円"
  },
  "risks": {
    "china_slowdown": "中程度",
    "taiwan_strait": "低〜中",
    "boj_policy": "正常化継続"
  }
}
```

### market_risk.json（市場危険度）

```json
{
  "history": [
    {
      "date": "YYYY-MM-DD",
      "total_score": 48,
      "items": {
        "valuation": {"score": 8.5, "reason": "PER 17.2は過去平均やや上"},
        "foreign_flow": {"score": 5.0, "reason": "買い越し継続"},
        "fx_risk": {"score": 6.0, "reason": "円安継続だが日銀正常化リスク"},
        "policy_risk": {"score": 4.0, "reason": "大きな政策変更なし"},
        "sentiment": {"score": 6.5, "reason": "信用買残やや高水準"},
        "china_risk": {"score": 7.0, "reason": "景気減速継続"},
        "geopolitics": {"score": 5.5, "reason": "台湾リスク低位安定"},
        "earnings_gap": {"score": 5.5, "reason": "株価とEPSは概ね連動"}
      },
      "verdict": "中リスク",
      "recommendation": "通常ポジション維持"
    }
  ]
}
```

### top30.json（Top30分析）

```json
{
  "history": [
    {
      "date": "YYYY-MM-DD",
      "top_conviction": {
        "ticker": "8035",
        "name": "東京エレクトロン",
        "reason": "コータ91%独占、AI半導体需要の爆発的拡大"
      },
      "rankings": [
        {
          "rank": 1,
          "previous_rank": 1,
          "rank_change": 0,
          "ticker": "8035",
          "name": "東京エレクトロン",
          "total_score": 92,
          "monopoly": 30,
          "capital_efficiency": 17,
          "synergy": 23,
          "asymmetry": 22,
          "certainty": 92,
          "upside": 92,
          "quadrant": "prime",
          "domains": ["AI", "半導体"],
          "note": "⭐コータ91%独占・最高確信"
        }
      ],
      "quadrant_summary": {
        "prime": ["8035", "6857", "7011", "2802", "6501", "6268"],
        "stable": ["6146", "4063", "6361", "7012"],
        "speculative": ["6890", "6324", "6702"],
        "avoid": ["6762", "7735"]
      }
    }
  ]
}
```

### state.json（実行状態）

```json
{
  "last_execution": "ISO8601",
  "events": {
    "last_collected": "ISO8601",
    "total_count": 156,
    "last_event_id": "evt_20250126_003"
  },
  "monopoly_map": {
    "last_update": "YYYY-MM-DD",
    "update_reason": "SEMI 2024レポート",
    "pending_triggers": []
  },
  "market_state": {
    "last_update": "ISO8601"
  },
  "analysis": {
    "market_risk": {
      "last_update": "ISO8601",
      "last_score": 48
    },
    "top30": {
      "last_update": "ISO8601",
      "top_conviction": "8035"
    }
  }
}
```

---

## 変化検出ルール

### イベント収集時のトリガー検出

以下のイベントは `is_trigger_for: "monopoly_map"` をセット：

| イベントタイプ | 例 |
|----------------|-----|
| share_update | 「SEMI発表: 東京エレクトロンのシェア91%」 |
| ma | 「A社がB社を買収完了」 |
| major_contract | 「5年間独占供給契約」 |
| major_loss | 「主要顧客が競合に切り替え」 |
| new_entrant | 「中国メーカーが量産開始」 |
| certification | 「防衛省認定取得/失効」 |

### 変化ログ（changelog.md）の生成

各分析完了時に自動生成：

```markdown
# 変化ログ: YYYY-MM-DD

## 前回分析: YYYY-MM-DD

## 新規イベント（N件）

### 政策
- [2025-01-24] 経産省、半導体補助金第3弾を発表
  - 受益: 東京エレクトロン、アドバンテスト

### 企業動向
- [2025-01-22] 味の素、ABF増産投資を発表
  - 受益: 味の素（生産能力+30%）

## 市場危険度

| 項目 | 前回 | 今回 | 変化 |
|------|------|------|------|
| 合計 | 42 | 48 | +6 |
| バリュエーション | 7.0 | 8.5 | +1.5 |
| ... | | | |

## Top30順位変動

| 銘柄 | 前回 | 今回 | 変化 | 理由 |
|------|------|------|------|------|
| 味の素 | 4位 | 3位 | ↑1 | ABF増産発表 |
| フェローテック | 5位 | 6位 | ↓1 | 中国リスク顕在化 |

## 独占マップ変更

（トリガーイベントがあった場合のみ）
```

---

## エラーハンドリング

### 検索失敗時
1. 3回リトライ
2. 失敗したらイベントに `"status": "search_failed"` を付与
3. 分析は既存データで続行

### データ整合性
- events.jsonへの追記前に重複チェック（同一日・同一タイトル）
- 不正なJSONは読み込み前にバリデーション

### Git競合
- pull --rebase を試行
- 失敗したらユーザーに通知

---

## 専門用語定義

### サプライチェーン階層
| 用語 | 定義 |
|------|------|
| Tier1 | 最終製品メーカーに直接納入 |
| Tier2 | Tier1に納入 |
| Tier3 | Tier2に納入 |

### 6ドメイン
| # | ドメイン | 領域 |
|---|----------|------|
| 1 | エネルギー | 原子力、送配電、蓄電、水素 |
| 2 | 軍事・防衛 | ミサイル、航空機、艦船 |
| 3 | AI | 計算基盤、製造装置、先端材料 |
| 4 | ロボティクス | 産業用、サービス、ドローン |
| 5 | 宇宙 | ロケット、衛星、月面 |
| 6 | サイバー | 暗号、量子、電子戦 |

### 信頼度
| 信頼度 | ソース |
|--------|--------|
| A | 政府発表、企業開示 |
| B+ | 専門メディア |
| B | 大手通信社 |
| 採用禁止 | SNS、個人ブログ |
