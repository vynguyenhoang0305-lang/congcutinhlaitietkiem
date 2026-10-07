import streamlit as st
import math
import pandas as pd
st.image("IMG_7834.JPG")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Máy tính lãi tiết kiệm",
    page_icon="💰",
    layout="wide"
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================
# TIÊU ĐỀ
# =========================
st.title("💰MÁY TÍNH LÃI TIẾT KIỆM GỬI NGÂN HÀNG_NGUYỄN HOÀNG BẢO VY💰")
st.markdown(
    "Tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép**, "
    "với nhiều hình thức nhận lãi khác nhau."
)

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================
col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

    lai_suat = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1
    )

with col2:
    loai_lai = st.selectbox(
        "🧮 Phương pháp tính lãi",
        ["Lãi đơn", "Lãi kép"]
    )

    hinh_thuc = st.selectbox(
        "💳 Hình thức nhận lãi",
        [
            "Lãnh lãi hàng tháng",
            "Lãnh lãi hàng quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

    muc_tieu = st.number_input(
        "🎯 Mục tiêu tiền nhận được sau kỳ hạn (VNĐ)",
        min_value=0.0,
        value=0.0,
        step=1_000_000.0,
        format="%.0f",
        help="Nhập 0 nếu không muốn sử dụng tính năng này."
    )

st.divider()

# =========================
# NÚT TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    # Lãi suất theo tháng
    lai_suat_nam = lai_suat / 100
    lai_suat_thang = lai_suat_nam / 12

    # Số tháng thực tế
    so_thang = ky_han

    # =========================
    # TÍNH LÃI
    # =========================

    if loai_lai == "Lãi đơn":
        tien_lai = tien_gui * lai_suat_nam * (so_thang / 12)
        tong_tien = tien_gui + tien_lai

        # Lãi định kỳ
        if hinh_thuc == "Lãnh lãi hàng tháng":
            lai_dinh_ky = tien_gui * lai_suat_thang

        elif hinh_thuc == "Lãnh lãi hàng quý":
            lai_dinh_ky = tien_gui * lai_suat_nam / 4

        else:
            lai_dinh_ky = tien_lai

        # Dữ liệu biểu đồ
        gia_tri = []
        for thang in range(0, so_thang + 1):
            gia_tri_thang = tien_gui + (
                tien_gui * lai_suat_nam * (thang / 12)
            )
            gia_tri.append(gia_tri_thang)

    else:
        # Lãi kép:
        # Lãi nhập vào vốn hàng tháng
        tong_tien = tien_gui * ((1 + lai_suat_thang) ** so_thang)
        tien_lai = tong_tien - tien_gui

        if hinh_thuc == "Lãnh lãi hàng tháng":
            lai_dinh_ky = tien_gui * lai_suat_thang

        elif hinh_thuc == "Lãnh lãi hàng quý":
            lai_dinh_ky = tien_gui * (
                (1 + lai_suat_thang) ** 3 - 1
            )

        else:
            lai_dinh_ky = tien_lai

        # Dữ liệu biểu đồ
        gia_tri = []
        for thang in range(0, so_thang + 1):
            gia_tri_thang = tien_gui * (
                (1 + lai_suat_thang) ** thang
            )
            gia_tri.append(gia_tri_thang)

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.subheader("📊 Kết quả tính toán")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with c2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tien_lai)
        )

    with c3:
        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(tong_tien)
        )

    # =========================
    # THÔNG TIN CHI TIẾT
    # =========================

    st.markdown("### 📋 Thông tin khoản gửi")

    thong_tin = pd.DataFrame({
        "Thông tin": [
            "Số tiền gửi",
            "Kỳ hạn",
            "Lãi suất",
            "Phương pháp",
            "Hình thức nhận lãi"
        ],
        "Giá trị": [
            format_money(tien_gui),
            f"{ky_han} tháng",
            f"{lai_suat:.2f}%/năm",
            loai_lai,
            hinh_thuc
        ]
    })

    st.table(thong_tin)

    # =========================
    # BIỂU ĐỒ TĂNG TRƯỞNG
    # =========================

    st.subheader("📈 Biểu đồ tăng trưởng khoản tiền")

    df_chart = pd.DataFrame({
        "Tháng": list(range(0, so_thang + 1)),
        "Giá trị": gia_tri
    })

    ax.plot(
        df_chart["Tháng"],
        df_chart["Giá trị"],
        marker="o"
    )

    ax.set_xlabel("Thời gian (tháng)")
    ax.set_ylabel("Số tiền (VNĐ)")
    ax.set_title("Giá trị khoản tiền theo thời gian")

    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

    # =========================
    # TÍNH NĂNG SÁNG TẠO:
    # MỤC TIÊU TIẾT KIỆM
    # =========================

    if muc_tieu > 0:

        st.divider()
        st.subheader("🎯 Kiểm tra mục tiêu tiết kiệm")

        chenh_lech = tong_tien - muc_tieu

        if chenh_lech >= 0:
            st.success(
                f"🎉 Chúc mừng! Bạn sẽ đạt mục tiêu "
                f"**{format_money(muc_tieu)}**.\n\n"
                f"Bạn sẽ dư khoảng **{format_money(chenh_lech)}**."
            )
        else:
            st.warning(
                f"⚠️ Sau {ky_han} tháng, bạn còn thiếu "
                f"**{format_money(abs(chenh_lech))}** "
                f"để đạt mục tiêu."
            )

        # =========================
        # ƯỚC TÍNH TIỀN GỬI CẦN THIẾT
        # =========================

        if loai_lai == "Lãi kép":
            so_tien_can_gui = muc_tieu / (
                (1 + lai_suat_thang) ** so_thang
            )

        else:
            so_tien_can_gui = muc_tieu / (
                1 + lai_suat_nam * (so_thang / 12)
            )

        st.info(
            f"💡 Để đạt mục tiêu **{format_money(muc_tieu)}** "
            f"sau {ky_han} tháng, với mức lãi suất hiện tại, "
            f"bạn cần gửi khoảng **{format_money(so_tien_can_gui)}** "
            f"ngay từ đầu."
        )

    # =========================
    # SO SÁNH LÃI ĐƠN - LÃI KÉP
    # =========================

    st.divider()
    st.subheader("⚖️ So sánh lãi đơn và lãi kép")

    lai_don = tien_gui * lai_suat_nam * (so_thang / 12)
    tong_don = tien_gui + lai_don

    lai_kep = tien_gui * (
        (1 + lai_suat_thang) ** so_thang
    ) - tien_gui

    tong_kep = tien_gui + lai_kep

    comparison = pd.DataFrame({
        "Phương pháp": [
            "Lãi đơn",
            "Lãi kép"
        ],
        "Tổng tiền lãi": [
            format_money(lai_don),
            format_money(lai_kep)
        ],
        "Tổng gốc + lãi": [
            format_money(tong_don),
            format_money(tong_kep)
        ]
    })

    st.table(comparison)

    chenh_lech_lai = lai_kep - lai_don

    if chenh_lech_lai > 0:
        st.success(
            f"💡 Với các thông số trên, **lãi kép** tạo ra "
            f"nhiều hơn lãi đơn khoảng "
            f"**{format_money(chenh_lech_lai)}**."
        )
    elif chenh_lech_lai == 0:
        st.info("Hai phương pháp cho kết quả bằng nhau.")
    else:
        st.info(
            f"Lãi đơn cao hơn khoảng "
            f"**{format_money(abs(chenh_lech_lai))}**."
        )

