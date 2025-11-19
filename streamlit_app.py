
import streamlit as st
import pandas as pd
from config import ESTRUTURA_DRE
from formatters import format_currency, gerar_resumo_filtros, normalizar_mes, ordenar_mes
from data_processing import parse_csv, extrair_anos_meses
from filters import filtrar_cascata
from dre_calculator import calcular_dre

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="DRE - Mar Brasil",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS CUSTOMIZADO COM ELEMENTOS FIXOS
st.markdown("""
<style>
    /* CONTAINER PRINCIPAL */
    .main .block-container {
        padding-top: 1rem;
        max-width: 100%;
    }
    
    /* HEADER FIXO */
    .header-fixo {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: white;
        padding: 0.5rem 0;
        margin-bottom: 1rem;
    }
    
    /* CARDS PRINCIPAIS FIXOS */
    .cards-fixos {
        position: sticky;
        top: 120px;
        z-index: 999;
        background: white;
        padding: 1rem 0;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-radius: 8px;
    }
    
    /* GRID DE CARDS - 6 COLUNAS */
    .cards-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    /* GRID DE OUTROS CARDS */
    .cards-grid-outros {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    /* CARD BASE */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 4px solid #E8E8E8;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(242, 145, 27, 0.3);
    }
    
    /* CARD AZUL - RECEITAS */
    .card-azul {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-left: 5px solid #2196F3;
    }
    
    .card-azul .valor {
        color: #0D47A1;
        font-size: 22px;
        font-weight: 700;
    }
    
    .card-azul .titulo {
        color: #1565C0;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    /* CARD VERMELHO - SAÍDAS */
    .card-vermelho {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        border-left: 5px solid #F44336;
    }
    
    .card-vermelho .valor {
        color: #B71C1C;
        font-size: 22px;
        font-weight: 700;
    }
    
    .card-vermelho .titulo {
        color: #C62828;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    /* CARD LARANJA - RESULTADO */
    .card-laranja {
        background: linear-gradient(135deg, #F2911B 0%, #F2B807 100%);
        border: none;
        box-shadow: 0 6px 20px rgba(242, 145, 27, 0.3);
    }
    
    .card-laranja .valor {
        color: white;
        font-size: 26px;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .card-laranja .titulo {
        color: rgba(255, 255, 255, 0.95);
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* CARD IMPORTANTE */
    .card-importante {
        background: linear-gradient(135deg, #ffffff 0%, #FFF9F0 100%);
        border-left: 5px solid #F2911B;
        box-shadow: 0 4px 12px rgba(242, 145, 27, 0.2);
    }
    
    .card-importante .valor {
        color: #F2911B;
        font-size: 22px;
        font-weight: 700;
    }
    
    .card-importante .titulo {
        color: #F2911B;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    /* ELEMENTOS DO CARD */
    .icon {
        font-size: 28px;
        margin-bottom: 0.5rem;
    }
    
    .titulo {
        font-size: 11px;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    
    .valor {
        font-size: 20px;
        font-weight: 700;
        color: #262223;
    }
    
    .positive {
        color: #28a745 !important;
    }
    
    .negative {
        color: #dc3545 !important;
    }
    
    /* TABELA */
    .dataframe {
        font-size: 9px !important;
    }
    
    .dataframe thead th {
        font-size: 10px !important;
        font-weight: 600 !important;
        background: #f8f9fa !important;
        position: sticky !important;
        top: 0 !important;
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# HEADER FIXO
st.markdown("""
<div class="header-fixo">
    <div style="background: linear-gradient(135deg, #F2911B 0%, #F2B807 100%); 
                padding: 1.5rem; border-radius: 16px; text-align: center; 
                box-shadow: 0 8px 32px rgba(242, 145, 27, 0.4);">
        <h1 style="color: white; margin: 0; font-size: 28px;">📊 DRE - Mar Brasil</h1>
        <p style="color: white; margin: 0.5rem 0 0 0; font-size: 14px;">Gestão Financeira Inteligente</p>
    </div>
</div>
""", unsafe_allow_html=True)

# INICIALIZA SESSION STATE
if 'df' not in st.session_state:
    st.session_state.df = None
if 'mapa_meses' not in st.session_state:
    st.session_state.mapa_meses = {}

# SIDEBAR - UPLOAD E FILTROS
with st.sidebar:
    st.header("📁 Carregar Dados")
    
    uploaded_file = st.file_uploader("Selecione o CSV", type=['csv'])
    
    if uploaded_file:
        df = parse_csv(uploaded_file)
        if df is not None:
            st.session_state.df = df
            anos, mapa_meses = extrair_anos_meses(df)
            st.session_state.mapa_meses = mapa_meses
            
            empresas = sorted(df['Empresa'].dropna().unique().tolist())
            
            meses_set = set()
            for mes in mapa_meses.values():
                meses_set.add(normalizar_mes(mes))
            meses_unicos = sorted(list(meses_set), key=ordenar_mes)
            
            projetos = sorted(df['Projeto'].dropna().unique().tolist())
            categorias = sorted(df['Categoria'].dropna().unique().tolist())
            
            st.success(f"✅ {len(df)} lançamentos")
            
            st.markdown("---")
            st.header("⚙️ Filtros")
            
            # Filtros
            empresas_sel = st.multiselect("🏢 Empresa", empresas, key="empresas")
            anos_sel = st.multiselect("📅 Ano", anos, key="anos")
            meses_sel = st.multiselect("📆 Mês", meses_unicos, key="meses")
            
            # Filtros em cascata
            if empresas_sel or anos_sel or meses_sel:
                proj_disp, cat_disp, meses_disp = filtrar_cascata(
                    df, empresas_sel, anos_sel, meses_sel, [], st.session_state.mapa_meses
                )
            else:
                proj_disp = projetos
                cat_disp = categorias
            
            projetos_sel = st.multiselect("📋 Projeto", proj_disp, key="projetos")
            categorias_sel = st.multiselect("🏷️ Categoria", cat_disp, key="categorias")
            
            if st.button("🗑️ Limpar Filtros", use_container_width=True):
                for key in ['empresas', 'anos', 'meses', 'projetos', 'categorias']:
                    if key in st.session_state:
                        st.session_state[key] = []
                st.rerun()

# ÁREA PRINCIPAL
if st.session_state.df is not None:
    df = st.session_state.df
    
    # Pega filtros
    empresas_filtro = st.session_state.get('empresas', [])
    anos_filtro = st.session_state.get('anos', [])
    meses_filtro = st.session_state.get('meses', [])
    projetos_filtro = st.session_state.get('projetos', [])
    categorias_filtro = st.session_state.get('categorias', [])
    
    # Calcula DRE
    dre, debug, metricas = calcular_dre(
        df, empresas_filtro, anos_filtro, meses_filtro, 
        projetos_filtro, categorias_filtro, st.session_state.mapa_meses
    )
    
    # Resumo dos filtros
    resumo = gerar_resumo_filtros(empresas_filtro, anos_filtro, meses_filtro, projetos_filtro, categorias_filtro)
    st.info(resumo)
    
    # PRIMEIRA LINHA DE CARDS (FIXA)
    st.markdown('<div class="cards-fixos"><div class="cards-grid">', unsafe_allow_html=True)
    
    cards_principais = [
        ('total_entradas', 'card-azul'),
        ('total_saidas', 'card-vermelho'),
        ('resultado', 'card-laranja'),
        ('perc_lucro_operacional', 'card-importante'),
        ('fcl', 'card-importante'),
        ('perc_fcl', 'card-importante')
    ]
    
    cols = st.columns(6)
    for idx, (key, classe) in enumerate(cards_principais):
        if key in metricas:
            with cols[idx]:
                metric = metricas[key]
                valor = metric['valor']
                titulo = metric['titulo']
                icon = metric.get('icon', '📊')
                tipo = metric.get('tipo', 'moeda')
                
                valor_class = 'valor'
                if key in ['resultado', 'fcl']:
                    if valor > 0:
                        valor_class += ' positive'
                    elif valor < 0:
                        valor_class += ' negative'
                
                if tipo == 'percentual':
                    valor_fmt = f"{valor:.2f}%"
                else:
                    valor_fmt = format_currency(valor)
                
                st.markdown(f'''
                <div class="metric-card {classe}">
                    <div class="icon">{icon}</div>
                    <div class="titulo">{titulo}</div>
                    <div class="{valor_class}">{valor_fmt}</div>
                </div>
                ''', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # DEMAIS CARDS
    st.markdown('<div class="cards-grid-outros">', unsafe_allow_html=True)
    
    outros_cards = [
        'outras_entradas', 'total_impostos', 'total_custos', 'total_despesas', 
        'total_investimentos', 'pessoal', 'pj_operacional', 'pj_administrativo', 
        'clts_card', 'terceirizacao', 'preventivas', 'corretivas',
        'mutuo_entradas', 'mutuo_saidas', 'dividendos'
    ]
    
    # Calcula quantas colunas cabem
    num_cols = min(5, len([k for k in outros_cards if k in metricas]))
    if num_cols > 0:
        cols_outros = st.columns(num_cols)
        col_idx = 0
        
        for key in outros_cards:
            if key in metricas:
                with cols_outros[col_idx % num_cols]:
                    metric = metricas[key]
                    valor = metric['valor']
                    titulo = metric['titulo']
                    icon = metric.get('icon', '📊')
                    tipo = metric.get('tipo', 'moeda')
                    
                    if tipo == 'percentual':
                        valor_fmt = f"{valor:.2f}%"
                    else:
                        valor_fmt = format_currency(valor)
                    
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="icon">{icon}</div>
                        <div class="titulo">{titulo}</div>
                        <div class="valor">{valor_fmt}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                col_idx += 1
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # TABELA DRE
    st.markdown("---")
    st.subheader("📋 Detalhamento do DRE")
    
    st.dataframe(
        dre,
        use_container_width=True,
        height=600,
        hide_index=True
    )
    
    # ABA DEBUG
    with st.expander("🔍 Debug - Totais por Categoria"):
        st.dataframe(debug, use_container_width=True, hide_index=True)

else:
    st.info("👆 Faça upload do arquivo CSV na barra lateral para começar")
