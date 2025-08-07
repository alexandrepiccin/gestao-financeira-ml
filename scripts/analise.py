
def resumo_por_categoria(df):
    resumo = df.groupby("categoria")["valor"].sum().sort_values()
    return resumo

def saldo_mensal(df):
    import pandas as pd
    df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
    df['ano_mes'] = df['data'].dt.to_period("M")
    return df.groupby('ano_mes')["valor"].sum()
