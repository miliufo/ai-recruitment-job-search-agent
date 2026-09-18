from langgraph.graph import StateGraph, START, END

from app.graph.state import RecruitmentState
from app.graph.nodes import (
    retrieval_node,
    matching_node,
    ranking_node,
)


def build_recruitment_graph():
    """
    Build the production-style AI recruitment workflow.

    Workflow:

    Candidate Profile
          ↓
    Semantic Job Retrieval
          ↓
    LLM Job Matching
          ↓
    Hybrid Ranking
          ↓
    Final Ranked Jobs
    """

    builder = StateGraph(RecruitmentState)

    # Register workflow nodes
    builder.add_node("retrieve_jobs", retrieval_node)
    builder.add_node("match_jobs", matching_node)
    builder.add_node("rank_jobs", ranking_node)

    # Define execution flow
    builder.add_edge(START, "retrieve_jobs")
    builder.add_edge("retrieve_jobs", "match_jobs")
    builder.add_edge("match_jobs", "rank_jobs")
    builder.add_edge("rank_jobs", END)

    return builder.compile()


# Compiled graph used by API, UI and services
recruitment_graph = build_recruitment_graph()