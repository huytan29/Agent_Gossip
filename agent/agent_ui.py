import streamlit as st
import random
import time

NUM_NODES = 10

# trạng thái node
if "nodes" not in st.session_state:
    st.session_state.nodes = [False] * NUM_NODES
    st.session_state.nodes[0] = True

if "mode" not in st.session_state:
    st.session_state.mode = "PUSH"

# =========================
# UI
# =========================
st.title("🤖 AI Agent - Gossip System")

# chọn mode
mode = st.selectbox("Chọn chế độ Gossip", ["PUSH", "PULL"])

st.session_state.mode = mode

# =========================
# HIỂN THỊ NODE
# =========================
st.subheader("📡 Trạng thái Nodes")

cols = st.columns(5)

for i in range(NUM_NODES):
    status = st.session_state.nodes[i]

    color = "green" if status else "red"

    cols[i % 5].markdown(
        f"<div style='background-color:{color};padding:10px;border-radius:10px;text-align:center'>Node {i}</div>",
        unsafe_allow_html=True
    )

# =========================
# GOSSIP LOGIC
# =========================
def gossip_push():
    new_nodes = st.session_state.nodes.copy()

    for i in range(NUM_NODES):
        if st.session_state.nodes[i]:
            targets = random.sample(range(NUM_NODES), 2)

            for t in targets:
                new_nodes[t] = True

    st.session_state.nodes = new_nodes


def gossip_pull():
    new_nodes = st.session_state.nodes.copy()

    for i in range(NUM_NODES):
        if not st.session_state.nodes[i]:
            target = random.randint(0, NUM_NODES - 1)

            if st.session_state.nodes[target]:
                new_nodes[i] = True

    st.session_state.nodes = new_nodes


# =========================
# ATTACK SIMULATION
# =========================
if st.button("🚨 Simulate Attack"):
    target = random.randint(0, NUM_NODES - 1)
    st.session_state.nodes[target] = True
    st.warning(f"Node {target} bị tấn công!")

# =========================
# RUN LOOP
# =========================
if st.button("▶️ Start System"):
    for _ in range(20):

        if st.session_state.mode == "PUSH":
            gossip_push()
        else:
            gossip_pull()

        time.sleep(0.5)
        st.rerun()