
@echo off
cd /d C:\Users\alexa\Downloads\gestao_financeira_ml_corrigido

echo ========================
echo Atualizando dados...
echo ========================
python main.py

echo ========================
echo Iniciando o dashboard...
echo ========================
REM encontrar o último arquivo Excel gerado pelo main.py
FOR /F "delims=" %%i IN ('dir /b /o-d relatorio_financeiro_*.xlsx') DO (
    SET "ultimo_excel=%%i"
    GOTO :iniciar
)

:iniciar
streamlit run dashboard_financeiro.py -- --file "%ultimo_excel%"
pause
