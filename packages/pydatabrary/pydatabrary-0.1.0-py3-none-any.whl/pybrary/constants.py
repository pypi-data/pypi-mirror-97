import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VOLUME_SCHEMA_FILE = os.path.join(ROOT_DIR, 'volume.json')

VIDEO_EXTENSIONS = ["webm", "mpg", "mp4",
                    "mov", "mts", "avi",
                    "wmv", "dv"]
AUDIO_EXTENSIONS = ["wav", "aac", "wma", "mp3"]
OPF_EXTENSION = ["opf"]


SUPPORTED_FORMATS = {
    "2": "csv",
    "4": "rtf",
    "5": "png",
    "6": "pdf",
    "7": "doc",
    "8": "odf",
    "9": "docx",
    "10": "xls",
    "11": "ods",
    "12": "xlsx",
    '13': "ppt",
    "14": "odp",
    "15": "pptx",
    "16": "opf",
    "18": "webm",
    "20": "mov",
    "-800": "mp4",
    "22": "avi",
    "23": "sav",
    "24": "wav",
    "19": "mpeg",
    "26": "chat",
    "-700": "jpeg",
    "21": "mts",
    "-600": "mp3",
    "27": "aac",
    "28": "wma",
    "25": "wmv",
    "29": "its",
    "30": "dv",
    "1": "txt",
    "31": "etf"
}
