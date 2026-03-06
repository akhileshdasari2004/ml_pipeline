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

# --- Architecture HTML Content ---
ARCHITECTURE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Enterprise ML Pipeline Architecture</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #050810;
    --panel: #0b0f1e;
    --border: #1a2240;
    --accent1: #00f5c4;
    --accent2: #4d7cff;
    --accent3: #ff6b6b;
    --accent4: #ffc94d;
    --accent5: #c084fc;
    --text: #e2e8f0;
    --muted: #4a5568;
    --glow1: rgba(0,245,196,0.15);
    --glow2: rgba(77,124,255,0.15);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: transparent;
    color: var(--text);
    font-family: 'Space Mono', monospace;
    min-height: 100vh;
    overflow-x: hidden;
  }

  .wrapper {
    position: relative;
    z-index: 1;
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
  }

  .header {
    text-align: center;
    margin-bottom: 32px;
  }

  .header .badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: var(--accent1);
    border: 1px solid var(--accent1);
    padding: 4px 14px;
    margin-bottom: 20px;
    text-transform: uppercase;
  }

  .header h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(24px, 4vw, 42px);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, var(--accent1) 0%, var(--accent2) 50%, var(--accent5) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
  }

  .header p {
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 1px;
  }

  .layer-label {
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 12px;
    padding-left: 4px;
  }

  .pipeline { display: flex; flex-direction: column; }

  .layer { transform: translateY(0); }

  .cards-row { display: flex; gap: 12px; flex-wrap: wrap; }

  .arrow-connector {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 40px;
    position: relative;
  }

  .arrow-connector::before {
    content: '';
    position: absolute;
    width: 2px;
    height: 100%;
    background: linear-gradient(to bottom, var(--accent2), var(--accent1));
    left: 50%;
    transform: translateX(-50%);
  }

  .arrow-connector .arrow-head {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 8px solid var(--accent1);
  }

  .arrow-connector .data-label {
    position: absolute;
    right: calc(50% + 16px);
    font-size: 9px;
    letter-spacing: 1px;
    color: var(--accent1);
    white-space: nowrap;
    opacity: 0.7;
  }

  .card {
    flex: 1;
    min-width: 160px;
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 16px 18px;
    position: relative;
    cursor: default;
    transition: all 0.3s ease;
    overflow: hidden;
  }

  .card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: var(--card-accent, var(--accent2));
  }

  .card:hover {
    border-color: var(--card-accent, var(--accent2));
    box-shadow: 0 0 24px var(--card-glow, var(--glow2));
    transform: translateY(-2px);
  }

  .card .card-icon { font-size: 20px; margin-bottom: 10px; display: block; }

  .card .card-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 6px;
  }

  .card .card-desc { font-size: 10px; color: var(--muted); line-height: 1.6; }

  .interface-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

  .card-central {
    background: linear-gradient(135deg, #0d1530 0%, #0b1525 100%);
    border: 1px solid var(--accent2);
    padding: 24px 28px;
    display: flex;
    align-items: center;
    gap: 24px;
    flex-wrap: wrap;
  }

  .card-central .central-icon { font-size: 36px; }

  .card-central .central-body { flex: 1; min-width: 200px; }

  .card-central .central-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 800;
    color: var(--accent2);
    margin-bottom: 6px;
  }

  .card-central .central-desc { font-size: 11px; color: #7090c0; line-height: 1.6; }

  .c-green { --card-accent: var(--accent1); --card-glow: var(--glow1); }
  .c-blue  { --card-accent: var(--accent2); --card-glow: var(--glow2); }
  .c-red   { --card-accent: var(--accent3); --card-glow: rgba(255,107,107,0.15); }
  .c-yellow{ --card-accent: var(--accent4); --card-glow: rgba(255,201,77,0.15); }
  .c-purple{ --card-accent: var(--accent5); --card-glow: rgba(192,132,252,0.15); }

</style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <div class="badge">Pipeline Overview</div>
    <h1>System Architecture</h1>
    <p>// Modular · Async · Production-Grade</p>
  </div>

  <div class="pipeline">
    <div class="layer">
      <div class="layer-label">// 01 — User Interfaces</div>
      <div class="interface-row">
        <div class="card c-purple">
          <span class="card-icon">⌨️</span>
          <div class="card-title">CLI Interface</div>
          <div class="card-desc">Terminal-based control.</div>
        </div>
        <div class="card c-purple">
          <span class="card-icon">📊</span>
          <div class="card-title">Streamlit Dashboard</div>
          <div class="card-desc">Web-based analytics.</div>
        </div>
      </div>
    </div>

    <div class="arrow-connector"><div class="arrow-head"></div></div>

    <div class="layer">
      <div class="layer-label">// 02 — Factory Manager</div>
      <div class="card card-central">
        <span class="central-icon">🧠</span>
        <div class="central-body">
          <div class="central-title">bot.py — The Factory Manager</div>
          <div class="central-desc">Central coordinator of all operations. Orchestrates document loading, text processing, quality assessment, and export.</div>
        </div>
      </div>
    </div>

    <div class="arrow-connector"><div class="arrow-head"></div></div>

    <div class="layer">
      <div class="layer-label">// 03 — Document Loaders</div>
      <div class="cards-row">
        <div class="card c-green"><span class="card-icon">🔀</span><div class="card-title">Unified</div></div>
        <div class="card c-green"><span class="card-icon">🌐</span><div class="card-title">Web</div></div>
        <div class="card c-green"><span class="card-icon">📄</span><div class="card-title">PDF</div></div>
        <div class="card c-green"><span class="card-icon">📁</span><div class="card-title">Files</div></div>
      </div>
    </div>

    <div class="arrow-connector"><div class="arrow-head"></div></div>

    <div class="layer">
      <div class="layer-label">// 04 — Text Kitchen</div>
      <div class="cards-row">
        <div class="card c-yellow"><span class="card-icon">🧹</span><div class="card-title">Cleaner</div></div>
        <div class="card c-yellow"><span class="card-icon">✂️</span><div class="card-title">Chunker</div></div>
      </div>
    </div>

    <div class="arrow-connector"><div class="arrow-head"></div></div>

    <div class="layer">
      <div class="layer-label">// 05 — AI Brain</div>
      <div class="cards-row">
        <div class="card c-blue"><span class="card-icon">📋</span><div class="card-title">Manager</div></div>
        <div class="card c-blue"><span class="card-icon">⚡</span><div class="card-title">AI Client</div></div>
      </div>
    </div>

    <div class="arrow-connector"><div class="arrow-head"></div></div>

    <div class="layer">
      <div class="layer-label">// 06 — Quality Lab</div>
      <div class="cards-row">
        <div class="card c-red"><span class="card-icon">🔬</span><div class="card-title">Evaluator</div></div>
        <div class="card c-red"><span class="card-icon">📑</span><div class="card-title">Reporter</div></div>
      </div>
    </div>

    <div class="arrow-connector"><div class="arrow-head"></div></div>

    <div class="layer">
      <div class="layer-label">// 07 — Shipping</div>
      <div class="cards-row">
        <div class="card c-green"><span class="card-icon">📦</span><div class="card-title">JSON</div></div>
        <div class="card c-green"><span class="card-icon">📊</span><div class="card-title">CSV</div></div>
        <div class="card c-green"><span class="card-icon">🗜️</span><div class="card-title">Parquet</div></div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

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
tab_home, tab_ingest, tab_kitchen, tab_brain, tab_lab, tab_ship = st.tabs([
    "🏠 Architecture", "📥 Ingestion", "🔪 Kitchen", "🧠 AI Brain", "🔬 Quality", "🚢 Shipping"
])

# 0. HOME / ARCHITECTURE
with tab_home:
    import streamlit.components.v1 as components
    components.html(ARCHITECTURE_HTML, height=1600, scrolling=True)

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
            g_model = st.selectbox("Core Processor", ["gemini-1.5-pro", "gemini-1.5-flash", "gpt-4-turbo", "claude-3-opus", "simulation"])
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
