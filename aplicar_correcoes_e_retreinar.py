
import pandas as pd
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# 1. Atualizar categorias_treinamento_exemplo.csv
nome_excel = "relatorio_financeiro_corrigido.xlsx"
csv_treinamento = "categorias_treinamento_exemplo.csv"

# Leitura do Excel com correções
df_corrigido = pd.read_excel(nome_excel, sheet_name="Transacoes")
df_corrigido = df_corrigido[df_corrigido["categoria_corrigida"].notnull() & (df_corrigido["categoria_corrigida"] != "")]
df_corrigido = df_corrigido[["descricao", "transacao", "categoria_corrigida"]].rename(columns={"categoria_corrigida": "categoria"})

# Leitura do dataset existente
try:
    df_existente = pd.read_csv(csv_treinamento, sep=";", encoding="utf-8")
except UnicodeDecodeError:
    df_existente = pd.read_csv(csv_treinamento, sep=";", encoding="latin1")

# Combinar e remover duplicatas
df_final = pd.concat([df_existente, df_corrigido], ignore_index=True).drop_duplicates()
df_final.to_csv(csv_treinamento, sep=";", index=False, encoding="utf-8")
print("✅ Correções aplicadas ao arquivo de treinamento.")

# 2. Reentreinar o modelo com os dados atualizados
df_final["descricao"] = df_final["descricao"].astype(str)
df_final["transacao"] = df_final["transacao"].astype(str)
df_final["texto"] = df_final["descricao"].str.lower() + " " + df_final["transacao"].str.lower()
df_final = df_final[df_final["categoria"].notnull()]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df_final["texto"])
y = df_final["categoria"]

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X, y)

# Garantir pasta
os.makedirs("modelo", exist_ok=True)
joblib.dump(modelo, "modelo/modelo_categorizacao_financeira.pkl")
joblib.dump(vectorizer, "modelo/vetor_tfidf.pkl")

print("✅ Modelo reentreinado e salvo com sucesso.")
