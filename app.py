import streamlit as st
st.image("IMG_7834.JPG")
# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="APP TÍNH TIỀN GỬI TIẾT KIỆM TẠI NGÂN HÀNG_NGUYỄN HOÀNG BẢO VY",
    page_icon="💰",
    layout="centered"
)

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# ==============================
# TIÊU ĐỀ
# ==============================
st.title("💰 APP TÍNH LÃI TIỀN GỬI TIẾT KIỆM TẠI NGÂN HÀNG_NGUYỄN HOÀNG BẢO VY💰")
st.caption("Tính toán theo lãi đơn hoặc lãi kép")

st.divider()

# ==============================
# NHẬP THÔNG TIN
# ==============================
st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=1200,
        value=12,
        step=1
    )

    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.01,
        format="%.2f"
    )

with col2:
    loai_lai = st.selectbox(
        "Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    hinh_thuc_nhan_lai = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Lãnh lãi hàng tháng",
            "Lãnh lãi hàng quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

st.divider()

# ==============================
# NÚT TÍNH TOÁN
# ==============================
if st.button("🧮 TÍNH LÃI", type="primary", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất theo tháng
    lai_suat_nam = lai_suat / 100
    lai_suat_thang = lai_suat_nam / 12

    # Tổng số tháng
    so_thang = ky_han

    # ==============================
    # LÃI ĐƠN
    # ==============================
    if loai_lai == "Lãi đơn":

        # Tổng tiền lãi trong toàn bộ kỳ hạn
        tong_tien_lai = tien_gui * lai_suat_nam * (so_thang / 12)

        # Lãi định kỳ
        if hinh_thuc_nhan_lai == "Lãnh lãi hàng tháng":
            lai_dinh_ky = tien_gui * lai_suat_thang

        elif hinh_thuc_nhan_lai == "Lãnh lãi hàng quý":
            lai_dinh_ky = tien_gui * lai_suat_nam / 4

        else:
            lai_dinh_ky = tong_tien_lai

        tong_tien = tien_gui + tong_tien_lai

    # ==============================
    # LÃI KÉP
    # ==============================
    else:

        # Số lần nhập lãi
        if hinh_thuc_nhan_lai == "Lãnh lãi hàng tháng":
            so_ky = so_thang
            lai_moi_ky = lai_suat_nam / 12

        elif hinh_thuc_nhan_lai == "Lãnh lãi hàng quý":
            so_ky = so_thang / 3
            lai_moi_ky = lai_suat_nam / 4

        else:
            # Cuối kỳ: tính theo tháng để phản ánh đúng kỳ hạn
            so_ky = so_thang
            lai_moi_ky = lai_suat_nam / 12

        # Nếu lãnh lãi cuối kỳ:
        # tiền lãi được cộng dồn vào gốc trong quá trình tính
        if hinh_thuc_nhan_lai == "Lãnh lãi cuối kỳ":
            tong_tien = tien_gui * (1 + lai_suat_thang) ** so_thang
            tong_tien_lai = tong_tien - tien_gui
            lai_dinh_ky = tong_tien_lai

        else:
            # Lãi kép theo tháng/quý
            tong_tien = tien_gui * (1 + lai_moi_ky) ** so_ky
            tong_tien_lai = tong_tien - tien_gui

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = tien_gui * lai_moi_ky

    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================
    st.subheader("📊 Kết quả tính toán")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_tien_lai)
        )

    with col3:
        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(tong_tien)
        )

    st.divider()

    # ==============================
    # CHI TIẾT
    # ==============================
    st.subheader("📝 Chi tiết")

    st.write(f"**Số tiền gửi:** {format_money(tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Phương pháp:** {loai_lai}")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")

    st.success(
        f"💰 Sau {ky_han} tháng, tổng số tiền dự kiến là "
        f"**{format_money(tong_tien)}**."
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

### 3. Lãnh lãi hàng tháng

Lãi suất năm được quy đổi theo tháng:

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
