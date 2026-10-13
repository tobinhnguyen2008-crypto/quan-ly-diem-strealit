import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Cấu hình trang web
st.set_page_config(page_title="Quản lý điểm sinh viên", layout="wide")

# Tiêu đề chính
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 1. Khởi tạo dữ liệu
data = {
    "Họ và tên": [
        "An",
        "Bình",
        "Chi",
        "Dũng",
        "Hà",
        "Lan",
        "Minh",
        "Nam",
        "Phúc",
        "Nhật",
    ],
    "Chuyên cần": [8.5, 9.0, 7.0, 9.5, 8.0, 6.0, 9.0, 7.5, 8.0, 9.5],
    "Giữa kỳ": [7.5, 8.5, 6.5, 9.0, 7.0, 5.5, 8.5, 6.5, 7.5, 9.0],
    "Cuối kỳ": [8.0, 8.5, 6.5, 9.0, 7.5, 6.0, 8.5, 7.0, 7.5, 9.0],
}

df = pd.DataFrame(data)

# Tính điểm tổng kết
df["Tong_ket"] = (
    df["Chuyên cần"] * 0.2 + df["Giữa kỳ"] * 0.3 + df["Cuối kỳ"] * 0.5
).round(2)


# Hàm xếp loại
def xep_loai(diem):
  if diem >= 8.5:
    return "Giỏi"
  elif diem >= 7.0:
    return "Khá"
  elif diem >= 5.0:
    return "Trung bình"
  else:
    return "Yếu"


df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 2. Hiển thị bảng điểm
st.subheader("Bảng điểm sinh viên")
st.dataframe(df, use_container_width=True)

# 3. Thống kê
st.subheader("Thống kê chung")
col1, col2, col3, col4 = st.columns(4)

diem_tb = df["Tong_ket"].mean()
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = (df["Tong_ket"] >= 5.0).sum()

col1.metric("Điểm TB cả lớp", f"{diem_tb:.2f}")
col2.metric("Cao nhất", f"{sv_max['Họ và tên']} ({sv_max['Tong_ket']})")
col3.metric("Thấp nhất", f"{sv_min['Họ và tên']} ({sv_min['Tong_ket']})")
col4.metric("Số SV đạt (>=5)", f"{so_sv_dat}/{len(df)}")

st.divider()

# 4. Tra cứu thông tin từng sinh viên bằng Selectbox
st.subheader("Tra cứu thông tin sinh viên")
selected_student = st.selectbox("Chọn sinh viên:", df["Họ và tên"].unique())

student_info = df[df["Họ và tên"] == selected_student].iloc[0]

# Hiển thị thông tin sinh viên được chọn
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", student_info["Chuyên cần"])
c2.metric("Giữa kỳ", student_info["Giữa kỳ"])
c3.metric("Cuối kỳ", student_info["Cuối kỳ"])
c4.metric("Điểm tổng kết", student_info["Tong_ket"])
c5.metric("Xếp loại", student_info["Xep_loai"])

st.divider()

# 5. Biểu đồ điểm tổng kết
st.subheader("Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(df["Họ và tên"], df["Tong_ket"], color="#4a90e2")
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Họ và tên")
ax.set_xlim(0, 10)
ax.invert_yaxis()

for i, v in enumerate(df["Tong_ket"]):
  ax.text(v + 0.1, i, str(v), va="center")

st.pyplot(fig)

# 6. Thông tin người tạo (ở cuối trang, cỡ chữ nhỏ)
st.markdown("---")
st.caption("Người thực hiện: Tô Bình Nguyên | MSSV: 052208")
