# フェーズ完了検証プロトコル

**目的**: 各フェーズ完了時に必須ファイルが全て生成されていることを確認する

---

## 検証タイミング

各フェーズ完了時、**git commit前**に以下を実行:

```
1. 該当フェーズの必須出力ファイルが全て存在するか確認
2. 存在しない場合は生成してから次へ進む
3. 全て確認後にcommit
```

---

## Phase 7: レポート生成 検証コマンド

```bash
# 実行日を変数に設定
DATE=$(date +%Y-%m-%d)

# 必須ファイル確認
ls -la reports/$DATE/executive_summary.md
ls -la reports/$DATE/final_report.md
ls -la reports/$DATE/information_quality_report.md
ls -la reports/$DATE/quadrant_chart.html

# シンボリックリンク確認
ls -la latest/
```

**全て存在すればPhase 7完了**

---

## Phase 8: 継続的改善 検証コマンド

```bash
DATE=$(date +%Y-%m-%d)

# 必須ファイル確認
ls -la reinforcement/pending_tasks.json
ls -la reinforcement/results/claude_auto/$DATE.md
ls -la reinforcement/prompts/grok/${DATE}_tasks.md
ls -la reinforcement/prompts/gemini/${DATE}_tasks.md
```

**全て存在すればPhase 8完了**

---

## Phase 9: 完了 検証コマンド

```bash
# 全必須ファイル一括確認
echo "=== Phase 7 Reports ===" && \
ls reports/$(date +%Y-%m-%d)/ && \
echo "=== Phase 8 Reinforcement ===" && \
ls reinforcement/pending_tasks.json && \
ls reinforcement/results/claude_auto/ && \
ls reinforcement/prompts/grok/ && \
ls reinforcement/prompts/gemini/ && \
echo "=== All checks passed ==="
```

---

## Claudeへの指示（CLAUDE.mdに追加推奨）

### フル分析実行時の必須チェック

**Phase 7完了時:**
```
以下の4ファイルが reports/[DATE]/ に存在することを確認:
- executive_summary.md
- final_report.md
- information_quality_report.md
- quadrant_chart.html

存在しない場合は生成してからPhase 8へ進む
```

**Phase 8完了時:**
```
以下のファイルが存在することを確認:
- reinforcement/pending_tasks.json
- reinforcement/results/claude_auto/[DATE].md
- reinforcement/prompts/grok/[DATE]_tasks.md
- reinforcement/prompts/gemini/[DATE]_tasks.md

存在しない場合は生成してからPhase 9へ進む
```

**Phase 9（コミット前）:**
```
全フェーズの必須ファイルが存在することを最終確認
不足があればそのフェーズに戻って生成
```

---

## チェックリスト（TodoWriteで使用）

フル分析実行時、TodoWriteに以下を追加することを推奨:

```
Phase 7タスク:
- [ ] executive_summary.md 生成
- [ ] final_report.md 生成
- [ ] information_quality_report.md 生成
- [ ] quadrant_chart.html 生成
- [ ] latest シンボリックリンク更新
- [ ] Phase 7 検証完了

Phase 8タスク:
- [ ] pending_tasks.json 更新
- [ ] Claude自動補強結果 生成
- [ ] Grok用プロンプト 生成
- [ ] Gemini用プロンプト 生成
- [ ] Phase 8 検証完了
```

---

## エラー時の対応

### ファイルが不足している場合

1. 該当フェーズの出力を生成
2. 検証コマンドを再実行
3. 全て存在することを確認後、次へ進む

### 過去の分析でファイルが不足していた場合

```bash
# 特定フェーズのみ再実行
run phase 7    # レポート生成のみ
run phase 8    # 継続的改善のみ
```

---

**作成日**: 2026-01-28
**参照**: data/checkpoints/phase_checklist.json
