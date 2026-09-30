import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Savings Lab - Máy tính tiết kiệm thông minh",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f8fbff 0%, #eef5ff 100%);
    }

    .hero {
        padding: 28px;
        border-radius: 24px;
        background: linear-gradient(135deg, #0f172a, #1d4ed8, #06b6d4);
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 12px 35px rgba(15, 23, 42, 0.20);
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 8px;
    }

    .hero p {
        font-size: 17px;
        opacity: 0.92;
    }

    .card {
        padding: 20px;
        border-radius: 18px;
        background: white;
        box-shadow: 0 5px 20px rgba(15, 23, 42, 0.07);
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }

    .result-card {
        padding: 22px;
        border-radius: 18px;
        background: linear-gradient(135deg, #ffffff, #f0f9ff);
        border: 1px solid #bae6fd;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.10);
    }

    .big-number {
        font-size: 27px;
        font-weight: 800;
        color: #0f172a;
    }

    .small-label {
        color: #64748b;
        font-size: 14px;
    }

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: #dbeafe;
        color: #1d4ed8;
        font-weight: 700;
        font-size: 13px;
    }

    .tip {
        padding: 16px;
        border-left: 5px solid #06b6d4;
        background: #ecfeff;
        border-radius: 10px;
        margin: 10px 0;
    }

    .warning {
        padding: 16px;
        border-left: 5px solid #f59e0b;
        background: #fffbeb;
        border-radius: 10px;
        margin: 10px 0;
    }

    .footer {
        text-align: center;
        color: #64748b;
        padding: 30px;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCTIONS
# =========================================================
def money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


def money_short(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} tỷ"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f} triệu"
    elif value >= 1_000:
        return f"{value / 1_000:.1f} nghìn"
    return f"{value:.0f}"


def calculate_simple(principal, annual_rate, months):
    """
    Lãi đơn:
    I = P * r * t
    """
    years = months / 12
    interest = principal * annual_rate * years
    total = principal + interest

    return interest, total


def calculate_compound(principal, annual_rate, months, frequency):
    """
    Lãi kép.
    frequency:
        monthly = 12
        quarterly = 4
        end = 1
    """
    if frequency == "monthly":
        n = 12
    elif frequency == "quarterly":
        n = 4
    else:
        n = 1

    periods = months / 12 * n

    total = principal * (1 + annual_rate / n) ** periods
    interest = total - principal

    return interest, total


def create_growth_table(
    principal,
    annual_rate,
    months,
    method,
    frequency
):
    rows = []

    if frequency == "monthly":
        period_months = 1
    elif frequency == "quarterly":
        period_months = 3
    else:
        period_months = months

    if method == "Lãi đơn":
        for m in range(1, months + 1):
            interest, total = calculate_simple(
                principal,
                annual_rate,
                m
            )

            rows.append({
                "Tháng": m,
                "Tiền gốc": principal,
                "Tiền lãi": interest,
                "Tổng tiền": total
            })

    else:
        for m in range(1, months + 1):
            interest, total = calculate_compound(
                principal,
                annual_rate,
                m,
                frequency
            )

            rows.append({
                "Tháng": m,
                "Tiền gốc": principal,
                "Tiền lãi": interest,
                "Tổng tiền": total
            })

    return pd.DataFrame(rows)


def financial_health_score(
    principal,
    total_interest,
    months,
    annual_rate
):
    """
    Điểm chỉ mang tính trực quan, không phải đánh giá tài chính cá nhân.
    """
    score = 50

    if annual_rate >= 7:
        score += 15
    elif annual_rate >= 5:
        score += 10

    if months >= 12:
        score += 10

    if total_interest / max(principal, 1) >= 0.05:
        score += 10

    if principal >= 100_000_000:
        score += 10

    return min(score, 100)


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <h1>💰 SAVINGS LAB</h1>
    <p>
        Phòng thí nghiệm tiền gửi tiết kiệm — tính lãi, mô phỏng tăng trưởng,
        so sánh kịch bản và khám phá sức mạnh của lãi kép.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.header("⚙️ Thiết lập")

    st.markdown("### 💵 Tiền gửi")

    principal = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=100_000,
        value=100_000_000,
        step=1_000_000,
        format="%.0f"
    )

    months = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=360,
        value=12,
        step=1
    )

    annual_rate_percent = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )

    annual_rate = annual_rate_percent / 100

    st.markdown("### 🧮 Phương pháp")

    method = st.radio(
        "Chọn cách tính",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    st.markdown("### 💸 Hình thức nhận lãi")

    payout = st.selectbox(
        "Chọn hình thức",
        [
            "Lãnh lãi theo tháng",
            "Lãnh lãi theo quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

    st.divider()

    st.caption(
        "💡 Bạn có thể thay đổi thông số để khám phá "
        "các kịch bản tiết kiệm khác nhau."
    )


# =========================================================
# CONVERT PAYOUT
# =========================================================
if payout == "Lãnh lãi theo tháng":
    frequency = "monthly"
elif payout == "Lãnh lãi theo quý":
    frequency = "quarterly"
else:
    frequency = "end"


# =========================================================
# CALCULATION
# =========================================================
if method == "Lãi đơn":
    total_interest, total_amount = calculate_simple(
        principal,
        annual_rate,
        months
    )
else:
    total_interest, total_amount = calculate_compound(
        principal,
        annual_rate,
        months,
        frequency
    )


# =========================================================
# PERIODIC INTEREST
# =========================================================
if payout == "Lãnh lãi theo tháng":
    if method == "Lãi đơn":
        periodic_interest = principal * annual_rate / 12
    else:
        periodic_interest = principal * annual_rate / 12

elif payout == "Lãnh lãi theo quý":
    if method == "Lãi đơn":
        periodic_interest = principal * annual_rate / 4
    else:
        periodic_interest = principal * annual_rate / 4

else:
    periodic_interest = total_interest


# =========================================================
# TOP METRICS
# =========================================================
st.subheader("📊 Kết quả chính")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="small-label">💵 Tiền lãi định kỳ</div>
            <div class="big-number">{money(periodic_interest)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="small-label">📈 Tổng tiền lãi</div>
            <div class="big-number">{money(total_interest)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="small-label">💰 Tổng gốc + lãi</div>
            <div class="big-number">{money(total_amount)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    interest_rate_effective = (
        total_interest / principal * 100
        if principal > 0
        else 0
    )

    st.markdown(
        f"""
        <div class="result-card">
            <div class="small-label">🚀 Tăng trưởng vốn</div>
            <div class="big-number">
                +{interest_rate_effective:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BASIC INFORMATION
# =========================================================
st.markdown("---")

info1, info2, info3 = st.columns(3)

with info1:
    st.info(
        f"**Số tiền ban đầu**\n\n{money(principal)}"
    )

with info2:
    st.info(
        f"**Kỳ hạn**\n\n{months} tháng"
    )

with info3:
    st.info(
        f"**Lãi suất**\n\n{annual_rate_percent:.2f}%/năm"
    )


# =========================================================
# GROWTH CHART
# =========================================================
st.markdown("---")
st.subheader("📈 Bản đồ tăng trưởng tài sản")

growth_df = create_growth_table(
    principal,
    annual_rate,
    months,
    method,
    frequency
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=growth_df["Tháng"],
        y=growth_df["Tổng tiền"],
        mode="lines",
        name="Tổng tiền",
        line=dict(
            color="#2563eb",
            width=4
        ),
        fill="tozeroy",
        fillcolor="rgba(37, 99, 235, 0.10)"
    )
)

fig.add_trace(
    go.Scatter(
        x=growth_df["Tháng"],
        y=growth_df["Tiền lãi"],
        mode="lines",
        name="Tiền lãi",
        line=dict(
            color="#06b6d4",
            width=3,
            dash="dot"
        )
    )
)

fig.update_layout(
    height=450,
    xaxis_title="Thời gian (tháng)",
    yaxis_title="Giá trị (VNĐ)",
    hovermode="x unified",
    template="plotly_white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# SIMPLE VS COMPOUND
# =========================================================
st.markdown("---")
st.subheader("⚔️ Đấu trường Lãi đơn vs Lãi kép")

simple_interest, simple_total = calculate_simple(
    principal,
    annual_rate,
    months
)

compound_interest, compound_total = calculate_compound(
    principal,
    annual_rate,
    months,
    frequency
)

difference = compound_total - simple_total

compare_df = pd.DataFrame({
    "Phương pháp": [
        "Lãi đơn",
        "Lãi kép"
    ],
    "Tổng tiền lãi": [
        simple_interest,
        compound_interest
    ],
    "Tổng tiền": [
        simple_total,
        compound_total
    ]
})

cc1, cc2 = st.columns(2)

with cc1:
    st.dataframe(
        compare_df.style.format({
            "Tổng tiền lãi": "{:,.0f}",
            "Tổng tiền": "{:,.0f}"
        }),
        use_container_width=True,
        hide_index=True
    )

with cc2:
    comparison_fig = go.Figure()

    comparison_fig.add_trace(
        go.Bar(
            x=["Lãi đơn", "Lãi kép"],
            y=[simple_total, compound_total],
            marker_color=["#94a3b8", "#2563eb"],
            text=[
                money_short(simple_total),
                money_short(compound_total)
            ],
            textposition="auto"
        )
    )

    comparison_fig.update_layout(
        height=300,
        title="Tổng giá trị cuối kỳ",
        yaxis_title="VNĐ",
        template="plotly_white"
    )

    st.plotly_chart(
        comparison_fig,
        use_container_width=True
    )

if difference > 0:
    st.success(
        f"🔥 Trong mô hình hiện tại, chênh lệch giữa hai phương pháp "
        f"là **{money(difference)}**."
    )


# =========================================================
# SMART SCENARIO SIMULATOR
# =========================================================
st.markdown("---")
st.subheader("🧪 Máy mô phỏng 'Nếu như...'")

st.write(
    "Thử thay đổi lãi suất và xem số tiền cuối kỳ có thể thay đổi như thế nào."
)

s1, s2, s3 = st.columns(3)

with s1:
    scenario_rate = st.slider(
        "Lãi suất giả định (%/năm)",
        0.0,
        20.0,
        float(annual_rate_percent),
        0.1
    )

with s2:
    scenario_months = st.slider(
        "Kỳ hạn giả định (tháng)",
        1,
        360,
        int(months),
        1
    )

with s3:
    scenario_method = st.selectbox(
        "Phương pháp",
        ["Lãi đơn", "Lãi kép"],
        key="scenario_method"
    )

scenario_rate_decimal = scenario_rate / 100

if scenario_method == "Lãi đơn":
    scenario_interest, scenario_total = calculate_simple(
        principal,
        scenario_rate_decimal,
        scenario_months
    )
else:
    scenario_interest, scenario_total = calculate_compound(
        principal,
        scenario_rate_decimal,
        scenario_months,
        frequency
    )

st.markdown(
    f"""
    <div class="card">
        <h3>🔮 Kịch bản dự kiến</h3>
        <p>
            Gửi <b>{money(principal)}</b> trong
            <b>{scenario_months} tháng</b> với lãi suất
            <b>{scenario_rate:.2f}%/năm</b>.
        </p>
        <h2>{money(scenario_total)}</h2>
        <p>Tiền lãi: <b>{money(scenario_interest)}</b></p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FINANCIAL GOAL
# =========================================================
st.markdown("---")
st.subheader("🎯 Máy săn mục tiêu tài chính")

goal = st.number_input(
    "Mục tiêu số tiền muốn đạt được (VNĐ)",
    min_value=principal,
    value=max(principal * 1.5, principal + 10_000_000),
    step=1_000_000,
    format="%.0f"
)

goal_rate = st.number_input(
    "Lãi suất dự kiến cho mục tiêu (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=float(annual_rate_percent),
    step=0.1,
    format="%.2f"
)

goal_rate_decimal = goal_rate / 100

if goal_rate_decimal > 0:

    # Tính số tháng cần thiết bằng mô phỏng
    current = principal
    goal_months = 0

    while current < goal and goal_months < 1200:
        goal_months += 1

        current = (
            principal
            * (1 + goal_rate_decimal / 12) ** goal_months
        )

    if current >= goal:

        goal_years = goal_months / 12

        st.success(
            f"🎯 Với mức lãi suất giả định "
            f"**{goal_rate:.2f}%/năm**, cần khoảng "
            f"**{goal_months} tháng ({goal_years:.1f} năm)** "
            f"để đạt **{money(goal)}** nếu không rút lãi."
        )

    else:
        st.warning(
            "Mục tiêu vượt quá khoảng thời gian mô phỏng "
            "tối đa 100 năm."
        )


# =========================================================
# PERIODIC CASHFLOW
# =========================================================
st.markdown("---")
st.subheader("🗓️ Lịch dòng tiền")

if payout == "Lãnh lãi theo tháng":
    periods = range(1, months + 1)
    period_name = "Tháng"

elif payout == "Lãnh lãi theo quý":
    periods = range(3, months + 1, 3)
    period_name = "Tháng"

else:
    periods = [months]
    period_name = "Tháng"

cashflow = []

for m in periods:

    if method == "Lãi đơn":
        interest_m, total_m = calculate_simple(
            principal,
            annual_rate,
            m
        )
    else:
        interest_m, total_m = calculate_compound(
            principal,
            annual_rate,
            m,
            frequency
        )

    cashflow.append({
        period_name: m,
        "Tiền lãi lũy kế": interest_m,
        "Tổng giá trị": total_m
    })

cashflow_df = pd.DataFrame(cashflow)

st.dataframe(
    cashflow_df.style.format({
        "Tiền lãi lũy kế": "{:,.0f}",
        "Tổng giá trị": "{:,.0f}"
    }),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# INTEREST BREAKDOWN
# =========================================================
st.markdown("---")
st.subheader("🍰 Cơ cấu số tiền cuối kỳ")

fig_pie = go.Figure(
    data=[
        go.Pie(
            labels=["Tiền gốc", "Tiền lãi"],
            values=[principal, total_interest],
            hole=0.55,
            marker=dict(
                colors=["#2563eb", "#06b6d4"]
            ),
            textinfo="label+percent"
        )
    ]
)

fig_pie.update_layout(
    height=400,
    showlegend=True,
    template="plotly_white"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)


# =========================================================
# FINANCIAL SCORE
# =========================================================
st.markdown("---")
st.subheader("🧠 Savings Intelligence")

score = financial_health_score(
    principal,
    total_interest,
    months,
    annual_rate_percent
)

sc1, sc2 = st.columns([1, 2])

with sc1:
    st.metric(
        "Chỉ số tăng trưởng mô phỏng",
        f"{score}/100"
    )

with sc2:
    st.progress(score / 100)

st.caption(
    "Chỉ số này chỉ nhằm mục đích trực quan hóa kịch bản mô phỏng, "
    "không phải đánh giá khả năng tài chính hoặc khuyến nghị đầu tư."
)


# =========================================================
# INSIGHT ENGINE
# =========================================================
st.markdown("---")
st.subheader("💡 Savings Insight")

if annual_rate_percent >= 7:
    insight = (
        "Mức lãi suất đang ở vùng tương đối cao trong mô hình. "
        "Hãy kiểm tra kỹ điều kiện áp dụng lãi suất thực tế, "
        "đặc biệt là điều kiện rút trước hạn và tái tục."
    )
elif annual_rate_percent >= 5:
    insight = (
        "Mô hình đang cho thấy lãi suất có ảnh hưởng đáng kể "
        "đến số tiền cuối kỳ. Khi kỳ hạn dài hơn, sự khác biệt "
        "giữa lãi đơn và lãi kép sẽ dễ quan sát hơn."
    )
else:
    insight = (
        "Với mức lãi suất hiện tại, phần tăng trưởng đến chủ yếu "
        "từ tiền gốc. Bạn có thể dùng máy mô phỏng bên trên để "
        "thử các mức lãi suất và kỳ hạn khác nhau."
    )

st.markdown(
    f"""
    <div class="tip">
        💡 <b>Insight:</b> {insight}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DOWNLOAD DATA
# =========================================================
st.markdown("---")
st.subheader("📥 Xuất dữ liệu")

csv = growth_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="⬇️ Tải lịch tăng trưởng CSV",
    data=csv,
    file_name="lich_tang_truong_tien_gui.csv",
    mime="text/csv",
    use_container_width=True
)


# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
    💰 <b>Savings Lab</b> — Công cụ mô phỏng tiền gửi tiết kiệm<br>
    Dữ liệu chỉ mang tính chất tham khảo, không phải tư vấn tài chính.
</div>
""", unsafe_allow_html=True)
