#!/bin/bash

# Verificação de argumentos e erros
set -eu

# Coletando os ID e colocando em um array
ARQS_SRA=("$@")

# Organizando os caminhos
DIR_RAW="1-raw_data"
DIR_QC="2-qc_reports"
DIR_TRIM="3-trimmed_data"

# Organizando os arquivos de input e output
echo "[1/6] Criando os diretórios"
mkdir -p $DIR_RAW $DIR_QC $DIR_TRIM

# Loop para download dos SRAs
echo -e "\n[2/6] Download dos SRAs"
for ID in "${ARQS_SRA[@]}"
do
    echo "Baixando $ID"
    fastq-dump --gzip "$ID" -O $DIR_RAW
done

# Raw data FastQC
echo -e "\n[3/6] Gerando o relatório QC dos arquivos RAW"
fastqc ${DIR_RAW}/*.fastq.gz -O $DIR_QC

# Trimando os dados
echo -e "\n[4/6] Limpando os reads de baixa qualidade e removendo adaptadores"
for ID in "${ARQS_SRA[@]}"
do
    echo -e "\n Triando o arquivo $ID"
    trim_galore "${DIR_RAW}/${ID}.fastq.gz" -o $DIR_TRIM
done

# Trimmed data FastQC
echo -e "\n[5/6] Gerando relatório dos arquivos triados"
fastqc ${DIR_TRIM}/*fq.gz -o $DIR_QC

# Unindo os relatórios
echo -e "\n[6/6] Unindo os relatórios"
multiqc $DIR_QC -o $DIR_QC

echo ""
echo "Pipeline finalizado!" 
echo "O relatório está em ${DIR_QC}/multiqc_report.html"