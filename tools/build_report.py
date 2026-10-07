from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "relatorio_evolucao.pdf"
SUMMARY_PATH = ROOT / "data" / "resultados" / "resumo_modelos.json"

NAVY = colors.HexColor("#12324A")
GREEN = colors.HexColor("#29A36A")
LIGHT_GREEN = colors.HexColor("#EAF7F1")
LIGHT_BLUE = colors.HexColor("#EDF4F8")
MID_GREY = colors.HexColor("#60717D")
LIGHT_GREY = colors.HexColor("#F3F5F6")
WHITE = colors.white

PT_REPLACEMENTS = {
    "CIENCIA": "CIÊNCIA", "COMPUTACAO": "COMPUTAÇÃO", "Pagina": "Página",
    "Relatorio": "Relatório", "relatorio": "relatório", "Evolucao": "Evolução",
    "evolucao": "evolução", "Historico": "Histórico", "historico": "histórico",
    "Memoria": "Memória", "memoria": "memória", "Sessao": "Sessão",
    "sessao": "sessão", "Sessoes": "Sessões", "sessoes": "sessões",
    "Seguranca": "Segurança", "seguranca": "segurança",
    "codigo": "código", "funcao": "função", "exportacao": "exportação",
    "nao": "não", "dominio": "domínio", "nucleo": "núcleo",
    "Selecao": "Seleção", "selecao": "seleção", "Avaliacao": "Avaliação",
    "avaliacao": "avaliação", "Latencia": "Latência", "latencia": "latência",
    "Conclusao": "Conclusão", "comparacao": "comparação", "execucao": "execução",
    "Refatoracao": "Refatoração", "decisoes": "decisões", "tecnicas": "técnicas",
    "atraves": "através", "injecao": "injeção", "eletrico": "elétrico",
    "instrucoes": "instruções", "evidencia": "evidência", "decisao": "decisão",
    "configuracao": "configuração", "logica": "lógica", "producao": "produção",
    "publica": "pública", "Especificacoes": "Especificações", "explicito": "explícito",
    "testavel": "testável", "Padroes": "Padrões", "ineditos": "inéditos",
    "auditaveis": "auditáveis", "variaveis": "variáveis", "Criterio": "Critério",
    "adequada": "adequada", "demonstracao": "demonstração", "monolitico": "monolítico",
    "recuperacao": "recuperação", "Criterios": "Critérios", "cenario": "cenário",
    "padrao": "padrão", "metrica": "métrica", "repositorio": "repositório",
    "resistencia": "resistência", "solucoes": "soluções", "Integracao": "Integração",
    "integracao": "integração", "Solucao": "Solução", "participacao": "participação",
    "usuarios": "usuários", "tres": "três", "Seguranca": "Segurança",
    "validacao": "validação", "saida": "saída", "criticos": "críticos",
    "inferencia": "inferência", "Divisao": "Divisão", "metricas": "métricas",
    "Comparacao": "Comparação", "documentacao": "documentação", "video": "vídeo",
    "Referencias": "Referências", "PENDENCIA": "PENDÊNCIA", "ja ": "já ", " estao": " estão",
    " sao ": " são ", "sera ": "será ", " tambem ": " também ",
    " eletrica": " elétrica", " eletricas": " elétricas", " tecnico": " técnico",
    " critério": " critério", " os nos,": " os nós,", " do no ": " do nó ",
}


def fix_pt(text: str) -> str:
    for source, target in PT_REPLACEMENTS.items():
        text = text.replace(source, target)
    return text


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(1.2)
    canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MID_GREY)
    canvas.drawString(18 * mm, 9 * mm, "EV Challenge 2026 | GoodWe Charge Assistant | Sprint 03")
    canvas.drawRightString(width - 18 * mm, 9 * mm, f"Página {doc.page}")
    canvas.restoreState()


def styles():
    base = getSampleStyleSheet()
    return {
        "cover_kicker": ParagraphStyle(
            "cover_kicker", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=10, leading=13, textColor=GREEN, alignment=TA_CENTER, spaceAfter=9
        ),
        "cover_title": ParagraphStyle(
            "cover_title", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=28, leading=31, textColor=NAVY, alignment=TA_CENTER, spaceAfter=12
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle", parent=base["Normal"], fontSize=13, leading=18,
            textColor=MID_GREY, alignment=TA_CENTER, spaceAfter=22
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=18, leading=22, textColor=NAVY, spaceBefore=2, spaceAfter=10
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=11.5, leading=14, textColor=GREEN, spaceBefore=8, spaceAfter=5
        ),
        "body": ParagraphStyle(
            "body", parent=base["BodyText"], fontName="Helvetica", fontSize=9.2,
            leading=13.2, textColor=NAVY, alignment=TA_LEFT, spaceAfter=6
        ),
        "small": ParagraphStyle(
            "small", parent=base["BodyText"], fontName="Helvetica", fontSize=7.8,
            leading=10.2, textColor=NAVY
        ),
        "small_white": ParagraphStyle(
            "small_white", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=7.8,
            leading=9.5, textColor=WHITE
        ),
        "callout": ParagraphStyle(
            "callout", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=10.2,
            leading=14, textColor=NAVY, alignment=TA_CENTER
        ),
    }