# =========================
# FOOTER
# =========================
st.divider()

st.caption(
    "💰 Công cụ tính toán mang tính tham khảo. "
    "Lãi suất thực tế của ngân hàng có thể thay đổi tùy sản phẩm "
    "và điều kiện tiền gửi."
)
# ==============================
# GIẢI THÍCH
# ==============================
with st.expander("ℹ️ Giải thích cách tính"):

    st.markdown("""
### 1. Lãi đơn

Lãi được tính dựa trên số tiền gốc ban đầu và không cộng tiền lãi vào gốc.

**Công thức:**

> Tiền lãi = Tiền gốc × Lãi suất năm × Số năm

---

### 2. Lãi kép

Tiền lãi phát sinh được cộng vào tiền gốc để tiếp tục tính lãi cho kỳ tiếp theo.

**Công thức tổng quát:**

> Tổng tiền = Tiền gốc × (1 + lãi suất kỳ) ^ số kỳ

---

### 3. Lãnh lãi hàng thángLãi suất năm được quy đổi theo tháng:

> Lãi suất tháng = Lãi suất năm / 12

---

### 4. Lãnh lãi hàng quý

Lãi suất năm được quy đổi theo quý:

> Lãi suất quý = Lãi suất năm / 4

---

### Lưu ý

Đây là công cụ tính toán mang tính tham khảo. Lãi suất thực tế của ngân hàng
có thể áp dụng các quy định, phương thức tính ngày và điều kiện sản phẩm
tiền gửi khác nhau.
""")
