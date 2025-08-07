
import pandas as pd
import os
from config import CAMINHO_EXTRATOS
import unicodedata

def normalizar(texto):
    if pd.isna(texto):
        return ""
    return (
        unicodedata.normalize("NFKD", str(texto))
        .encode("ascii", errors="ignore")
        .decode("utf-8")
        .lower()
    )

def linha_eh_cabecalho_repetido(linha):
    termos_indesejados = ["categoria", "transacao", "transação", "descricao", "descrição"]
    return any(normalizar(str(valor)) in termos_indesejados for valor in linha)

def importar_extratos():
    arquivos = [arq for arq in os.listdir(CAMINHO_EXTRATOS) if arq.endswith(".csv")]
    df_total = pd.DataFrame()

    for arquivo in arquivos:
        caminho = os.path.join(CAMINHO_EXTRATOS, arquivo)
        try:
            try:
                df = pd.read_csv(caminho, sep=";", encoding="utf-8", engine="python", skip_blank_lines=True)
            except UnicodeDecodeError:
                df = pd.read_csv(caminho, sep=";", encoding="latin1", engine="python", skip_blank_lines=True)

            df.columns = [col.strip().lower() for col in df.columns]

            if "descricao" in df.columns:
                df["descricao"] = df["descricao"].astype(str)
                df = df[df["descricao"].apply(lambda x: "saldo diario" not in normalizar(x))]

            df = df[~df.apply(linha_eh_cabecalho_repetido, axis=1)]

            if "valor" in df.columns:
                df["valor"] = df["valor"].astype(str).apply(
                    lambda x: x.replace(".", "").replace(",", ".") if "," in x else x
                )
                df["valor"] = pd.to_numeric(df["valor"], errors='coerce')

            df_total = pd.concat([df_total, df], ignore_index=True)
        except Exception as e:
            print(f"Erro ao ler {arquivo}: {e}")

    df_total.drop_duplicates(inplace=True)
    return df_total
