import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard GIKnowledge Building 2025",
    layout="wide"
)

st.title("📊 Dashboard GIKnowledge Building 2025")
st.caption("Tugas 1 – Pembangunan Dashboard Interaktif")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("MASTER DATA - GIKNOWLEDGE BUILDING 2025.xlsx")

df = load_data()

# =========================
# PREPROCESSING
# =========================
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
df["Tanggal Pendaftaran"] = df["Timestamp"].dt.date

## =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔎 Filter Data")

filter_jenjang = st.sidebar.multiselect(
    "Jenjang Pendidikan",
    options=df["Jenjang pendidikan asal"].dropna().unique(),
    default=df["Jenjang pendidikan asal"].dropna().unique()
)

filter_gender = st.sidebar.multiselect(
    "Jenis Kelamin",
    options=df["Jenis kelamin"].dropna().unique(),
    default=df["Jenis kelamin"].dropna().unique()
)

df_filtered = df[
    (df["Jenjang pendidikan asal"].isin(filter_jenjang)) &
    (df["Jenis kelamin"].isin(filter_gender))
]

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["📥 Dashboard Pendaftar", "👥 Dashboard Peserta"])

# =====================================================
# TAB 1 – DASHBOARD PENDAFTAR
# =====================================================
with tab1:
    st.subheader("📥 Dashboard Data Pendaftar")

    col1, col2 = st.columns(2)

    # Jenis Kelamin
    fig_gender = px.pie(
        df_filtered,
        names="Jenis kelamin",
        title="Distribusi Jenis Kelamin Pendaftar"
    )
    col1.plotly_chart(fig_gender, use_container_width=True)

    # Jenjang Pendidikan
    jenjang_count = df_filtered["Jenjang pendidikan asal"].value_counts().reset_index()
    jenjang_count.columns = ["Jenjang", "Jumlah"]

    fig_jenjang = px.bar(
        jenjang_count,
        x="Jenjang",
        y="Jumlah",
        title="Jenjang Pendidikan Pendaftar"
    )
    col2.plotly_chart(fig_jenjang, use_container_width=True)

    # Asal Universitas
    st.markdown("### 🎓 Asal Universitas Pendaftar")

    univ_count = df_filtered["Asal Instansi"].value_counts().head(10).reset_index()
    univ_count.columns = ["Universitas", "Jumlah"]

    fig_univ = px.bar(
        univ_count,
        x="Universitas",
        y="Jumlah",
        title="Top 10 Asal Universitas Pendaftar"
    )
    st.plotly_chart(fig_univ, use_container_width=True)

    # Tren Waktu Pendaftaran
    st.markdown("### 📈 Tren Waktu Pendaftaran")

    trend = (
        df_filtered
        .groupby("Tanggal Pendaftaran")
        .size()
        .reset_index(name="Jumlah Pendaftar")
    )

    fig_trend = px.line(
        trend,
        x="Tanggal Pendaftaran",
        y="Jumlah Pendaftar",
        markers=True,
        title="Kapan Waktu Pendaftaran Paling Ramai?"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# =====================================================
# TAB 2 – DASHBOARD PESERTA
# =====================================================
with tab2:
    st.subheader("👥 Dashboard Data Peserta")

    col1, col2 = st.columns(2)

    # Jenjang Pendidikan Peserta
    peserta_jenjang = df_filtered["Jenjang pendidikan asal"].value_counts().reset_index()
    peserta_jenjang.columns = ["Jenjang", "Jumlah"]

    fig_peserta_jenjang = px.bar(
        peserta_jenjang,
        x="Jenjang",
        y="Jumlah",
        title="Jenjang Pendidikan Peserta"
    )
    col1.plotly_chart(fig_peserta_jenjang, use_container_width=True)

    # Asal Universitas Peserta
    peserta_univ = df_filtered["Asal Instansi"].value_counts().head(10).reset_index()
    peserta_univ.columns = ["Universitas", "Jumlah"]

    fig_peserta_univ = px.bar(
        peserta_univ,
        x="Universitas",
        y="Jumlah",
        title="Asal Universitas Peserta"
    )
    col2.plotly_chart(fig_peserta_univ, use_container_width=True)
