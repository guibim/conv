# Conv+ ⚙️  
Conversor simples e direto de arquivos acessível via Web.

🔗 Acesse o app: https://convplus.lovable.app  
🖥️ API pública: https://conv-api-la6e.onrender.com

---

## 🧠 Sobre o Projeto

O **Conv+** é um conversor online minimalista criado para facilitar a vida de quem trabalha com dados.

O projeto nasceu com propósito de **estudo, aprendizado e experimentação**, servindo como base para testar:

- FastAPI
- Deploy em Render (free tier)
- Integração com Lovable.dev
- Processamento de arquivos diretamente no navegador
- UX simplificada com foco em acessibilidade e rapidez

O Conv+ está **em desenvolvimento constante** e novas funcionalidades serão adicionadas ao longo do tempo.

---

## 🚀 Funcionalidade Ativa

| Conversão | Descrição |
|-----------|-----------|
| **DTA → CSV** | Converte arquivos do Stata para CSV de forma leve e rápida |
| **TXT → CSV** | Converte linhas de texto em coluna CSV |
| **CSV → TXT** | Exporta o CSV como arquivo TXT formatado |
| **CSV → JSON** | Transforma CSV tabular em JSON estruturado |
| **JSON → CSV** | Converte lista JSON em tabela CSV |
| **CSV → XML** | Converte conteúdo tabular de CSV em estrutura XML hierárquica |
| **XML → CSV** | Transforma elementos XML repetitivos em tabela CSV |
| **CSV → HTML** | Gera uma tabela HTML completa baseada nos dados do CSV |
| **HTML → TXT** | Extrai apenas o texto legível de um arquivo HTML |
| **TXT → JSON** | Converte cada linha de um arquivo TXT em um item de lista JSON |
| **JSON → TXT** | Converte uma lista JSON em um arquivo TXT com um item por linha |

---

## ⚠️ Sobre CSV → DTA (Funcionalidade temporariamente desativada)

A funcionalidade **CSV → DTA** foi planejada, iniciada e testada, **porém está temporariamente desativada**, e aqui está o motivo técnico:

### 📌 **Justificativa técnica**

Para salvar arquivos `.dta`, o pacote `pyreadstat` exige obrigatoriamente um **DataFrame real do pandas** — não aceita listas de dicionários, nem DataFrames alternativos ou “compatíveis”.

Entretanto:

- O **pandas não pode ser instalado no plano gratuito do Render**, pois requer dependências do sistema (compilação C, OpenBLAS, libgcc etc.)
- O ambiente **não possui suporte para compilar essas dependências**
- Alternativas como `pandas-lite` não funcionam, pois **não implementam estrutura interna compatível** com o formato `.dta`
- O resultado disso é erro permanente `500 Internal Server Error` ao tentar gerar `.dta`

> **Conclusão:**  
> `CSV → DTA` **não pode ser suportado no ambiente atual (Render Free)**.  
> A funcionalidade será reativada futuramente caso o backend migre para um ambiente com suporte completo ao pandas (Railway, Fly.io, Cloud Run etc).

---

## 🧊 Sobre Cold Start

A API está hospedada em um ambiente gratuito (Render Free), o que significa que:

- Após alguns minutos de inatividade, o servidor entra em "sleep mode".
- Ao receber a primeira requisição novamente, ele precisa **"acordar"**, o que leva entre **20 e 60 segundos**.
- Depois disso, a API fica rápida novamente.

No frontend, essa informação é exibida para o usuário no momento da conversão.

---

## 🧱 Estrutura do Projeto

### **Frontend**
- Construído no **Lovable.dev**
- Interface simples, responsiva e minimalista
- Upload direto do navegador
- Comunicação via `fetch()` com a API FastAPI

### **Backend**
- Python + FastAPI
- Hospedado no Render (Free Tier)
- Endpoints:
  - `POST /convert` 

### **Dependências principais**
- `fastapi`
- `uvicorn`
- `python-multipart`
- `pyreadstat` (somente leitura de `.dta`)

### **Futuro (Planejado)**
- Reativar CSV → DTA
- Converter PDF ↔ Imagem
- Conversores adicionais (XLSX, JSON, Parquet)
- Histórico de conversões com Supabase

---

## 📡 Como usar a API

### **Endpoint:**

### Campos enviados:
- `file`
- `from_format`
- `to_format`

### **Resposta:**
Um arquivo convertido, pronto para download.

---

## 🧪 Status do projeto

> **Conv+ é um projeto de estudo em constante aprimoramento.**  
> Seu propósito é educativo e exploratório, e mudanças podem ocorrer com frequência.

Feedbacks e sugestões são sempre bem-vindos!

---

## 👤 Créditos

Desenvolvido por:

- GitHub: https://github.com/guibim  
- LinkedIn: https://www.linkedin.com/in/guilherme-bim

---
