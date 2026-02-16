
from utils.directories import directories_verify
from utils.conda_verify import conda_verify
from utils.verify_id import verify_valid_id
import sys
from argparse import ArgumentParser

# configurando o parser
parser = ArgumentParser(description="Pipeline SRA -> QC -> Trim")

parser.add_argument("--sra", required=True,
                    help="ID de acesso do SRA", type=str, nargs="+")
parser.add_argument("--outdir", default="results",
                    help="Pasta onde os resultados serão salvos (Padrão: results/)")

args = parser.parse_args()

# verificando diretórios e instalação do conda
directories_verify(args.outdir)

conda_verify()

# recebe, verifica e baixa os SRA de acordo com os IDs do user
sra_user_ids = args.sra

valid_ids = verify_valid_id(sra_ids=sra_user_ids)
