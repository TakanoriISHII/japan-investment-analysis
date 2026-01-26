# Step 1.5: 情報品質チェック

## ミッション

収集したイベントの品質を検証し、矛盾・陳腐化・未検証のアラートを生成する。
情報の不確実性を減少させるためのゲートキーパー。

---

## 実行タイミング

- Step 1（イベント収集）完了後に必ず実行
- 定期的な品質監視として単独実行も可

---

## チェック項目

### 1. 未検証情報の検出

**条件:**
```
verification.level == "single_unverified" 
AND 
(現在日時 - freshness.recorded_at) > 7日
```

**アクション:**
- information_quality.jsonのalerts.unverifiedに追加
- 確度スコアを10%減少させることを推奨
- 追加検索で一次資料を探す

### 2. 矛盾情報の検出

**チェック対象:**
- 同一企業の同一指標（シェア、売上比率、生産能力等）
- 乖離が10%以上ある場合

**例:**
```
イベントA: 東京エレクトロンの中国売上比率 25%（会社発表）
イベントB: 東京エレクトロンの中国売上比率 30%（アナリスト推計）
→ 矛盾として記録
```

**アクション:**
- information_quality.jsonのalerts.conflictsに追加
- 両方のソースを記録
- 解決方法（次回決算で確認等）を記載

### 3. 陳腐化情報の検出

**ルール:**

| 情報タイプ | 陳腐化判定 | アクション |
|------------|------------|------------|
| シェアデータ | 180日以上前 | 最新データ検索を推奨 |
| 政策情報 | 実行期限を過ぎた | 結果を確認 |
| ガイダンス | 次回決算後 | 実績との比較が必要 |
| 契約情報 | 契約期間満了 | 更新状況を確認 |

**アクション:**
- information_quality.jsonのalerts.staleに追加
- 更新検索を実行するか、次回Step 1での優先項目に追加

### 4. 時系列矛盾の検出

**チェック:**
- 同一トピックで「契約締結」の後に「検討中」が来ていないか
- 日付の逆転がないか

**アクション:**
- 日付と内容を再確認
- 必要に応じて訂正イベントを追加

---

## 品質スコアの計算

```
quality_score = (
  (primary_confirmed件数 × 1.0) +
  (multi_source件数 × 0.9) +
  (single_reliable件数 × 0.7) +
  (single_unverified件数 × 0.3)
) / 総イベント数 × 100

減点:
- 未検証アラート1件につき -2
- 矛盾アラート1件につき -5
- 陳腐化アラート1件につき -1
```

---

## 出力フォーマット

`data/information_quality.json`を更新：

```json
{
  "last_updated": "2025-01-26T10:30:00Z",
  "summary": {
    "total_events": 156,
    "by_certainty_stage": {
      "executed": 12,
      "contract_signed": 23,
      "official_announcement": 45,
      "report_confirmed": 34,
      "report_unconfirmed": 28,
      "rumor": 14
    },
    "by_verification_level": {
      "primary_confirmed": 34,
      "multi_source": 56,
      "single_reliable": 45,
      "single_unverified": 21
    },
    "average_certainty_score": 62.5,
    "high_confidence_ratio": 0.65
  },
  "alerts": {
    "unverified": [
      {
        "event_id": "evt_20250120_003",
        "title": "○○社の増産計画",
        "issue": "単一ソースで7日以上未検証",
        "days_since_record": 10,
        "current_certainty": 35,
        "action": "一次資料で検証、または確度を降格",
        "search_suggestion": "[企業名] 増産 発表 公式"
      }
    ],
    "conflicts": [
      {
        "topic": "東京エレクトロンの中国売上比率",
        "event_ids": ["evt_20250115_001", "evt_20250118_002"],
        "values": [
          {"value": "25%", "source": "2024年度有価証券報告書", "reliability": "A"},
          {"value": "30%", "source": "○○証券レポート", "reliability": "B"}
        ],
        "recommended_value": "25%（一次資料を優先）",
        "action": "次回決算で確認、一次資料の値を採用"
      }
    ],
    "stale": [
      {
        "event_id": "evt_20240801_001",
        "title": "○○のシェア情報",
        "data_date": "2024-06-01",
        "age_days": 240,
        "action": "最新シェアデータを検索",
        "search_suggestion": "[製品名] market share 2024 2025"
      }
    ]
  },
  "quality_score": 78,
  "quality_trend": "+3 vs 前回",
  "recommendations": [
    "未検証イベント21件の一次資料確認を推奨",
    "シェアデータ3件が陳腐化、更新検索を推奨"
  ]
}
```

---

## 重大アラートの報告

以下の場合は、分析を進める前にユーザーに報告：

1. **矛盾アラートが3件以上** — 情報基盤の信頼性に問題
2. **quality_scoreが60未満** — 情報品質が低い
3. **投資判断の核心に関わる矛盾** — Top10銘柄のシェア、契約情報等

---

## 完了後アクション

```bash
git add data/information_quality.json
git commit -m "情報品質チェック完了: スコア[XX]/100, アラート[N]件"
```

次のステップ: Step 2（独占マップ更新判定）へ
