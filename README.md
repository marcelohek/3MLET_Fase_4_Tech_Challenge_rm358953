# 3MLET_Fase_4_Tech_Challenge_rm358953


## API Previsão de fechamento da ação NVDA


## Como Executar o Projeto

### 1. Clone o Repositório

```bash
git clone https://github.com/marcelohek/3MLET_Fase_1_Tech_Challenge_rm358953.git
```

### 2. Crie um Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o Aplicativo

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

O aplicativo estará disponível em `http://127.0.0.1:8000/predict` 
sendo necessário passar no body da requisição POST um JSON com 30 valores de fechamento. ex 
`{
    "sequence": [
        150.12,
        151.34,
        150.87,
        152.10,
        153.45,
        154.30,
        155.00,
        154.75,
        155.20,
        156.10,
        155.80,
        156.25,
        157.00,
        156.50,
        157.20,
        158.00,
        157.80,
        158.30,
        159.10,
        158.90,
        159.50,
        160.20,
        159.80,
        160.50,
        161.00,
        160.75,
        161.20,
        162.00,
        161.80,
        162.50
    ]
}`
