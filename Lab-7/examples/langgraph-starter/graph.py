from langgraph.graph import StateGraph, START, END

from state import AgentState
from nodes import (
    research_node,
    write_node,
    human_review_node,
    finalize_without_review,
    route_after_write,
)


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("research", research_node)
    builder.add_node("write", write_node)
    builder.add_node("human_review", human_review_node)
    builder.add_node("finalize", finalize_without_review)

    builder.add_edge(START, "research")
    builder.add_edge("research", "write")
    builder.add_conditional_edges(
        "write",
        route_after_write,
        {
            "human_review": "human_review",
            "finalize": "finalize",
        },
    )
    builder.add_edge("human_review", END)
    builder.add_edge("finalize", END)

    return builder.compile()
