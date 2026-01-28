# プロンプトディレクトリ

## 概要

LLM別に最適化されたプロンプトを格納。各LLMの特性を活かした役割分担を実現。

## ディレクトリ構造

```
prompts/
├── README.md           # このファイル
├── shared/             # 共通定義
│   └── definitions.md  # ドメイン、カテゴリ、出力形式
├── grok/               # Grok用（速度重視）- 初期収集専用
│   ├── README.md
│   ├── broad_info.md   # 広域情報収集
│   └── company_scan.md # 企業スキャン
├── gemini/             # Gemini用（深さ重視）- 初期収集専用
│   ├── README.md
│   ├── company_deep.md # 企業深掘り
│   └── broad_info.md   # 広域情報（詳細）
├── claude/             # Claude用（検証重視）
│   ├── README.md
│   ├── contradiction_resolver.md    # 矛盾解消
│   ├── primary_source_verifier.md   # 一次情報源確認
│   ├── high_asymmetry_verifier.md   # 高非対称性確認
│   └── top30_reinforcement.md       # Top 30補強
└── external/           # 旧プロンプト（参考用）
    └── ...

※ 補強調査プロンプトは reinforcement/prompts/ に配置
```

## LLM役割分担

| LLM | 速度 | 強み | 主要タスク |
|-----|------|------|-----------|
| **Grok** | ★★★★★ | リアルタイム、大量処理 | 広域情報、企業スキャン、大量補強 |
| **Gemini** | ★★★☆☆ | 長文処理、包括的分析 | 企業深掘り、詳細調査 |
| **Claude** | ★★★★☆ | 論理推論、矛盾検出 | 検証、矛盾解消、統合 |

## 実行フロー

```
┌─────────────────────────────────────────────────────────┐
│ Phase 2: インテリジェンス収集（並列実行可能）            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Grok                    Gemini                        │
│  ├── broad_info.md       ├── company_deep.md           │
│  └── company_scan.md     └── broad_info.md             │
│                                                         │
│  → data/intelligence/raw/grok/                         │
│  → data/intelligence/raw/gemini/                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Phase 3-4: 比較分析・補足調査（Claude自動）             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Claude                                                │
│  ├── contradiction_resolver.md    (矛盾検出時)         │
│  ├── primary_source_verifier.md   (要確認情報あり時)    │
│  └── high_asymmetry_verifier.md   (非対称性15+時)      │
│                                                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Phase 8: 継続的改善（必要に応じて）                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Grok/Gemini                      Claude               │
│  └── data/.../reinforcement/      └── top30_reinforcement.md │
│      prompts/grok|gemini/                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## タスクスケジューラー連携

Grok/Geminiはタスクスケジューラーで定期実行:

### 週次実行（推奨: 日曜夜）

```bash
# Grok
grok/broad_info.md → data/intelligence/raw/grok/broad_info_YYYYMMDD.md
grok/company_scan.md → data/intelligence/raw/grok/company_scan_YYYYMMDD.md

# Gemini
gemini/company_deep.md → data/intelligence/raw/gemini/company_deep_YYYYMMDD.md
gemini/broad_info.md → data/intelligence/raw/gemini/broad_info_YYYYMMDD.md
```

### イベントドリブン実行

重大イベント発生時に追加実行:
- 地政学リスク急変
- 重要政策発表
- 市場急落

## 出力ディレクトリ

```
data/intelligence/
├── raw/
│   ├── grok/
│   │   ├── broad_info_YYYYMMDD.md
│   │   └── company_scan_YYYYMMDD.md
│   └── gemini/
│       ├── company_deep_YYYYMMDD.md
│       └── broad_info_YYYYMMDD.md
├── reinforcement/
│   ├── grok/
│   ├── gemini/
│   └── claude_auto/
└── ...
```

## 使用方法

### 手動実行

1. 該当LLMのプロンプトを開く
2. 内容をコピーしてLLMに貼り付け
3. 出力を指定ディレクトリに保存
4. ファイル名に日付を含める（YYYYMMDD形式）

### 自動実行（Claude）

Claudeプロンプトは条件を満たした場合に自動実行:
- `run analysis` コマンドで自動判定
- 条件: contradictions.json、quality_issues等の存在

## 更新履歴

| 日付 | 変更内容 |
|------|---------|
| 2025-01 | LLM別プロンプト構造に再編 |
| 2025-01 | Claude自動補強プロンプト追加 |
| 2025-01 | タスクスケジューラー対応 |
