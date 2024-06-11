# 2024 人工智慧概論 Final Project

Fine-tune ChatGPT 以生成吸引人的影片標題。

### 主要程式入口

- `preprocess.py`：用於生成 fine-tuning 的數據集（`.jsonl`）
- `test.py`：用於生成測試的標題，包括未 fine-tuned、已 fine-tuned 和原始 YouTube 影片標題
- `generate.py`：用於生成標題，支援輸入格式音檔（`.mp3`）或是字幕檔（`.srt`）

### 使用方式

建立 Python 虛擬環境並啟用（可忽略此步驟）。
```
python -m venv venv
. venv/bin/activate
```

安裝套件。
```
pip install -r requirements.txt
```

將以下資訊寫入 `.env`。
```
API_KEY=<你的 ChatGPT API Key>
FINE_TUNED_MODEL_NAME=<Fine-tuned 完成的模型名稱>
```

然後就可以用 `generate.py` 產生標題，我們支援音檔（.mp3）或是字幕檔（.srt）作為輸入。
```
python generate.py <音檔/字幕檔> -n 3 -t 驚嘆 疑問
```

### 準備訓練資料

```
python preprocess.py <訓練用 metadata 檔案>
```

備註：可以使用 `utils/parse.js` 來獲取目標 YouTube 影片的相關資料。

### 比較模型和原標題

```
python test.py <測試用 metadata 檔案>
```

### 使用模型

- GPT-3.5 Turbo
- Jingmiao/whisper-small-zh_tw (fine-tuned openai/whisper-small)