# Step 1: イベント収集

## ミッション

前回収集日以降に発生した新規イベントを収集し、**4次元評価**（確度・検証度・非対称性・鮮度）を付与してevents.jsonに追記する。

**絶対ルール**: 既存イベントの削除・変更は禁止。追記のみ。

---

## 情報収集の原則

### 1. 確度を最大化する

```
報道を発見 → 一次資料を検索 → 確度を判定
```

- 「○○を検討」という報道を見つけたら、政府発表や企業開示を検索
- 一次資料が見つかれば確度UP、見つからなければ確度は低いまま記録

### 2. 検証度を高める

| 目標 | 行動 |
|------|------|
| primary_confirmed | 政府発表、企業開示のURLを取得 |
| multi_source | 2つ以上の独立したソースで確認 |
| single_reliable | 信頼できるソース1つ（要注意フラグ） |

### 3. 非対称性を評価する

情報を見つけたら、以下を確認：
- 英語メディアで報道されているか？ → Noなら非対称性高
- Tier2/Tier3のサプライチェーン情報か？ → Yesなら非対称性高
- 認証・参入障壁に関する情報か？ → Yesなら非対称性高

### 4. 鮮度を記録する

- イベント発生日と記録日を区別
- 有効期限（valid_until）を設定

---

## 事前確認

1. `data/state.json`から前回収集日を取得
2. `data/events.json`から最後のイベントIDを取得
3. `data/information_quality.json`の未検証アラートを確認（追加検証の機会）

---

## 収集対象と検索戦略

### A. 日本政府政策（非対称性：高）

**検索クエリ（日本語優先）:**
```
"経済産業省 発表 [今週/今月]"
"防衛省 予算 発表"
"経済安全保障 政策 決定"
"原子力規制委員会 審査 許可"
"半導体 補助金 採択 発表"
```

**一次資料の確認先:**
- 経産省: https://www.meti.go.jp/
- 防衛省: https://www.mod.go.jp/
- 内閣府: https://www.cao.go.jp/

**確度判定:**
| 文言 | stage | score |
|------|-------|-------|
| 「検討」「方針」 | report_unconfirmed | 30-40 |
| 「決定」「発表」 | official_announcement | 70-80 |
| 「成立」「施行」 | contract_signed | 85-95 |

### B. 米国政策→日本波及（非対称性：低〜中）

**検索クエリ（英語）:**
```
"CHIPS Act Japan supplier"
"US semiconductor export control Japan"
"DOE nuclear SMR Japan partner"
"Pentagon defense budget Japan ally"
```

**一次資料の確認先:**
- DOE: https://www.energy.gov/
- Commerce: https://www.commerce.gov/
- DoD: https://www.defense.gov/

### C. 企業動向（非対称性：高〜中）

**検索クエリ（日本語）:**
```
"[企業名] 決算発表"
"[企業名] 受注 契約"
"[企業名] 増産 投資"
"[企業名] 自社株買い"
"[企業名] 決算説明会"  ← Q&Aは非対称性の宝庫
```

**一次資料の確認先:**
- 適時開示: https://www.release.tdnet.info/
- EDINET: https://disclosure.edinet-fsa.go.jp/

**非対称性チェック:**
- 決算説明会Q&Aは日本語のみか？ → 英語transcriptの有無を確認
- 業界紙のみの報道か？ → 日経/Bloomberg/Reutersでの報道有無を確認

### D. 市場シェア・調査レポート（非対称性：低〜中）

**検索クエリ:**
```
"SEMI semiconductor equipment market share"
"Gartner market share report 2024/2025"
"TrendForce market share"
"半導体製造装置 シェア ランキング 最新"
```

**確度判定:**
- 調査機関公式発表 → official_announcement (75)
- 報道での引用 → report_confirmed (55)

### E. 地政学（非対称性：低）

**検索クエリ:**
```
"台湾海峡 緊張 最新"
"中国 半導体 規制 日本"
"日米同盟 防衛 最新"
```

---

## 出力フォーマット

### 基本構造

