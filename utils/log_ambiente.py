import subprocess, logging
from pathlib import Path

logger = logging.getLogger(__name__)

def save_environment_info():
    """Salva um log detalhando o ambiente conda e as versões das ferramentas dele."""
    
    path_log = Path("logs/environment_snapshot.log")
    
    with open(path_log, "w") as f:
        subprocess.run(["conda", "list"], stdout=f)
    
    logger.info(f"Versões de ambiente salvas em {path_log.absolute()}")

