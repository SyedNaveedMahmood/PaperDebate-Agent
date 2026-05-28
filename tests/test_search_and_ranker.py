from paperdebate_agent.retrieval.ranker import rank_papers
from paperdebate_agent.search import offline_search, stable_id


def test_stable_id_is_deterministic() -> None:
    title = "A Test Paper About Agents"
    assert stable_id(title) == stable_id(title)
    assert stable_id(title).startswith("a-test-paper-about-agents")


def test_offline_search_returns_papers() -> None:
    papers = offline_search("sparse autoencoders privacy", max_papers=2)
    assert len(papers) == 2
    assert all(p.paper_id for p in papers)
    assert all(p.source == "offline_stub" for p in papers)


def test_rank_papers_orders_relevant_items() -> None:
    papers = offline_search("sparse autoencoders privacy", max_papers=5)
    ranked = rank_papers(papers, topic="sparse autoencoders privacy")
    assert ranked[0].score >= ranked[-1].score
    assert ranked[0].paper.title
