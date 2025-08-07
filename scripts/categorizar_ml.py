
import pandas as pd
import joblib
import os

# Carregar modelo e vetor
modelo_path = "modelo/modelo_categorizacao_financeira.pkl"
vetor_path = "modelo/vetor_tfidf.pkl"

modelo = joblib.load(modelo_path)
vectorizer = joblib.load(vetor_path)

def categorizar_transacoes_ml(df):
    df["descricao"] = df["descricao"].astype(str)
    if "transacao" not in df.columns:
        df["transacao"] = ""
    df["transacao"] = df["transacao"].astype(str)
    df["texto"] = df["descricao"].str.lower() + " " + df["transacao"].str.lower()
    df["categoria"] = modelo.predict(vectorizer.transform(df["texto"]))
    return df
