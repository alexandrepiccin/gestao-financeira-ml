
import os
import subprocess
import time
import glob
from pathlib import Path

# Caminho do diretório do projeto
projeto_path = Path(__file__).parent.resolve()

# Passo 1: Executar main.py
print("📦 Executando main.py para atualizar os dados...")
subprocess.run(["python", "main.py"], cwd=projeto_path)

# Aguardar alguns segundos para garantir que o arquivo seja salvo
time.sleep(2)

# Passo 2: Encontrar o último arquivo Excel gerado
arquivos_excel = sorted(glob.glob(str(projeto_path / "relatorio_financeiro_*.xlsx")), key=os.path.getmtime, reverse=True)

if not arquivos_excel:
    print("❌ Nenhum arquivo Excel encontrado.")
    exit(1)

ultimo_excel = arquivos_excel[0]
print(f"📁 Último arquivo encontrado: {os.path.basename(ultimo_excel)}")

# Passo 3: Rodar o Streamlit com argumento do arquivo
print("🚀 Iniciando Streamlit com o último relatório...")
subprocess.run(["streamlit", "run", "dashboard_financeiro.py", "--", "--file", ultimo_excel], cwd=projeto_path)
