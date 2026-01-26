# Step 1: イベント収集

## ミッション

前回収集日以降に発生した新規イベントを収集し、events.jsonに追記する。
**既存イベントの削除・変更は禁止。追記のみ。**

---

## 事前確認

1. `data/state.json`から前回収集日を取得
2. `data/events.json`から最後のイベントIDを取得

---

## 収集対象イベント

### A. 日本政府政策

```
検索クエリ:
- "経済産業省 発表 [前回収集日以降]"
- "防衛省 予算 発表"
- "経済安全保障 政策 最新"
- "原子力規制委員会 審査 最新"
- "半導体 補助金 日本 最新"
```

### B. 米国政策（日本企業への波及）

```
検索クエリ:
- "US semiconductor policy Japan latest"
- "CHIPS Act Japan impact latest"
- "US defense budget Japan ally"
- "US China export control semiconductor"
```

### C. 企業動向（独占マップ掲載企業を優先）

```
検索クエリ:
- "[企業名] 決算 発表"
- "[企業名] 受注 契約"
- "[企業名] M&A 買収"
- "[企業名] 設備投資 増産"
- "[企業名] 自社株買い 増配"
```

### D. 市場シェアレポート

```
検索クエリ:
- "SEMI semiconductor equipment market share"
- "Gartner market share report"
- "TrendForce market share"
- "半導体製造装置 シェア 最新"
```

### E. 地政学

```
検索クエリ:
- "台湾海峡 最新"
- "中国 半導体 規制 最新"
- "日本 防衛 同盟 最新"
```

---

## イベント分類ルール

| type | 説明 | is_trigger_forの判定 |
|------|------|----------------------|
| policy | 政策発表、法案成立 | 法案成立・予算確定時 |
| earnings | 決算発表、業績修正 | バックログ大幅変動時 |
| ma | M&A発表、完了 | 完了時にmonopoly_map |
| contract | 契約締結、受注 | 大型契約時 |
| market_data | シェアレポート発表 | monopoly_map |
| geopolitics | 地政学イベント | なし |
| other | その他 | なし |

---

## 出力フォーマット

events.jsonに以下の形式で追記：

```json
{
  "id": "evt_YYYYMMDD_NNN",
  "date": "YYYY-MM-DD",
  "type": "policy",
  "category": "japan_policy",
  "title": "経産省、半導体補助金第3弾を発表",
  "content": "総額1.5兆円規模、国内製造装置メーカーも対象に含む",
  "affected_tickers": ["8035", "6857", "6146"],
  "source": "経産省プレスリリース",
  "source_url": "https://...",
  "reliability": "A",
  "recorded_at": "2025-01-26T10:30:00Z",
  "is_trigger_for": null
}
```

---

## 重複チェックルール

追記前に以下を確認：
1. 同一日付 + 同一タイトル（類似含む）のイベントが存在しないか
2. 存在する場合はスキップ

---

## トリガー検出

以下のイベントは `is_trigger_for: "monopoly_map"` をセット：

- type: "market_data" かつ シェア情報を含む
- type: "ma" かつ 完了報道
- type: "contract" かつ 大型独占契約
- 「シェア」「市場占有率」「首位」「独占」等のキーワードを含む

---

## 完了後アクション

```bash
git add data/events.json
git commit -m "イベント収集完了: N件追加"
```

次のステップ: トリガーイベントの有無を確認し、Step 2へ
