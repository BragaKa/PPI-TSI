# fundsfinder — API REST com Django REST Framework

Projeto desenvolvido durante a componente curricular **Programação para Internet**, do Curso Superior de Tecnologia em Sistemas de Informação (TSI) do Instituto Federal de Brasília (Campus Brasília).

O projeto consiste em uma API Web RESTful para cadastro, consulta, filtragem e gerenciamento de indicadores financeiros de Fundos de Investimento Imobiliário (FIIs), desenvolvida de forma progressiva utilizando Python, Django e Django REST Framework (DRF).

## Professor

Prof. Fábio Henrique Monteiro Oliveira
E-mail: fabio.oliveira@ifb.edu.br

## Tecnologias utilizadas

- Python
- Django
- Django REST Framework (DRF)
- django-filter
- SQLite
- Git e GitHub
- Postman (testes e validação de requisições)

## Estrutura do projeto

```text
fundsfinder/
├── manage.py
├── requirements.txt
├── .gitignore
├── db.sqlite3
│
├── fundsfinder/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── api/
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_fundoimobiliario_id.py
│   │   └── 0003_fundoimobiliario_data_referencia.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
└── docs/
    └── capturas/        (capturas de tela dos testes)
```

## Arquitetura e camadas da API

O desenvolvimento com o Django REST Framework baseia-se no fluxo de quatro etapas principais:

1. **Model** (`api/models.py`): definição da entidade `FundoImobiliario`, armazenando ticker (`codigo`), setor de atuação, dividend yield médio, vacâncias, quantidade de ativos e data de referência, com identificador único universal (UUID v4).
2. **Serializer** (`api/serializers.py`): mapeamento bidirecional via `ModelSerializer`, convertendo instâncias do Django ORM em tipos primitivos do Python (para envio em JSON) e validando os dados recebidos para gravação.
3. **Views / ViewSets** (`api/views.py`): implementação da lógica e resposta às operações REST por meio do `ModelViewSet`, com filtros, busca, ordenação e permissões.
4. **Routers e URLs** (`api/urls.py` e `fundsfinder/urls.py`): mapeamento e geração automática de rotas sob o prefixo padronizado `/api/v1/`.

## Ambiente virtual e dependências

Recomenda-se a utilização de um ambiente virtual para isolar as dependências do projeto. É necessário Python 3.12 ou superior.

### 1. Criar e ativar o ambiente virtual (Windows)

```powershell
py -m venv .venv
```

Ative o ambiente virtual:

```powershell
.venv\Scripts\activate
```

(O terminal exibirá a indicação `(.venv)` no início da linha de comando, confirmando a ativação.)

### 2. Instalação dos pacotes necessários

Com o ambiente virtual ativado, instale as dependências:

```powershell
python -m pip install django djangorestframework django-filter
```

Caso esteja clonando o repositório em uma nova máquina:

```powershell
python -m pip install -r requirements.txt
```

Para salvar e congelar as versões instaladas no arquivo de dependências:

```powershell
python -m pip freeze > requirements.txt
```

## Banco de dados e migrações

Após a definição do modelo `FundoImobiliario`, gere e aplique as migrações para criar as tabelas no SQLite:

```powershell
python manage.py makemigrations api
python manage.py migrate
```

Crie um superusuário para gerenciar a aplicação e testar acessos autenticados na API:

```powershell
python manage.py createsuperuser
```

## Executando o projeto

Inicie o servidor local de desenvolvimento:

```powershell
python manage.py runserver
```

Acesse os serviços pelo navegador:

- Django Admin: http://localhost:8000/admin/
- Login da Browsable API: http://localhost:8000/api-auth/login/
- Interface Navegável da API (DRF Browsable API): http://localhost:8000/api/v1/
- Endpoint de Fundos: http://localhost:8000/api/v1/fundos

## Endpoints da API

| Método HTTP | Endpoint | Descrição |
|---|---|---|
| GET | `/api/v1/fundos` | Lista os fundos cadastrados (paginado) |
| POST | `/api/v1/fundos` | Cria um novo registro de fundo imobiliário |
| GET | `/api/v1/fundos/{id}` | Recupera os detalhes de um fundo pelo UUID |
| PUT | `/api/v1/fundos/{id}` | Atualização integral de um fundo pelo UUID |
| PATCH | `/api/v1/fundos/{id}` | Atualização parcial de um fundo pelo UUID |
| DELETE | `/api/v1/fundos/{id}` | Remove um fundo do banco de dados pelo UUID |

### Exemplo de payload para criação / edição (POST / PUT)

```json
{
  "codigo": "XPLG11",
  "setor": "logistica",
  "dividend_yield_medio_12m": 6.30,
  "vacancia_financeira": 7.87,
  "vacancia_fisica": 12.36,
  "quantidade_ativos": 19,
  "data_referencia": "19/11/2026"
}
```

O campo `data_referencia` é opcional e aceita `DD/MM/AAAA` ou `AAAA-MM-DD`.

## Filtros, busca textual, ordenação e paginação

- **Filtro por atributo** (valor exato, em `codigo` e `setor`): `/api/v1/fundos?setor=logistica`
- **Busca textual** (parcial, em `codigo` e `setor`): `/api/v1/fundos?search=XPLG11`
- **Ordenação** (`-` para ordem decrescente; padrão: `codigo`): `/api/v1/fundos?ordering=-dividend_yield_medio_12m`
- **Paginação** (5 registros por página): `/api/v1/fundos?page=2`. A resposta traz os metadados `count`, `next`, `previous` e `results`.

Os recursos podem ser combinados: `/api/v1/fundos?setor=logistica&ordering=-dividend_yield_medio_12m&page=1`

## Autenticação, permissões e formato de datas

Configuradas globalmente em `fundsfinder/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DATE_INPUT_FORMATS': ['%d/%m/%Y', 'iso-8601'],
}
```

- Sem autenticação, a API responde `403 Forbidden`.
- No navegador, faça login em `/api-auth/login/`. No Postman, use Basic Auth com o usuário criado pelo `createsuperuser`.
- A `FundoImobiliarioViewSet` também declara `permission_classes = [IsAuthenticated]`, que prevalece sobre a configuração global.
- Datas em formato diferente de `DD/MM/AAAA` ou `AAAA-MM-DD` são rejeitadas com `400 Bad Request`.

## Controle de versão com Git

Para versionar as alterações na branch `api-fundsfinder` do repositório da disciplina:

```powershell
git add .
git commit -m "feat: filtros, busca, ordenação, paginação, autenticação e permissões"
git push -u origin api-fundsfinder
```

Repositório: https://github.com/BragaKa/PPI-TSI.git

### Arquivos ignorados (`.gitignore`)

O arquivo `.gitignore` impede o versionamento do ambiente virtual, de arquivos temporários de compilação e do banco de dados local:

```text
.venv/
venv/
__pycache__/
*.pyc
*.sqlite3
.vscode/
```

Programação para Internet
Curso Superior de Tecnologia em Sistemas de Informação (TSI)
Instituto Federal de Educação, Ciência e Tecnologia de Brasília (IFB) — Campus Brasília
