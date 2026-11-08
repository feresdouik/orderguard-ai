import altair as alt
import pandas as pd
import streamlit as st

from risk_engine import REQUIRED_COLUMNS, prepare_orders

st.set_page_config(page_title="OrderGuard AI", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

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
:root{--ink:#172033;--muted:#65718a;--line:#e5e9f2;--purple:#6846d9}
html,body,[class*="css"]{font-family:Inter,sans-serif!important}
.stApp,[data-testid="stAppViewContainer"]{background:#f5f7fb;color:var(--ink)}
.block-container{max-width:1480px;padding:2rem 2.4rem 3rem}
[data-testid="stVerticalBlock"]{gap:1rem}
[data-testid="stSidebar"] .block-container{padding:1.5rem 1rem 2rem}
[data-testid="stSidebar"]{background:#111827;border-right:1px solid #273247}
[data-testid="stSidebar"] *{color:#eef2ff!important}
[data-testid="stSidebar"] [data-testid="stFileUploader"] section{background:#1d2739!important;border:1px dashed #64748b!important}
[data-testid="stSidebar"] [data-testid="stFileUploader"] section *{color:#f8fafc!important}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button{background:#f8fafc!important;color:#172033!important}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button *{color:#172033!important}
.og-brand{color:#fff;font-size:1.35rem;font-weight:800;letter-spacing:-.04em}
.og-brand span{color:#a995ff}
.og-side-note{color:#9eabc1;font-size:.7rem;letter-spacing:.13em;font-weight:700}
.og-code{background:#263449;border:1px solid #40516b;border-radius:10px;padding:11px;color:#f8fafc!important;font: .7rem/1.8 ui-monospace,monospace;overflow-wrap:anywhere}
.og-eyebrow{display:block;color:#6846d9;font-size:.72rem;line-height:1.5;letter-spacing:.15em;font-weight:800;margin:0 0 8px;overflow-wrap:anywhere}
[data-testid="stHeading"] h1{color:#172033!important;font-size:clamp(1.8rem,3.2vw,2.5rem)!important;line-height:1.2!important;font-weight:800!important;letter-spacing:-.04em!important;margin:0!important;padding:0!important;overflow-wrap:anywhere}
.og-subtitle{display:block;max-width:820px;color:#65718a;font-size:1rem;line-height:1.7;margin:8px 0 26px;overflow-wrap:anywhere}
@media(max-width:700px){.block-container{padding:1.2rem 1rem 2rem}.og-subtitle{font-size:.92rem;line-height:1.6;margin-bottom:20px}}
.og-section{color:#172033;font-size:1.2rem;font-weight:800;letter-spacing:-.025em;margin:1.5rem 0 .8rem}
.og-card{background:#fff;border:1px solid #e5e9f2;border-radius:16px;padding:18px 20px;box-shadow:0 5px 18px #17203308;min-height:126px;height:100%}
.og-card-label{color:#69758c;font-size:.72rem;letter-spacing:.08em;font-weight:800}
.og-card-value{color:#172033;font-size:2.1rem;line-height:1.25;font-weight:800;margin-top:9px}
.og-card-note{color:#8791a5;font-size:.78rem;margin-top:4px}
.og-panel{background:#fff;border:1px solid #e5e9f2;border-radius:15px;padding:20px 22px;box-shadow:0 5px 18px #17203308;margin-bottom:12px}
.og-muted{color:#65718a;font-size:.9rem;line-height:1.65}
[data-testid="stAlert"]{border-radius:12px}
.og-footer{border-top:1px solid #e5e9f2;margin-top:2.3rem;padding-top:1rem;color:#8993a6;font-size:.75rem}
[data-testid="stMetric"]{background:#fff;border:1px solid #e5e9f2;border-radius:14px;padding:13px 15px;box-shadow:0 4px 14px #17203308}
[data-testid="stMetricLabel"] p{color:#65718a!important;font-weight:700}
[data-testid="stMetricValue"]{color:#172033!important;font-weight:800}
[data-testid="stDataFrame"]{background:#fff;border:1px solid #e5e9f2;border-radius:12px;overflow:hidden}
[data-testid="stDataFrame"] *{color:#172033}
.stTextInput input,.stSelectbox div[data-baseweb="select"]>div{background:#fff!important;color:#172033!important;border-color:#d9dfeb!important;border-radius:10px!important}
.stButton button,.stDownloadButton button{border-radius:10px;font-weight:700;min-height:2.6rem}
.stProgress>div>div>div{background:#6846d9}
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown('<div class="og-brand">🛡️ OrderGuard <span>AI</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="og-side-note">ORDER REVIEW WORKSPACE</div>', unsafe_allow_html=True)
    st.divider()
    page = st.radio("WORKSPACE", ["Overview", "Orders", "Analytics", "How it works"], label_visibility="visible")
    st.divider()
    st.markdown("**Import your orders**")
    upload = st.file_uploader("Choose a CSV file", type=["csv"], help="Maximum 200 MB. Use the required columns below.")
    st.caption("Required CSV columns")
    st.markdown('<div class="og-code">order_id, customer,<br>phone, address, total,<br>previous_orders, notes</div>', unsafe_allow_html=True)
    st.divider()
    if upload:
        st.caption(f"Loaded file: {upload.name}")
    else:
        st.caption("Using built-in synthetic demo data")
    st.markdown('<div class="og-side-note">PROTOTYPE · KIROWEEN 2026</div>', unsafe_allow_html=True)

try:
    if upload is not None:
        raw = pd.read_csv(upload, encoding="utf-8-sig")
        if len(raw.columns) == 0:
            st.error("The uploaded CSV is empty. Add the required columns and at least one order.")
            st.stop()
        if raw.empty:
            st.error("The uploaded CSV has no data rows. Add at least one order below the header.")
            st.stop()
        missing = [col for col in REQUIRED_COLUMNS if col not in raw.columns]
        if missing:
            st.error("CSV is missing required columns: " + ", ".join(missing))
            st.stop()
        raw = raw[REQUIRED_COLUMNS]
    else:
        raw = pd.DataFrame(SAMPLE, columns=REQUIRED_COLUMNS)
    df = prepare_orders(raw)
except Exception as exc:
    st.error(f"Could not read this CSV file: {exc}")
    st.stop()

n = len(df)
high = int((df.risk_level == "High").sum())
medium = int((df.risk_level == "Medium").sum())
low = int((df.risk_level == "Low").sum())
review = high + medium
review_pct = round(review / n * 100) if n else 0
issues_count = int((df.data_issues != "").sum())
average_value = float(df.total.mean()) if n else 0

page_headers = {
    "Overview": ("E-COMMERCE ORDER INTELLIGENCE", "Order command center", "A clear snapshot of incoming orders, review priorities, and data quality."),
    "Orders": ("ORDER OPERATIONS", "Manage orders", "Search, filter, inspect, and export orders from your current dataset."),
    "Analytics": ("PERFORMANCE INSIGHTS", "Order analytics", "Understand order values, risk signals, and data quality at a glance."),
    "How it works": ("PRODUCT GUIDE", "How OrderGuard works", "Learn how order data is checked and how review recommendations are generated."),
}
eyebrow, heading, subtitle = page_headers[page]
st.markdown(f'<div class="og-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
st.title(heading)
st.markdown(f'<div class="og-subtitle">{subtitle}</div>', unsafe_allow_html=True)

if page == "Overview":
    cols = st.columns(4, gap="medium")
    metrics = [
        ("TOTAL ORDERS", n, "Orders in this dataset"),
        ("HIGH RISK", high, "Manual confirmation priority"),
        ("MEDIUM RISK", medium, "Review details before dispatch"),
        ("DATA ISSUES", issues_count, "Rows with invalid or missing fields"),
    ]
    for col, (label, value, note) in zip(cols, metrics):
        with col:
            st.markdown(f'<div class="og-card"><div class="og-card-label">{label}</div><div class="og-card-value">{value}</div><div class="og-card-note">{note}</div></div>', unsafe_allow_html=True)

    left, right = st.columns([1.35, 1], gap="large")
    with left:
        st.markdown('<div class="og-section">Risk distribution</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({"Risk level": ["High risk", "Needs review", "Low risk"], "Orders": [high, medium, low]})
        bars = alt.Chart(chart_data).mark_bar(cornerRadiusEnd=7, height=34).encode(
            y=alt.Y("Risk level:N", sort=["High risk", "Needs review", "Low risk"], title=None,
                    axis=alt.Axis(labelFontSize=13, labelColor="#47536b", ticks=False, domain=False)),
            x=alt.X("Orders:Q", title="Number of orders", scale=alt.Scale(domain=[0, max(1, int(chart_data.Orders.max()) + 1)]),
                    axis=alt.Axis(tickMinStep=1, labelFontSize=11, labelColor="#65718a", gridColor="#edf0f6")),
            color=alt.Color("Risk level:N", scale=alt.Scale(domain=["High risk", "Needs review", "Low risk"],
                range=["#d84d5b", "#e5a33c", "#36a887"]), legend=None),
            tooltip=["Risk level", "Orders"],
        )
        labels = bars.mark_text(align="left", baseline="middle", dx=8, fontSize=13, fontWeight="bold", color="#172033").encode(text="Orders:Q")
        st.altair_chart((bars + labels).properties(height=190), width="stretch")
    with right:
        st.markdown('<div class="og-section">Review workload</div>', unsafe_allow_html=True)
        st.metric("Orders to review", review, f"{review_pct}% of all orders")
        st.progress(review_pct / 100 if n else 0)
        st.caption("Share of orders with medium or high rule-based risk.")
        st.metric("Average order value", f"{average_value:,.2f} DT")
        st.info("Scores are review signals, not proof of fraud.")

    st.markdown('<div class="og-section">Priority review queue</div>', unsafe_allow_html=True)
    priority = df[df.risk_level.isin(["High", "Medium"])].head(8)
    if priority.empty:
        st.success("No orders currently require manual review.")
    else:
        st.dataframe(priority[["order_id", "customer", "total", "risk_score", "risk_level"]],
            width="stretch", height=280, hide_index=True,
            column_config={
                "order_id": st.column_config.TextColumn("Order ID", width="small"),
                "customer": st.column_config.TextColumn("Customer", width="medium"),
                "total": st.column_config.NumberColumn("Order value", format="%.2f DT", width="small"),
                "risk_score": st.column_config.ProgressColumn("Risk score", min_value=0, max_value=100, format="%d/100", width="medium"),
                "risk_level": st.column_config.TextColumn("Risk level", width="small"),
            })
        chosen_pos = st.selectbox(
            "Suggested action for order",
            options=list(range(len(priority))),
            format_func=lambda i: f"{priority.iloc[i].order_id} — {priority.iloc[i].customer or 'Unknown customer'}",
        )
        st.info(priority.iloc[chosen_pos].recommended_action)

elif page == "Orders":
    st.markdown('<div class="og-section">Filter orders</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c1: level = st.selectbox("Risk level", ["All", "High", "Medium", "Low"])
    with c2: query = st.text_input("Search", placeholder="Order ID, customer, phone, or address")
    with c3: issue_filter = st.selectbox("Data quality", ["All rows", "Issues only", "No issues"])
    view = df.copy()
    if level != "All": view = view[view.risk_level == level]
    if query.strip():
        mask = pd.Series(False, index=view.index)
        for col in ["order_id", "customer", "phone", "address"]:
            mask |= view[col].str.contains(query.strip(), case=False, na=False, regex=False)
        view = view[mask]
    if issue_filter == "Issues only": view = view[view.data_issues != ""]
    elif issue_filter == "No issues": view = view[view.data_issues == ""]
    st.caption(f"Showing {len(view)} of {n} orders")
    if view.empty:
        st.info("No orders match these filters. Try changing the risk level, search term, or data-quality filter.")
    else:
        st.dataframe(view[["order_id", "customer", "phone", "address", "total", "risk_score", "risk_level"]],
            width="stretch", height=390, hide_index=True,
            column_config={
                "order_id": st.column_config.TextColumn("Order ID", width="small"),
                "customer": st.column_config.TextColumn("Customer", width="medium"),
                "phone": st.column_config.TextColumn("Phone", width="small"),
                "address": st.column_config.TextColumn("Address", width="medium"),
                "total": st.column_config.NumberColumn("Order value", format="%.2f DT", width="small"),
                "risk_score": st.column_config.ProgressColumn("Risk score", min_value=0, max_value=100, format="%d/100", width="medium"),
                "risk_level": st.column_config.TextColumn("Risk level", width="small"),
            })
    download_col, count_col = st.columns([1, 2], vertical_alignment="center")
    with download_col:
        st.download_button("Export filtered orders", view.to_csv(index=False).encode("utf-8-sig"), "orderguard-orders.csv", "text/csv", type="primary", width="stretch")
    with count_col:
        st.caption(f"{len(view)} matching orders · {issues_count} data-quality issues in the full dataset")
    st.markdown('<div class="og-section">Order investigation</div>', unsafe_allow_html=True)
    if n:
        selected_index = st.selectbox(
            "Select an order to inspect",
            options=list(range(n)),
            format_func=lambda index: f"{df.iloc[index].order_id or 'No ID'} — {df.iloc[index].customer or 'Unknown customer'}",
            key="order_inspector",
        )
        item = df.iloc[selected_index]
        a, b = st.columns([1, 2], gap="large")
        with a:
            st.metric("Risk score", f"{int(item.risk_score)}/100", item.risk_level)
            st.write(f"**Customer:** {item.customer or 'Not provided'}")
            st.write(f"**Phone:** {item.phone or 'Not provided'}")
            st.write(f"**Address:** {item.address or 'Not provided'}")
            st.write(f"**Order value:** {item.total:,.2f} DT")
        with b:
            st.markdown("**Risk indicators**")
            st.write(item.risk_reasons)
            if item.data_issues:
                st.error(f"Data quality: {item.data_issues}")
            st.markdown("**Recommended next step**")
            st.info(item.recommended_action)
            st.caption("This recommendation supports manual review; it does not automatically reject an order.")

elif page == "Analytics":
    st.markdown('<div class="og-section">Order analytics</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    a.metric("Average order value", f"{average_value:,.2f} DT")
    b.metric("Orders with review signals", review, f"{review_pct}%")
    c.metric("Data quality issues", issues_count)
    st.markdown('<div class="og-section">Order value by risk level</div>', unsafe_allow_html=True)
    value_chart = df.groupby("risk_level", as_index=False).agg(Orders=("order_id", "count"), Average_value=("total", "mean"))
    if not value_chart.empty:
        chart = alt.Chart(value_chart).mark_bar(cornerRadiusEnd=6).encode(
            x=alt.X("risk_level:N", sort=["High", "Medium", "Low"], title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Average_value:Q", title="Average order value (DT)"),
            color=alt.Color("risk_level:N", scale=alt.Scale(domain=["High", "Medium", "Low"], range=["#d84d5b", "#e5a33c", "#36a887"]), legend=None),
            tooltip=["risk_level", "Orders", alt.Tooltip("Average_value:Q", format=".2f")])
        st.altair_chart(chart.properties(height=300), width="stretch")
    st.markdown('<div class="og-section">Risk level breakdown</div>', unsafe_allow_html=True)
    breakdown = pd.DataFrame({"Risk level": ["High", "Medium", "Low"], "Orders": [high, medium, low]})
    st.dataframe(breakdown, width="stretch", hide_index=True)
    st.caption("Analytics are calculated from the currently loaded CSV or synthetic demo dataset.")
    st.info("Risk levels are heuristic review indicators. They should support human checks, not automated order rejection.")

else:
    st.markdown('<div class="og-section">How OrderGuard works</div>', unsafe_allow_html=True)
    steps = [
        ("01", "Import orders", "Upload a CSV with the seven required fields or use the built-in synthetic sample."),
        ("02", "Validate the data", "The app checks required columns and flags missing IDs, missing customer names, and invalid numeric values."),
        ("03", "Review risk signals", "Transparent rules score missing contact details, limited order history, higher order values, and notes that need attention."),
        ("04", "Investigate and act", "Open an order, read the reasons behind its score, and use the suggested manual confirmation step."),
        ("05", "Export results", "Download the analyzed order dataset as a CSV file for your workflow."),
    ]
    for number, title, description in steps:
        st.markdown(f'<div class="og-panel" style="margin-bottom:12px"><div class="og-eyebrow">{number}</div><div style="font-size:1.08rem;font-weight:800;color:#172033;margin:5px 0">{title}</div><div style="color:#65718a;line-height:1.6">{description}</div></div>', unsafe_allow_html=True)
    st.warning("Prototype limitation: OrderGuard currently uses transparent rule-based scoring, not a trained machine-learning model. It does not verify identity, phone ownership, or delivery addresses. Use synthetic data for public demos.")

st.markdown('<div class="og-footer">ORDERGUARD AI · EARLY PROTOTYPE · KIROWEEN 2026 · Use synthetic data for public demos.</div>', unsafe_allow_html=True)
