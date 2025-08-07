
import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Criar pasta modelo se não existir
os.makedirs("modelo", exist_ok=True)

# Leitura com fallback de encoding e separador ;
try:
    df = pd.read_csv("categorias_treinamento_exemplo.csv", sep=";", encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv("categorias_treinamento_exemplo.csv", sep=";", encoding="latin1")

# Garantir que colunas são texto
df["descricao"] = df["descricao"].astype(str)
df["transacao"] = df["transacao"].astype(str)

# Criar campo de texto para vetorização
df["texto"] = df["descricao"].str.lower() + " " + df["transacao"].str.lower()

# Filtrar linhas válidas
df = df[df["categoria"].notnull()]

# Vetorização
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["texto"])
y = df["categoria"]

# Treinamento com RandomForest
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X, y)

# Salvar arquivos
joblib.dump(modelo, "modelo/modelo_categorizacao_financeira.pkl")
joblib.dump(vectorizer, "modelo/vetor_tfidf.pkl")

print("✅ Modelo RandomForest e vetor salvos na pasta 'modelo/'")