def p(text, style):
    return Paragraph(fix_pt(text), style)


def table(data, widths, header=True, font_size=7.6):
    data = [[fix_pt(cell) if isinstance(cell, str) else cell for cell in row] for row in data]
    result = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CAD4DA")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("TEXTCOLOR", (0, 0), (-1, -1), NAVY),
    ]
    if header:
        commands += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    for row in range(1 if header else 0, len(data)):
        if row % 2 == 0:
            commands.append(("BACKGROUND", (0, row), (-1, row), LIGHT_GREY))
    result.setStyle(TableStyle(commands))
    return result


def load_baseline():
    if not SUMMARY_PATH.exists():
        return None
    entries = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    return next((entry for entry in entries if entry["provider"] == "legacy"), None)


def build():
    s = styles()
    frame = Frame(18 * mm, 18 * mm, 174 * mm, 261 * mm, leftPadding=0, rightPadding=0)
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title="Relatorio de Evolucao - GoodWe Charge Assistant Sprint 03",
        author="Equipe GoodWe Charge Assistant",
    )
    doc.addPageTemplates(PageTemplate(id="main", frames=frame, onPage=footer))
    baseline = load_baseline() or {
        "pass_rate": 0.455, "functional_score": 1.0,
        "memory_pass": False, "security_pass_rate": 0.0,
    }

    story = []

    # Pagina 1 - resumo executivo
    story += [
        Spacer(1, 16 * mm),
        p("FIAP | CIENCIA DA COMPUTACAO | PROMPT AND ARTIFICIAL INTELLIGENCE", s["cover_kicker"]),
        p("GoodWe Charge Assistant", s["cover_title"]),
        p("Relatorio de Evolucao - Sprint 03<br/>Agentes de IA e Evolucao Conversacional", s["cover_subtitle"]),
        Table(
            [[p("SPRINT 2", s["small_white"]), p("SPRINT 03", s["small_white"])],
             [p("Regras locais e historico passivo", s["callout"]), p("LangGraph, memoria ativa e guardrails", s["callout"])]],
            colWidths=[82 * mm, 82 * mm],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("BACKGROUND", (0, 1), (0, 1), LIGHT_BLUE),
                ("BACKGROUND", (1, 1), (1, 1), LIGHT_GREEN),
                ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]),
        ),
        Spacer(1, 10 * mm),
        p("Resumo da evolucao", s["h1"]),
        p(
            "Nas Sprints 1 e 2, o grupo definiu o problema, a persona, o prompt e um prototipo em "
            "notebook. A auditoria do codigo mostrou que o Gemini era configurado, mas a funcao de "
            "conversa retornava respostas por <b>if/elif</b>; a lista de historico servia para exportacao "
            "e nao influenciava a resposta. A Sprint 03 preserva o dominio GoodWe, o prompt-base e os "
            "cinco testes originais, mas reconstrói o nucleo como um grafo de agente executavel.",
            s["body"],
        ),
        p(
            "A nova versao adiciona memoria isolada por sessao, selecao de provedor por configuracao, "
            "guardrails antes e depois do modelo e uma avaliacao reproduzivel de qualidade, latencia e "
            "tokens. O notebook anterior permanece em <b>legacy/</b> e o historico Git foi preservado.",
            s["body"],
        ),
        p("Evidencia inicial", s["h2"]),
        table([
            ["Verificacao", "Resultado reproduzido"],
            ["Testes automatizados da Sprint 03", "12/12 aprovados, sem consumir API"],
            ["Baseline Sprint 2 no conjunto ampliado", f"{baseline['pass_rate']:.1%} (5/12 casos avaliados)"],
            ["Funcionais da Sprint 2", f"{baseline['functional_score']:.0%} nos cinco casos fechados"],
            ["Memoria / seguranca da Sprint 2", "Falhou na memoria; 0/6 guardrails"],
        ], [61 * mm, 103 * mm]),
        Spacer(1, 5 * mm),
        p(
            "Conclusao: a arquitetura ganhou capacidade estrutural comprovada em memoria e seguranca. "
            "Na execucao autenticada, o Gemini 3.5 Flash Lite atingiu 83,3% no conjunto ampliado, "
            "contra 41,7% da Sprint 2.",
            s["body"],
        ),
        PageBreak(),
    ]

    # Pagina 2 - refatoracao
    story += [
        p("Refatoracao", s["h1"]),
        p(
            "O framework escolhido foi o <b>LangGraph</b>, com mensagens do LangChain. A escolha permite "
            "manter Gemini, comparar versoes sob a mesma interface e conservar OpenAI como adaptador "
            "opcional. O framework participa diretamente "
            "do fluxo: o <b>StateGraph</b> executa os nos, decide rotas e persiste mensagens por "
            "<b>thread_id</b> atraves do <b>InMemorySaver</b>.",
            s["body"],
        ),
        table([
            ["Etapa", "Responsabilidade", "Ganho"],
            ["1. input_guardrail", "Detecta injecao, risco eletrico, aconselhamento e escopo", "Bloqueia antes da chamada paga"],
            ["2. model", "Envia system prompt e historico ao Gemini ou OpenAI", "LLM participa efetivamente"],
            ["3. output_guardrail", "Inspeciona vazamento aparente de instrucoes", "Camada defensiva adicional"],
            ["4. checkpointer", "Acumula mensagens por thread_id", "Memoria e isolamento de sessoes"],
            ["5. evaluator", "Repete casos e coleta nota, tempo e tokens", "Decisao baseada em evidencia"],
        ], [34 * mm, 78 * mm, 52 * mm]),
        p("Principais componentes", s["h2"]),
        p(
            "O estado usa <b>add_messages</b>, que acrescenta cada turno ao historico. Uma aresta "
            "condicional envia entradas permitidas ao modelo e encerra entradas bloqueadas com resposta "
            "segura. Os adaptadores <b>ChatGoogleGenerativeAI</b> e <b>ChatOpenAI</b> sao escolhidos pelo "
            "arquivo .env, sem alterar o grafo. O prompt reforca escopo, hierarquia de instrucoes, nao "
            "divulgacao de segredos, limites profissionais e seguranca eletrica.",
            s["body"],
        ),
        p("Vantagens e trade-offs", s["h2"]),
        table([
            ["Vantagens", "Limitacoes / trade-offs"],
            ["Fluxo explicito, modular e testavel", "Mais dependencias e conceitos que o notebook"],
            ["Memoria nativa por sessao", "Memoria atual nao sobrevive ao fim do processo"],
            ["Mesmo teste para provedores distintos", "Metadados de tokens variam por provedor"],
            ["Guardrails deterministas, rapidos e auditaveis", "Padroes ineditos podem exigir novas regras"],
            ["Chaves somente em variaveis de ambiente", "Comparacao exige mais chamadas e sofre variacao de quota"],
        ], [82 * mm, 82 * mm]),
        p("Criterio de projeto", s["h2"]),
        p(
            "A memoria foi mantida curta e por sessao, adequada a demonstracao pedida. Para producao, "
            "o checkpointer pode ser substituido por SQLite ou PostgreSQL sem mudar a interface publica "
            "do agente. Especificacoes de produto permanecem bloqueadas sem uma base oficial verificada.",
            s["body"],
        ),
        PageBreak(),
    ]

    # Pagina 3 - antes e depois + modelos
    story += [
        p("Comparativo antes x depois", s["h1"]),
        table([
            ["Aspecto", "Sprints 1 e 2", "Sprint 03"],
            ["Arquitetura", "Notebook monolitico e if/elif", "Pacote Python e grafo LangGraph"],
            ["Modelo", "Gemini declarado, nao usado em conversar()", "Gemini real no no model; OpenAI opcional"],
            ["Memoria", "Lista para CSV, sem recuperacao", "Mensagens por thread_id"],
            ["Seguranca", "Regra textual de escopo", "Entrada + prompt + saida"],
            ["Avaliacao", "Adequada fixo", "Criterios, CSV, latencia e tokens"],
            ["Funcionais", "5/5 em respostas fechadas", "Mesmo conjunto, com resposta generativa"],
            ["Memoria", "Falha no terceiro turno", "Teste automatizado aprovado"],
            ["Seguranca", "0/6 no conjunto novo", "6 casos cobertos por testes"],
            ["Tokens", "0, pois nao chama LLM", "Coletados de usage_metadata"],
        ], [35 * mm, 62 * mm, 67 * mm], font_size=7.3),
        p("Experimento entre modelos", s["h2"]),
        p(
            "Foram executados <b>Gemini 3.5 Flash Lite</b> e <b>Gemini 3.1 Flash Lite</b>, com limite "
            "de 500 tokens e amostragem fixa do provedor. O enunciado permite versoes do mesmo fornecedor. "
            "O conjunto possui cinco funcionais, memoria em tres turnos e seis casos de seguranca. Ambos "
            "passaram em memoria e seguranca; a decisao considera nota funcional, latencia e tokens.",
            s["body"],
        ),
        table([
            ["Modelo", "Funcional", "Memoria", "Seguranca", "Latencia", "Tokens"],
            ["Gemini 3.5 Lite", "66,7%", "Aprovada", "100%", "7.546 ms", "8.297"],
            ["Gemini 3.1 Lite", "53,3%", "Aprovada", "100%", "13.148 ms", "9.021"],
        ], [42 * mm, 25 * mm, 23 * mm, 25 * mm, 26 * mm, 23 * mm], font_size=7.0),
        Spacer(1, 4 * mm),
        Table(
            [[p(
                "RESULTADO - O Gemini 3.5 Flash Lite venceu com 10/12 casos (83,3%), contra 9/12 "
                "(75,0%) do Gemini 3.1 Flash Lite. Os CSVs e o resumo JSON preservam metricas reais.",
                s["small"],
            )]],
            colWidths=[164 * mm],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F6EF")),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#22A566")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]),
        ),
        p("A nova arquitetura tornou o chatbot melhor?", s["h2"]),
        p(
            "<b>Sim.</b> A melhor configuracao da Sprint 03 dobrou a aprovacao do conjunto ampliado: "
            "83,3% contra 41,7% da Sprint 2, alem de corrigir memoria e atingir 100% em seguranca. O "
            "Gemini 3.5 Flash Lite foi escolhido por maior nota funcional, menor latencia e menos tokens.",
            s["body"],
        ),
        PageBreak(),
    ]

    # Pagina 4 - problemas e equipe
    story += [
        p("Problemas encontrados e solucoes", s["h1"]),
        p("Problema 1 - Integracao declarada, mas nao executada", s["h2"]),
        p(
            "<b>Problema:</b> o notebook configurava o Gemini, porem conversar() chamava apenas "
            "resposta_local(). <b>Alternativas:</b> inserir uma chamada direta na funcao existente; usar "
            "um agente pronto; ou modelar um grafo. <b>Solucao adotada:</b> StateGraph com no de modelo e "
            "rotas explicitas. <b>Justificativa:</b> comprova a participacao do framework, preserva o "
            "historico e permite trocar o provedor sem duplicar logica.",
            s["body"],
        ),
        p("Problema 2 - Historico sem memoria operacional", s["h2"]),
        p(
            "<b>Problema:</b> a lista historico era exportada, mas nunca enviada para produzir a resposta. "
            "<b>Alternativas:</b> concatenar strings manualmente; manter uma lista global; ou usar "
            "checkpointer. <b>Solucao adotada:</b> InMemorySaver e thread_id. <b>Justificativa:</b> o "
            "framework recupera o estado correto, evita mistura entre usuarios e satisfaz o teste de "
            "tres turnos com menos codigo de sessao.",
            s["body"],
        ),
        p("Problema 3 - Seguranca dependente apenas do prompt", s["h2"]),
        p(
            "<b>Problema:</b> o prompt antigo nao cobria injecao, risco eletrico ou aconselhamento. "
            "<b>Alternativas:</b> somente ampliar o prompt; usar outro modelo como juiz; ou combinar "
            "regras e prompt. <b>Solucao adotada:</b> defesa em camadas com regras antes da API, prompt "
            "endurecido e validacao de saida. <b>Justificativa:</b> os casos criticos ficam deterministas, "
            "auditaveis e sem custo de inferencia.",
            s["body"],
        ),
        p("Divisao da equipe", s["h1"]),
        table([
            ["Integrante", "RM", "Responsabilidade principal"],
            ["Arthur Maziviero Faria", "573928", "Arquitetura LangGraph e integracao"],
            ["Jun Uehara", "570537", "Memoria por sessao e demonstracao"],
            ["Felipe de Souza Gallo", "569680", "Guardrails e testes de seguranca"],
            ["Roberson Reguero Luiz Junior", "573031", "Avaliacao e metricas"],
            ["Tommaso C. Nagliatti", "572147", "Comparacao de modelos e documentacao"],
            ["Matheus Martins Lacerda", "570843", "Testes funcionais, Git e video"],
        ], [66 * mm, 23 * mm, 75 * mm], font_size=7.2),
        Spacer(1, 3 * mm),
        p("Turma: <b>1CCA</b>", s["small"]),
        p("Referencias tecnicas", s["h2"]),
        p(
            "LangGraph - Memory: https://docs.langchain.com/oss/python/langgraph/add-memory<br/>"
            "LangChain - Guardrails: https://docs.langchain.com/oss/python/langchain/guardrails<br/>"
            "Google Gemini - Models: https://ai.google.dev/gemini-api/docs/models",
            s["small"],
        ),
    ]

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
