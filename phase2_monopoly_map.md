# Phase 2: グローバル独占マップ構築

## ミッション

日本企業のグローバル市場シェア・競争優位の最新情報を収集し、構造化されたマップとして整理する。

**出力先**: `reports/[TODAY]/02_monopoly_map.md`

---

## 実行手順

### Step 1: カテゴリ別検索

#### A. 半導体製造装置
```
semiconductor equipment market share 2025 Japan
半導体製造装置 シェア ランキング 最新
EUV lithography supply chain Japan
semiconductor test equipment market share
```

#### B. 電子部品・材料
```
electronic components market share Japan 2025
MLCC market share latest
photoresist market share Japan
silicon wafer market share global
ABF substrate market share
HBM materials supplier share
半導体材料 シェア 日本企業 最新
```

#### C. 産業機械・ロボティクス
```
industrial robot market share 2025
precision reducer market share global
servo motor market share Japan
factory automation market share
ロボット 減速機 シェア 世界 最新
```

#### D. エネルギー・電力インフラ
```
power transformer market share global Japan
power semiconductor market share SiC GaN
nuclear power plant components supplier Japan
パワー半導体 SiC シェア 最新
```

#### E. 防衛・宇宙
```
Japan defense industry companies export
防衛装備品 主要企業 調達 最新
Japan space industry suppliers
Japan rocket supply chain companies
```

#### F. 素材・化学
```
specialty chemicals market share Japan
carbon fiber market share global
advanced materials Japan global leader
電池材料 シェア 日本 最新
```

### Step 2: 情報整理

**信頼度の付与:**
| 信頼度 | 基準 |
|--------|------|
| A | 業界団体・調査機関の公式データ |
| B+ | 専門メディアの引用データ |
| B | 一般メディアの報道 |
| 未確認 | 単一ソース |

---

## 出力フォーマット

```markdown
# グローバル独占マップ
**実行日**: [YYYY-MM-DD]

## サマリー

| カテゴリ | 世界シェア30%超の日本企業数 | 特筆事項 |
|----------|---------------------------|----------|
| 半導体製造装置 | | |
| 電子部品・材料 | | |
| 産業機械・ロボティクス | | |
| エネルギー・電力インフラ | | |
| 防衛・宇宙 | | |
| 素材・化学 | | |

## A. 半導体製造装置

| 工程/製品 | 日本企業 | 世界シェア | 出典 | 競合 | 信頼度 |
|-----------|----------|------------|------|------|--------|
| | | | | | |

## B. 電子部品・材料

| 製品 | 日本企業 | 世界シェア | 出典 | 競合 | 信頼度 |
|------|----------|------------|------|------|--------|
| | | | | | |

## C. 産業機械・ロボティクス

| 製品 | 日本企業 | 世界シェア | 出典 | 競合 | 信頼度 |
|------|----------|------------|------|------|--------|
| | | | | | |

## D. エネルギー・電力インフラ

| 製品 | 日本企業 | 世界シェア/強み | 出典 | 信頼度 |
|------|----------|-----------------|------|--------|
| | | | | |

## E. 防衛・宇宙

| 分野 | 日本企業 | 市場地位 | 出典 | 信頼度 |
|------|----------|----------|------|--------|
| | | | | |

## F. 素材・化学

| 製品 | 日本企業 | 世界シェア | 出典 | 競合 | 信頼度 |
|------|----------|------------|------|------|--------|
| | | | | | |

## 投資候補リスト

| 企業名 | コード | 主力製品 | 世界シェア | 関連ドメイン |
|--------|--------|----------|------------|--------------|
| | | | | |

（最低20社以上）
```

---

## 完了後アクション

```bash
git add reports/[TODAY]/02_monopoly_map.md
git commit -m "Phase 2: グローバル独占マップ完了"
```
