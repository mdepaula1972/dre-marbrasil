@echo off
echo Tentando corrigir erro de escrita do Git...
git config windows.appendAtomically false
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Sucesso! A configuracao foi aplicada.
    echo Tente fazer o commit novamente no GitHub Desktop.
) else (
    echo.
    echo Erro ao executar o comando git.
    echo Verifique se o Git esta instalado e disponivel no terminal.
)
pause
