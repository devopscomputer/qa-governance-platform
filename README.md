# 🚀 QA Governance Platform

Plataforma avançada de Governança de Testes Automatizados com geração de métricas inteligentes, automação de ponta a ponta, relatórios interativos com Allure, rastreabilidade por requisito, cobertura de testes, controle de flakiness e integração com pipelines CI/CD — ideal para squads de alta performance em qualidade contínua.

---

## 🧠 Visão Geral

Este projeto foi desenvolvido com o objetivo de:

- Centralizar **testes automatizados (UI + API)**
- **Rastrear métricas críticas**: cobertura, flakiness, regressão, sucesso, duração
- **Visualizar resultados em dashboards interativos** (Streamlit + Plotly)
- Permitir **tomada de decisão orientada por dados**
- Integrar com **CI/CD, Docker e SonarQube**

---

## 📦 Estrutura de Pastas

```
QA-GOVERNANCE-PLATFORM/
├── tests/                 # Testes automatizados (API e UI)
│   ├── api/
│   ├── ui/
│   ├── data/
│   ├── conftest.py
│   └── test_metadata.json
├── metrics/               # Scripts de análise de métricas
│   ├── analyze.py
│   ├── flakiness_tracker.py
│   └── coverage_report.py
├── dashboard/             # App em Streamlit com KPIs e gráficos
│   └── app.py
├── ci/                    # CI/CD e docker-compose.yml
├── reports/               # Relatórios Allure
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── sonar-project.properties
└── README.md
```

---

## ⚙️ Tecnologias e Ferramentas

| Camada               | Ferramenta                             |
|----------------------|-----------------------------------------|
| Testes               | Python, Pytest, Selenium, Requests      |
| Relatórios           | Allure, pytest-cov                      |
| Métricas             | Pandas, Streamlit, Plotly               |
| Análise de Qualidade | SonarQube                               |
| Integração           | GitLab CI, Jenkins, GitHub Actions      |
| Contêinerização      | Docker, Docker Compose                  |

---

## ✅ Funcionalidades

- 🔹 Automação UI (Selenium Headless)
- 🔹 Testes de API (Requests + validação de contrato)
- 🔹 Fixtures reutilizáveis e `--env` (dev, staging, prod)
- 🔹 Geração de relatórios com Allure
- 🔹 Métricas: flakiness, duração, regressão, sucesso
- 🔹 Extração de cobertura com `coverage.xml`
- 🔹 Dashboard com KPIs e gráficos via Streamlit
- 🔹 Histórico de execuções com `history_log.csv`
- 🔹 Identificação automática de testes flakey
- 🔹 Rastreabilidade com `test_metadata.json`
- 🔹 Integração com CI/CD e execução via Docker

---

## 🚀 Como Rodar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seuusuario/qa-governance-platform.git
cd qa-governance-platform
```

### 2. Instale as dependências

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

### 3. Execute os testes

```bash
pytest tests/ --env=dev --alluredir=reports/allure-results --cov=tests --cov-report=xml
```

### 4. Gere relatório Allure

```bash
allure serve reports/allure-results
```

---

## 🐳 Executando com Docker

```bash
docker-compose up --build
```

Acesse o relatório Allure em:  
👉 http://localhost:5050

---

## 📈 Visualizar Métricas no Dashboard

```bash
python metrics/analyze.py
python metrics/coverage_report.py
python metrics/flakiness_tracker.py
streamlit run dashboard/app.py
```

---

## 🧪 Executando com múltiplos ambientes

```bash
pytest tests/ --env=staging --alluredir=reports/allure-results
```

---

## 📌 Exemplo de Rastreabilidade

```json
{
  "test_id": "test_get_user_by_id",
  "description": "Valida GET /users/{id} com IDs válidos",
  "module": "API",
  "component": "UserService",
  "priority": "high",
  "type": "contract, regression",
  "linked_requirement": "REQ-USER-001"
}
```

🧠 Execução via PowerShell ou BAT (Windows)

{
  ./run_qa_dashboard.ps1
  ou
  ./run_qa_dashboard.bat

}




---

## 📣 Autor

**Paulo Silas de Campos Filho**  
Tech Lead | QA | Automação | Segurança | DevSecOps  
📍 Campinas/SP  
🔗 [LinkedIn](https://www.linkedin.com/in/itmanagerpaulocampos)  
🔗 [GitHub](https://github.com/devopscomputer)

---

## 🛡️ Licença

MIT © 2025 – Livre para uso, adaptação e melhoria com créditos.