```json
{
  "id": "evt_YYYYMMDD_NNN",
  "date": "YYYY-MM-DD",
  "type": "policy|earnings|ma|contract|market_data|geopolitics",
  
  "content": {
    "title": "イベントタイトル（簡潔に）",
    "detail": "詳細内容（重要な数字、発言を含む）",
    "affected_tickers": ["8035", "6857"]
  },
  
  "certainty": {
    "stage": "official_announcement",
    "score": 75,
    "rationale": "なぜこの確度か（一次資料で確認、報道のみ等）",
    "upgrade_trigger": "何が起きたら確度が上がるか",
    "downgrade_risk": "何が起きたら確度が下がるか"
  },
  
  "verification": {
    "level": "primary_confirmed|multi_source|single_reliable|single_unverified",
    "sources": [
      {
        "type": "primary|secondary",
        "name": "ソース名",
        "url": "URL（可能なら）",
        "date": "YYYY-MM-DD"
      }
    ],
    "cross_checked": true|false,
    "conflicts": null | "矛盾の内容"
  },
  
  "asymmetry": {
    "score": 0-25,
    "sources": {
      "language_barrier": true|false,
      "supply_chain_depth": true|false,
      "certification_barrier": true|false
    },
    "detail": "非対称性の具体的な理由",
    "known_by": ["誰が知っているか"],
    "unknown_to": ["誰が知らないか"],
    "resolution_trigger": "何が起きたら非対称性が解消されるか",
    "estimated_resolution": "いつ頃解消されそうか"
  },
  
  "freshness": {
    "event_date": "YYYY-MM-DD",
    "recorded_at": "ISO8601",
    "decay_rate": "fast|medium|slow",
    "valid_until": "YYYY-MM-DD"
  },
  
  "is_trigger_for": null | "monopoly_map"
}
```

### 確度（certainty）の判定基準

| stage | score | 条件 |
|-------|-------|------|
| rumor | 10-20 | 「関係者によると」「検討している模様」 |
| report_unconfirmed | 30-40 | 報道あり、一次資料なし |
| report_confirmed | 50-60 | 複数報道で確認、一次資料なし |
| official_announcement | 70-80 | 政府発表、企業開示で確認 |
| contract_signed | 85-95 | 契約締結、予算成立、法案成立 |
| executed | 95-99 | 実行済み、決算で数字確定 |

### 検証度（verification）の判定基準

| level | 条件 |
|-------|------|
| primary_confirmed | 政府発表/企業開示のURLを取得済み |
| multi_source | 2つ以上の独立ソースで確認 |
| single_reliable | 信頼できるソース1つ（日経、専門紙等） |
| single_unverified | 上記以外、または確認不十分 |
| conflicting | 複数ソースで情報が矛盾 |

### 非対称性（asymmetry）スコアの目安

| score | 条件 |
|-------|------|
| 21-25 | 3源泉全て該当、英語報道なし、Tier3、認証必須 |
| 16-20 | 2源泉該当、英語報道ほぼなし |
| 11-15 | 1源泉該当、英語報道少ない |
| 6-10 | 英語報道あるが詳細は日本語のみ |
| 0-5 | 英語で広く報道済み |

---

## トリガーイベントの判定

以下に該当する場合、`is_trigger_for: "monopoly_map"` を設定：

| 条件 | 例 |
|------|-----|
| シェアレポート発表 | SEMI、Gartner、TrendForce公式 |
| M&A完了 | 「買収完了」「統合完了」 |
| 大型独占契約 | 「5年間独占供給」「長期契約」 |
| 大型失注 | 「主要顧客が競合に切り替え」 |
| 新規参入 | 「○○が量産開始」「○○が市場参入」 |
| 認証取得/失効 | 「防衛省認定取得」「資格失効」 |

---

## 重複チェック

追記前に確認：
1. 同一日付 + 同一タイトル（類似含む）が存在しないか
2. 同一内容で異なる日付のイベントがないか（更新の場合は新規イベントとして追記し、関連付け）

---

## 品質チェック（収集完了時）

- [ ] 全イベントに4次元評価が付与されているか
- [ ] primary_confirmed以外のイベントに一次資料検索を試みたか
- [ ] 非対称性スコア16以上のイベントには詳細な理由が記載されているか
- [ ] 矛盾する情報がある場合、conflictsに記録したか

---

## 完了後アクション

```bash
git add data/events.json
git commit -m "イベント収集完了: N件追加（確度70+: X件、非対称性16+: Y件）"
```

次のステップ: Step 1.5（情報品質チェック）へ
