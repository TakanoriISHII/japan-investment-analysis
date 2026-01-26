# Step 2: 独占マップ更新

## ミッション

トリガーイベントが検出された場合、または定期更新条件を満たす場合に、独占マップを更新する。
**シェア情報は確度の高い一次資料を優先する。**

---

## 更新判定

### 更新する条件

| 条件 | 詳細 |
|------|------|
| トリガーイベント | Step 1で `is_trigger_for: "monopoly_map"` のイベントあり |
| 定期更新 | 前回更新から30日以上経過 |
| 強制更新 | ユーザーが「独占マップを更新」と指示 |
| 品質アラート | information_quality.jsonでシェア関連のstaleアラートあり |

### 更新しない条件

上記いずれにも該当しない場合：
- スキップを宣言
- 「独占マップは[日付]更新済み。トリガーイベントなし。」と通知
- Step 3へ進む

---

## 更新時の検索戦略

### シェア情報の確度優先順位

| 優先度 | ソース | 確度 |
|--------|--------|------|
| 1 | 調査機関公式発表（SEMI、Gartner、TrendForce） | 最高 |
| 2 | 企業開示（有価証券報告書、決算説明資料） | 高 |
| 3 | 専門メディア報道（調査機関引用） | 中 |
| 4 | アナリストレポート推計 | 低 |
| 5 | 一般報道、推測 | 採用注意 |

### 検索クエリ

#### A. 半導体製造装置

```
# 一次資料を優先
"SEMI market statistics 2024 2025"
"semiconductor equipment market share official"

# 日本語
"半導体製造装置 市場シェア SEMI発表"
"[企業名] シェア 決算説明資料"
```

#### B. 電子部品・材料

```
"MLCC market share 2024 Murata TDK"
"photoresist market share JSR Tokyo Ohka"
"silicon wafer market share Shin-Etsu SUMCO"
"ABF substrate market share Ajinomoto"
```

#### C. 産業機械・ロボティクス

```
"industrial robot market share 2024 IFR"
"precision reducer market share Nabtesco Harmonic"
"servo motor market share Yaskawa Fanuc"
```

#### D. エネルギー・電力インフラ

```
"power transformer market share global"
"SiC power semiconductor market share"
"GaN power device market share"
```

#### E. 防衛・宇宙

```
# 公開情報が限定的、調達実績から推定
"防衛省 調達実績 [企業名]"
"Japan defense procurement [company]"
"JAXA supplier [company]"
```

---

## シェア情報の記録ルール

### 複数ソースで値が異なる場合

```json
{
  "share": 91,
  "share_range": [87, 91],
  "share_note": "SEMI発表91%、アナリスト推計87-90%。SEMI公式を採用。",
  "share_source": "SEMI Market Statistics 2024",
  "share_source_type": "primary",
  "share_as_of": "2024-12"
}
```

### 公開情報がない場合

```json
{
  "share": null,
  "share_estimated": 40,
  "share_note": "公式発表なし。調達実績から推定40%程度。",
  "share_source": "防衛省調達実績（推定）",
  "share_source_type": "estimated",
  "share_confidence": "low"
}
```

---

## 出力フォーマット

`data/snapshots/monopoly_map.json`を更新：

```json
{
  "metadata": {
    "last_update": "2025-01-26",
    "update_reason": "SEMI 2024年レポート発表",
    "update_trigger_event_id": "evt_20250126_001",
    "next_expected_triggers": [
      "2025-04: Gartner年次レポート",
      "2025-06: SEMI中間統計"
    ],
    "data_quality": {
      "primary_source_ratio": 0.75,
      "estimated_ratio": 0.15,
      "stale_ratio": 0.10
    }
  },
  "companies": {
    "8035": {
      "name": "東京エレクトロン",
      "name_en": "Tokyo Electron",
      "ticker": "8035",
      
      "products": [
        {
          "name": "コータ/デベロッパ",
          "name_en": "Coater/Developer",
          "category": "semiconductor_equipment",
          
          "share": {
            "value": 91,
            "range": null,
            "source": "SEMI Market Statistics 2024",
            "source_type": "primary",
            "source_url": "https://...",
            "as_of": "2024-12",
            "previous_value": 87,
            "previous_as_of": "2023-12",
            "change": "+4pp",
            "confidence": "high"
          },
          
          "competitors": [
            {"name": "ASML", "share": 5, "trend": "stable"},
            {"name": "その他", "share": 4, "trend": "declining"}
          ],
          
          "entry_barrier": {
            "years": 10,
            "factors": ["技術蓄積", "顧客認定", "プロセス統合"],
            "moat_strength": "極めて強い"
          },
          
          "switching_cost": "極めて高い（プロセス再認定に1-2年）"
        }
      ],
      
      "domains": ["AI", "半導体"],
      "domain_synergies": "半導体装置がAI計算基盤の製造に不可欠",
      
      "certifications": [],
      
      "geographic_exposure": {
        "china_revenue_pct": 25,
        "china_risk_note": "規制対象外製品中心だが、追加規制リスクあり",
        "us_revenue_pct": 15,
        "japan_revenue_pct": 20
      },
      
      "asymmetry_factors": {
        "language_barrier": false,
        "supply_chain_depth": false,
        "certification_barrier": false,
        "overall_score": 8,
        "note": "大型株で認知度高いが、技術深度は過小評価"
      }
    },
    
    "2802": {
      "name": "味の素",
      "name_en": "Ajinomoto",
      "ticker": "2802",
      
      "products": [
        {
          "name": "ABF（味の素ビルドアップフィルム）",
          "name_en": "Ajinomoto Build-up Film",
          "category": "semiconductor_materials",
          
          "share": {
            "value": 95,
            "range": [90, 95],
            "source": "会社開示、業界推計",
            "source_type": "mixed",
            "as_of": "2024",
            "confidence": "high"
          },
          
          "competitors": [
            {"name": "なし（実質独占）", "share": 5, "trend": "n/a"}
          ],
          
          "entry_barrier": {
            "years": 7,
            "factors": ["素材技術", "品質認定", "顧客関係"],
            "moat_strength": "極めて強い"
          }
        }
      ],
      
      "domains": ["AI", "半導体"],
      
      "asymmetry_factors": {
        "language_barrier": true,
        "supply_chain_depth": true,
        "certification_barrier": false,
        "overall_score": 22,
        "note": "食品会社として認識され、半導体材料事業が過小評価"
      }
    }
  }
}
```

---

## 品質チェック

更新完了時に確認：
- [ ] シェア情報に出典（source）が全て記載されているか
- [ ] 一次資料比率（primary_source_ratio）が60%以上か
- [ ] 推定値（estimated）には confidence: low が付与されているか
- [ ] 前回値（previous_value）が記録されているか

---

## 完了後アクション

更新した場合：
```bash
git add data/snapshots/monopoly_map.json
git commit -m "独占マップ更新: [理由]（一次資料比率: XX%）"
```

スキップした場合：
→ Step 3へ進む
