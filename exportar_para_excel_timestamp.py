
import pandas as pd
import os
import sys
from datetime import datetime
from scripts.importar_extrato import importar_extratos
from scripts.categorizar_ml import categorizar_transacoes_ml
from scripts.analise import resumo_por_categoria, saldo_mensal

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# Importar e classificar
df = importar_extratos()
df = categorizar_transacoes_ml(df)

# Garantir coluna de data formatada
df["data"] = pd.to_datetime(df["data"], errors="coerce", dayfirst=True)
df = df[df["data"].notnull()]
df["ano_mes"] = df["data"].dt.to_period("M").astype(str)

# Adicionar coluna para correção manual
df["categoria_corrigida"] = ""

# Resumo
resumo = resumo_por_categoria(df).to_frame("valor").reset_index()
mensal = saldo_mensal(df).to_frame("valor").reset_index()

# Nome com timestamp
datahora = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"relatorio_financeiro_{datahora}.xlsx"

# Gerar planilha com múltiplas abas
with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Transacoes", index=False)
    resumo.to_excel(writer, sheet_name="Resumo_Categorias", index=False)
    mensal.to_excel(writer, sheet_name="Saldo_Mensal", index=False)

print(f"✅ Relatório com coluna de correção exportado para: {output_path}")
