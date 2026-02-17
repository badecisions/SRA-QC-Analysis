from pathlib import Path
import subprocess

def run_multiqc(result_path:str):
    """Gera a partir do MultiQC um arquivo único para visualização de alterações nos SRAs."""

    output_dir = Path(result_path) / "04_multiqc"
    
    commmand_multiqc = ["multiqc", result_path, "-o", output_dir]

    multiqc = subprocess.run(commmand_multiqc, capture_output=True, text=True)

    if multiqc.returncode != 0:
        print(f"ERRO no MULTIQC")
        print(multiqc.stderr)
    else:
        print(f"Arquivo MULTIQC gerado: {output_dir.absolute()}")
