import pandas as pd
import streamlit as st

st.set_page_config(page_title="OrderGuard AI", page_icon="🛡️", layout="wide")

REQUIRED = ["order_id", "customer", "phone", "address", "total", "previous_orders", "notes"]
SAMPLE = [
    ["OG-1001", "Amira Ben Salem", "20123456", "Sousse, Khzema", 89, 4, "Customer confirmed by message"],
    ["OG-1002", "Mohamed Ali", "", "Tunis", 145, 0, "Asked for urgent delivery"],
    ["OG-1003", "Sarra Trabelsi", "55112233", "", 320, 1, "Address needs confirmation"],
    ["OG-1004", "Yassine K.", "98112233", "Monastir, centre ville", 59, 7, "Returning customer"],
    ["OG-1005", "Demo Customer", "", "", 410, 0, "Please send quickly"],
    ["OG-1006", "Nour Haddad", "22114567", "Sfax, Sakiet Ezzit", 125, 3, "Confirmed size and color"],
    ["OG-1007", "Karim Mansour", "55190876", "Ariana, Ennasr", 275, 2, "Asked to change address"],
]
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:radial-gradient(ellipse at 75% -10%,rgba(124,58,237,.20),transparent 38%),#0b0d14;color:#f5f5fa}
.block-container{max-width:1440px;padding-top:2rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:#10131d;border-right:1px solid rgba(255,255,255,.08)}
[data-testid="stMetric"]{background:linear-gradient(145deg,#191e2d,#121622);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:16px 18px}
[data-testid="stMetricLabel"]{color:#a7aec0;font-weight:600}
[data-testid="stMetricValue"]{color:#fff;font-weight:800}
.eyebrow{color:#b9a0ff;font-size:.74rem;font-weight:800;letter-spacing:.16em}
.hero{font-size:2.35rem;font-weight:800;letter-spacing:-.045em;color:#fff;margin:.3rem 0}
.sub{color:#9ca3b7;font-size:1rem}
.card{background:linear-gradient(145deg,#191e2d,#121622);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px 20px;min-height:112px}
.klabel{color:#9ca3b7;font-size:.78rem;font-weight:700;letter-spacing:.04em}
.kvalue{color:#fff;font-size:2rem;font-weight:800;margin-top:8px}
.knote{color:#7f879c;font-size:.76rem;margin-top:2px}
.section{font-size:1.2rem;font-weight:750;color:#fff;margin:1.3rem 0 .8rem}
.stButton>button{border-radius:10px}
[data-testid="stDataFrame"]{border:1px solid rgba(255,255,255,.08);border-radius:14px;overflow:hidden}
.footer{color:#737b90;font-size:.78rem;border-top:1px solid rgba(255,255,255,.08);padding-top:16px;margin-top:30px}
</style>
""", unsafe_allow_html=True)

def assess(row):
    score, reasons = 0, []
    checks = [
        (not str(row.phone).strip(), 30, "Phone number is missing"),
        (not str(row.address).strip(), 25, "Delivery address is missing"),
        (row.previous_orders <= 0, 15, "No previous successful orders recorded"),
        (row.total >= 250, 10, "Order value is relatively high"),
        (any(w in str(row.notes).lower() for w in ["urgent", "cancel", "fake", "change address"]), 20, "Order note needs manual review"),
    ]
    for condition, points, reason in checks:
        if condition:
            score += points
            reasons.append(reason)
    score = min(score, 100)
    level = "High" if score >= 50 else "Medium" if score >= 25 else "Low"
    action = {
        "High": "Contact customer and confirm phone + full address before dispatch.",
        "Medium": "Review missing details and send a confirmation message.",
        "Low": "Continue with the normal confirmation workflow.",
    }[level]
    return pd.Series([score, level, " • ".join(reasons) if reasons else "No rule-based warning detected", action])

with st.sidebar:
    st.markdown("## 🛡️ OrderGuard AI")
    st.caption("INTELLIGENT ORDER REVIEW")
    st.divider()
    page = st.radio("WORKSPACE", ["Overview", "Orders", "How it works"])
    st.divider()
    st.markdown("**Import order data**")
    upload = st.file_uploader("Upload CSV", type=["csv"])
    st.caption("Required: " + ", ".join(REQUIRED))
    st.divider()
    st.caption("EARLY ACCESS · KIROWEEN 2026")

try:
    if upload:
        df = pd.read_csv(upload)
        missing = [c for c in REQUIRED if c not in df.columns]
        if missing:
            st.error("Missing CSV columns: " + ", ".join(missing))
            st.stop()
    else:
        df = pd.DataFrame(SAMPLE, columns=REQUIRED)
    for c in ["order_id", "customer", "phone", "address", "notes"]:
        df[c] = df[c].fillna("").astype(str)
    df["total"] = pd.to_numeric(df["total"], errors="coerce").fillna(0)
    df["previous_orders"] = pd.to_numeric(df["previous_orders"], errors="coerce").fillna(0)
    df[["risk_score", "risk_level", "risk_reasons", "recommended_action"]] = df.apply(assess, axis=1)
    df = df.sort_values("risk_score", ascending=False).reset_index(drop=True)
except Exception as exc:
    st.error(f"Could not load orders: {exc}")
    st.stop()

n = len(df)
high = int((df.risk_level == "High").sum())
medium = int((df.risk_level == "Medium").sum())
low = int((df.risk_level == "Low").sum())
review_pct = round((high + medium) / n * 100) if n else 0

st.markdown('<div class="eyebrow">E-COMMERCE RISK INTELLIGENCE</div><div class="hero">Order command center</div><div class="sub">A clearer view of incoming orders, risk signals, and the next best action.</div>', unsafe_allow_html=True)

if page == "Overview":
    cols = st.columns(4)
    cards = [
        ("TOTAL ORDERS", n, "Orders in current dataset"),
        ("HIGH RISK", high, "Require manual confirmation"),
        ("NEEDS REVIEW", medium, "Check details before dispatch"),
        ("LOW RISK", low, "No major rule-based flags"),
    ]
    for col, (label, value, note) in zip(cols, cards):
        with col:
            st.markdown(f'<div class="card"><div class="klabel">{label}</div><div class="kvalue">{value}</div><div class="knote">{note}</div></div>', unsafe_allow_html=True)
    left, right = st.columns([1.35, 1])
    with left:
        st.markdown('<div class="section">Risk distribution</div>', unsafe_allow_html=True)
        st.bar_chart(pd.DataFrame({"Orders": [high, medium, low]}, index=["High risk", "Needs review", "Low risk"]), color="#8b5cf6", height=270)
    with right:
        st.markdown('<div class="section">Review priority</div>', unsafe_allow_html=True)
        st.metric("Orders to review", high + medium, f"{review_pct}% of all orders")
        st.progress(review_pct / 100 if n else 0)
        st.caption("Share of orders with at least one rule-based signal.")
        st.info("A risk score is a review signal, not proof of fraud.")
    st.markdown('<div class="section">Priority queue</div>', unsafe_allow_html=True)
    priority = df[df.risk_level.isin(["High", "Medium"])].head(6)
    st.dataframe(priority[["order_id", "customer", "total", "risk_score", "risk_level", "recommended_action"]], width="stretch", hide_index=True, column_config={
        "total": st.column_config.NumberColumn("Order value", format="%.2f DT"),
        "risk_score": st.column_config.ProgressColumn("Risk score", min_value=0, max_value=100, format="%d/100"),
        "recommended_action": st.column_config.TextColumn("Suggested action", width="large"),
    })

elif page == "Orders":
    st.markdown('<div class="section">Order management</div>', unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        level = st.selectbox("Risk level", ["All", "High", "Medium", "Low"])
    with b:
        query = st.text_input("Search", placeholder="Order ID or customer")
    view = df.copy()
    if level != "All":
        view = view[view.risk_level == level]
    if query.strip():
        view = view[view.order_id.str.contains(query, case=False) | view.customer.str.contains(query, case=False)]
    st.caption(f"Showing {len(view)} of {n} orders")
    st.dataframe(view[["order_id", "customer", "phone", "address", "total", "risk_score", "risk_level", "risk_reasons"]], width="stretch", hide_index=True, column_config={
        "total": st.column_config.NumberColumn("Order value", format="%.2f DT"),
        "risk_score": st.column_config.ProgressColumn("Risk score", min_value=0, max_value=100, format="%d/100"),
    })
    st.download_button("↓ Export analyzed orders", df.to_csv(index=False).encode("utf-8-sig"), "orderguard-analysis.csv", "text/csv", type="primary")
    st.markdown('<div class="section">Investigate an order</div>', unsafe_allow_html=True)
    if n:
        order_id = st.selectbox("Select order", df.order_id.tolist())
        item = df[df.order_id == order_id].iloc[0]
        x, y = st.columns([1, 2])
        with x:
            st.metric("Risk score", f"{int(item.risk_score)}/100")
            st.write(f"**Risk level:** {item.risk_level}")
        with y:
            st.markdown("**Risk indicators**")
            st.write(item.risk_reasons)
            st.markdown("**Recommended next step**")
            st.success(item.recommended_action)

else:
    st.markdown('<div class="section">How OrderGuard works</div>', unsafe_allow_html=True)
    for number, title, description in [
        ("01", "Import orders", "Upload a CSV or explore the built-in synthetic dataset."),
        ("02", "Review risk signals", "Transparent rules flag missing details, limited order history, high order values, and notes requiring attention."),
        ("03", "Take action", "Use the suggested next step to guide manual customer confirmation before dispatch."),
        ("04", "Export results", "Download analyzed orders and use them in your existing workflow."),
    ]:
        st.markdown(f'<div class="card" style="margin-bottom:12px;min-height:0"><div class="eyebrow">{number}</div><div style="font-size:1.12rem;font-weight:750;color:#fff;margin:5px 0">{title}</div><div class="sub">{description}</div></div>', unsafe_allow_html=True)
    st.warning("This prototype uses explainable rules. It is not a trained fraud model and does not verify customer identity or address. A high score does not mean an order is fraudulent.")

st.markdown('<div class="footer">ORDERGUARD AI · EARLY PROTOTYPE · KIROWEEN 2026 · Use synthetic data for public demos.</div>', unsafe_allow_html=True)
