# Plano de Refatoracao e Padronizacao de Conversoes

## Objetivo

Este documento transforma o diagnostico inicial do projeto `conv` em um blueprint de execucao.

O foco da refatoracao e:

- padronizar o contrato de todos os conversores
- separar a logica de conversao da camada HTTP
- classificar quais conversoes sao estaveis, beta, limitadas ou bloqueadas por infraestrutura
- reduzir inconsistencias entre arquivos, imports, assinaturas e documentacao
- manter a proposta original do projeto: leve, gratuito, simples e especifico

## Problema Central Atual

Hoje o backend mistura dois modelos de implementacao:

1. Conversores antigos baseados em arquivo:
   `convert_x(input_path, output_path)`
2. Conversores novos baseados em memoria:
   `convert_x(input_bytes) -> bytes`

Essa mistura cria quatro problemas:

- o router atual espera apenas o modelo baseado em arquivo
- parte dos imports aponta para modulos que nao existem com aqueles nomes
- varias conversoes novas nao estao realmente integradas ao endpoint `/convert`
- o repositorio parece suportar mais formatos do que de fato suporta em runtime

## Principios da Arquitetura Alvo

### 1. Contrato unico

Todo conversor deve obedecer ao mesmo contrato:

```python
def convert(input_bytes: bytes, context: ConversionContext) -> ConversionResult:
    ...
```

Estruturas sugeridas:

```python
from dataclasses import dataclass, field


@dataclass
class ConversionContext:
    source_format: str
    target_format: str
    filename: str | None = None
    options: dict[str, str] = field(default_factory=dict)


@dataclass
class ConversionResult:
    output_bytes: bytes
    media_type: str
    extension: str
    warnings: list[str] = field(default_factory=list)
```

Beneficios:

- um unico fluxo de execucao no endpoint
- testes mais simples
- melhor suporte a streaming e futuras filas
- menor dependencia de IO em disco

### 2. Router fino

O endpoint HTTP deve apenas:

- validar request
- montar `ConversionContext`
- chamar a engine
- traduzir erros de dominio para respostas HTTP
- devolver o arquivo convertido

Toda a logica de conversao deve sair de `app/routes/convert.py`.

### 3. Registry central de conversoes

Em vez de um `conversion_map` puro, usar um registro com metadados:

```python
@dataclass(frozen=True)
class ConversionSpec:
    source_format: str
    target_format: str
    handler: Callable[[bytes, ConversionContext], ConversionResult]
    status: str
    stability: str
    media_type: str
    extension: str
    notes: str = ""
```

Campos importantes:

- `status`: `enabled`, `disabled`, `infra_blocked`
- `stability`: `stable`, `beta`, `limited`, `experimental`
- `notes`: limitacoes importantes da conversao

### 4. Representacoes intermediarias por familia

Nem toda conversao deve lidar diretamente com `bytes` o tempo todo.
O contrato externo pode ser `bytes in / bytes out`, mas internamente vale padronizar representacoes:

- tabular: `TableData(headers, rows)`
- texto linear: `list[str]`
- estrutura hierarquica: `dict | list`
- resumo BIM/IFC: `ModelSummary`

Isso evita repetir parsing e encoding em todos os arquivos.

## Estrutura de Pastas Proposta

```text
app/
  api/
    routes/
      convert.py
  core/
    errors.py
    models.py
    registry.py
  converters/
    common/
      encodings.py
      io.py
    tabular/
      csv_to_json.py
      json_to_csv.py
      csv_to_xml.py
      xml_to_csv.py
      csv_to_xlsx.py
      xlsx_to_csv.py
      dta_to_csv.py
      csv_to_dta.py
    text/
      txt_to_csv.py
      csv_to_txt.py
      txt_to_json.py
      json_to_txt.py
      txt_to_xml.py
    markup/
      csv_to_html.py
      html_to_txt.py
      html_to_markdown.py
      csv_to_markdown.py
      json_to_xml.py
      xml_to_json.py
      json_to_yaml.py
      csv_to_sql.py
    bim/
      ifc_summary.py
      ifc_to_csv.py
      ifc_to_json.py
      ifc_to_html.py
      ifc_to_txt.py
  services/
    legacy/
```

Observacao:

