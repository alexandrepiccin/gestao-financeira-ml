
import os
import subprocess
import time
import glob
from pathlib import Path

# Caminho do diretório do projeto
projeto_path = Path(__file__).parent.resolve()

# Passo 0: Treinar ou atualizar o modelo
print("📘 Treinando o modelo com base no CSV de categorias...")
subprocess.run(["python", "treinar_e_salvar_modelo.py"], cwd=projeto_path)

# Passo 1: Rodar exportar_para_excel_timestamp.py
print("📦 Executando exportar_para_excel_timestamp.py para salvar Excel com timestamp...")
subprocess.run(["python", "exportar_para_excel_timestamp.py"], cwd=projeto_path)

# Aguardar para garantir que o arquivo seja salvo
time.sleep(2)

# Passo 2: Localizar o arquivo mais recente gerado
arquivos_excel = sorted(glob.glob(str(projeto_path / "relatorio_financeiro_*.xlsx")), key=os.path.getmtime, reverse=True)

if not arquivos_excel:
    print("❌ Nenhum arquivo Excel encontrado.")
    exit(1)

ultimo_excel = arquivos_excel[0]
print(f"📁 Último arquivo encontrado: {os.path.basename(ultimo_excel)}")

# Passo 3: Iniciar Streamlit com o dashboard corrigido
print("🚀 Iniciando Streamlit com o relatório...")
subprocess.Popen(
    ["streamlit", "run", "dashboard_financeiro_com_auto_load.py", "--", "--file", ultimo_excel],
    cwd=projeto_path,
)
