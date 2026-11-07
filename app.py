import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="OrderGuard AI", page_icon="🛡️", layout="wide")

REQUIRED_COLUMNS = ["order_id", "customer", "phone", "address", "total", "previous_orders", "notes"]

SAMPLE_ORDERS = [
    {"order_id": "OG-1001", "customer": "Amira Ben Salem", "phone": "20123456", "address": "Sousse, Khzema", "total": 89, "previous_orders": 4, "notes": "Customer confirmed by message"},
    {"order_id": "OG-1002", "customer": "Mohamed Ali", "phone": "", "address": "Tunis", "total": 145, "previous_orders": 0, "notes": "Asked for urgent delivery"},
    {"order_id": "OG-1003", "customer": "Sarra Trabelsi", "phone": "55112233", "address": "", "total": 320, "previous_orders": 1, "notes": "Address needs confirmation"},
    {"order_id": "OG-1004", "customer": "Yassine K.", "phone": "98112233", "address": "Monastir, centre ville", "total": 59, "previous_orders": 7, "notes": "Returning customer"},
    {"order_id": "OG-1005", "customer": "Unknown customer", "phone": "", "address": "", "total": 410, "previous_orders": 0, "notes": "Please send quickly"},
]

st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {background: rgba(120, 120, 140, .08); padding: 14px; border-radius: 12px;}
.small-muted {color: #9297a5; font-size: .9rem;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ OrderGuard AI")
st.caption("E-commerce order review • Explainable risk indicators • Cash-on-delivery workflow")
st.info("Demo mode: the risk score uses transparent rules on the information provided. It is a decision-support signal, not proof of fraud or a guarantee of delivery outcome.")

with st.sidebar:
    st.header("Order data")
    uploaded = st.file_uploader("Upload orders CSV", type=["csv"])
    st.caption("Expected columns: " + ", ".join(REQUIRED_COLUMNS))
    st.divider()
    st.markdown("**About this demo**")
    st.markdown("Use the sample dataset or upload synthetic/test orders. Avoid uploading sensitive customer data into public demos.")

if uploaded is not None:
    try:
        orders = pd.read_csv(uploaded)
        missing = [c for c in REQUIRED_COLUMNS if c not in orders.columns]
        if missing:
            st.error("CSV is missing required columns: " + ", ".join(missing))
            st.stop()
    except Exception as exc:
        st.error(f"Could not read CSV: {exc}")
        st.stop()
else:
    orders = pd.DataFrame(SAMPLE_ORDERS)

for col in ["phone", "address", "notes", "customer", "order_id"]:
    orders[col] = orders[col].fillna("").astype(str)
orders["total"] = pd.to_numeric(orders["total"], errors="coerce").fillna(0)
orders["previous_orders"] = pd.to_numeric(orders["previous_orders"], errors="coerce").fillna(0)

def assess_order(row):
    score = 0
    reasons = []
    if not row["phone"].strip():
        score += 30
        reasons.append("Phone number is missing")
    if not row["address"].strip():
        score += 25
        reasons.append("Delivery address is missing")
    if row["previous_orders"] <= 0:
        score += 15
        reasons.append("No previous successful orders recorded")
    if row["total"] >= 250:
        score += 10
        reasons.append("Order value is relatively high")
    note = row["notes"].lower()
    if any(word in note for word in ["urgent", "cancel", "fake", "change address"]):
        score += 20
        reasons.append("Notes contain a keyword that may need manual review")
    score = min(score, 100)
    level = "High" if score >= 50 else "Medium" if score >= 25 else "Low"
    if level == "High":
        action = "Contact customer and confirm phone + full address before dispatch"
    elif level == "Medium":
        action = "Review missing details and send a confirmation message"
    else:
        action = "Ready for normal confirmation workflow"
    return pd.Series([score, level, " • ".join(reasons) if reasons else "No rule-based warning detected", action])

orders[["risk_score", "risk_level", "risk_reasons", "recommended_action"]] = orders.apply(assess_order, axis=1)
orders = orders.sort_values("risk_score", ascending=False).reset_index(drop=True)

total_orders = len(orders)
high_count = int((orders["risk_level"] == "High").sum())
medium_count = int((orders["risk_level"] == "Medium").sum())
low_count = int((orders["risk_level"] == "Low").sum())

m1, m2, m3, m4 = st.columns(4)
m1.metric("Orders analyzed", total_orders)
m2.metric("High risk", high_count)
m3.metric("Needs review", medium_count)
m4.metric("Low risk", low_count)

st.subheader("Order risk overview")
chart_data = orders.groupby("risk_level").size().reindex(["High", "Medium", "Low"], fill_value=0)
st.bar_chart(chart_data)

st.subheader("Orders requiring attention")
risk_filter = st.multiselect("Filter by risk level", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])
visible = orders[orders["risk_level"].isin(risk_filter)]
display_cols = ["order_id", "customer", "total", "risk_score", "risk_level", "risk_reasons"]
st.dataframe(visible[display_cols], use_container_width=True, hide_index=True)

st.subheader("Order review")
if not orders.empty:
    selected_id = st.selectbox("Select an order", orders["order_id"].tolist())
    selected = orders[orders["order_id"] == selected_id].iloc[0]
    left, right = st.columns([1, 2])
    with left:
        st.metric("Risk score", f'{int(selected["risk_score"])}/100')
        st.markdown(f"**Risk level:** {selected['risk_level']}")
    with right:
        st.markdown("**Indicators**")
        st.write(selected["risk_reasons"])
        st.markdown("**Suggested next step**")
        st.success(selected["recommended_action"])
        st.caption("A human should review the context before taking action.")

csv_bytes = orders.to_csv(index=False).encode("utf-8")
st.download_button("Download analyzed orders (CSV)", data=csv_bytes, file_name="orderguard-analysis.csv", mime="text/csv")

st.divider()
st.markdown('<p class="small-muted">OrderGuard AI • Early prototype for the Kiroween 2026 hackathon. Synthetic sample data only.</p>', unsafe_allow_html=True)
