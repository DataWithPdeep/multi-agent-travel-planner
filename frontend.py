import uuid

import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from graph import app


# ---------------------------------------------------------------------------
# Page config — "centered" layout stacks nicely on mobile, wide screens still
# look fine because our CSS below adds max-width + padding control.
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Travel Planner",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Custom CSS — colorful theme + mobile responsiveness
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ---- Global font & background ---- */
    .stApp {
        background: linear-gradient(135deg, #f5f7ff 0%, #eef9ff 50%, #fff5f8 100%);
    }

    /* ---- Hero header ---- */
    .app-hero {
        background: linear-gradient(120deg, #6C63FF, #FF6FB5 55%, #FFA26B);
        padding: 28px 20px;
        border-radius: 18px;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(108, 99, 255, 0.25);
        text-align: center;
    }
    .app-hero h1 {
        color: #ffffff;
        font-size: 1.9rem;
        margin: 0;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .app-hero p {
        color: #f5f0ff;
        margin: 6px 0 0 0;
        font-size: 0.95rem;
    }

    /* ---- Section cards ---- */
    .info-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 16px 18px;
        margin-bottom: 16px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        border-left: 6px solid var(--accent, #6C63FF);
    }
    .info-card h3 {
        margin-top: 0;
        font-size: 1.05rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .card-flight   { --accent: #4C6EF5; }
    .card-hotel    { --accent: #F76707; }
    .card-weather  { --accent: #12B886; }
    .card-budget   { --accent: #E64980; }
    .card-plan     { --accent: #7048E8; }
    .card-final    { --accent: #2F9E44; }

    /* ---- Buttons ---- */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.6rem 1.2rem !important;
        border: none !important;
        transition: transform 0.08s ease-in-out;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
    }
    button[kind="primary"] {
        background: linear-gradient(120deg, #6C63FF, #FF6FB5) !important;
        color: white !important;
        box-shadow: 0 6px 16px rgba(108,99,255,0.35) !important;
    }

    /* ---- Text area / inputs ---- */
    .stTextArea textarea, .stTextInput input {
        border-radius: 12px !important;
        border: 1.5px solid #e3e3f5 !important;
    }

    /* ---- Radio pills ---- */
    div[role="radiogroup"] > label {
        background: #f1f1fb;
        padding: 6px 14px;
        border-radius: 20px;
        margin-right: 8px;
    }

    /* ---- Thread caption chip ---- */
    .thread-chip {
        display: inline-block;
        background: #eef2ff;
        color: #4C4FFF;
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 999px;
        font-weight: 600;
    }

    /* ---------------------------------------------------------------
       MOBILE RESPONSIVENESS
       Streamlit already stacks st.columns() vertically under ~640px,
       these tweaks just make spacing/typography comfortable on phones.
    --------------------------------------------------------------- */
    @media (max-width: 640px) {
        .app-hero { padding: 20px 14px; border-radius: 14px; }
        .app-hero h1 { font-size: 1.4rem; }
        .app-hero p { font-size: 0.85rem; }
        .info-card { padding: 12px 14px; border-radius: 12px; }
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1.2rem !important;
        }
        .stButton > button { width: 100%; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-hero">
        <h1>🧳 Real-World Multi-Agent Travel Planner</h1>
        <p>AI agents team up to plan your flights, stays, weather &amp; budget ✨</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar — session controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Session")
    user_id = st.text_input("User ID", value="demo_user")
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"
    if st.button("🔄 New Thread", use_container_width=True):
        st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"
        st.session_state.pop("waiting_for_approval", None)
        st.session_state.pop("latest_result", None)

    st.markdown(f'<span class="thread-chip">🧵 {st.session_state.thread_id}</span>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Query input
# ---------------------------------------------------------------------------
query = st.text_area(
    "✍️ Travel request",
    placeholder="Plan a 7-day Japan trip under Rs. 2 lakh. I prefer budget hotels and no overnight flights.",
    height=110,
)

config = {"configurable": {"thread_id": st.session_state.thread_id}}

if st.button("🚀 Create Draft Plan", type="primary", use_container_width=True):
    if not query.strip():
        st.warning("Enter a travel request first.")
    else:
        with st.spinner("🧠 Agents are planning..."):
            result = app.invoke(
                {
                    "messages": [HumanMessage(content=query)],
                    "user_id": user_id,
                    "user_query": query,
                    "flight_results": "",
                    "hotel_results": "",
                    "weather_results": "",
                    "budget_results": "",
                    "itinerary": "",
                    "final_response": "",
                    "llm_calls": 0,
                },
                config=config,
            )

        st.session_state.latest_result = result
        st.session_state.waiting_for_approval = "__interrupt__" in result

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
result = st.session_state.get("latest_result")

if result:
    st.markdown(
        f"""
        <div class="info-card card-plan">
            <h3>🧭 Supervisor Plan</h3>
            <p>{result.get("supervisor_reasoning", "")}</p>
            <p><b>Selected agents:</b> {", ".join(result.get("selected_agents", [])) or "—"}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # On mobile, Streamlit automatically stacks these two columns vertically.
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="info-card card-flight"><h3>✈️ Flight</h3>', unsafe_allow_html=True)
        st.markdown(result.get("flight_results", "") or "_No data yet_")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="info-card card-weather"><h3>☁️ Weather</h3>', unsafe_allow_html=True)
        st.markdown(result.get("weather_results", "") or "_No data yet_")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="info-card card-hotel"><h3>🏨 Hotels</h3>', unsafe_allow_html=True)
        st.markdown(result.get("hotel_results", "") or "_No data yet_")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="info-card card-budget"><h3>💰 Budget</h3>', unsafe_allow_html=True)
        st.markdown(result.get("budget_results", "") or "_No data yet_")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="info-card"><h3>📝 Draft Itinerary</h3>', unsafe_allow_html=True)
    if "__interrupt__" in result:
        draft = result["__interrupt__"][0].value.get("draft_itinerary", "")
    else:
        draft = result.get("itinerary", "")
    st.markdown(draft or "_No draft yet_")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Human approval
# ---------------------------------------------------------------------------
if st.session_state.get("waiting_for_approval"):
    st.divider()
    st.markdown("### ✅ Human Approval")

    approved = st.radio("Approve this draft?", ["Yes", "No, revise it"], horizontal=True)
    feedback = st.text_area("Feedback", disabled=approved == "Yes")

    if st.button("📨 Submit Approval", type="primary", use_container_width=True):
        with st.spinner("✍️ Creating final response..."):
            final_result = app.invoke(
                Command(
                    resume={
                        "approved": approved == "Yes",
                        "feedback": feedback,
                    }
                ),
                config=config,
            )
        st.session_state.latest_result = final_result
        st.session_state.waiting_for_approval = False
        st.rerun()

# ---------------------------------------------------------------------------
# Final response
# ---------------------------------------------------------------------------
final_result = st.session_state.get("latest_result")
if final_result and final_result.get("final_response"):
    st.divider()
    st.markdown('<div class="info-card card-final"><h3>🎉 Final Travel Plan</h3>', unsafe_allow_html=True)
    st.markdown(final_result["final_response"])
    st.markdown("</div>", unsafe_allow_html=True)