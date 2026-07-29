from typing import TypedDict

from langgraph.graph import StateGraph, END

from services.summarizer import summarize_article


class ArticleState(TypedDict):
    text: str
    summary: str


def summarize_node(state):

    summary = summarize_article(
        state["text"]
    )

    return {
        "summary": summary
    }


graph = StateGraph(ArticleState)

graph.add_node(
    "summarize",
    summarize_node
)

graph.set_entry_point("summarize")

graph.add_edge(
    "summarize",
    END
)

workflow = graph.compile()