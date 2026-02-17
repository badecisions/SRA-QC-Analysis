
from utils import create_directories, conda_verify, verify_valid_id, check_layout_file
from modules import sra_downloader, quality_control, trimm_files
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
parser.add_argument("--threads", default=4, type=int,
                    help="Quantos threads do processador serão utilizadas (Padrão: 4)")


args = parser.parse_args()

# verificando diretórios e instalação do conda
create_directories(args.outdir, args.data)

conda_verify()

# recebe, verifica e baixa os SRA de acordo com os IDs do user
sra_user_ids = args.sra

valid_ids = verify_valid_id(sra_ids=sra_user_ids)

down_sra = sra_downloader(sra_ids=valid_ids, download_path=args.data)

# separando os tipos de arquivos de sequenciamento por layout
paired_id, single_id = check_layout_file(download_path=args.data, sra_ids=down_sra)

# rodando o fastqc nos arquivos raw
print("\nFASTQC RAW FILES")
quality_control(data_path=args.data, results_path=args.outdir, threads=args.threads, raw=True, sra_ids=down_sra)

# passa os .fastqc pelo fastp para limpeza dos dados
print("\nRUNNING FASTP")
trimm_files(data_path=args.data, results_path=args.outdir, sra_ids=paired_id, paried_end=True, threads=args.threads)
trimm_files(data_path=args.data, results_path=args.outdir, sra_ids=single_id, paried_end=False, threads=args.threads)

# rodando o fastqc nos arquivos processed
print("\nFASTQC PROCESSED FILES")
quality_control(data_path=args.data, results_path=args.outdir, threads=args.threads, raw=False, sra_ids=down_sra)