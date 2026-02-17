from pathlib import Path
import shutil

def realocate_logfile():
    """Realoca a .log para dentro do diretório logs/"""

    path_log = Path("logs")

    for i in Path(".").glob(f"*.log"):
        shutil.move(i.absolute(), path_log)
