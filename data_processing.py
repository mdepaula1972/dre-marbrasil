
import pandas as pd
from formatters import normalizar_mes

def parse_csv(file):
    """Lê CSV com limpeza completa de dados"""
    if file is None:
        return None

    print(f"\n=== LEITURA DO CSV ===")

    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-8-sig']
    delimitadores = [';', ',']

    for enc in encodings:
        for delim in delimitadores:
            try:
                df = pd.read_csv(file.name, delimiter=delim, encoding=enc)

                # Limpa nomes das colunas
                df.columns = df.columns.str.strip().str.replace('"', '').str.replace("'", '')

                # Remove colunas completamente vazias
                df = df.loc[:, df.columns.str.strip() != '']

                # Valida colunas obrigatórias
                if 'Empresa' in df.columns and 'Projeto' in df.columns and 'Categoria' in df.columns:

                    print(f"✅ Encoding: {enc}, Delimitador: '{delim}'")

                    # Remove linhas com Projeto ou Categoria vazios
                    antes = len(df)
                    df = df[df['Projeto'].notna()]
                    df = df[df['Categoria'].notna()]
                    df = df[df['Projeto'].astype(str).str.strip() != '']
                    df = df[df['Categoria'].astype(str).str.strip() != '']
                    depois = len(df)

                    if antes != depois:
                        print(f"⚠️ Removidas {antes - depois} linhas vazias")

                    # Normaliza textos
                    df['Projeto'] = df['Projeto'].astype(str).str.strip().str.title()
                    df['Empresa'] = df['Empresa'].astype(str).str.strip()
                    df['Categoria'] = df['Categoria'].astype(str).str.strip()

                    print(f"✅ {len(df)} linhas | {len(df['Projeto'].unique())} projetos únicos")

                    return df

            except Exception as e:
                continue

    print("❌ Não foi possível ler o CSV")
    return None

def extrair_anos_meses(df):
    """Extrai anos e meses das colunas do CSV"""
    colunas_data = [c for c in df.columns if c not in ['Empresa', 'Projeto', 'Categoria']]
    anos = set()
    mapa_meses = {}

    for col in colunas_data:
        partes = col.split('/')
        if len(partes) == 2:
            mes_nome = partes[0].strip()
            ano = partes[1].strip()
            anos.add(ano)
            # Força normalização (ago -> Ago, SET -> Set)
            mapa_meses[col] = normalizar_mes(mes_nome)

    return sorted(list(anos)), mapa_meses
