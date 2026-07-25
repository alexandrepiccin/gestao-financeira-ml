
import subprocess
import glob
import os
from pathlib import Path

# Caminho do diretório do projeto
projeto_path = Path(__file__).parent.resolve()

# Passo 1: Treinar/atualizar o modelo com base no CSV de categorias
print("📘 Treinando o modelo com base no CSV de categorias...")
subprocess.run(["python", "treinar_e_salvar_modelo.py"], cwd=projeto_path, check=True)

# Passo 2: Importar extratos, categorizar e exportar Excel com timestamp
print("📦 Gerando relatório categorizado...")
subprocess.run(["python", "exportar_para_excel_timestamp.py"], cwd=projeto_path, check=True)

# Passo 3: Localizar o relatório mais recente gerado
arquivos_excel = sorted(
    glob.glob(str(projeto_path / "relatorio_financeiro_*.xlsx")),
    key=os.path.getmtime,
    reverse=True,
)

if not arquivos_excel:
    print("❌ Nenhum arquivo Excel encontrado.")
    exit(1)

ultimo_excel = arquivos_excel[0]
print(f"📁 Último arquivo encontrado: {os.path.basename(ultimo_excel)}")

# Passo 4: Iniciar o dashboard Streamlit com o relatório mais recente
print("🚀 Iniciando o dashboard...")
subprocess.run(
    ["streamlit", "run", "dashboard_financeiro.py", "--", "--file", ultimo_excel],
    cwd=projeto_path,
)
