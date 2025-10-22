# Imagem base - Ubuntu 24.04.3 LTS
FROM ubuntu:24.04.3

# Evita instaladores interativos
ENV DEBIAN_FRONTEND=noninteractive

# Dependências básicas
RUN apt-get update && apt-get install -y wget ca-certificades && rm -rf /var/lib/apt/lists/*

# Instalando o Mamba no /opt e incluindo no PATH
RUN wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh" -O /tmp/mamba.sh && \
	sh /tmp/mamba.sh -b -p /opt/mambaforge && \
	rm /tmp/mamba.sh
ENV PATH="/opt/mambaforge/bin:${PATH}"

# Criando o ambiente mamba com as ferramentas FastQC, MultiQC, Trimgalore e SRA-Tools
RUN mamba create -n qc_env -c conda-forge -c bioconda -y \
	sra-tools \
	fastqc \
	multiqc \
	trim-galore

# Definindo o comando padrão ao entrar no contêiner
CMD ["conda", "run", "-n", "qc_env", "/bin/bash"]