- `app/services/` pode virar uma pasta `legacy/` temporaria durante a migracao
- `extract-img-api/` deve permanecer separado, porque hoje e outra API com outro escopo

## Contratos e Padroes

### Naming

Padrao obrigatorio:

- arquivo: `csv_to_json.py`
- funcao exportada: `convert_csv_to_json`
- chave do registro: `("csv", "json")`

Isso elimina divergencias como:

- `csv_to_markdown.py` vs import `csv_to_md`
- `html_to_markdown.py` vs import `html_to_md`
- `app.services.utils` vs import atual `app.utils`

### Erros padronizados

Criar erros de dominio em `app/core/errors.py`:

- `ConversionError`
- `UnsupportedConversionError`
- `InvalidInputError`
- `InvalidStructureError`
- `EncodingDetectionError`
- `DependencyUnavailableError`
- `InfrastructureBlockedError`

Mapeamento HTTP sugerido:

- `UnsupportedConversionError` -> `400`
- `InvalidInputError` -> `400`
- `InvalidStructureError` -> `422`
- `EncodingDetectionError` -> `400`
- `DependencyUnavailableError` -> `503`
- `InfrastructureBlockedError` -> `503`
- erro inesperado -> `500`

### Encodings

Centralizar politicas em utilitarios comuns:

- `decode_text_with_fallback`
- `decode_json_with_fallback`
- `read_csv_with_fallback`
- `normalize_line_endings`

Politica recomendada:

- tentar `utf-8`
- tentar `utf-8-sig`
- tentar `windows-1252`
- tentar `latin-1`
- falhar com mensagem clara

## Matriz de Conversoes

### Stable candidatas

Estas conversoes estao alinhadas com a proposta do produto e devem ser as primeiras a estabilizar:

| Conversao | Status alvo | Observacao |
| --- | --- | --- |
| `dta -> csv` | stable | forte aderencia ao projeto, depende de `pyreadstat` |
| `txt -> csv` | stable | simples e confiavel |
| `csv -> txt` | stable | simples e confiavel |
| `csv -> json` | stable | bom custo-beneficio |
| `json -> csv` | stable | exigir lista de objetos |
| `csv -> xml` | stable com limites | apenas estrutura tabular simples |
| `xml -> csv` | stable com limites | apenas XML repetitivo previsivel |
| `csv -> html` | stable | saida simples, leve |
| `html -> txt` | stable com limites | extracao de texto simples |
| `txt -> json` | stable | lista linear de linhas |
| `json -> txt` | stable | apenas lista linear |
| `txt -> xml` | stable | estrutura simples e previsivel |

### Beta

Estas conversoes sao uteis, mas precisam de integracao e testes antes de serem promovidas:

| Conversao | Status alvo | Observacao |
| --- | --- | --- |
| `csv -> xlsx` | beta -> stable | boa proposta, precisa integrar no contrato unico |
| `xlsx -> csv` | beta -> stable | boa proposta, precisa integrar no contrato unico |
| `csv -> md` | beta | hoje existe como utilitario bytes-only |
| `html -> md` | beta | parser simples, cobertura limitada |
| `json -> xml` | beta | precisa definir contrato de estrutura |
| `xml -> json` | beta | precisa definir comportamento para repeticao e atributos |
| `json -> yaml` | beta | serializer atual e simplificado |
| `csv -> sql` | beta | mais export do que conversao tradicional |

### Limited

Estas conversoes podem continuar existindo, mas devem ser comunicadas com escopo real:

| Conversao | Status alvo | Observacao |
| --- | --- | --- |
| `ifc -> csv` | limited | gera resumo de entidades, nao conversao integral |
| `ifc -> json` | limited | gera sumario e metadados basicos |
| `ifc -> html` | limited | relatorio resumido |
| `ifc -> txt` | limited | lista de entidades encontradas |

Recomendacao:

- no frontend e na documentacao, tratar essas rotas como `IFC summary/export`
- nao vender como conversao completa de modelo BIM

### Disabled ou infra-blocked

| Conversao | Status alvo | Observacao |
| --- | --- | --- |
| `csv -> dta` | infra_blocked | depende de ambiente com suporte real a pandas/pyreadstat |

Recomendacao:

