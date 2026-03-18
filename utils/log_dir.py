from pathlib import Path
import shutil

def realocate_logfile():
    """Realoca a .log para dentro do diretório logs/"""

    path_log = Path("logs")

    for log_file in Path(".").glob(f"*.log"):
        shutil.move(log_file.absolute(), path_log)
