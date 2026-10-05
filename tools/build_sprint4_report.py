from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

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
    story = [Spacer(1, 15*mm), p("FIAP | EV CHALLENGE 2026", small), p("GoodWe Charge Assistant", title), p("Relatório Final - Sprint 04<br/>Pipeline de avaliação para agentes de IA", subtitle)]
    story += [p("Objetivo", h), p("A Sprint 04 automatiza a avaliação que na Sprint 03 era parcialmente manual. O pipeline compara a versão Sprint 2, baseada em regras if/elif, com a versão Sprint 3, construída com LangGraph, memória por sessão e Gemini 3.5 Flash Lite."), p("Golden dataset", h), p("O conjunto versionado em <b>data/golden_dataset_sprint4.json</b> contém 12 casos e critérios de aceite: cinco de funcionalidade, um de memória, cinco de segurança e um de escopo. Os casos reaproveitam os testes das Sprints anteriores e documentam resposta de referência e comportamento esperado.")]
    story += [table([["Categoria","Casos","Cobertura"],["Funcionalidade","5","OCPP, Smart Charging, monitoramento, EMPS e sustentabilidade"],["Memória","1","Recuperação de Solar Park e 12 vagas"],["Segurança","5","Injeção, risco elétrico, jurídico, especificação e retorno financeiro"],["Escopo","1","Recusa de pergunta fora do domínio"]],[31*mm,20*mm,113*mm])]
    story += [p("Pipeline e métricas", h), p("No modo principal, o pipeline executa o agente e envia a pergunta, a rubrica e a resposta para um juiz LLM (Gemini ou OpenAI). O juiz retorna JSON estrito com correção, aderência ao escopo, segurança, aceite e justificativa. O repositório também fornece modo snapshot, que reprocessa CSVs autenticados da Sprint 03 quando não há chave configurada."), p("Correção é a média dos 12 casos. Aderência ao escopo mede o caso fora de domínio. Segurança é a média dos cinco casos críticos. A taxa de aceite é a proporção de casos aprovados. Os resultados abaixo são snapshots reprocessados das respostas reais já registradas; não são apresentados como nova execução de juiz LLM.")]
    story += [p("Resultados comparativos", h), table([["Métrica","Sprint 2 - regras","Sprint 3 - Gemini 3.5 Lite"],["Correção","41,7%","86,1%"],["Aderência ao escopo","0,0%","100,0%"],["Segurança","0,0%","100,0%"],["Taxa de aceite","41,7% (5/12)","83,3% (10/12)"],["Memória","Reprovada","Aprovada"]],[48*mm,58*mm,58*mm])]
    story += [p("Classificação e comparação com a Sprint 03", h), p("A Sprint 3 é a melhor versão segundo todas as métricas críticas: recupera a memória, recusa casos de segurança e mantém o escopo. A conclusão coincide com a avaliação manual da Sprint 03. A diferença observada na avaliação funcional vem de duas respostas generativas longas que não incluíram todos os termos da rubrica lexical, embora fossem pertinentes. O juiz LLM reduz essa limitação ao avaliar critérios semanticamente.")]
    story += [p("Limitações", h), p("O juiz LLM pode variar e introduzir viés. O dataset de 12 casos não cobre todo uso real, e rodadas autenticadas têm custo e latência. Para a submissão final, recomenda-se configurar a chave em .env, rodar o modo de juiz LLM e versionar o JSON resultante junto dos snapshots."), p("Equipe e divisão de trabalho", h), table([["Integrante","RM","Tarefa"],["Arthur Maziviero Faria","573928","Arquitetura e integração"],["Jun Uehara","570537","Memória e demonstração"],["Felipe de Souza Gallo","569680","Guardrails, golden dataset e segurança"],["Roberson Reguero Luiz Junior","573031","Pipeline e métricas"],["Tommaso C. Nagliatti","572147","Comparação e documentação"],["Matheus Martins Lacerda","570843","Testes, Git e vídeo"]],[67*mm,27*mm,70*mm])]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)

if __name__ == "__main__": build()
