import streamlit as st
import requests

API_URL = "http://localhost:8000"

# ─────────────────────────────────────────────
# 🔹 Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="📝",
    layout="centered"
)

st.title("📝 AI Blog Generator with HITL")
st.caption("Generate → Review → Revise → Approve")

# ─────────────────────────────────────────────
# 🔹 Session state
# ─────────────────────────────────────────────
if "flow_id" not in st.session_state:
    st.session_state.flow_id = None

if "blog" not in st.session_state:
    st.session_state.blog = None

if "iteration" not in st.session_state:
    st.session_state.iteration = 0

if "approved" not in st.session_state:
    st.session_state.approved = False


# ─────────────────────────────────────────────
# 🔹 Step 1 — Topic input
# ─────────────────────────────────────────────
if not st.session_state.blog and not st.session_state.approved:

    st.subheader("Step 1 — Enter your topic")

    topic = st.text_input("Blog topic", placeholder="How AI is Transforming Healthcare in 2026")

    if st.button("🚀 Generate Blog", disabled=not topic):
        with st.spinner("🤖 Crew is researching and writing..."):
            try:
                res = requests.post(f"{API_URL}/generate", json={"topic": topic})
                data = res.json()

                st.session_state.flow_id = data["flow_id"]
                st.session_state.blog = data["blog"]
                st.session_state.iteration = data["iteration"]
                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")


# ─────────────────────────────────────────────
# 🔹 Step 2 — Review + Feedback
# ─────────────────────────────────────────────
elif st.session_state.blog and not st.session_state.approved:

    st.subheader(f"Step 2 — Review Blog (Iteration #{st.session_state.iteration})")

    # Show generated blog
    st.markdown("---")
    st.markdown(st.session_state.blog)
    st.markdown("---")

    # Feedback input
    st.subheader("Your Feedback")
    feedback = st.text_input(
        "Type 'approved' to publish or give revision feedback:",
        placeholder="approved  /  add more examples  /  make it shorter"
    )

    if st.button("📤 Submit", disabled=not feedback, use_container_width=True):
        with st.spinner("Processing..."):
            try:
                res = requests.post(
                    f"{API_URL}/feedback/{st.session_state.flow_id}",
                    json={"feedback": feedback}
                )
                data = res.json()

                if data["status"] == "completed":
                    st.session_state.approved = data["approved"]
                    st.session_state.blog = data["blog"]
                else:
                    st.session_state.blog = data["blog"]
                    st.session_state.flow_id = data["flow_id"]
                    st.session_state.iteration = data["iteration"]

                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")


# ─────────────────────────────────────────────
# 🔹 Step 3 — Approved
# ─────────────────────────────────────────────
elif st.session_state.approved:

    st.success("✅ Blog Approved and Published!")
    st.markdown("---")
    st.markdown(st.session_state.blog)
    st.markdown("---")

    if st.button("🔄 Generate New Blog"):
        # Reset session state
        st.session_state.flow_id = None
        st.session_state.blog = None
        st.session_state.iteration = 0
        st.session_state.approved = False
        st.rerun()