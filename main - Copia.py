
from scripts.importar_extrato import importar_extratos
from scripts.categorizar_ml import categorizar_transacoes_ml
from scripts.analise import resumo_por_categoria, saldo_mensal

df = importar_extratos()

print("\n🔍 Transações carregadas:")
print(df.head())

if df.empty:
    print("\n⚠️ Nenhuma transação encontrada.")
else:
    df = categorizar_transacoes_ml(df)

    print("\n📊 Resumo por Categoria:")
    print(resumo_por_categoria(df))

    print("\n📈 Evolução do Saldo Mensal:")
    print(saldo_mensal(df))
