
from utils import directories_verify, conda_verify
from modules.downloader import verify_name_run
import sys

# verificando diretórios e instalação do conda
directories_verify()

conda_verify()

# recebe, verifica e baixa os SRA de acordo com os IDs do user
sra_user_ids = sys.argv[1:]

valid_ids = verify_name_run(sra_ids=sra_user_ids)
