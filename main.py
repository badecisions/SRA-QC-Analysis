
from utils import create_directories, conda_verify, verify_valid_id
from modules import sra_downloader
import sys
from argparse import ArgumentParser

# configurando o parser
parser = ArgumentParser(description="Pipeline para o Download, Verificação e Limpeza de arquivos SRA.")

parser.add_argument("--sra", required=True,
                    help="IDs de acesso do SRA", type=str, nargs="+")
parser.add_argument("--outdir", default="results",
                    help="Diretório onde os resultados serão salvos (Padrão: results/)")
parser.add_argument("--data", default="data",
                    help="Diretório onde os dados, brutos e processados, serão salvos (Padrão: data/)")

args = parser.parse_args()

# verificando diretórios e instalação do conda
create_directories(args.outdir, args.data)

conda_verify()

# recebe, verifica e baixa os SRA de acordo com os IDs do user
sra_user_ids = args.sra

valid_ids = verify_valid_id(sra_ids=sra_user_ids)

down_sra = sra_downloader(sra_ids=valid_ids, download_path=args.data)