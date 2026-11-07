import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="OrderGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root { --ink:#172033; --muted:#65718a; --line:#e5e9f2; --purple:#6846d9; --surface:#ffffff; }
html, body, [class*="css"] { font-family: Inter, sans-serif !important; }
.stApp { background:#f5f7fb; color:var(--ink); }
[data-testid="stAppViewContainer"] { background:#f5f7fb; }
.block-container { max-width:1680px; padding:2.6rem 3.2rem 3.5rem; }
[data-testid="stMarkdownContainer"] { font-size:1rem; line-height:1.65; }
[data-testid="stSidebar"] [data-testid="stCode"] { background:#1d2739; border:1px solid #35445d; border-radius:10px; }
[data-testid="stSidebar"] [data-testid="stCode"] pre, [data-testid="stSidebar"] [data-testid="stCode"] code { color:#f1f5ff !important; font-size:.78rem !important; white-space:pre-wrap !important; }
.og-title { font-size:2.7rem; }
.og-subtitle { font-size:1.08rem; }
.og-card { min-height:138px; padding:22px 23px; }
.og-card-label { font-size:.78rem; }
.og-card-value { font-size:2.35rem; }
.og-card-note { font-size:.86rem; }
.og-section { font-size:1.3rem; margin:1.8rem 0 1rem; }
[data-testid="stDataFrame"] { width:100%; }
[data-testid="stDataFrame"] iframe { min-height:250px; }

[data-testid="stHeader"] { background:rgba(245,247,251,.92); }
[data-testid="stSidebar"] { background:#111827; border-right:1px solid #273247; }
[data-testid="stSidebar"] * { color:#eef2ff !important; }
[data-testid="stSidebar"] [data-testid="stFileUploader"] section { background:#1d2739 !important; border:1px dashed #64748b !important; }
[data-testid="stSidebar"] [data-testid="stFileUploader"] section,
[data-testid="stSidebar"] [data-testid="stFileUploader"] section * { color:#f8fafc !important; }
[data-testid="stSidebar"] [data-testid="stFileUploader"] button { background:#f8fafc !important; color:#172033 !important; border:0 !important; }
[data-testid="stSidebar"] [data-testid="stFileUploader"] button * { color:#172033 !important; }
.og-columns-code { background:#263449; border:1px solid #40516b; border-radius:10px; padding:12px 10px; color:#f8fafc !important; font-family:ui-monospace, SFMono-Regular, Consolas, monospace; font-size:.72rem; line-height:1.8; overflow-wrap:anywhere; }
h1,h2,h3,h4,p,label,span,div { text-rendering:optimizeLegibility; }
h1,h2,h3 { color:var(--ink) !important; letter-spacing:-.03em; }
p, label, [data-testid="stMarkdownContainer"] p { color:#47536b; }
.og-brand { color:#fff; font-size:1.35rem; font-weight:800; letter-spacing:-.04em; padding:.35rem 0 .15rem; }
.og-brand span { color:#a995ff; }
.og-side-note { color:#9eabc1; font-size:.72rem; letter-spacing:.13em; font-weight:700; }
.og-eyebrow { color:#6846d9; font-size:.72rem; letter-spacing:.15em; font-weight:800; margin-bottom:.5rem; }
.og-title { color:#172033; font-size:2.35rem; line-height:1.15; font-weight:800; letter-spacing:-.055em; margin:0 0 .55rem; }
.og-subtitle { color:#65718a; font-size:1rem; line-height:1.65; margin-bottom:1.7rem; }
.og-card { background:#fff; border:1px solid #e5e9f2; border-radius:16px; padding:18px 20px; box-shadow:0 5px 18px rgba(23,32,51,.035); min-height:124px; }
.og-card-label { color:#69758c; font-size:.72rem; letter-spacing:.08em; font-weight:800; }
.og-card-value { color:#172033; font-size:2.05rem; line-height:1.25; font-weight:800; margin-top:10px; }
.og-card-note { color:#8791a5; font-size:.78rem; margin-top:4px; }
.og-section { color:#172033; font-size:1.18rem; font-weight:800; letter-spacing:-.025em; margin:1.65rem 0 .85rem; }
.og-panel { background:#fff; border:1px solid #e5e9f2; border-radius:16px; padding:18px 20px; box-shadow:0 5px 18px rgba(23,32,51,.035); }
.og-footer { border-top:1px solid #e5e9f2; margin-top:2.5rem; padding-top:1rem; color:#8993a6; font-size:.76rem; }
[data-testid="stMetric"] { background:#fff; border:1px solid #e5e9f2; border-radius:14px; padding:14px 16px; box-shadow:0 4px 14px rgba(23,32,51,.03); }
[data-testid="stMetricLabel"] p { color:#65718a !important; font-weight:700; font-size:.8rem; }
[data-testid="stMetricValue"] { color:#172033 !important; font-weight:800; }
[data-testid="stMetricDelta"] { font-size:.76rem; }
[data-testid="stDataFrame"] { background:#fff; border:1px solid #e5e9f2; border-radius:12px; overflow:hidden; }
[data-testid="stDataFrame"] * { color:#172033; }
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div { background:#fff !important; color:#172033 !important; border-color:#d9dfeb !important; border-radius:10px !important; }
.stButton button, .stDownloadButton button { border-radius:10px; font-weight:700; min-height:2.7rem; }
.stProgress > div > div > div { background:#6846d9; }
hr { border-color:#e5e9f2; }
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
        "High": "Contact the customer and confirm the phone number and full address before dispatch.",
        "Medium": "Review the flagged details and send a customer confirmation message.",
        "Low": "Continue with the normal order-confirmation workflow.",
    }[level]
    return pd.Series([score, level, " • ".join(reasons) if reasons else "No rule-based warning detected", action])

with st.sidebar:
    st.markdown('<div class="og-brand">🛡️ OrderGuard <span>AI</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="og-side-note">ORDER REVIEW WORKSPACE</div>', unsafe_allow_html=True)
    st.divider()
    page = st.radio("NAVIGATION", ["Overview", "Orders", "How it works"], label_visibility="visible")
    st.divider()
    st.markdown("**Import your orders**")
    upload = st.file_uploader("Choose a CSV file", type=["csv"], help="Your file should include the required columns.")
    st.caption("Required columns")
    st.markdown('<div class="og-columns-code">order_id, customer,<br>phone, address, total,<br>previous_orders, notes</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="og-side-note">PROTOTYPE · KIROWEEN 2026</div>', unsafe_allow_html=True)

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

st.markdown('<div class="og-eyebrow">E-COMMERCE ORDER INTELLIGENCE</div><div class="og-title">Order command center</div><div class="og-subtitle">Understand incoming orders, spot missing information, and decide which customers need a manual confirmation.</div>', unsafe_allow_html=True)

if page == "Overview":
    metrics = st.columns(4, gap="medium")
    cards = [
        ("TOTAL ORDERS", n, "Orders in this dataset"),
        ("HIGH RISK", high, "Manual confirmation needed"),
        ("NEEDS REVIEW", medium, "Check details before dispatch"),
        ("LOW RISK", low, "No major rule-based flags"),
    ]
    for col, (label, value, note) in zip(metrics, cards):
        with col:
            st.markdown(f'<div class="og-card"><div class="og-card-label">{label}</div><div class="og-card-value">{value}</div><div class="og-card-note">{note}</div></div>', unsafe_allow_html=True)

    left, right = st.columns([1.35, 1], gap="large")
    with left:
        st.markdown('<div class="og-section">Risk distribution</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({
            "Risk level": ["High risk", "Needs review", "Low risk"],
            "Orders": [high, medium, low],
        })
        bars = alt.Chart(chart_data).mark_bar(cornerRadiusEnd=7, height=34).encode(
            y=alt.Y("Risk level:N", sort=["High risk", "Needs review", "Low risk"], title=None,
                    axis=alt.Axis(labelFontSize=13, labelColor="#47536b", ticks=False, domain=False)),
            x=alt.X("Orders:Q", title="Number of orders",
                    axis=alt.Axis(tickMinStep=1, labelFontSize=11, labelColor="#65718a", gridColor="#edf0f6")),
            color=alt.Color("Risk level:N",
                scale=alt.Scale(domain=["High risk", "Needs review", "Low risk"],
                                range=["#d84d5b", "#e5a33c", "#36a887"]),
                legend=None),
            tooltip=["Risk level", "Orders"],
        )
        labels = bars.mark_text(align="left", baseline="middle", dx=8, fontSize=13,
                                fontWeight="bold", color="#172033").encode(text="Orders:Q")
        st.altair_chart((bars + labels).properties(height=190, padding={"left": 8, "right": 28, "top": 12, "bottom": 8}),
                        width="stretch")
    with right:
        st.markdown('<div class="og-section">Review workload</div>', unsafe_allow_html=True)
        st.metric("Orders to review", high + medium, f"{review_pct}% of all orders")
        st.progress(review_pct / 100 if n else 0)
        st.caption("Orders with at least one rule-based signal.")
        st.info("A risk score is a review aid — not proof of fraud.")

    st.markdown('<div class="og-section">Priority review queue</div>', unsafe_allow_html=True)
    priority = df[df.risk_level.isin(["High", "Medium"])].head(6)
    if priority.empty:
        st.success("No orders currently require manual review.")
    else:
        st.dataframe(
            priority[["order_id", "customer", "total", "risk_score", "risk_level"]],
            width="stretch", height=260, hide_index=True,
            column_config={
                "order_id": st.column_config.TextColumn("Order ID", width="small"),
                "customer": st.column_config.TextColumn("Customer", width="medium"),
                "total": st.column_config.NumberColumn("Order value", format="%.2f DT", width="small"),
                "risk_score": st.column_config.ProgressColumn("Risk score", min_value=0, max_value=100, format="%d/100", width="medium"),
                "risk_level": st.column_config.TextColumn("Risk level", width="small"),
            },
        )
        selected_priority = st.selectbox("View suggested action for", priority.order_id.tolist(), key="priority_order_detail")
        selected_item = priority[priority.order_id == selected_priority].iloc[0]
        st.info(f"{selected_item['recommended_action']}")

elif page == "Orders":
    st.markdown('<div class="og-section">All orders</div>', unsafe_allow_html=True)
    a, b = st.columns([1, 2], gap="medium")
    with a:
        level = st.selectbox("Filter by risk", ["All", "High", "Medium", "Low"])
    with b:
        query = st.text_input("Search orders", placeholder="Type an order ID or customer name")
    view = df.copy()
    if level != "All":
        view = view[view.risk_level == level]
    if query.strip():
        view = view[view.order_id.str.contains(query, case=False) | view.customer.str.contains(query, case=False)]
    st.caption(f"Showing {len(view)} of {n} orders")
    st.dataframe(
        view[["order_id", "customer", "phone", "address", "total", "risk_score", "risk_level"]],
        width="stretch", height=360, hide_index=True,
        column_config={
            "order_id": st.column_config.TextColumn("Order ID", width="small"),
            "customer": st.column_config.TextColumn("Customer", width="medium"),
            "phone": st.column_config.TextColumn("Phone", width="small"),
            "address": st.column_config.TextColumn("Address", width="medium"),
            "total": st.column_config.NumberColumn("Order value", format="%.2f DT", width="small"),
            "risk_score": st.column_config.ProgressColumn("Risk score", min_value=0, max_value=100, format="%d/100", width="medium"),
            "risk_level": st.column_config.TextColumn("Risk level", width="small"),
        },
    )
    st.download_button("Export analyzed orders as CSV", df.to_csv(index=False).encode("utf-8-sig"), "orderguard-analysis.csv", "text/csv", type="primary")
    st.markdown('<div class="og-section">Inspect an order</div>', unsafe_allow_html=True)
    if n:
        order_id = st.selectbox("Choose an order", df.order_id.tolist())
        item = df[df.order_id == order_id].iloc[0]
        x, y = st.columns([1, 2], gap="large")
        with x:
            st.metric("Risk score", f"{int(item.risk_score)}/100")
            st.write(f"**Risk level:** {item.risk_level}")
        with y:
            st.markdown("**Risk indicators**")
            st.write(item.risk_reasons)
            st.markdown("**Recommended next step**")
            st.info(item.recommended_action)

else:
    st.markdown('<div class="og-section">How OrderGuard works</div>', unsafe_allow_html=True)
    steps = [
        ("01", "Import orders", "Upload a CSV file or explore the built-in synthetic sample orders."),
        ("02", "Review risk signals", "Transparent rules flag missing contact details, limited order history, higher order values, and notes that need attention."),
        ("03", "Take action", "Use the suggested next step to guide a manual customer confirmation before dispatch."),
        ("04", "Export results", "Download the analyzed order list and continue using your existing workflow."),
    ]
    for number, title, description in steps:
        st.markdown(f'<div class="og-panel" style="margin-bottom:12px"><div class="og-eyebrow">{number}</div><div style="font-size:1.08rem;font-weight:800;color:#172033;margin:5px 0">{title}</div><div style="color:#65718a;line-height:1.6">{description}</div></div>', unsafe_allow_html=True)
    st.warning("This prototype uses explainable rules. It is not a trained fraud model and does not verify a customer's identity or address. A high score does not mean an order is fraudulent.")

st.markdown('<div class="og-footer">ORDERGUARD AI · EARLY PROTOTYPE · KIROWEEN 2026 · Use synthetic data for public demos.</div>', unsafe_allow_html=True)
