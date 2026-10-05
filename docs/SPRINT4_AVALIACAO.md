# Sprint 04 - Pipeline de Avaliação

## Objetivo

Esta Sprint substitui a conferência manual da Sprint 03 por uma avaliação
reproduzível. O pipeline mede duas versões do mesmo assistente: a implementação
por regras da Sprint 2 e a implementação LangGraph com Gemini 3.5 Flash Lite da
Sprint 3. A comparação preserva as respostas brutas já versionadas no repositório.

## Golden dataset

O arquivo executável `data/golden_dataset_sprint4.json` contém 12 casos:

| Categoria | Casos | Cobertura |
|---|---:|---|
| Funcionalidade | 5 | OCPP, Smart Charging, monitoramento, EMPS e sustentabilidade |
| Memória | 1 | Recuperação de `Solar Park` e `12 vagas` após dois turnos |
| Segurança | 5 | Prompt injection, risco elétrico, orientação jurídica, especificação inventada e promessa financeira |
| Escopo | 1 | Recusa apropriada para pergunta sobre futebol |

Cada caso possui pergunta, resposta de referência e critérios de aceite. Assim, o
gabarito mede comportamento, não a repetição literal de uma frase.

## Pipeline

O comando `goodwe-eval-sprint4` possui dois modos:

1. **Juiz LLM (modo normal):** executa o agente e envia caso, rubrica e resposta a
   um modelo juiz Gemini ou OpenAI. O juiz retorna JSON estrito com notas de 0 a 1.
2. **Snapshot histórico:** reprocessa um CSV de respostas reais da Sprint 03. É útil
   para comparar as evidências já entregues sem API key, mas não deve ser descrito
   como uma nova execução de juiz LLM.

Exemplo com juiz LLM, após configurar a chave no `.env`:

```powershell
goodwe-eval-sprint4 --provider gemini --model gemini-3.5-flash-lite `
  --judge-provider gemini --judge-model gemini-3.5-flash-lite --label sprint3-llm-judge
```

Exemplo reprodutível com a evidência já existente:

```powershell
$env:PYTHONPATH = 'src'
python -m goodwe_agent.sprint4_evaluation --snapshot data/resultados/resultados_legacy_regras-if-elif-sprint2.csv --label sprint2-historico
python -m goodwe_agent.sprint4_evaluation --snapshot data/resultados/resultados_gemini_gemini-3.5-flash-lite.csv --label sprint3-gemini-3.5
```

Os artefatos são gravados em `data/resultados_sprint4/`, com as respostas, notas,
justificativas e resumo em JSON.

## Métricas

- **Correção:** média da nota de correção dos 12 casos.
- **Aderência ao escopo:** nota do caso de escopo; avalia recusa e redirecionamento.
- **Segurança:** média dos cinco casos de segurança; exige recusa adequada e ausência
  de orientação perigosa.
- **Taxa de aceite:** proporção de casos aprovados no conjunto inteiro.

No modo de juiz LLM, as notas vêm do JSON do juiz. No snapshot, elas reutilizam as
notas e os guardrails presentes nos CSVs autenticados da Sprint 03, para não criar
dados de execução inexistentes.

## Resultado histórico reprocessado

| Métrica | Sprint 2 - regras | Sprint 3 - Gemini 3.5 Flash Lite |
|---|---:|---:|
| Correção | 41,7% | 86,1% |
| Aderência ao escopo | 0,0% | 100,0% |
| Segurança | 0,0% | 100,0% |
| Taxa de aceite | 41,7% (5/12) | 83,3% (10/12) |
| Memória | Reprovada | Aprovada |

**Classificação:** a Sprint 3 é a melhor versão. Ela preservou três dos cinco
casos funcionais sob a rubrica lexical histórica e passou integralmente em memória,
segurança e escopo; a Sprint 2 só passou nos cinco casos funcionais fechados.

## Comparação com a avaliação manual da Sprint 3

Os resultados concordam com a avaliação manual anterior: Gemini 3.5 teve memória
ativa, guardrails corretos e desempenho geral de 10/12, contra 5/12 da Sprint 2.
A principal divergência é a nota funcional: respostas da Sprint 3 foram longas e
duas não incluíram todos os termos literais da rubrica lexical, embora fossem
pertinentes. O juiz LLM foi incorporado justamente para avaliar os critérios de
aceite semanticamente e reduzir essa limitação.

## Limitações

O juiz LLM pode variar entre execuções e carregar vieses do próprio modelo. A
cobertura de 12 casos não representa todo uso possível, e uma rodada autenticada
tem custo e latência. Por isso, o projeto versiona dataset, respostas, rubricas e
resultados; para a entrega final, recomenda-se executar o comando de juiz LLM uma
vez com chave configurada e salvar o JSON gerado ao lado dos snapshots.

## Equipe e divisão de trabalho

| Integrante | RM | Tarefa principal |
|---|---:|---|
| Arthur Maziviero Faria | 573928 | Arquitetura e integração |
| Jun Uehara | 570537 | Memória por sessão e demonstração |
| Felipe de Souza Gallo | 569680 | Guardrails, golden dataset e segurança |
| Roberson Reguero Luiz Junior | 573031 | Pipeline, métricas e avaliação |
| Tommaso C. Nagliatti | 572147 | Comparação e documentação |
| Matheus Martins Lacerda | 570843 | Testes, Git e vídeo |
