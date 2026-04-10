"""Legacy backend 用のランタイムパス定義。"""

from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent
DATA_DIR = BACKEND_ROOT / "data"

CHAT_SQLITE_PATH = DATA_DIR / "chat.sqlite"
PARQUET_DATA_DIR = DATA_DIR / "parquet"
LEGACY_CHAT_DUCKDB_PATH = DATA_DIR / "legacy" / "chat.duckdb"