- manter no codigo somente se entrar no registry com `status="infra_blocked"`
- remover do endpoint publico enquanto a infraestrutura nao mudar

## Fases de Execucao

### Fase 1 - Restaurar consistencia minima

Objetivo:

- fazer o projeto refletir corretamente o que realmente funciona

Entregas:

- corrigir imports quebrados no router
- alinhar nomes de arquivos e funcoes
- remover referencias a modulos inexistentes
- atualizar README para bater com o estado real da API

Criterio de saida:

- app sobe sem erro de import
- rota `/convert` carrega todos os handlers realmente suportados

### Fase 2 - Introduzir o novo contrato

Objetivo:

- criar a fundacao da arquitetura sem reescrever tudo de uma vez

Entregas:

- criar `ConversionContext`, `ConversionResult` e erros comuns
- criar registry central
- criar adapter temporario para handlers antigos baseados em caminho de arquivo
- permitir coexistencia controlada entre legacy e novo modelo

Criterio de saida:

- o endpoint passa a executar handlers via registry
- legacy e novos handlers convivem sem branchs manuais no router

### Fase 3 - Migrar familia por familia

Ordem sugerida:

1. tabular simples
2. texto
3. markup
4. xlsx
5. bim/ifc
6. formatos bloqueados por dependencia

Entregas:

- mover os handlers para `app/converters/`
- padronizar leitura de bytes
- padronizar `media_type` e extensao retornada
- eliminar escrita temporaria quando desnecessaria

Criterio de saida:

- todos os handlers ativos usam o mesmo contrato

### Fase 4 - Testes e classificacao oficial

Entregas:

- testes unitarios por conversor
- testes de integracao para `/convert`
- fixtures pequenas de exemplo
- classificacao formal no registry: `stable`, `beta`, `limited`, `infra_blocked`

Criterio de saida:

- cada conversao publica possui ao menos um teste de sucesso e um de falha esperada

### Fase 5 - Exposicao para frontend e documentacao

Entregas:

- endpoint opcional `GET /conversions`
- lista de conversoes com status e notas
- frontend passa a esconder ou marcar recursos beta/limitados
- README alinhado ao registry, nao a uma lista manual

Criterio de saida:

- documentacao e runtime exibem a mesma fonte de verdade

## Testes Recomendados

Criar uma matriz minima para cada conversao:

- arquivo valido
- arquivo vazio
- encoding alternativo
- estrutura invalida
- extensao incorreta
- round-trip quando aplicavel

Exemplos importantes:

- `json -> csv`: rejeitar objeto unico em vez de `list[dict]`
- `xml -> csv`: rejeitar XML sem estrutura repetitiva reconhecivel
- `csv -> json`: lidar com linhas com colunas faltantes
- `html -> txt`: ignorar markup e preservar texto legivel
- `csv -> xlsx -> csv`: validar integridade basica

## Decisoes de Produto

Para preservar a proposta do `conv`, a refatoracao deve evitar:

- dependencias pesadas sem necessidade clara
- suporte "meia-boca" a formatos complexos que vao gerar frustracao
- prometer conversao semantica quando o que existe e export/resumo

Prioridade de produto:

1. ser leve
2. ser previsivel
3. comunicar limitacoes com honestidade
4. expandir formatos so quando a base estiver coesa

## Backlog Tecnico Imediato

### Sprint 1

- corrigir `app.routes.convert` para refletir o estado real dos arquivos
- criar `app/core/models.py`
- criar `app/core/errors.py`
- criar `app/core/registry.py`
- registrar apenas conversoes realmente suportadas

### Sprint 2

- migrar `csv/json/txt/xml/html` para o novo contrato
- criar testes unitarios para essas familias
- marcar `csv -> dta` como `infra_blocked`

### Sprint 3

- migrar `xlsx`
- reclassificar `ifc` como `summary/export`
- expor `GET /conversions`

## Proximo Passo Recomendado

Se a execucao for comecar agora, a melhor sequencia pratica e:

1. corrigir a base para subir sem erros de import
2. criar o registry e os tipos comuns
3. adaptar primeiro as conversoes estaveis e simples
4. deixar formatos problematicos classificados, mas fora do caminho critico

Esse caminho entrega ganho rapido sem perder a identidade enxuta do projeto.
