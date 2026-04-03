"""Build the LangGraph graph for Kitsune."""

from langgraph.graph import END, StateGraph

from kitsune.graph.nodes import ask_node, explain_node, fallback_node
from kitsune.graph.router import get_next_node, route
from kitsune.graph.state import KitsuneState


def build_graph():
    graph = StateGraph(KitsuneState)

    graph.add_node("router", route)
    graph.add_node("explain", explain_node)
    graph.add_node("ask", ask_node)
    graph.add_node("fallback", fallback_node)

    graph.set_entry_point("router")
    graph.add_conditional_edges(
        "router",
        get_next_node,
        {"explain": "explain", "ask": "ask", "fallback": "fallback"},
    )
    graph.add_edge("explain", END)
    graph.add_edge("ask", END)
    graph.add_edge("fallback", END)

    return graph.compile()


app = build_graph()
