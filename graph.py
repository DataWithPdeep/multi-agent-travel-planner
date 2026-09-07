import psycopg
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph

from agent import (
    budget_agent,
    final_response_agent,
    flight_agent,
    hotel_agent,
    human_approval_agent,
    itinerary_agent,
    supervisor_agent,
    weather_agent,
)

from config import DATABASE_URL
from state import TravelState


def build_graph():

    graph = StateGraph(TravelState)

    # =========================
    # NODES
    # =========================

    graph.add_node("supervisor", supervisor_agent)

    graph.add_node("flight_agent", flight_agent)
    graph.add_node("hotel_agent", hotel_agent)
    graph.add_node("weather_agent", weather_agent)

    graph.add_node("budget_agent", budget_agent)
    graph.add_node("itinerary_agent", itinerary_agent)

    graph.add_node("human_approval", human_approval_agent)
    graph.add_node("final_response", final_response_agent)

    # =========================
    # START
    # =========================

    graph.add_edge(START, "supervisor")

    # =========================
    # PARALLEL AGENTS
    # =========================
    #
    # Supervisor ke baad ye 3 agents
    # parallel execute honge.
    #

    graph.add_edge("supervisor", "flight_agent")
    graph.add_edge("supervisor", "hotel_agent")
    graph.add_edge("supervisor", "weather_agent")

    # =========================
    # BUDGET
    # =========================
    #
    # Budget ko Flight + Hotel + Weather
    # ke results chahiye.
    #
    # Isliye Budget in teenon ke baad chalega.
    #

    graph.add_edge("flight_agent", "budget_agent")
    graph.add_edge("hotel_agent", "budget_agent")
    graph.add_edge("weather_agent", "budget_agent")

    # =========================
    # ITINERARY
    # =========================

    graph.add_edge("budget_agent", "itinerary_agent")

    # =========================
    # HUMAN APPROVAL
    # =========================

    graph.add_edge("itinerary_agent", "human_approval")

    # =========================
    # FINAL RESPONSE
    # =========================

    graph.add_edge("human_approval", "final_response")

    graph.add_edge("final_response", END)

    # =========================
    # POSTGRES CHECKPOINTER
    # =========================

    # =========================
    # POSTGRES CHECKPOINTER
    # =========================
    
        if DATABASE_URL:
        
            conn = psycopg.connect(
                DATABASE_URL,
                autocommit=True
            )
        
            checkpointer = PostgresSaver(conn)
        
            checkpointer.setup()
        
            return graph.compile(
                checkpointer=checkpointer
            )

            return graph.compile()

app = build_graph()
