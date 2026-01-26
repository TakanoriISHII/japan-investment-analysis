# Step 0: グローバル・ボトルネック機会の動的発掘

## ミッション

**外国人投資家が見落としている「グローバル・ボトルネック支配」企業を発掘する。**

このステップは**毎回実行**し、以下を達成する：
1. 6ドメインのカバレッジバランスを確認
2. 不足領域の企業を積極的に発掘
3. 隠れたチャンピオン（Tier2/Tier3）を発見
4. 情報の非対称性が高い投資機会を特定

---

## 参照ファイル

```
data/sources/primary_sources.json      # 情報源マスター
data/sources/discovery_queries.json    # 発掘クエリ体系
data/sources/verification_protocols.json # 検証プロトコル
data/snapshots/monopoly_map.json       # 現在の独占マップ
```

---

## 実行手順

### Phase A: カバレッジ診断（5分）

#### A-1. 現在のドメイン別企業数を確認

```
monopoly_map.jsonを読み込み、以下を集計：

| ドメイン | 現在の企業数 | 目標 | 不足 |
|---------|-------------|------|------|
| AI | ? | 8-10社 | ? |
| エネルギー | ? | 5-7社 | ? |
| 軍事・防衛 | ? | 5-7社 | ? |
| ロボティクス | ? | 4-6社 | ? |
| 宇宙 | ? | 3-5社 | ? |
| サイバー | ? | 3-5社 | ? |
```

#### A-2. 優先発掘ドメインを決定

```
優先度 = (目標企業数 - 現在企業数) × ドメイン重要度係数

ドメイン重要度係数：
- AI: 1.2（市場規模大、投資機会多）
- エネルギー: 1.1（政策追い風）
- 軍事・防衛: 1.3（非対称性最大）
- ロボティクス: 1.0
- 宇宙: 1.1（成長期待）
- サイバー: 1.2（需要急増）
```

---

### Phase B: 系統的発掘（30-45分）

#### B-1. 認証リスト法（非対称性が最も高い）

**防衛装備庁の契約実績から発掘**

```
1. https://www.mod.go.jp/atla/souhon/supply/jisseki/ にアクセス
2. 直近年度の契約実績上位企業を確認
3. monopoly_mapにない企業を抽出
4. 各企業の独占領域を調査
```

**原子力認定企業から発掘**

```
1. 原子力規制委員会の認可事業者を確認
2. 原子力部品で独占的地位を持つ企業を特定
```

**航空宇宙認証（JISQ9100）企業から発掘**

```
1. 航空宇宙品質認証取得企業を検索
2. 宇宙・防衛領域のTier2サプライヤーを特定
```

#### B-2. サプライチェーン逆引き法

**既知のTier1から上流を辿る**

```
discovery_queries.jsonの「supply_chain_entry_points」を使用

例：東京エレクトロン（8035）の場合
検索: "東京エレクトロン サプライヤー" "東京エレクトロン 協力会社"
→ 部品・材料サプライヤーを特定
→ そのサプライヤーのシェアを調査
→ 独占的なら候補に追加
```

**グローバル企業の日本サプライヤーを探す**

```
例：ASML（EUVリソグラフィ）の日本サプライヤー
検索: "ASML 日本 サプライヤー" "EUV 日本企業 部品"
→ 光学系、ステージ機構、真空技術等
```

#### B-3. ボトルネック・ニュース法

**供給不足報道から逆算**

```
discovery_queries.jsonの「shortage_signals」を使用

検索例：
"{product} 供給不足 日本企業"
"{product} 納期遅延"
"{product} 世界で唯一"

不足している = ボトルネック = 支配力あり
```

#### B-4. ドメイン別発掘クエリ実行

**discovery_queries.jsonの「by_domain」を使用**

不足しているドメインから優先的に実行：

```
例：ロボティクスが不足の場合

検索実行：
1. "減速機 ハーモニックドライブ シェア"
2. "減速機 サイクロイド ナブテスコ シェア"
3. "サーボモータ 産業用 シェア 日本"
4. "エンコーダ 高精度 シェア 日本"

→ シェア50%以上の企業を候補リストに追加
```

---

### Phase C: 候補企業の4次元評価（20-30分）

発見した各候補企業に対して：

#### C-1. 確度（Certainty）の検証

```
verification_protocols.jsonの「certainty_verification」に従う

1. シェア情報の出典を特定
   - 調査機関名は？
   - 調査時期は？
   - 対象市場の定義は？

2. 一次資料を探す
   - 企業IR資料
   - 業界団体発表
   - 政府統計

3. 確度stageとscoreを決定
```

#### C-2. 検証度（Verification）の判定

```
verification_protocols.jsonの「verification_level」に従う

1. 一次資料で確認できた → primary_confirmed
2. 複数ソースで確認 → multi_source
3. 単一だが信頼できる → single_reliable
4. 単一、未検証 → single_unverified（追加検証必要）
```

