import streamlit as st
import pandas as pd
import altair as alt


fb = pd.read_csv('fb_summary.csv') 
gl = pd.read_csv('gl_summary.csv')
tt = pd.read_csv('tt_summary.csv')

kpi = pd.read_csv('platform_level_kpi.csv')


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Marketing KPI Dashboard", layout="wide")
st.title("Marketing Platform KPI Dashboard")
st.caption("Comparative view of Facebook, Google & TikTok ad performance")

# ── Platform color scheme ────────────────────────────────────────────────────
PLATFORM_COLORS = alt.Scale(
    domain=["Facebook", "Google", "TikTok"],
    range=["#1877F2", "#FBBC05", "#EE1D52"],  # blue, yellow, red
)

def kpi_bar_chart(data, metric, title):
    """Reusable Altair bar chart with platform colors."""
    return (
        alt.Chart(data)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("platform:N", sort=["Facebook", "Google", "TikTok"], title=None),
            y=alt.Y(f"{metric}:Q", title=title),
            color=alt.Color("platform:N", scale=PLATFORM_COLORS, legend=None),
            tooltip=["platform", alt.Tooltip(f"{metric}:Q", format=",.2f")],
        )
        .properties(height=350)
    )

# ── Metric cards (one column per platform) ───────────────────────────────────
st.subheader("Platform Overview")
cols = st.columns(3)
for i, row in kpi.iterrows():
    with cols[i]:
        st.markdown(f"### {row['platform']}")
        st.metric("Total Conversions", f"{row['total_conversions']:,}")
        st.metric("Total Cost", f"${row['total_cost']:,.2f}")
        st.metric("Cost per Conversion", f"${row['cost_per_conversion']:.2f}")
        st.metric("Clicks / Conversion", f"{row['clicks_to_conversion']:.1f}")
        st.metric("Impressions / Conversion", f"{row['impressions_to_conversion']:,.1f}")

# ── Full KPI table ───────────────────────────────────────────────────────────
st.divider()
st.subheader("Full KPI Table")
st.dataframe(
    kpi.style.format({
        "total_cost": "${:,.2f}",
        "total_conversions": "{:,}",
        "total_clicks": "{:,}",
        "total_impressions": "{:,}",
        "clicks_to_conversion": "{:.2f}",
        "impressions_to_conversion": "{:,.2f}",
        "cost_per_conversion": "${:.2f}",
    }),
    use_container_width=True,
    hide_index=True,
)

# ── Comparison bar charts ────────────────────────────────────────────────────
# st.divider()
# st.subheader("Comparison Charts")

# chart_col1, chart_col2 = st.columns(2)
# with chart_col1:
#     st.markdown("**Total Conversions**")
#     st.bar_chart(kpi.set_index("platform")["total_conversions"])
# with chart_col2:
#     st.markdown("**Cost per Click ($)**")
#     st.bar_chart(kpi.set_index("platform")["cost_per_conversion"])

# chart_col3, chart_col4 = st.columns(2)
# with chart_col3:
#     st.markdown("**Total Cost ($)**")
#     st.bar_chart(kpi.set_index("platform")["total_cost"])
# with chart_col4:
#     st.markdown("**Clicks per Conversion**")
#     st.bar_chart(kpi.set_index("platform")["clicks_to_conversion"])
# ── Comparison bar charts ────────────────────────────────────────────────────
st.divider()
st.subheader("Comparison Charts")

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.altair_chart(kpi_bar_chart(kpi, "total_conversions", "Total Conversions"), use_container_width=True)
with chart_col2:
    st.altair_chart(kpi_bar_chart(kpi, "cost_per_conversion", "Cost per Conversion ($)"), use_container_width=True)

chart_col3, chart_col4 = st.columns(2)
with chart_col3:
    st.altair_chart(kpi_bar_chart(kpi, "total_cost", "Total Cost ($)"), use_container_width=True)
with chart_col4:
    st.altair_chart(kpi_bar_chart(kpi, "clicks_to_conversion", "Clicks per Conversion"), use_container_width=True)