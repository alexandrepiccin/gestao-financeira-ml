
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier

# Leitura do CSV com fallback de encoding
try:
    df = pd.read_csv("categorias_treinamento_exemplo.csv", encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv("categorias_treinamento_exemplo.csv", encoding="latin1")

# Pré-processamento
df["descricao"] = df["descricao"].astype(str)
df["texto"] = df["descricao"].str.lower() + " " + df["transacao"].str.lower()
df = df[df["categoria"].notnull()]

# Vetorização
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["texto"])
y = df["categoria"]

# Treinamento
modelo = DecisionTreeClassifier()
modelo.fit(X, y)

# Salvando modelo e vetor
joblib.dump(modelo, "modelo/modelo_categorizacao_financeira.pkl")
joblib.dump(vectorizer, "modelo/vetor_tfidf.pkl")

print("✅ Modelo salvo com sucesso em: modelo/modelo_categorizacao_financeira.pkl")
