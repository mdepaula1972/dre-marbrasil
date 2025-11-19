
import pandas as pd
from config import ESTRUTURA_DRE, METRICAS_CARDS
from formatters import format_currency, normalizar_mes

def calcular_dre(df, empresas_filtro, anos_filtro, meses_filtro, projetos_filtro, categorias_filtro, mapa_meses):
    """Calcula o DRE completo com valores por mês"""
    if df is None:
        return None, None, {}
    
    df_filtrado = df.copy()
    
    # Aplica filtros
    if empresas_filtro:
        df_filtrado = df_filtrado[df_filtrado['Empresa'].isin(empresas_filtro)]
    if projetos_filtro:
        df_filtrado = df_filtrado[df_filtrado['Projeto'].isin(projetos_filtro)]
    if categorias_filtro:
        df_filtrado = df_filtrado[df_filtrado['Categoria'].isin(categorias_filtro)]
    
    colunas_fixas = ['Empresa', 'Projeto', 'Categoria']
    colunas_meses = [c for c in df_filtrado.columns if c not in colunas_fixas]
    
    # Filtra colunas de meses
    meses_filtrados = []
    for col in colunas_meses:
        partes = col.split('/')
        if len(partes) == 2:
            mes_nome = normalizar_mes(partes[0])
            ano = partes[1].strip()
            
            ano_ok = not anos_filtro or ano in anos_filtro
            mes_ok = not meses_filtro or mes_nome in meses_filtro
            
            if ano_ok and mes_ok:
                meses_filtrados.append(col)
    
    colunas_meses = meses_filtrados if meses_filtrados else colunas_meses
    
    # Converte para numérico
    for col in colunas_meses:
        df_filtrado[col] = pd.to_numeric(df_filtrado[col], errors='coerce').fillna(0)
    
    df_filtrado['Total'] = df_filtrado[colunas_meses].sum(axis=1)
    
    # Debug
    debug_categorias = df_filtrado.groupby('Categoria')['Total'].sum().reset_index()
    debug_categorias.columns = ['Categoria', 'Total']
    debug_categorias['Total (R$)'] = debug_categorias['Total'].apply(format_currency)
    debug_categorias = debug_categorias.sort_values('Total', ascending=False)
    
    # ========================================
    # CALCULA VALORES POR CATEGORIA E POR MÊS
    # ========================================
    
    cat_valores_total = {}
    cat_valores_por_mes = {}
    
    for cat in df_filtrado['Categoria'].unique():
        df_cat = df_filtrado[df_filtrado['Categoria'] == cat]
        
        # Total
        cat_valores_total[cat] = df_cat['Total'].sum()
        
        # Por mês
        cat_valores_por_mes[cat] = {}
        for col_mes in colunas_meses:
            cat_valores_por_mes[cat][col_mes] = df_cat[col_mes].sum()
    
    # Valores base para fórmulas
    servicos_base_total = cat_valores_total.get('Serviços', 0)
    consorcios_valor_total = cat_valores_total.get('Consórcios - a contemplar', 0)
    
    servicos_base_por_mes = cat_valores_por_mes.get('Serviços', {})
    consorcios_por_mes = cat_valores_por_mes.get('Consórcios - a contemplar', {})
    
    # ========================================
    # CALCULA VALORES POR LINHA (TOTAL E POR MÊS)
    # ========================================
    
    valores_total = {}
    valores_por_mes = {}
    
    for item in ESTRUTURA_DRE:
        tipo = item['tipo']
        titulo = item['titulo']
        
        if tipo == 'linha':
            categorias = item.get('categorias', [])
            
            # Total
            valor_total = sum(cat_valores_total.get(cat, 0) for cat in categorias)
            valores_total[titulo] = valor_total
            
            # Por mês
            valores_por_mes[titulo] = {}
            for col_mes in colunas_meses:
                valor_mes = sum(cat_valores_por_mes.get(cat, {}).get(col_mes, 0) for cat in categorias)
                valores_por_mes[titulo][col_mes] = valor_mes
        
        elif tipo == 'linha_calc':
            formula = item.get('formula', '')
            if formula == 'servicos_menos_consorcios':
                # Total
                valores_total[titulo] = servicos_base_total - consorcios_valor_total
                
                # Por mês
                valores_por_mes[titulo] = {}
                for col_mes in colunas_meses:
                    serv_mes = servicos_base_por_mes.get(col_mes, 0)
                    cons_mes = consorcios_por_mes.get(col_mes, 0)
                    valores_por_mes[titulo][col_mes] = serv_mes - cons_mes
            else:
                valores_total[titulo] = 0
                valores_por_mes[titulo] = {col_mes: 0 for col_mes in colunas_meses}
    
    # ========================================
    # CÁLCULOS DOS TOTALIZADORES
    # ========================================
    
    receita_operacional = valores_total.get("Receita Bruta de Vendas", 0)
    receita_indireta = valores_total.get("Receitas Indiretas", 0)
    total_entradas = receita_operacional + receita_indireta
    
    outras_receitas = valores_total.get("Outras Receitas", 0)
    receitas_fin = valores_total.get("Receitas Financeiras", 0)
    honorarios = valores_total.get("Honorários", 0)
    juros = valores_total.get("Juros e Devoluções", 0)
    outras_entradas_total = outras_receitas + receitas_fin + honorarios + juros
    
    impostos = valores_total.get("Impostos", 0)
    provisao = valores_total.get("Provisão IRPJ e CSSL Trimestral", 0)
    total_impostos = impostos + provisao
    
    mei_oper = valores_total.get("Prestador de serviço PJ MEI Operacional", 0)
    terc = valores_total.get("Terceirização de Mão de Obra", 0)
    clts = valores_total.get("CLTs", 0)
    custos_serv = valores_total.get("Custo dos Serviços Prestados", 0)
    prev = valores_total.get("M. Preventiva Climatização B2G", 0)
    corr = valores_total.get("M. Corretiva Climatização B2G", 0)
    outros_custos = valores_total.get("Outros Custos", 0)
    total_custos = mei_oper + terc + clts + custos_serv + prev + corr + outros_custos
    
    mei_adm = valores_total.get("Prestador de serviço PJ MEI Administrativo", 0)
    mei_ti = valores_total.get("Prestador de serviço PJ MEI TI", 0)
    desp_adm = valores_total.get("Despesas Administrativas", 0)
    desp_vend = valores_total.get("Despesas de Vendas e Marketing", 0)
    desp_fin = valores_total.get("Despesas Financeiras", 0)
    outros_trib = valores_total.get("Outros Tributos", 0)
    desp_event = valores_total.get("Despesas Eventuais", 0)
    desp_var = valores_total.get("Despesas Variáveis", 0)
    interm = valores_total.get("Intermediação de Negócios", 0)
    total_despesas = mei_adm + mei_ti + desp_adm + desp_vend + desp_fin + outros_trib + desp_event + desp_var + interm
    
    consorcios = valores_total.get("Consórcios a contemplar", 0)
    servicos = valores_total.get("Serviços", 0)
    ativos = valores_total.get("Ativos", 0)
    total_investimentos = consorcios + servicos + ativos
    
    total_saidas = total_impostos + total_custos + total_despesas + total_investimentos
    
    # RESULTADO (mantendo suas correções)
    resultado = total_entradas + ativos + outras_entradas_total - total_saidas
    fcl = resultado - ativos
    
    # Percentuais
    perc_lucro_operacional = (resultado / total_entradas * 100) if total_entradas != 0 else 0
    perc_fcl = (fcl / total_entradas * 100) if total_entradas != 0 else 0
    
    # Mútuo e Dividendos
    mutuo_entradas = sum(cat_valores_total.get(cat, 0) for cat in ["Mútuo - Entradas"])
    mutuo_saidas = sum(cat_valores_total.get(cat, 0) for cat in ["Mútuo - Saídas"])
    dividendos = sum(cat_valores_total.get(cat, 0) for cat in ["Distribuição de Dividendos", "Dividendos"])
    
    # ========================================
    # NOVOS CARDS - BUSCAR DOS VALORES DO DRE
    # ========================================
    
    corretivas = valores_total.get("M. Corretiva Climatização B2G", 0)
    preventivas = valores_total.get("M. Preventiva Climatização B2G", 0)
    pj_operacional = valores_total.get("Prestador de serviço PJ MEI Operacional", 0)
    pj_administrativo = (
        valores_total.get("Prestador de serviço PJ MEI Administrativo", 0) +
        valores_total.get("Prestador de serviço PJ MEI TI", 0)
    )
    clts_card = valores_total.get("CLTs", 0)
    terceirizacao = valores_total.get("Terceirização de Mão de Obra", 0)
    pessoal = (
        valores_total.get("Prestador de serviço PJ MEI Administrativo", 0) +
        valores_total.get("Prestador de serviço PJ MEI TI", 0) +
        valores_total.get("Prestador de serviço PJ MEI Operacional", 0) +
        valores_total.get("CLTs", 0) +
        valores_total.get("Terceirização de Mão de Obra", 0)
    )
    
    # ========================================
    # DICIONÁRIO DE MÉTRICAS PARA CARDS
    # ========================================
    
    metricas_cards = {
        'resultado': {'valor': resultado, 'titulo': 'Resultado', 'icon': '🎯', 'destaque': 'hero'},
        'total_entradas': {'valor': total_entradas, 'titulo': 'Receitas Operacionais', 'icon': '💰'},
        'outras_entradas': {'valor': outras_entradas_total, 'titulo': 'Outras Entradas', 'icon': '💵'},
        'total_impostos': {'valor': total_impostos, 'titulo': 'Impostos', 'icon': '🏛️'},
        'total_custos': {'valor': total_custos, 'titulo': 'Custos', 'icon': '⚙️'},
        'total_despesas': {'valor': total_despesas, 'titulo': 'Despesas Rateadas', 'icon': '📊'},
        'total_investimentos': {'valor': total_investimentos, 'titulo': 'Investimentos', 'icon': '💼'},
        'total_saidas': {'valor': total_saidas, 'titulo': 'Total Saídas', 'icon': '📉'},
        'fcl': {'valor': fcl, 'titulo': 'FCL', 'icon': '💎', 'destaque': 'importante'},
        'perc_lucro_operacional': {'valor': perc_lucro_operacional, 'titulo': 'Lucro Operacional', 'tipo': 'percentual', 'icon': '📈', 'destaque': 'importante'},
        'perc_fcl': {'valor': perc_fcl, 'titulo': 'FCL s/ Receita', 'tipo': 'percentual', 'icon': '📊', 'destaque': 'importante'},
        'corretivas': {'valor': corretivas, 'titulo': 'Corretivas', 'icon': '🔧'},
        'preventivas': {'valor': preventivas, 'titulo': 'Preventivas', 'icon': '🛠️'},
        'pessoal': {'valor': pessoal, 'titulo': 'Pessoal', 'icon': '👥'},
        'terceirizacao': {'valor': terceirizacao, 'titulo': 'Terceirização', 'icon': '🤝'},
        'clts_card': {'valor': clts_card, 'titulo': "CLT's", 'icon': '👔'},
        'pj_administrativo': {'valor': pj_administrativo, 'titulo': 'PJ Administrativo', 'icon': '💼'},
        'pj_operacional': {'valor': pj_operacional, 'titulo': 'PJ Operacional', 'icon': '⚙️'},
        'mutuo_entradas': {'valor': mutuo_entradas, 'titulo': 'Mútuo Entradas', 'icon': '➕'},
        'mutuo_saidas': {'valor': mutuo_saidas, 'titulo': 'Mútuo Saídas', 'icon': '➖'},
        'dividendos': {'valor': dividendos, 'titulo': 'Dividendos', 'icon': '💎'},
    }
    
    # ========================================
    # MONTA TABELA COM COLUNAS DE MESES + MÉDIA
    # ========================================
    
    num_meses = len(colunas_meses) if colunas_meses else 1
    
    resultados = []
    for item in ESTRUTURA_DRE:
        tipo_linha = item['tipo']
        titulo = item['titulo']
        
        # Pula itens que vão para cards
        if tipo_linha in ['card', 'card_percentual']:
            continue
        
        if tipo_linha == 'divisor':
            # SEPARADOR REDUZIDO (apenas uma linha)
            linha = {'Descrição': '―'}
            for col_mes in colunas_meses:
                linha[col_mes] = ''
            linha['Total'] = ''
            linha['Média'] = ''
            resultados.append(linha)
            
        elif tipo_linha in ['linha', 'linha_calc']:
            linha = {'Descrição': titulo}
            
            # Adiciona valor de cada mês
            for col_mes in colunas_meses:
                valor_mes = valores_por_mes.get(titulo, {}).get(col_mes, 0)
                linha[col_mes] = format_currency(valor_mes)
            
            # Total
            valor_total = valores_total.get(titulo, 0)
            linha['Total'] = format_currency(valor_total)
            
            # MÉDIA (Total / número de meses)
            media = valor_total / num_meses if num_meses > 0 else 0
            linha['Média'] = format_currency(media)
            
            resultados.append(linha)
    
    df_resultado = pd.DataFrame(resultados)
    
    # Reordena colunas: Descrição, meses, Total, Média
    colunas_ordem = ['Descrição'] + colunas_meses + ['Total', 'Média']
    df_resultado = df_resultado[colunas_ordem]
    
    return df_resultado, debug_categorias, metricas_cards
