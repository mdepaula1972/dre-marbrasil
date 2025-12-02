# Como Configurar Google Sheets para Integração Automática

## Passo 1: Publicar a Planilha

1. Abra sua planilha no Google Sheets: https://docs.google.com/spreadsheets/d/1aBSas0JlWuXEubN6ti7tYVUPrCz_qfmXA6LWwbdPMiw/edit

2. Clique em **Arquivo** → **Compartilhar** → **Publicar na Web**

3. Na janela que abrir:
   - Em "Link", selecione a aba **"Dados"** (ou a aba que contém seus dados)
   - Em "Formato", selecione **"Página da Web"**
   - Clique em **"Publicar"**
   - Confirme clicando em **"OK"**

## Passo 2: Tornar a Planilha Acessível

1. Clique no botão verde **"Compartilhar"** (canto superior direito)

2. Em "Acesso geral", altere para:
   - **"Qualquer pessoa com o link"**
   - Permissão: **"Visualizador"**

3. Clique em **"Concluído"**

## Passo 3: Testar a Integração

1. Abra o arquivo `index.html` no navegador

2. Clique no botão **"Carregar do Google Sheets"**

3. Se tudo estiver correto, os dados serão carregados automaticamente!

## Estrutura Esperada da Planilha

A planilha deve ter as seguintes colunas:

| Empresa | Projeto | Categoria | Jan/24 | Fev/24 | Mar/24 | ... |
|---------|---------|-----------|--------|--------|--------|-----|
| ...     | ...     | ...       | valor  | valor  | valor  | ... |

**Importante:**
- As colunas de meses devem estar no formato: `Mês/Ano` (ex: `Jan/24`, `Fev/24`)
- Os valores podem usar vírgula ou ponto como separador decimal

## Automação com Power Automate

Agora que a planilha está publicada, você pode:

1. Criar um fluxo no Power Automate que:
   - Busca dados do Omie via API
   - Busca dados do Gestão Click
   - Atualiza a planilha do Google Sheets

2. O app DRE carregará automaticamente os dados atualizados sempre que você clicar em "Carregar do Google Sheets"

## Solução de Problemas

### Erro: "Recebido HTML ao invés de CSV"
- Verifique se a planilha está publicada (Passo 1)
- Verifique se o compartilhamento está como "Qualquer pessoa com o link" (Passo 2)

### Erro: "A planilha está vazia"
- Certifique-se de que a aba "Dados" contém informações
- Verifique se o nome da aba está correto no código

### Erro CORS
- Este erro não deve ocorrer se a planilha estiver publicada corretamente
- Se persistir, verifique as configurações de compartilhamento
