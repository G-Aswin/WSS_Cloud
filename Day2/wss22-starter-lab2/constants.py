from typing import Final

LOGFILE: Final[str] = "/tmp/wc.log"
N_WORKERS: Final[int] = 10
GLOB: Final[str] = "data/*.txt"
IN: Final[bytes] = b"files"
FNAME: Final[bytes] = b"fname"
COUNT: Final[bytes] = b"count"