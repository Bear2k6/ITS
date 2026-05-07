import os
import time

# ======================================================
# LOG DIR
# ======================================================
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "system.log")


# ======================================================
# WRITE LOG
# ======================================================
def log(message):

    try:

        timestamp = time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"[{timestamp}] {message}\n"
            )

    except Exception as e:

        print("LOGGER ERROR:", e)