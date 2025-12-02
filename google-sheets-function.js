// ========================================
// Google Sheets Integration
// ========================================
async function loadFromGoogleSheets() {
    const SHEET_ID = '1aBSas0JlWuXEubN6ti7tYVUPrCz_qfmXA6LWwbdPMiw';
    const SHEET_NAME = 'Dados';

    // URL para exportar como CSV (requer planilha publicada)
    const url = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&sheet=${encodeURIComponent(SHEET_NAME)}`;

    document.getElementById('loadingOverlay').classList.remove('d-none');
    document.getElementById('fileStatus').textContent = 'Carregando dados do Google Sheets...';

    try {
        const response = await fetch(url, {
            method: 'GET',
            mode: 'cors'
        });

        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}: ${response.statusText}. Verifique se a planilha está publicada.`);
        }

        const csvText = await response.text();

        // Verificar se recebemos dados válidos
        if (!csvText || csvText.trim().length === 0) {
            throw new Error('A planilha está vazia ou não foi possível ler os dados.');
        }

        // Verificar se não é uma página de erro HTML
        if (csvText.trim().startsWith('<')) {
            throw new Error('Recebido HTML ao invés de CSV. Verifique se a planilha está publicada como "Qualquer pessoa com o link pode visualizar".');
        }

        Papa.parse(csvText, {
            header: true,
            skipEmptyLines: true,
            complete: processParsedData,
            error: (error) => {
                throw new Error(`Erro ao processar CSV: ${error.message}`);
            }
        });

    } catch (error) {
        document.getElementById('loadingOverlay').classList.add('d-none');

        let errorMessage = `Erro ao carregar Google Sheets: ${error.message}\n\n`;
        errorMessage += 'INSTRUÇÕES:\n';
        errorMessage += '1. Abra a planilha no Google Sheets\n';
        errorMessage += '2. Clique em "Arquivo" → "Compartilhar" → "Publicar na Web"\n';
        errorMessage += '3. Escolha a aba "Dados" e formato "Página da Web"\n';
        errorMessage += '4. Clique em "Publicar"\n';
        errorMessage += '5. Depois, vá em "Compartilhar" (botão verde) e defina como "Qualquer pessoa com o link pode visualizar"';

        alert(errorMessage);
        console.error('Erro detalhado:', error);
    }
}
