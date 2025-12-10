# Conv+ ⚙️

Conversor de arquivos simples e direto, acessível via Web.

🔗 Acesse o app: [https://convplus.lovable.app](https://convplus.lovable.app)

---

## 🧠 Sobre o projeto

**Conv+** é uma aplicação web minimalista que permite **converter arquivos entre os formatos `.dta` (Stata) e `.csv`**, com objetivo de tornar tarefas comuns de manipulação de dados mais simples e rápidas — direto do navegador, sem precisar instalar nada.

O projeto foi criado com foco em **experimentos, aprendizado e praticidade**, e está em constante evolução com novas funcionalidades previstas (ex: PDF para imagem, compactação, etc).

---

## 🚀 Funcionalidade atual

- ✅ Upload de arquivos `.dta` ou `.csv`
- ✅ Conversão entre os dois formatos
- ✅ Download automático do arquivo convertido
- ✅ Interface limpa, rápida e responsiva
- ✅ Feedback visual (status, loading, erro)
- ✅ Aviso sobre tempo de espera inicial (cold start)

---

## 🧱 Estrutura do projeto

| Camada      | Tecnologia                |
|-------------|---------------------------|
| **Frontend** | [Lovable.dev](https://lovable.dev) - No-code/low-code builder |
| **Backend**  | FastAPI + Python          |
| **Hospedagem API** | [Render.com](https://render.com) |
| **Banco de dados (futuro)** | Supabase (em fase de planejamento) |

---

## 📡 Sobre a API

A API está hospedada gratuitamente em: https://conv-api-la6e.onrender.com/


### 📥 Endpoint disponível:

- `POST /convert`  
  Envia um arquivo `.dta` ou `.csv` e recebe o arquivo convertido.

**Campos esperados:**
- `file`: o arquivo a ser convertido
- `from_format`: formato de origem (`dta` ou `csv`)
- `to_format`: formato de destino (`csv` ou `dta`)

**Resposta:** um arquivo convertido para download direto.

---

## 🧊 Aviso: Cold Start

> ⚠️ Como a API está hospedada em um serviço gratuito (Render), a primeira requisição após um tempo de inatividade pode levar **até 1 minuto** para responder.  
> Esse atraso acontece apenas no primeiro uso após o app "dormir".

---

## 🧪 Status do projeto

> Este é um **projeto de estudo** e **experimento pessoal**, criado por [Guilherme Bim](https://www.linkedin.com/in/guilherme-bim).  
> O código, layout e funcionalidades ainda estão sendo **testados, aprimorados e evoluídos com o tempo**.

Contribuições, feedbacks e sugestões são bem-vindos!

---

## 👤 Créditos

Desenvolvido por:

- GitHub: [@guibim](https://github.com/guibim)
- LinkedIn: [Guilherme Bim](https://www.linkedin.com/in/guilherme-bim)

---
