# 外部LLM用プロンプト

## 概要

外部LLM（GPT-4、Gemini、Perplexity等）で情報収集を行い、Claudeが分析するアーキテクチャです。

```
┌─────────────────────────────────────────────────────────┐
│  外部LLM（情報収集）                                     │
│  - 形式は柔軟でOK                                       │
│  - 情報量を重視                                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  保存先                                                  │
│  data/intelligence/raw/company_info/[llm名].md          │
│  data/intelligence/raw/broad_info/[llm名].md            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Claude（分析）                                          │
│  - raw/配下を読み込み                                    │
│  - 様々な形式を柔軟に解釈                                │
│  - 4軸評価、Top30選出、レポート生成                      │
└─────────────────────────────────────────────────────────┘
```

---

## プロンプト一覧

| ファイル | 用途 | 保存先 |
|----------|------|--------|
| `prompt_company_info.md` | 企業発掘・独占情報・財務情報 | `raw/company_info/` |
| `prompt_broad_info.md` | 広域情報（市場・政策・トレンド） | `raw/broad_info/` |

---

## 使い方

### 1. 企業情報の収集

```
1. prompt_company_info.md の内容を外部LLMに貼り付け
2. 実行結果を保存:
   data/intelligence/raw/company_info/[llm名].md

   例: gemini.md, gpt4.md, perplexity.md
```

### 2. 広域情報の収集

```
1. prompt_broad_info.md の内容を外部LLMに貼り付け
2. 実行結果を保存:
   data/intelligence/raw/broad_info/[llm名].md
```

### 3. Claude分析

```
Claudeに「分析を実行」と指示すると:
- raw/company_info/ と raw/broad_info/ を読み込み
- 情報を統合・評価
- Top30選出、レポート生成
```

---

## 出力形式について

**外部LLMの出力形式は自由です。**

Claudeが柔軟に解釈するため、以下のような様々な形式に対応：

- 箇条書き
- 表形式
- 文章形式
- JSON風
- 混在形式

**重要なのは情報量**であり、形式の正確さではありません。

---

## 保存先ディレクトリ

```
data/intelligence/raw/
├── company_info/      ← 企業・独占・財務情報
│   ├── gemini.md
│   ├── gpt4.md
│   └── perplexity.md
└── broad_info/        ← 広域情報（市場・政策）
    ├── gemini.md
    └── gpt4.md
```

---

## 注意事項

- ファイル名は `[llm名].md` 形式で統一
- 同じLLMで複数回実行する場合は上書き or 日付追加
- 古いディレクトリ（company_discovery等）は廃止
