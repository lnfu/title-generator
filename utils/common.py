import os

TITLE_TYPE_DESCRIPTIONS = {
    "驚嘆": "驚嘆語句",
    "疑問": "疑問語句",
    "項目數": "影片中主要內容列表的項目數量",
    "數據": "影片提到的重要數據",
    "轉折": "轉折句",
}


def ensureDirectoryExists(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
