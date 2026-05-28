from paperdebate_agent.pipelines.run import run_pipeline


def test_pipeline_returns_ranked_papers_and_gaps() -> None:
    result = run_pipeline(
        topic="LLM unlearning with representation-level diagnostics",
        direction="internal metrics and reviewer risk",
        max_papers=3,
    )

    assert result.topic == "LLM unlearning with representation-level diagnostics"
    assert len(result.ranked_papers) == 3
    assert len(result.debate) >= 3
    assert len(result.gaps) >= 1
    assert result.gaps[0].evidence_ids


def test_pipeline_rejects_empty_topic() -> None:
    try:
        run_pipeline(topic="   ")
    except ValueError as exc:
        assert "topic" in str(exc)
    else:
        raise AssertionError("empty topic should raise ValueError")
