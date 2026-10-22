import streamlit as st
from analyzer import analyze_url
from ai_agent import explain_with_strands

st.set_page_config(page_title="SENTINEL-X | URL Intelligence", page_icon="🛡️", layout="wide")
st.markdown("""<style>
.stApp {background:linear-gradient(145deg,#0d0d1d,#19102e);color:#f1ebff}
h1,h2,h3 {color:#c5a2ff!important}
[data-testid="stMetricValue"] {color:#d5b9ff}
</style>""", unsafe_allow_html=True)
st.title("🛡️ SENTINEL-X")
st.caption("Defensive URL intelligence · Offline heuristics · Optional AWS Strands AI")
st.warning("This tool never visits submitted URLs. Scores are warning indicators, NOT a safety or phishing verdict.")
url = st.text_input("Website URL", placeholder="https://example.com/login", max_chars=2048)
if st.button("🔍 Analyze URL", type="primary"):
    try:
        st.session_state["result"] = analyze_url(url)
        st.session_state.pop("ai_report", None)
    except ValueError as exc:
        st.session_state.pop("result", None)
        st.error(str(exc))
result = st.session_state.get("result")
if result:
    a, b, c = st.columns(3)
    a.metric("Heuristic score", f"{result.score}/100")
    b.metric("Risk indicators", result.level)
    c.metric("Findings", len(result.findings))
    st.subheader("Analyzed hostname")
    st.code(result.host)
    st.subheader("Evidence")
    if result.findings:
        for item in result.findings:
            st.info(f"+{item.points} · {item.detail}")
    else:
        st.success("No selected heuristic warning signs detected. This does NOT prove safety.")
    st.download_button("⬇️ Download JSON report", data=result.to_json(),
                       file_name="sentinel-x-report.json", mime="application/json")
    st.divider()
    st.subheader("🧠 AWS Strands AI explanation (optional)")
    st.caption("Requires AWS credentials, an enabled Bedrock model, and ENABLE_AWS_AI=1. AWS charges may apply. Only the hostname and findings are sent to AWS; no full URL, query string, or credentials.")
    consent = st.checkbox("I understand this sends the hostname and findings to AWS and may incur charges.")
    if st.button("Generate AI explanation", disabled=not consent):
        try:
            with st.spinner("Generating explanation..."):
                st.session_state["ai_report"] = explain_with_strands(result)
        except Exception as exc:
            st.error(f"AI unavailable: {type(exc).__name__}. Check configuration and AWS access; see README.")
    if "ai_report" in st.session_state:
        st.write(st.session_state["ai_report"])
st.divider()
st.caption("SENTINEL-X v1.0 · No URL fetching, DNS lookup, scanning, or malware execution · Do not enter secrets")
