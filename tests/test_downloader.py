from unittest.mock import patch, MagicMock
import pytest
from modules.downloader import prefetch_run, sra_decompress

def test_prefetch_sucesso(tmp_path):
    # verifica que o ID aparece em sucesso_ids

    mock_result = MagicMock()
    mock_result.returncode = 0

    (tmp_path / "logs").mkdir()

    with patch("modules.downloader.subprocess.run", return_value = mock_result):
        sucesso_ids = prefetch_run(sra_ids=["SRR48123181"], download_path=tmp_path)

    assert sucesso_ids == ["SRR48123181"], "ERRO: não conseguiu realizar o download do arquivo."

def test_prefetch_falha(tmp_path):
    # verifica que o ID NÃO aparece em sucesso_ids

    mock_falha = MagicMock()
    mock_falha.returncode = 1
    mock_sucesso = MagicMock()
    mock_sucesso.returncode = 0

    (tmp_path / "logs").mkdir()

    with patch("modules.downloader.subprocess.run", side_effect = [mock_falha, mock_sucesso]):
            sucesso_ids = prefetch_run(sra_ids=["SRR412412", "SRR9318128"], download_path=tmp_path)

    assert "SRR412412" not in sucesso_ids, "ERRO: não conseguiu lidar com falha no download"
    assert "SRR9318128" in sucesso_ids

def test_prefetch_todos_falham_encerra(tmp_path):
    # verifica sys.exit com pytest.raises(SystemExit)

    mock_result = MagicMock()
    mock_result.returncode = 1

    (tmp_path / "logs").mkdir()

    with patch("modules.downloader.subprocess.run", return_value = mock_result):
        with pytest.raises(SystemExit):
            prefetch_run(sra_ids=[], download_path=tmp_path)

def test_prefetch_ferramenta_ausente(tmp_path):
    # verifica sys.exit quando não encontra ferramenta

    (tmp_path / "logs").mkdir()

    with patch("modules.downloader.subprocess.run", side_effect = FileNotFoundError):
         with pytest.raises(SystemExit):
              prefetch_run(sra_ids=["SRR281281"], download_path=tmp_path)
