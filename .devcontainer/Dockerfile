# Imagem base - Ubuntu 24.04 LTS
FROM ubuntu:24.04

# Evita instaladores interativos
ENV DEBIAN_FRONTEND=noninteractive

# Dependências básicas e configurando locale
RUN apt-get update && apt-get install -y \
	wget \
	ca-certificates \
	git \
	locales \
	&& rm -rf /var/lib/apt/lists/* \
	&& sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
	&& locale-gen

# Definindo o locale padrão
ENV LANG en_US.UTF-8

# Instalando o Mamba no /opt e incluindo no PATH
RUN wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh" -O /tmp/mamba.sh && \
	sh /tmp/mamba.sh -b -p /opt/mambaforge && \
	rm /tmp/mamba.sh
ENV PATH="/opt/mambaforge/bin:${PATH}"

# Criando o ambiente mamba com as ferramentas FastQC, MultiQC, Trimgalore, SRA-Tools e ShellCheck
RUN mamba create -n qc_env -c conda-forge -c bioconda -y \
	sra-tools \
	fastqc \
	multiqc \
	trim-galore \
	shellcheck

# Iniciando o mamba para o shell e já abrindo no ambiente
RUN mamba shell init --shell bash --root-prefix /opt/mambaforge/ && \
	echo "mamba activate qc_env" >> /root/.bashrc

# Iniciar o shell
CMD [ "/bin/bash" ]