#### C-3. 非対称性（Asymmetry）の評価

```
verification_protocols.jsonの「asymmetry_evaluation」に従う

基本スコア: 5点
+ 言語障壁（英語報道なし）: +8点
+ サプライチェーン深度（Tier2/3）: +7点
+ 認証障壁（防衛・原子力等）: +5点

英語カバレッジ確認：
- Bloomberg/Reuters英語版で検索
- 報道なし → 非対称性高い
```

#### C-4. 鮮度（Freshness）の確認

```
- 情報の取得日を記録
- decay_rateを設定
- valid_untilを設定
```

---

### Phase D: monopoly_map更新候補の作成

#### D-1. 候補リストの作成

```json
{
  "discovery_date": "YYYY-MM-DD",
  "domain_coverage_before": {
    "AI": 6, "エネルギー": 2, "軍事・防衛": 1,
    "ロボティクス": 0, "宇宙": 1, "サイバー": 0
  },
  "candidates": [
    {
      "ticker": "XXXX",
      "name": "企業名",
      "domain": "ロボティクス",
      "bottleneck": "精密減速機で世界シェア60%",
      "tier": "Tier1",
      "certainty": {
        "stage": "official_announcement",
        "score": 75,
        "source": "会社IR資料"
      },
      "verification": "primary_confirmed",
      "asymmetry": {
        "score": 18,
        "language_barrier": true,
        "supply_chain_depth": false,
        "certification_barrier": true
      },
      "recommendation": "追加推奨",
      "rationale": "ロボティクスドメインの欠落を補完、高い非対称性"
    }
  ]
}
```

#### D-2. 追加基準

| 基準 | 閾値 |
|------|------|
| 世界シェア | 30%以上、または特定領域で独占的 |
| 確度 | stage: report_confirmed以上、score: 50以上 |
| 検証度 | single_reliable以上 |
| 非対称性 | 10以上を優先、16以上は最優先 |

---

## 出力フォーマット

### discovery_result.json

```json
{
  "execution_date": "YYYY-MM-DD",
  "execution_time_minutes": 45,

  "coverage_analysis": {
    "before": {
      "AI": 6, "エネルギー": 2, "軍事・防衛": 1,
      "ロボティクス": 0, "宇宙": 1, "サイバー": 0,
      "total": 10
    },
    "gaps": ["ロボティクス", "サイバー"],
    "priority_domains": ["ロボティクス", "サイバー", "軍事・防衛"]
  },

  "discovery_methods_used": [
    {
      "method": "認証リスト法",
      "source": "防衛装備庁契約実績",
      "candidates_found": 3
    },
    {
      "method": "サプライチェーン逆引き",
      "entry_point": "ファナック",
      "candidates_found": 2
    }
  ],

  "candidates_discovered": [
    {
      "ticker": "6268",
      "name": "ナブテスコ",
      "domain": "ロボティクス",
      "bottleneck": "精密減速機（RV）世界シェア60%",
      "four_dimensions": {
        "certainty": {"stage": "executed", "score": 92},
        "verification": "multi_source",
        "asymmetry": {"score": 16, "sources": {"language": true, "depth": true, "cert": false}},
        "freshness": {"decay_rate": "slow", "valid_until": "2026-12"}
      },
      "recommendation": "追加",
      "priority": "high"
    }
  ],

  "monopoly_map_updates": {
    "additions": ["6268"],
    "domain_coverage_after": {
      "AI": 6, "エネルギー": 2, "軍事・防衛": 1,
      "ロボティクス": 1, "宇宙": 1, "サイバー": 0,
      "total": 11
    }
  },

  "next_actions": [
    "サイバードメインの追加発掘が必要",
    "軍事・防衛のTier2サプライヤー調査継続"
  ]
}
```

---

## 完了後アクション

```bash
# 発掘結果を保存
git add data/discovery/discovery_result_YYYYMMDD.json
git commit -m "Step 0完了: N社発掘（ドメイン: X, Y, Z）"
```

次のステップ: Step 1（イベント収集）へ
- 発掘した企業も対象に含めてイベント収集を実行

---

## 重要な注意事項

### やってはいけないこと

1. **企業名をハードコードしない** — 常に動的に発掘
2. **AI・半導体に偏重しない** — 6ドメインをバランスよくカバー
3. **Tier1だけを見ない** — Tier2/3こそ非対称性が高い
4. **英語情報だけで判断しない** — 日本語情報こそ価値がある

### 成功の指標

- 6ドメイン全てに最低1社以上
- 非対称性スコア16以上の企業を3社以上発見
- Tier2/3企業を全体の30%以上含む
- 確度70以上の情報で裏付けられた候補のみ採用
