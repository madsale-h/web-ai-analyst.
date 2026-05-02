import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# 1. Masukkan API Key
API_KEY = "AIzaSyBM68EZoH4L9IRmEmiKtvtx4J7R0XCRNXw"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash') 

st.set_page_config(page_title="AI Analyst Pro", page_icon="💎", layout="wide")
st.title("💎 AI Data Analyst & Interactive Dashboard")

# --- FITUR ANTI-AMNESIA (SESSION STATE) ---
if 'data_bersih' not in st.session_state:
    st.session_state.data_bersih = None

uploaded_file = st.file_uploader("Upload file Excel/CSV di sini", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    # Baca data
    if uploaded_file.name.endswith('csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.write("### 1. Data Asli (Masih Kotor)")
    st.dataframe(df.head())

    st.write("---")
    
    # Tombol Pembersih Data
    if st.button("🧹 Bersihkan Data Otomatis"):
        # Bersihkan dan SIMPAN ke ingatan Streamlit
        st.session_state.data_bersih = df.dropna().drop_duplicates()
        st.success("✅ Data bersih dan tersimpan di memori!")

    # Jika memori data bersih sudah ada, tampilkan sisanya
    if st.session_state.data_bersih is not None:
        df_bersih = st.session_state.data_bersih
        
        st.write("### 2. Hasil Data Bersih")
        st.dataframe(df_bersih.head())
        
        st.write("---")
        st.write("### 3. Dashboard Interaktif (Plotly)")
        
        kolom_angka = df_bersih.select_dtypes(include='number').columns.tolist()
        
        if len(kolom_angka) > 0:
            # Menggunakan Plotly untuk grafik yang elegan dan interaktif
            fig = px.line(df_bersih, y=kolom_angka[0], title=f"Tren Data: {kolom_angka[0]}", markers=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tambahan chart kedua kalau ada lebih dari 1 kolom angka
            if len(kolom_angka) > 1:
                fig2 = px.bar(df_bersih, y=kolom_angka[1], title=f"Distribusi Data: {kolom_angka[1]}")
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Tidak ada kolom angka untuk dibuatkan grafik.")

        st.write("---")
        st.write("### 4. Konsultan AI")
        
        # Tombol Analisis AI sekarang tidak akan hilang
        if st.button("🧠 Minta AI Analisis Sekarang!"):
            with st.spinner('AI sedang menganalisis secara mendalam...'):
                try:
                    data_text = df_bersih.head(50).to_string()
                    perintah_ke_ai = f"""
                    Kamu adalah data analyst senior. Analisis data bersih berikut ini.
                    Berikan:
                    1. Pola tersembunyi yang menarik.
                    2. Anomali (jika ada data yang aneh).
                    3. Action plan bisnis 1 bulan ke depan.
                    Bahasa: Indonesia santai dan profesional.
                    Data:\n\n{data_text}
                    """
                    response = model.generate_content(perintah_ke_ai)
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error AI: {e}")