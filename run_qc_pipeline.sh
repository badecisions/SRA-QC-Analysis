#!/bin/bash

# Verificação de argumentos e erros
set -eu

# Coletando o ID e construindo nomes
ARQ_SRA=$1
FILE_RAW="${ARQ_SRA}.fastq.gz"
FILE_TRIMMED="${ARQ_SRA}_trimmed.fq.gz"

# Organizando os caminhos
DIR_RAW="1-raw_data"
DIR_QC="2-qc_reports"
DIR_TRIM="3-trimmed_data"

# Organizando os arquivos de input e output
echo "[1/6] Criando os diretórios"
mkdir -p $DIR_RAW $DIR_QC $DIR_TRIM

# Download do SRA
echo "[2/6] Fazendo o Download do arquivo $FILE_RAW"
fastq-dump --gzip "$ARQ_SRA" -O $DIR_RAW

# Raw data FastQC
echo "[3/6] Gerando o relatório QC do arquivo RAW"
fastqc "$DIR_RAW/$FILE_RAW" -O $DIR_QC

# Trimando os dados
echo "[4/6] Limpando os reads de baixa qualidade e removendo adaptadores"
trim_galore "$DIR_RAW/$FILE_RAW" -o $DIR_TRIM

# Trimmed data FastQC
echo "[5/6] Gerando relatório do $FILE_TRIMMED"
fastqc "$DIR_TRIM/$FILE_TRIMMED" -o $DIR_QC

# Unindo os relatórios
echo "[6/6] Unindo os dois relatórios"
multiqc $DIR_QC -o $DIR_QC

echo ""
echo "Pipeline finalizado!" 
echo "O relatório está em ${DIR_QC}/multiqc_report.html"