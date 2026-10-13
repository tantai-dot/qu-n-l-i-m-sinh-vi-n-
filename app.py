import pandas as pd
import streamlit as st

# 1. Dữ liệu mẫu (kết hợp các yêu cầu trước)
data = {
    "Ho_va_ten": [
        "Nguyễn Văn An",
        "Trần Thị Bình",
        "Lê Văn Cường",
        "Phạm Thị Dung",
        "Hoàng Văn Em",
        "Vũ Thị Phương",
        "Đỗ Văn Giang",
        "Bùi Thị Hoa",
        "Ngô Văn Hùng",
        "Dương Thị Linh",
    ],
    "Chuyen_can": [8.0, 9.0, 7.5, 6.0, 8.5, 9.5, 5.0, 7.0, 8.0, 10.0],
    "Giua_ky": [7.0, 8.5, 6.5, 5.5, 8.0, 9.0, 4.5, 6.5, 7.5, 9.5],
    "Cuoi_ky": [7.5, 8.0, 7.0, 5.0, 8.5, 9.0, 4.0, 6.0, 7.5, 9.0],
}

df = pd.DataFrame(data)

# Tính điểm tổng kết và xếp loại
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"] + 0.3 * df["Giua_ky"] + 0.5 * df["Cuoi_ky"]
).round(2)


def xep_loai(score):
  if score >= 8.5:
    return "Giỏi"
  elif score >= 7.0:
    return "Khá"
  elif score >= 5.0:
    return "Trung bình"
  else:
    return "Yếu"


df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 2. Giao diện Web App với Streamlit
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Hiển thị bảng điểm
st.subheader("Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df, use_container_width=True)

# Thống kê tổng quan
st.subheader("Thống kê chung")
avg_tong_ket = df["Tong_ket"].mean()
max_student = df.loc[df["Tong_ket"].idxmax()]
min_student = df.loc[df["Tong_ket"].idxmin()]
passing_count = (df["Tong_ket"] >= 5.0).sum()

col1, col2 = st.columns(2)
with col1:
  st.metric(label="Điểm TB của lớp", value=f"{avg_tong_ket:.2f}")
  st.metric(
      label="Sinh viên điểm cao nhất",
      value=f"{max_student['Ho_va_ten']} ({max_student['Tong_ket']})",
  )
with col2:
  st.metric(
      label="Số sinh viên đạt (>= 5.0)",
      value=f"{passing_count} / {len(df)}",
  )
  st.metric(
      label="Sinh viên điểm thấp nhất",
      value=f"{min_student['Ho_va_ten']} ({min_student['Tong_ket']})",
  )

# Danh sách xổ xuống chọn sinh viên
st.subheader("Tra cứu thông tin cá nhân sinh viên")
selected_student = st.selectbox(
    "Chọn họ tên sinh viên cần xem:", df["Ho_va_ten"].tolist()
)

# Lọc thông tin sinh viên được chọn
student_info = df[df["Ho_va_ten"] == selected_student].iloc[0]
st.write(f"Kết quả học tập của **{selected_student}**:")
col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
col_s1.metric("Chuyên cần", student_info["Chuyen_can"])
col_s2.metric("Giữa kỳ", student_info["Giua_ky"])
col_s3.metric("Cuối kỳ", student_info["Cuoi_ky"])
col_s4.metric("Tổng kết", student_info["Tong_ket"])
col_s5.metric("Xếp loại", student_info["Xep_loai"])

# Biểu đồ cột điểm tổng kết
st.subheader("Biểu đồ điểm tổng kết của 10 sinh viên")
st.bar_chart(df.set_index("Ho_va_ten")["Tong_ket"])

# Thông tin người tạo ở cuối trang
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>Người tạo ứng"
    " dụng: [Họ và tên của bạn] - MSSV: [Mã số sinh viên của bạn]</p>",
    unsafe_allow_html=True,
)
