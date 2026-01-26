# Step 2: 独占マップ更新

## ミッション

トリガーイベントが検出された場合、または前回更新から30日以上経過した場合に、独占マップの該当部分を更新する。

---

## 更新判定

### 更新する条件

以下のいずれかを満たす場合に更新：

1. **トリガーイベント検出**
   - Step 1で `is_trigger_for: "monopoly_map"` のイベントがあった
   - 該当イベントに関連する企業・製品のみを更新

2. **定期更新**
   - 前回更新から30日以上経過
   - 全体を再検証

3. **強制更新**
   - ユーザーが「独占マップを更新」と指示

### 更新しない条件

- トリガーイベントなし AND 30日未満
- → 「独占マップは[日付]更新済み。トリガーイベントなし。次回予定トリガー: [リスト]」と通知してスキップ

---

## 更新時の検索クエリ

### トリガーイベント起因の部分更新

該当企業・製品に絞って検索：

```
"[企業名] [製品名] 世界シェア 最新"
"[企業名] market share [year]"
```

### 定期更新（全体）

#### A. 半導体製造装置
```
semiconductor equipment market share 2025 Japan
半導体製造装置 シェア ランキング 最新
```

#### B. 電子部品・材料
```
MLCC market share latest
photoresist market share Japan
silicon wafer market share global
ABF substrate market share
HBM materials supplier share
```

#### C. 産業機械・ロボティクス
```
industrial robot market share 2025
precision reducer market share global
servo motor market share Japan
```

#### D. エネルギー・電力インフラ
```
power transformer market share global Japan
power semiconductor market share SiC GaN
```

#### E. 防衛・宇宙
```
Japan defense industry companies
Japan space industry suppliers
```

#### F. 素材・化学
```
specialty chemicals market share Japan
carbon fiber market share global
```

---

## 更新ルール

### シェア情報の記録

```json
{
  "name": "コータ/デベロッパ",
  "share": 91,
  "share_range": null,
  "share_source": "SEMI 2024",
  "share_as_of": "2024",
  "previous_share": 87,
  "competitors": [{"name": "ASML", "share": 5}]
}
```

- `previous_share`: 更新前の値を必ず保持
- `share_range`: 複数ソースで差がある場合は範囲で記載（例: `[85, 90]`）
- `share_source`: データの出典を明記
- `share_as_of`: データの時点（年または年月）

### メタデータの更新

```json
{
  "metadata": {
    "last_update": "2025-01-26",
    "update_reason": "SEMI 2024レポート発表",
    "update_trigger_event_id": "evt_20250126_001",
    "next_expected_triggers": ["2025-04 Gartner", "2025-06 SEMI"]
  }
}
```

---

## 出力フォーマット

`data/snapshots/monopoly_map.json`を更新：

```json
{
  "metadata": {
    "last_update": "YYYY-MM-DD",
    "update_reason": "理由",
    "update_trigger_event_id": "evt_...",
    "next_expected_triggers": ["2025-04 Gartner"]
  },
  "companies": {
    "8035": {
      "name": "東京エレクトロン",
      "products": [...],
      "domains": ["AI", "半導体"],
      "certifications": [],
      "china_revenue_pct": 25
    }
  }
}
```

---

## 新規企業の追加基準

以下の条件を満たす企業を発見したら追加：

1. 世界シェア30%以上、または
2. 特定工程で唯一の供給者、または
3. 6ドメインのうち2つ以上に関与

---

## 完了後アクション

更新した場合：
```bash
git add data/snapshots/monopoly_map.json
git commit -m "独占マップ更新: [理由]"
```

スキップした場合：
```
→ Step 3へ進む
```
