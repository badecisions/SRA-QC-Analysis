from pathlib import Path
import subprocess, logging

logger = logging.getLogger(__name__)

def run_multiqc(result_path:str):
    """Gera a partir do MultiQC um arquivo único para visualização de alterações nos SRAs."""

    output_dir = Path(result_path) / "04_multiqc"
    
    command_multiqc = ["multiqc", result_path, "-o", output_dir]
    
    logger.info(f"MultiQC: Comando {' '.join(map(str, command_multiqc))}")

    multiqc = subprocess.run(command_multiqc, capture_output=True, text=True)

    if multiqc.returncode != 0:
        print(f"ERRO no MULTIQC")
        logger.error("MultiQC: ERRO")
        logger.error(multiqc.stderr)
        print(multiqc.stderr)
    else:
        print(f"Arquivo MULTIQC gerado: {output_dir.absolute()}")
        logger.info(f"MultiQC: Arquivo gerado e disponível em {output_dir.absolute()}")
