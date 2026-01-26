# Step 3: 市場状態取得

## ミッション

動的な市場データを取得し、market_state.jsonを更新する。
**このステップは毎回実行する（鮮度が重要）。**

---

## 取得項目

### 1. 為替

**検索クエリ:**
```
"ドル円 現在"
"USD JPY rate"
```

**取得項目:**
- 現在レート
- 週間変動
- 日銀政策スタンス

### 2. 株価指数・バリュエーション

**検索クエリ:**
```
"日経平均 現在"
"日経平均 PER"
"日経平均 PBR"
"TOPIX 現在"
```

**取得項目:**
- 日経平均株価
- 日経平均PER（過去平均との比較）
- 日経平均PBR
- TOPIX

### 3. 投資家動向

**検索クエリ:**
```
"外国人投資家 売買動向 週間"
"信用買残 最新"
"裁定残高 最新"
```

**取得項目:**
- 外国人投資家の週間売買（金額、トレンド）
- 信用買残高
- 裁定残高

### 4. リスク要因

**検索クエリ:**
```
"中国経済 最新"
"台湾海峡 情勢"
"日銀 金融政策 見通し"
```

**取得項目:**
- 中国リスク評価
- 台湾海峡リスク評価
- 日銀政策見通し

---

## 確度の担保

市場データは速報性が重要だが、確度も確保する：

| データ | 優先ソース | 確度 |
|--------|------------|------|
| 為替 | 金融情報サービス（リアルタイム） | 高 |
| 株価指数 | 取引所公式、金融情報サービス | 高 |
| PER/PBR | 日経、Bloomberg | 中〜高 |
| 外国人売買 | 東証公式発表（週次） | 高 |
| 信用残高 | 東証公式発表（週次） | 高 |

**注意**: 速報値と確定値が異なる場合、確定値を優先。

---

## 出力フォーマット

`data/snapshots/market_state.json`を上書き：

```json
{
  "as_of": "2025-01-26T10:30:00Z",
  "data_quality": {
    "all_items_retrieved": true,
    "stale_items": [],
    "estimated_items": []
  },
  
  "fx": {
    "usdjpy": {
      "value": 155.50,
      "change_1d": "+0.30",
      "change_1w": "+1.20",
      "source": "検索結果",
      "as_of": "2025-01-26T10:00:00Z"
    },
    "outlook": {
      "boj_stance": "正常化継続",
      "next_meeting": "2025-03-14",
      "market_expectation": "据え置き70%、利上げ30%",
      "risk_direction": "円高リスクやや高い"
    }
  },
  
  "indices": {
    "nikkei225": {
      "value": 39500,
      "change_1d_pct": "+0.5%",
      "change_1w_pct": "+2.1%",
      "source": "検索結果"
    },
    "nikkei225_per": {
      "value": 17.2,
      "historical_avg": 15.5,
      "percentile": 75,
      "assessment": "やや割高",
      "source": "検索結果"
    },
    "nikkei225_pbr": {
      "value": 1.45,
      "vs_1x": "+45%",
      "source": "検索結果"
    },
    "topix": {
      "value": 2750,
      "change_1w_pct": "+1.8%",
      "source": "検索結果"
    }
  },
  
  "sentiment": {
    "foreign_investor": {
      "weekly_flow": "+1500億円",
      "trend": "3週連続買い越し",
      "cumulative_ytd": "+2.5兆円",
      "assessment": "買い意欲継続",
      "source": "東証（週次発表）",
      "data_date": "2025-01-24"
    },
    "margin_buying": {
      "balance": "3.8兆円",
      "change_1w": "+500億円",
      "historical_percentile": 70,
      "assessment": "やや高水準",
      "source": "東証"
    },
    "arbitrage": {
      "balance": "5000億円",
      "assessment": "中立",
      "source": "東証"
    },
    "overall_sentiment": "やや楽観"
  },
  
  "risks": {
    "china": {
      "level": "中",
      "score": 6.5,
      "factors": [
        "不動産セクター低迷継続",
        "消費回復鈍い",
        "輸出は底堅い"
      ],
      "japan_exposure": "製造業の中国売上比率平均15-20%",
      "source": "検索結果"
    },
    "taiwan_strait": {
      "level": "低〜中",
      "score": 5.0,
      "factors": [
        "大きな動きなし",
        "米中対話継続"
      ],
      "source": "検索結果"
    },
    "boj_policy": {
      "level": "注意",
      "score": 6.0,
      "factors": [
        "追加利上げ観測",
        "3月会合が焦点"
      ],
      "impact_on_stocks": "円高→輸出企業にマイナス",
      "source": "検索結果"
    },
    "us_policy": {
      "level": "中",
      "score": 5.5,
      "factors": [
        "関税政策の不確実性",
        "半導体規制の動向"
      ],
      "source": "検索結果"
    }
  },
  
  "summary": {
    "overall_risk_level": "中",
    "key_watchpoints": [
      "日銀3月会合",
      "外国人買いの持続性",
      "バリュエーションの高止まり"
    ],
    "favorable_factors": [
      "外国人買い継続",
      "企業業績堅調"
    ]
  }
}
```

---

## 取得失敗時の対応

| 状況 | 対応 |
|------|------|
| 一部データ取得失敗 | `data_quality.stale_items`に記録、前回値を参照 |
| 週次データが古い | `data_date`を明記、次回更新日を記載 |
| 矛盾するデータ | 公式ソース（東証等）を優先 |

---

## 完了後アクション

```bash
git add data/snapshots/market_state.json
git commit -m "市場状態更新: 日経[値] ドル円[値] 外国人[買/売]越し"
```

次のステップ: Step 4（市場危険度分析）へ
