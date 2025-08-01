
# Aplicação de Gestão de Produtores Rurais

## Visão Geral

Esta aplicação Django gerencia produtores rurais e suas propriedades, permitindo:

- Cadastro, edição e exclusão de produtores rurais.
- Validação de documentos CPF e CNPJ.
- Gerenciamento de fazendas com validação das áreas.
- Registro de diversas culturas plantadas por fazenda e safra.
- Dashboard com total de fazendas, hectares e gráficos de pizza por estado, cultura e uso do solo.
- API RESTful com filtros dinâmicos como `iexact`, `icontains`, `gte`, `lte`.
- Logs para rastreamento e observabilidade das ações.

---

## Tecnologias Usadas

- Python 3.10+
- Django
- Django REST Framework
- PostgreSQL
- Chart.js (frontend)
- validate-docbr
- Docker + Docker Compose
- Poetry (gerenciador de dependências)
- Logging do Django
- Pytest para testes automatizados

---

## Instalando Docker (opcional, mas recomendado)

Para usar o ambiente Docker, instale os seguintes componentes:

### Links Oficiais

- Docker Desktop (Windows/Mac): [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- Docker para Linux: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

### Verifique a Instalação

```bash
docker --version
docker-compose --version
```

---

## Rodando com Docker

### Pré-requisitos

- Docker
- Docker Compose

### Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/JacksonCypriano/rural_producers.git
   cd rural_producers
   ```

2. Crie o arquivo `.env`:
   ```env
   POSTGRES_DB=ruraldb
   POSTGRES_USER=ruraluser
   POSTGRES_PASSWORD=ruraluser
   SECRET_KEY=sua_chave_secreta
   DEBUG=True
   ```

3. Construa e suba os containers:
   ```bash
   docker-compose up --build
   ```

4. Rode as migrações:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. Acesse:
   - API: `http://localhost:8000/api/`
   - Dashboard: `http://localhost:8000/dashboard/`

---

## Rodando Localmente (sem Docker)

### Pré-requisitos

- Python 3.10 ou superior
- [Poetry](https://python-poetry.org/docs/) instalado
- PostgreSQL rodando localmente

### Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/JacksonCypriano/rural_producers.git
   cd rural_producers
   ```

2. Instale as dependências:
   ```bash
   poetry install
   ```

3. Ative o ambiente virtual:
   ```bash
   poetry shell
   ```

4. Configure as variáveis de ambiente (`.env` ou export direto):
   ```env
   SECRET_KEY=sua_chave_secreta
   DEBUG=True
   DATABASE_URL=postgres://usuario:senha@localhost:5432/ruraldb
   ```

5. Rode as migrações:
   ```bash
   python manage.py migrate
   ```

6. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

7. Acesse:
   - API: `http://localhost:8000/api/`
   - Dashboard: `http://localhost:8000/dashboard/`

---

## Dashboard

### TemplateView
- URL: `/dashboard/`
- Exibe:
  - Total de fazendas
  - Total de hectares
  - Fazendas por estado
  - Culturas plantadas
  - Uso do solo (área agricultável e vegetação)

### APIView
- URL: `/api/dashboard/`
- Retorna os mesmos dados em JSON

---

## Filtros Dinâmicos na API

As views `ModelViewSet` aceitam query params, incluindo:

```http
?nome__iexact=João
?document__icontains=123
?total_area__gte=100
?state__exact=SP
```

O sistema valida e aplica os filtros diretamente no queryset.

---

## Validações

- CPF e CNPJ validados com `validate-docbr`
- Somatório das áreas não pode exceder o total da propriedade

---

## Logs e Observabilidade

A aplicação possui logging nas views e ações principais:

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
```

Use `INFO` ou `DEBUG` conforme necessidade.

---

## Testes Automatizados

Organizados por entidade:

- Criação, listagem, edição e exclusão
- Validações de documentos e áreas
- Respostas da API e status HTTP

Execute com cobertura:

```bash
pytest --cov=apps.farmers
```

---

## Endpoints da API

Abaixo estão listados os principais endpoints RESTful disponíveis:

### Prefixo base: `/api/`

| Recurso        | Endpoint               | Descrição                                |
|----------------|------------------------|--------------------------------------------|
| 👤 Farmers     | `/api/farmers/`        | CRUD de produtores rurais                  |
| 🌾 Farms       | `/api/farms/`          | CRUD de fazendas                           |
| 🌱 Crops       | `/api/crops/`          | CRUD de culturas                           |
| 🌽 Harvests    | `/api/harvests/`       | CRUD de safras                             |
| 📊 Dashboard   | `/api/dashboard/`      | API com dados agregados para visualização  |
| 📈 Dashboard   | `/dashboard/`          | Dashboard com gráficos via frontend        |

Os endpoints suportam operações padrão (GET, POST, PUT, PATCH, DELETE) conforme o ViewSet correspondente.

### Exemplos de chamadas

- `GET /api/farmers/`: lista todos os produtores
- `POST /api/farms/`: cria uma nova fazenda
- `GET /api/harvests/1/`: detalhes de uma safra específica
- `DELETE /api/crops/3/`: remove a cultura com ID 3

---
