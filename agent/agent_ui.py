import streamlit as st
import time
import json
from agent_node import AgentNode, logs, attack_nodes

NUM_NODES = 5

# INIT
if "nodes" not in st.session_state:
    st.session_state.nodes = [
        AgentNode(i, 5000 + i) for i in range(NUM_NODES)
    ]
    st.session_state.nodes[0].informed = True

if "running" not in st.session_state:
    st.session_state.running = False

if "history" not in st.session_state:
    st.session_state.history = []

# UI
st.title("🤖 AI Gossip Control System")

mode = st.selectbox("Chọn Gossip Mode", ["PUSH", "PULL"])

col1, col2 = st.columns(2)

if col1.button("▶️ Start"):
    st.session_state.running = True

if col2.button("⏹ Stop"):
    st.session_state.running = False

# =========================
# ACTION BUTTONS
# =========================
st.subheader("⚙️ Control Actions")

colA, colB, colC = st.columns(3)

shutdown = colA.button("🛑 Shutdown")
counter = colB.button("⚔️ Counter Attack")
backup = colC.button("🟡 Backup Mode")

# =========================
# DISPLAY NODES
# =========================
st.subheader("📡 Network")

cols = st.columns(NUM_NODES)

for i, node in enumerate(st.session_state.nodes):

    if i in attack_nodes:
        color = "orange"
    else:
        color = "green" if node.informed else "red"

    cols[i].markdown(
        f"<div style='background:{color};padding:15px;text-align:center'>Node {i}</div>",
        unsafe_allow_html=True
    )

# =========================
# LOG DISPLAY
# =========================
st.subheader("📜 Logs")
st.write(logs[-10:])

# =========================
# METRICS CHART
# =========================
st.subheader("📊 Push vs Pull Analysis")

try:
    with open("metrics.json") as f:
        metrics = json.load(f)
except:
    metrics = {"push": 0, "pull": 0}

st.bar_chart(metrics)

# =========================
# PROPAGATION CHART
# =========================
informed = sum(n.informed for n in st.session_state.nodes)
st.session_state.history.append(informed)

st.subheader("📈 Propagation")
st.line_chart(st.session_state.history)

# =========================
# MAIN LOOP
# =========================
if st.session_state.running:

    # SHUTDOWN
    if shutdown:
        st.session_state.running = False
        st.error("System shutdown")

    # COUNTER ATTACK
    elif counter:
        for node in st.session_state.nodes:
            if node.informed:
                node.push(st.session_state.nodes)

    # BACKUP
    elif backup:
        time.sleep(1)

    # NORMAL
    else:
        for node in st.session_state.nodes:

            if node.detect():
                node.informed = True

            if node.informed:
                if mode == "PUSH":
                    node.push(st.session_state.nodes)
                else:
                    node.pull(st.session_state.nodes)

    time.sleep(0.5)
    st.rerun()