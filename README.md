# 2024 人工智慧概論 Final Project

Fine-tune ChatGPT 以生成吸引人的影片標題。

### 主要程式
- `preprocess.py`：用於生成 fine-tuning 的數據集（`.jsonl`）
- `test.py`：用於生成測試的標題，包括未 fine-tuned、已 fine-tuned 和原始 YouTube 影片標題
- `generate.py`：用於生成標題，支援輸入格式音檔（`.mp3`）或是字幕檔（`.srt`）

### 使用方法
