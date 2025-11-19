
from config import MESES_ORDEM

def format_currency(value):
    """Formata valor em reais SEM CENTAVOS"""
    try:
        # Arredonda para inteiro
        value = round(value)
        
        if value < 0:
            return f"-R$ {abs(value):,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"R$ {value:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "R$ 0"

def normalizar_mes(mes_str):
    """Normaliza nome do mês"""
    return mes_str.strip().capitalize()

def ordenar_mes(mes):
    """Retorna índice do mês para ordenação"""
    try:
        return MESES_ORDEM.index(normalizar_mes(mes))
    except:
        return 999

def gerar_resumo_filtros(empresas, anos, meses, projetos, categorias):
    """Gera resumo dos filtros aplicados"""
    filtros = []
    
    if empresas:
        filtros.append(f"🏢 **Empresas:** {', '.join(empresas)}")
    if anos:
        filtros.append(f"📅 **Anos:** {', '.join(anos)}")
    if meses:
        filtros.append(f"📆 **Meses:** {', '.join(meses)}")
    if projetos:
        filtros.append(f"📋 **Projetos:** {', '.join(projetos[:3])}{'...' if len(projetos) > 3 else ''}")
    if categorias:
        filtros.append(f"🏷️ **Categorias:** {', '.join(categorias[:3])}{'...' if len(categorias) > 3 else ''}")
    
    if not filtros:
        return "📊 **Exibindo:** Todos os dados"
    
    return " | ".join(filtros)
