
from utils import create_directories, conda_verify, verify_valid_id, check_layout_file, save_environment_info, realocate_logfile, id_or_file
from modules import sra_decompress, prefetch_run, quality_control, trimm_files, run_multiqc
import logging
from argparse import ArgumentParser
from datetime import datetime

logger = logging.getLogger(__name__)

def main():
    # config do arquivo de log
    log_filename = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        filename=log_filename,
        filemode="w",
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )

    # configurando o parser
    parser = ArgumentParser(description="Pipeline para o Download, Verificação e Limpeza de arquivos SRA.")

    parser.add_argument("--sra",
                        help="IDs de acesso do SRA", type=str, nargs="+")
    parser.add_argument("-o", "--outdir", default="results",
                        help="Diretório onde os resultados serão salvos (Padrão: results/)")
    parser.add_argument("-d", "--data", default="data",
                        help="Diretório onde os dados, brutos e processados, serão salvos (Padrão: data/)")
    parser.add_argument("-t", "--threads", default=4, type=int,
                        help="Quantos threads do processador serão utilizadas (Padrão: 4)")
    parser.add_argument("-f", "--file", type=str,
                        help="Arquivo .txt contendo uma lista de IDs (um por linha)")

    args = parser.parse_args()

    logger.info("Pipeline iniciado.")
    logger.info(f"Argumentos: {args}")

    try:
        # criando os diretórios
        logger.info(f"Criando os diretórios")
        create_directories(args.outdir, args.data)

        # verificando o conda
        logger.info(f"Verificando a instalação do CONDA")
        conda_verify()
        save_environment_info()

        # recebe, verifica e baixa os SRA de acordo com os IDs do user
        sra_user_ids = id_or_file(sra_file=args.file, sra_lista=args.sra)

        logger.info(f"Validando os IDs")
        valid_ids = verify_valid_id(sra_ids=sra_user_ids)

        logger.info(f"Iniciando o download dos SRAs validados")
        down_sra = prefetch_run(sra_ids=valid_ids, download_path=args.data)

        logger.info(f"Iniciando descompressão dos SRAs")
        ready_sra = sra_decompress(sra_ids=down_sra, download_path=args.data, num_threads=args.threads)

        # separando os tipos de arquivos de sequenciamento por layout
        logger.info(f"Separando os arquivos por layout")
        paired_id, single_id = check_layout_file(download_path=args.data, sra_ids=ready_sra)

        # rodando o fastqc nos arquivos raw
        print("\nFASTQC RAW FILES")
        logger.info(f"FastQC RAW FILES")
        quality_control(data_path=args.data, results_path=args.outdir, threads=args.threads, raw=True, sra_ids=ready_sra)

        # passa os .fastqc pelo fastp para limpeza dos dados
        print("\nRUNNING FASTP")
        logger.info(f"Iniciando a limpeza com o Fastp")
        trimm_files(data_path=args.data, results_path=args.outdir, sra_ids=paired_id, paired_end=True, threads=args.threads)
        trimm_files(data_path=args.data, results_path=args.outdir, sra_ids=single_id, paired_end=False, threads=args.threads)

        # rodando o fastqc nos arquivos processed
        print("\nFASTQC PROCESSED FILES")
        logger.info(f"FASTQC PROCESSED FILES")
        quality_control(data_path=args.data, results_path=args.outdir, threads=args.threads, raw=False, sra_ids=ready_sra)

        # compilando todos os relatórios com o multiqc
        print("\nRUNNINNG MULTIQC")
        logger.info(f"Compilando os relatórios com o MultiQC")
        run_multiqc(args.outdir)
        print(f"\n\nPipeline FINALIZADO!")

    except Exception as e:
        logger.exception(f"Erro inesperado: {e}")
        raise
    finally:
        # colocando o .log no dir logs/
         realocate_logfile()

if __name__ == "__main__":
    main()