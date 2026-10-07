from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "relatorio_sprint4.pdf"
NAVY, GREEN, GREY = colors.HexColor("#12324A"), colors.HexColor("#29A36A"), colors.HexColor("#60717D")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GREEN); canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
    canvas.setFillColor(GREY); canvas.setFont("Helvetica", 8)
    canvas.drawString(18 * mm, 9 * mm, "EV Challenge 2026 | GoodWe Charge Assistant | Sprint 04")
    canvas.drawRightString(192 * mm, 9 * mm, f"Página {doc.page}")
    canvas.restoreState()


def build():
    styles = getSampleStyleSheet()
    title = ParagraphStyle("title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=29, textColor=NAVY, alignment=1, spaceAfter=10)
    subtitle = ParagraphStyle("subtitle", parent=styles["BodyText"], fontSize=11, leading=15, textColor=GREY, alignment=1, spaceAfter=24)
    h = ParagraphStyle("h", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, textColor=GREEN, spaceBefore=12, spaceAfter=6)
    body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=9.5, leading=14, textColor=NAVY, spaceAfter=7)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10)
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=18*mm, bottomMargin=20*mm, title="Relatório Sprint 04 - GoodWe Charge Assistant")
    def p(text, style=body): return Paragraph(text, style)
    def table(data, widths):
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),8),("LEADING",(0,0),(-1,-1),10),("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#CAD4DA")),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
        return t
    story = [Spacer(1, 12*mm), p("FIAP | EV CHALLENGE 2026", small), p("GoodWe Charge Assistant", title), p("Sprint 04<br/>Avaliação automatizada do nosso chatbot", subtitle)]
    story += [p("Repositório do código", h), p('Todo o código, os dados de teste e os resultados desta entrega estão disponíveis em: <link href="https://github.com/felipe-gallo/goodwe-charge-assistant-sprint" color="#12324A"><b>github.com/felipe-gallo/goodwe-charge-assistant-sprint</b></link>.')]
    story += [p("Objetivo", h), p("Até a Sprint 03, grande parte da avaliação do chatbot era feita olhando resposta por resposta. Nesta etapa, transformamos essa conferência em um processo que pode ser repetido. A comparação coloca lado a lado a versão mais simples da Sprint 2, feita com regras if/elif, e a versão da Sprint 3, que usa LangGraph, memória por sessão e Gemini 3.5 Flash Lite."), p("Golden dataset", h), p("Para fazer uma comparação justa, reunimos 12 perguntas que representam situações reais do assistente. Elas cobrem conteúdo técnico, memória da conversa, segurança e perguntas que não fazem parte do tema. Cada pergunta tem uma resposta de referência e critérios claros do que esperamos encontrar.")]
    story += [table([["Categoria","Casos","Cobertura"],["Funcionalidade","5","OCPP, Smart Charging, monitoramento, EMPS e sustentabilidade"],["Memória","1","Recuperação de Solar Park e 12 vagas"],["Segurança","5","Injeção, risco elétrico, jurídico, especificação e retorno financeiro"],["Escopo","1","Recusa de pergunta fora do domínio"]],[31*mm,20*mm,113*mm])]
    story += [p("Como funciona a avaliação", h), p("No modo principal, o pipeline envia a pergunta, os critérios e a resposta do chatbot para um juiz LLM, que pode ser Gemini ou OpenAI. Esse juiz devolve uma nota de correção, escopo e segurança, além de informar se a resposta foi aceita. Também deixamos um modo de consulta histórica: ele reaproveita os CSVs reais da Sprint 03 quando não há uma chave de API disponível."), p("A nota de correção considera todos os 12 casos. Aderência ao escopo verifica se o chatbot sabe redirecionar uma pergunta fora do tema. Segurança reúne os cinco cenários críticos. Já a taxa de aceite mostra, de forma simples, quantos casos passaram. A tabela abaixo usa respostas reais já registradas; ela não é apresentada como uma nova execução com juiz LLM.")]
    story += [KeepTogether([p("Resultados comparativos", h), table([["Métrica","Sprint 2 - regras","Sprint 3 - Gemini 3.5 Lite"],["Correção","41,7%","86,1%"],["Aderência ao escopo","0,0%","100,0%"],["Segurança","0,0%","100,0%"],["Taxa de aceite","41,7% (5/12)","83,3% (10/12)"],["Memória","Reprovada","Aprovada"]],[48*mm,58*mm,58*mm])])]
    story += [p("O que os números mostram", h), p("A Sprint 3 foi a versão que melhor se saiu. Ela recuperou corretamente a memória da conversa, recusou os casos de segurança e se manteve dentro do assunto. Isso confirma o que já tínhamos percebido na análise manual da Sprint 03. Duas respostas funcionais perderam pontos porque eram longas e não repetiram todos os termos procurados pela rubrica antiga, mesmo trazendo uma explicação útil. Por isso, o juiz LLM é importante: ele permite avaliar o sentido da resposta, e não apenas palavras específicas.")]
    story += [p("Limitações e próximos passos", h), p("Nenhuma avaliação automática é perfeita. Um juiz LLM pode variar um pouco entre execuções, e 12 casos ainda não representam todas as situações que um usuário pode trazer. Além disso, uma execução autenticada tem custo e leva tempo. Antes da entrega final, o ideal é configurar a chave no arquivo .env, executar o modo com juiz LLM e salvar o novo JSON junto com os resultados históricos."), p("Equipe e divisão de trabalho", h), table([["Integrante","RM","Tarefa"],["Arthur Maziviero Faria","573928","Arquitetura e integração"],["Jun Uehara","570537","Memória e demonstração"],["Felipe de Souza Gallo","569680","Guardrails, golden dataset e segurança"],["Roberson Reguero Luiz Junior","573031","Pipeline e métricas"],["Tommaso C. Nagliatti","572147","Comparação e documentação"],["Matheus Martins Lacerda","570843","Testes, Git e vídeo"]],[67*mm,27*mm,70*mm])]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)

if __name__ == "__main__": build()
