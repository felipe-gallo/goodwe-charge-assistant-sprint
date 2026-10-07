from goodwe_agent.sprint4_evaluation import ROOT, evaluate_snapshot, parse_judgement


def test_snapshot_historico_reprocessa_doze_casos():
    records, summary = evaluate_snapshot(
        ROOT / "data" / "resultados" / "resultados_legacy_regras-if-elif-sprint2.csv",
        "sprint2-historico",
    )

    assert len(records) == 12
    assert summary["cases"] == 12
    assert summary["acceptance_rate"] == 0.417
    assert summary["safety"] == 0.0


def test_juiz_exige_json_com_metricas_limitadas():
    judgement = parse_judgement(
        '{"correctness": 1.3, "scope_adherence": -0.2, "safety": 0.8, '
        '"accepted": true, "rationale": "Resposta adequada."}'
    )

    assert judgement.correctness == 1.0
    assert judgement.scope_adherence == 0.0
    assert judgement.safety == 0.8
    assert judgement.accepted is True
