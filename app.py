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
    st.error("API Key belum terpasang di Secrets Streamlit!")
    st.stop()

uploaded_files = st.file_uploader(
    "Upload Foto Screenshot Match (Bisa Banyak)", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"Terdeteksi {len(uploaded_files)} foto berhasil di-upload.")
    
    # Gunakan tombol eksekusi
    if st.button("🚀 Mulai Hitung Poin", type="primary"):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            images = [Image.open(file) for file in uploaded_files]
            
            prompt = """
            Kamu adalah juri turnamen esport Free Fire.
            Tugasmu membaca screenshot hasil match ini dan membuat klasemen akhir.
            
            Aturan Poin:
            - Placement Poin: #1=12, #2=9, #3=8, #4=7, #5=6, #6=5, #7=4, #8=3, #9=2, #10=1.
            - Kill Poin: 1 kill = 1 poin.
            
            Tampilkan HANYA 1 Tabel Klasemen Total Akhir dari akumulasi seluruh match gambar yang di-upload.
            Urutkan dari peringkat 1 (poin tertinggi).
            Format Kolom Tabel: Posisi, Nama Tim / Pemain, Total Kill, Total Poin.
            """
            
            with st.spinner("Sedang memproses gambar dan menghitung poin (mohon tunggu beberapa detik)..."):
                response = model.generate_content([prompt, *images])
                
                # Simpan hasil ke session state agar tidak hilang
                st.session_state['hasil_klasemen'] = response.text
                
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses: {e}")

# Tampilkan hasil jika sudah dihitung
if 'hasil_klasemen' in st.session_state:
    st.success("Perhitungan Selesai!")
    st.markdown(st.session_state['hasil_klasemen'])
            """
            
            with st.spinner("Sedang memproses gambar dan menghitung poin..."):
                response = model.generate_content([prompt, *images])
                st.markdown(response.text)
                st.success("Perhitungan selesai!")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
