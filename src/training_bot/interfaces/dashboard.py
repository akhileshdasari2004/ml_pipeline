import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import asyncio
import time
from typing import Any, List
from datetime import datetime
from training_bot import TrainingDataBot
from training_bot.config.constants import TaskType, SourceType, ExportFormat
from training_bot.models.task import TaskTemplate

# --- UI Configuration & Styling ---
st.set_page_config(
    page_title="TrainingBot",
    page_icon="🕶️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Cyber Dark Glassmorphism CSS
st.markdown("""
<style>
    /* Dark Theme Base */
    .stApp {
        background: radial-gradient(circle at top right, #1a1c2c, #0d0e12);
        color: #e0e0e0;
    }
    
    /* Cyber Glass Containers */
    div.stMetric, .stTabs [data-baseweb="tab-panel"], [data-testid="stExpander"] {
        background: rgba(30, 32, 48, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(0, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(13, 14, 18, 0.95) !important;
        border-right: 1px solid rgba(0, 255, 255, 0.1);
    }
    
    /* Cyber Buttons */
    .stButton>button {
        border-radius: 10px;
        border: 1px solid #00f2ff;
        background: rgba(0, 242, 255, 0.05);
        color: #00f2ff;
        font-weight: bold;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background: rgba(0, 242, 255, 0.2);
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
        transform: scale(1.02);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00f2ff !important;
        font-family: 'Inter', sans-serif;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00f2ff !important;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border: 1px solid rgba(0, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        color: #888;
    }
    .stTabs [aria-selected="true"] {
        color: #00f2ff !important;
        border-bottom-color: #00f2ff !important;
    }
    
    /* Hide some Streamlit defaults for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'bot' not in st.session_state:
    st.session_state.bot = TrainingDataBot()
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'last_action' not in st.session_state:
    st.session_state.last_action = None

bot = st.session_state.bot

def log_event(msg: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({"time": timestamp, "msg": msg, "level": level})


# --- Header Section ---
with st.container():
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("TrainingBot")
        st.caption("Next-gen enterprise workflow in stealth mode.")
    with c2:
        st.write("") # Spacer
        if st.button("🔄 Reboot System"):
            st.session_state.bot = TrainingDataBot()
            st.session_state.logs = []
            st.rerun()

st.markdown("---")

# --- Dashboard Overview Metrics ---
stats = bot.get_stats()
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("📦 Inventory", stats["documents"])
with m2:
    st.metric("🧩 Fragments", stats["chunks"])
with m3:
    st.metric("✨ Synapses", stats["examples"])
with m4:
    st.metric("💎 Energy Cost", stats["total_estimated_cost"])

# --- Main Functional Area ---
tab_ingest, tab_kitchen, tab_brain, tab_lab, tab_ship = st.tabs([
    "📥 Ingestion", "🔪 Kitchen", "🧠 AI Brain", "🔬 Quality", "🚢 Shipping"
])


# 1. INGESTION
with tab_ingest:
    st.header("Data Intake")
    with st.container():
        input_col, action_col = st.columns([3, 1])
        with input_col:
            source = st.text_input("Stream Source (URL/Path)", placeholder="https://api.intel.com/data")
            st_type = st.selectbox("Format Signature", ["Auto-Detect"] + [s.value for s in SourceType])
        with action_col:
            st.write("")
            st.write("")
            if st.button("🚀 Execute Ingest"):
                with st.status("Intercepting data stream...") as status:
                    t_type = None if st_type == "Auto-Detect" else SourceType(st_type)
                    async def run_load():
                        return await bot.load_documents(source, t_type)
                    docs = asyncio.run(run_load())
                    status.update(label="Stream captured successfully!", state="complete")
                    log_event(f"Captured {len(docs)} docs from {source}")
                    st.toast("Data Intercepted", icon="🛰️")

    if bot._documents:
        st.markdown("### 📊 Ingest Analytics")
        df_docs = pd.DataFrame([d.model_dump() for d in bot._documents])
        
        c1, c2 = st.columns(2)
        with c1:
            fig_types = px.pie(df_docs, names="source_type", title="Format Distribution", hole=0.5, template="plotly_dark")
            fig_types.update_traces(marker=dict(colors=['#00f2ff', '#7000ff', '#ff0070']))
            st.plotly_chart(fig_types, use_container_width=True)
        with c2:
            fig_words = px.bar(df_docs, x="title", y="word_count", title="Volume Analysis", template="plotly_dark")
            fig_words.update_traces(marker_color='#00f2ff')
            st.plotly_chart(fig_words, use_container_width=True)

# 2. KITCHEN (Processing)
with tab_kitchen:
    st.header("Refinery Kitchen")
    if not bot._documents:
        st.warning("No data streams detected. Redirect to Ingestion.")
    else:
        with st.expander("⚙️ Refinery Config", expanded=True):
            pc1, pc2 = st.columns(2)
            with pc1:
                c_size = st.slider("Sub-division Size", 500, 3000, 1000)
                c_overlap = st.slider("Context Overlap", 0, 500, 200)
            with pc2:
                st.write("")
                st.write("Clean Noise: ACTIVE")
                st.write("Normalize Whitespace: ACTIVE")
        
        if st.button("🔪 Start Refinery"):
            with st.status("Refining raw data into shards...") as status:
                bot.processor.chunker.chunk_size = c_size
                bot.processor.chunker.chunk_overlap = c_overlap
                async def run_proc():
                    return await bot.process_documents()
                chunks = asyncio.run(run_proc())
                status.update(label=f"Refinement Complete: {len(chunks)} fragments.", state="complete")
                log_event(f"Refined documents into {len(chunks)} shards")

        if bot._chunks:
            st.subheader("🧩 Shard Inspector")
            chunk_to_view = st.number_input("Shard Index", 0, len(bot._chunks)-1, 0)
            target = bot._chunks[chunk_to_view]
            st.code(target.text, language="text")

# 3. AI BRAIN (Generation)
with tab_brain:
    st.header("Neural Generation")
    if not bot._chunks:
        st.warning("Refinery empty. Await data fragments.")
    else:
        gc1, gc2 = st.columns([2, 1])
        with gc1:
            g_type = st.selectbox("Neural Task", [t.value for t in TaskType])
            g_model = st.selectbox("Core Processor", ["gpt-4-turbo", "claude-3-opus", "simulation"])
            g_prompt = st.text_area("Neural Template", "Synthesize training examples from: {{text}}")
        with gc2:
            g_temp = st.slider("Neural Entropy", 0.0, 1.2, 0.7)
        
        if st.button("🧠 Activate Neural Link"):
            with st.status("Synthesizing synapses...") as status:
                task = TaskTemplate(
                    task_type=TaskType(g_type),
                    prompt_template=g_prompt,
                    ai_params={"model": g_model, "temperature": g_temp}
                )
                async def run_gen():
                    return await bot.generate_training_data(task)
                
                if g_model == "simulation":
                    from training_bot.generators.simulation import SimulationClient
                    bot.task_manager.client = SimulationClient()
                    
                examples = asyncio.run(run_gen())
                status.update(label=f"Synthesis Complete: {len(examples)} synapses.", state="complete")
                log_event(f"Synthesized {len(examples)} examples")

        if bot._examples:
            st.subheader("✨ Synapse Registry")
            st.dataframe(pd.DataFrame([e.model_dump() for e in bot._examples])[["id", "input_text", "output_text"]])

# 4. QUALITY LAB
with tab_lab:
    st.header("Neural Pulse Audit")
    if not bot._examples:
        st.info("Await neural synthesis...")
    else:
        if st.button("🔬 Execute Audit"):
            async def run_eval():
                return await bot.evaluate_quality()
            asyncio.run(run_eval())
            log_event("Pulse audit complete")
            st.success("Quality Pulse: STABLE")

        df_ex = pd.DataFrame([e.model_dump() for e in bot._examples])
        
        lc1, lc2 = st.columns([2, 1])
        with lc1:
            fig_quality = px.histogram(df_ex, x="quality_score", title="Pulse Integrity Map", template="plotly_dark")
            fig_quality.update_traces(marker_color='#00f2ff')
            st.plotly_chart(fig_quality, use_container_width=True)
        with lc2:
            avg_score = df_ex["quality_score"].mean()
            st.metric("Integrity Delta", f"{avg_score:.2f}")
            st.progress(avg_score)

# 5. SHIPPING
with tab_ship:
    st.header("Stealth Dispatch")
    if not bot._examples:
        st.warning("Package empty.")
    else:
        st.write(f"Preparing **{len(bot._examples)}** synapses for dispatch.")
        sc1, sc2 = st.columns(2)
        with sc1:
            ds_name = st.text_input("Packet ID", f"stealth_pkg_{int(time.time())}")
            exp_fmt = st.selectbox("Encapsulation", [f.value for f in ExportFormat])
        with sc2:
            st.write("")
            st.write("")
            if st.button("🚢 Initiate Dispatch"):
                async def run_exp():
                    return await bot.export(ds_name, ExportFormat(exp_fmt))
                f_path = asyncio.run(run_exp())
                st.session_state.last_export = f_path
                log_event(f"Packet dispatched to {f_path}")
                st.success(f"Package encrypted and safe at: {f_path}")

        if hasattr(st.session_state, 'last_export'):
            with open(st.session_state.last_export, "rb") as f:
                st.download_button("💾 Download Encrypted Packet", f, use_container_width=True)

# --- Sidebar System Monitor ---
with st.sidebar:
    st.title("Cyber Matrix")
    st.markdown("---")
    
    st.subheader("System pulse")
    for log in reversed(st.session_state.logs[-12:]):
        st.markdown(f"<code style='color:#00f2ff; background:transparent;'>[{log['time']}]</code> <small>{log['msg']}</small>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("v1.0.0-Stealth | 00ff-Cyber-Protocol")
