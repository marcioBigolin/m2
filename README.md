My Data Analyzer
---

Módulo do streamlit para rodar o analisador de dados.

1 - Configurar o arquivo secrets.toml (configure para uma instancia válida do MDI)


Dica: Duplique para um arquivo chamado **secrets.local.toml** (os arquivos que tiverem o local terão preferencia sobre o default)

Para rodar, execute o comando abaixo no diretório do módulo pela primeira vez:

```
pip install -r requirements.txt
```

Nas demais execuções, apenas execute:
```
streamlit run src/Home.py
```