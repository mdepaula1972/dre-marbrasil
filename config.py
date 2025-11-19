
# Configurações e Estrutura DRE - Mar Brasil

COLORS = {
    'primary': '#F2911B',
    'secondary': '#F2B807',
    'dark': '#262223',
    'light': '#F2F2F2'
}

MESES_ORDEM = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Itens que vão para CARDS (não aparecem na tabela)
METRICAS_CARDS = [
    'total_entradas',
    'outras_entradas',
    'total_impostos',
    'total_custos',
    'total_despesas',
    'total_investimentos',
    'total_saidas',
    'fcl',
    'perc_lucro',
    'perc_fcl',
    'mutuo_entradas',
    'mutuo_saidas',
    'dividendos'
]

ESTRUTURA_DRE = [
    # ENTRADAS
    {"titulo": "Receita Bruta de Vendas", "tipo": "linha", "categorias": ["Receita Bruta de Vendas"]},
    {"titulo": "Receitas Indiretas", "tipo": "linha", "categorias": ["Receitas Indiretas"]},
    {"titulo": "Total Entradas Operacionais", "tipo": "card", "var": "total_entradas"},
    {"titulo": "", "tipo": "divisor"},

    {"titulo": "Outras Receitas", "tipo": "linha", "categorias": ["Outras Receitas"]},
    {"titulo": "Receitas Financeiras", "tipo": "linha", "categorias": ["Receitas Financeiras"]},
    {"titulo": "Honorários", "tipo": "linha", "categorias": ["Honorários"]},
    {"titulo": "Juros e Devoluções", "tipo": "linha", "categorias": ["Juros e devoluções"]},
    {"titulo": "Outras Entradas", "tipo": "card", "var": "outras_entradas"},
    {"titulo": "", "tipo": "divisor"},

    # IMPOSTOS
    {"titulo": "Impostos", "tipo": "linha", "categorias": ["Impostos"]},
    {"titulo": "Provisão IRPJ e CSSL Trimestral", "tipo": "linha", "categorias": ["Provisão - IRPJ e CSSL Trimestral"]},
    {"titulo": "Total de Impostos", "tipo": "card", "var": "total_impostos"},
    {"titulo": "", "tipo": "divisor"},

    # CUSTOS OPERACIONAIS
    {"titulo": "Prestador de serviço PJ MEI Operacional", "tipo": "linha", "categorias": ["Prestador de serviço - PJ (MEI - Operacional)", "Adiantamento - Prestador de Serviço - PJ (MEI - Operacional)"]},
    {"titulo": "Terceirização de Mão de Obra", "tipo": "linha", "categorias": ["Terceirização de Mão de Obra"]},
    {"titulo": "CLTs", "tipo": "linha", "categorias": ["Despesas com Pessoal"]},
    {"titulo": "Custo dos Serviços Prestados", "tipo": "linha", "categorias": ["Custo dos Serviços Prestados"]},
    {"titulo": "M. Preventiva Climatização B2G", "tipo": "linha", "categorias": ["M. Preventiva - Climatização B2G", "Manutenção Preventiva"]},
    {"titulo": "M. Corretiva Climatização B2G", "tipo": "linha", "categorias": ["M. Corretiva - Climatização B2G", "Manutenção Corretiva"]},
    {"titulo": "Outros Custos", "tipo": "linha", "categorias": ["Outros Custos"]},
    {"titulo": "Total Custos Operacionais", "tipo": "card", "var": "total_custos"},
    {"titulo": "", "tipo": "divisor"},

    # DESPESAS RATEADAS
    {"titulo": "Prestador de serviço PJ MEI Administrativo", "tipo": "linha", "categorias": ["Prestador de serviço - PJ (MEI - Administrativo)", "Adiantamento - Prestador de Serviço - PJ (MEI - Administrativo)"]},
    {"titulo": "Prestador de serviço PJ MEI TI", "tipo": "linha", "categorias": ["Prestador de serviço - PJ (MEI - TI)", "Adiantamento - Prestador de Serviço - PJ (MEI - TI)"]},
    {"titulo": "Despesas Administrativas", "tipo": "linha", "categorias": ["Despesas Administrativas"]},
    {"titulo": "Despesas de Vendas e Marketing", "tipo": "linha", "categorias": ["Despesas de Vendas e Marketing"]},
    {"titulo": "Despesas Financeiras", "tipo": "linha", "categorias": ["Despesas Financeiras"]},
    {"titulo": "Outros Tributos", "tipo": "linha", "categorias": ["Outros Tributos"]},
    {"titulo": "Despesas Eventuais", "tipo": "linha", "categorias": ["Jurídico"]},
    {"titulo": "Despesas Variáveis", "tipo": "linha", "categorias": ["Despesas Variáveis"]},
    {"titulo": "Intermediação de Negócios", "tipo": "linha", "categorias": ["Intermediação de Negócios"]},
    {"titulo": "Total Despesas Rateadas", "tipo": "card", "var": "total_despesas"},
    {"titulo": "", "tipo": "divisor"},

    # INVESTIMENTOS
    {"titulo": "Consórcios a contemplar", "tipo": "linha", "categorias": ["Consórcios - a contemplar"]},
    {"titulo": "Serviços", "tipo": "linha_calc", "formula": "servicos_menos_consorcios", "categorias": ["Serviços"]},
    {"titulo": "Ativos", "tipo": "linha", "categorias": ["Ativos"]},
    {"titulo": "Total Investimentos", "tipo": "card", "var": "total_investimentos"},
    {"titulo": "", "tipo": "divisor"},

    # CARDS FINAIS
    {"titulo": "Total Saídas", "tipo": "card", "var": "total_saidas"},
    {"titulo": "Fluxo de Caixa Livre FCL", "tipo": "card", "var": "fcl"},
    {"titulo": "Lucro s/ Receita Operacional", "tipo": "card_percentual", "var": "perc_lucro"},
    {"titulo": "FCL s/ Receita Operacional", "tipo": "card_percentual", "var": "perc_fcl"},

    # MÚTUO E DIVIDENDOS (vão para cards também)
    {"titulo": "Mútuo Entradas", "tipo": "card", "var": "mutuo_entradas", "categorias": ["Mútuo - Entradas"]},
    {"titulo": "Mútuo Saídas", "tipo": "card", "var": "mutuo_saidas", "categorias": ["Mútuo - Saídas"]},
    {"titulo": "Distribuição de Dividendos", "tipo": "card", "var": "dividendos", "categorias": ["Distribuição de Dividendos", "Dividendos"]},
]
