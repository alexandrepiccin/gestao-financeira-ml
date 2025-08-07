
@echo off
cd /d C:\Users\alexa\Downloads\gestao_financeira_ml_corrigido

echo ========================
echo Atualizando dados...
echo ========================
python main.py

echo ========================
echo Iniciando o dashboard...
echo ========================
streamlit run dashboard_financeiro.py

pause
