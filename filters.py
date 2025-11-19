
from formatters import normalizar_mes, ordenar_mes

def filtrar_cascata(df, empresas_sel, anos_sel, meses_sel, projetos_sel, mapa_meses):
    """Filtra opções em cascata - retorna apenas opções válidas"""

    # Garante que são listas
    empresas_sel = empresas_sel if isinstance(empresas_sel, list) else []
    anos_sel = anos_sel if isinstance(anos_sel, list) else []
    meses_sel = meses_sel if isinstance(meses_sel, list) else []
    projetos_sel = projetos_sel if isinstance(projetos_sel, list) else []

    df_filtrado = df.copy()

    # Aplica filtro de empresa
    if empresas_sel:
        df_filtrado = df_filtrado[df_filtrado['Empresa'].isin(empresas_sel)]

    colunas_data = [c for c in df.columns if c not in ['Empresa', 'Projeto', 'Categoria']]

    # Aplica filtro de ano/mês
    if anos_sel or meses_sel:
        colunas_validas = []
        for col in colunas_data:
            partes = col.split('/')
            if len(partes) == 2:
                mes_nome = normalizar_mes(partes[0])
                ano = partes[1].strip()

                ano_ok = not anos_sel or ano in anos_sel
                mes_ok = not meses_sel or mes_nome in meses_sel

                if ano_ok and mes_ok:
                    colunas_validas.append(col)

        if colunas_validas:
            df_filtrado = df_filtrado[df_filtrado[colunas_validas].notna().any(axis=1)]

    # Aplica filtro de projeto
    if projetos_sel:
        # Remove projetos inválidos da seleção
        projetos_sel = [p for p in projetos_sel if p in df_filtrado['Projeto'].values]
        if projetos_sel:
            df_filtrado = df_filtrado[df_filtrado['Projeto'].isin(projetos_sel)]

    # Extrai opções disponíveis após filtros
    projetos_disp = sorted([p for p in df_filtrado['Projeto'].dropna().unique().tolist() if str(p).strip()])
    categorias_disp = sorted([c for c in df_filtrado['Categoria'].dropna().unique().tolist() if str(c).strip()])

    # Extrai meses disponíveis
    meses_disp = set()
    if anos_sel:
        for col in colunas_data:
            partes = col.split('/')
            if len(partes) == 2 and partes[1].strip() in anos_sel:
                meses_disp.add(normalizar_mes(partes[0]))
    else:
        for col in colunas_data:
            partes = col.split('/')
            if len(partes) == 2:
                meses_disp.add(normalizar_mes(partes[0]))

    meses_lista = sorted(list(meses_disp), key=ordenar_mes)

    return projetos_disp, categorias_disp, meses_lista
