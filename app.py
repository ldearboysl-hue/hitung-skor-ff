import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Hitung Skor FF", layout="centered")
st.title("🏆 Rekap Skor Turnamen Free Fire")
st.write("Upload screenshot hasil match untuk membuat klasemen otomatis!")

# Ambil API Key dari Secrets Streamlit
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ GEMINI_API_KEY belum terpasang di Secrets Streamlit!")
    st.stop()

uploaded_files = st.file_uploader(
    "Upload Foto Screenshot Match (Bisa Banyak)", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

# Tombol selalu muncul di bawah area upload
if st.button("🚀 Mulai Hitung Poin", type="primary", use_container_width=True):
    if not uploaded_files:
        st.warning("Silakan upload minimal 1 foto screenshot match terlebih dahulu!")
    else:
        with st.spinner("Sedang memproses gambar dan menghitung poin... Mohon tunggu 5-10 detik..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                images = [Image.open(file) for file in uploaded_files]
                
                prompt = """
                Kamu adalah juri turnamen esport Free Fire profesional.
                Tugasmu membaca seluruh screenshot hasil match ini dan membuat klasemen akhir.
                
                Aturan Poin:
                - Placement Poin: #1=12, #2=9, #3=8, #4=7, #5=6, #6=5, #7=4, #8=3, #9=2, #10=1.
                - Kill Poin: 1 kill = 1 poin.
                
                Tunjukkan HANYA 1 Tabel Klasemen Total Akhir dari akumulasi seluruh match gambar yang di-upload.
                Urutkan dari peringkat 1 (poin tertinggi).
                Format Kolom Tabel: Posisi, Nama Tim / Pemain, Total Kill, Total Poin.
                """
                
                response = model.generate_content([prompt, *images])
                
                if response.text:
                    st.session_state['hasil_klasemen'] = response.text
                else:
                    st.error("Gagal mendapat respon dari API. Silakan coba lagi.")
                    
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat menghitung: {e}")

# Tampilkan Hasil Perhitungan
if 'hasil_klasemen' in st.session_state:
    st.divider()
    st.success("🎉 Perhitungan Selesai!")
    st.markdown(st.session_state['hasil_klasemen'])
