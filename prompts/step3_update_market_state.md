# Step 3: 市場状態取得

## ミッション

動的な市場データを取得し、market_state.jsonを更新する。
**このステップは毎回実行する。**

---

## 取得項目と検索クエリ

### 1. 為替

```
検索クエリ:
- "ドル円 現在"
- "USD JPY rate"
```

取得: 現在のドル円レート

### 2. 株価指数・バリュエーション

```
検索クエリ:
- "日経平均 現在"
- "日経平均 PER 最新"
- "日経平均 PBR 最新"
- "TOPIX 現在"
```

取得:
- 日経平均株価
- 日経平均PER
- 日経平均PBR
- TOPIX

### 3. 投資家動向

```
検索クエリ:
- "外国人 売買動向 日本株 週間"
- "信用買残 最新"
- "裁定残高 最新"
```

取得:
- 外国人投資家の週間売買動向
- 信用買残高
- 裁定残高

### 4. リスク要因

```
検索クエリ:
- "中国経済 最新 見通し"
- "台湾海峡 緊張 最新"
- "日銀 金融政策 最新"
```

取得:
- 中国リスク評価（高/中/低）
- 台湾海峡リスク評価（高/中/低）
- 日銀政策スタンス

---

## 出力フォーマット

`data/snapshots/market_state.json`を上書き：

```json
{
  "as_of": "2025-01-26T10:30:00Z",
  "fx": {
    "usdjpy": 155.50,
    "usdjpy_change_1w": "+1.2",
    "source": "検索結果より"
  },
  "indices": {
    "nikkei225": 39500,
    "nikkei225_change_1w_pct": "+2.1",
    "nikkei225_per": 17.2,
    "nikkei225_per_historical_avg": 15.5,
    "nikkei225_pbr": 1.45,
    "topix": 2750
  },
  "sentiment": {
    "foreign_investor_flow_weekly": "+1500億円",
    "foreign_investor_flow_trend": "3週連続買い越し",
    "margin_buying_balance": "3.8兆円",
    "margin_buying_change_1w": "+500億円",
    "arbitrage_balance": "5000億円"
  },
  "risks": {
    "china_slowdown": {
      "level": "中",
      "detail": "不動産セクター低迷継続、消費回復鈍い"
    },
    "taiwan_strait": {
      "level": "低〜中",
      "detail": "大きな動きなし"
    },
    "boj_policy": {
      "level": "注意",
      "detail": "追加利上げ観測、3月会合が焦点"
    }
  }
}
```

---

## データ取得の注意点

1. **リアルタイム性**: 可能な限り当日のデータを取得
2. **変化の記録**: 前週比、前月比も可能なら取得
3. **ソースの明記**: 検索結果から取得したことを記録
4. **取得失敗時**: 「取得失敗」と明記し、前回値があれば参照

---

## 完了後アクション

```bash
git add data/snapshots/market_state.json
git commit -m "市場状態更新"
```

次のステップ: Step 4（市場危険度分析）へ
