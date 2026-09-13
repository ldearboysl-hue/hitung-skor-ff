import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Hitung Skor FF", layout="centered")
st.title("🏆 Rekap Skor Turnamen Free Fire")
st.write("Upload screenshot hasil match untuk membuat klasemen otomatis!")

# 1. Verifikasi Ketersediaan API Key
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Error: GEMINI_API_KEY belum dimasukkan ke Secrets Streamlit!")
    st.info("Silakan buka Settings > Secrets di Streamlit Cloud dan masukkan API Key Anda.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]

# 2. Upload File Gambar
uploaded_files = st.file_uploader(
    "Upload Foto Screenshot Match (Bisa Banyak)", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"📁 Terdeteksi {len(uploaded_files)} foto berhasil di-upload.")
    
    # Tombol Eksekusi
    if st.button("🚀 Mulai Hitung Poin", type="primary"):
        with st.spinner("Sedang memproses gambar dan menghitung poin... Mohon tunggu 5-10 detik..."):
            try:
                # Konfigurasi Gemini API
                genai.configure(api_key=api_key)
                
                # Gunakan model Flash versi stabil
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Konversi file gambar ke PIL Image
                images = []
                for file in uploaded_files:
                    img = Image.open(file)
                    images.append(img)
                
                prompt = """
                Kamu adalah juri turnamen esport Free Fire profesional.
                Tugasmu adalah membaca seluruh screenshot hasil match ini dan menghitung total klasemen akhir.
                
                Aturan Poin:
                - Placement Poin: #1=12, #2=9, #3=8, #4=7, #5=6, #6=5, #7=4, #8=3, #9=2, #10=1.
                - Kill Poin: 1 kill = 1 poin.
                
                Tunjukkan hasil akhir dalam 1 Tabel Klasemen Total (diurutkan dari peringkat 1 dengan poin tertinggi).
                Sertakan kolom: Posisi, Nama Tim / Pemain, Total Kill, Total Poin.
                """
                
                # Kirim request ke Gemini API
                response = model.generate_content([prompt, *images])
                
                if response.text:
                    st.session_state['hasil_klasemen'] = response.text
                else:
                    st.error("Gagal mendapat respon dari Gemini API. Silakan coba lagi.")
                    
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat menghitung: {e}")

# Tampilkan Hasil Perhitungan jika sudah ada
if 'hasil_klasemen' in st.session_state:
    st.success("🎉 Perhitungan Selesai!")
    st.markdown(st.session_state['hasil_klasemen'])
            - Placement Poin: #1=12, #2=9, #3=8, #4=7, #5=6, #6=5, #7=4, #8=3, #9=2, #10=1.
            - Kill Poin: 1 kill = 1 poin.
            
            Tampilkan HANYA 1 Tabel Klasemen Total Akhir dari akumulasi seluruh match gambar yang di-upload.
            Urutkan dari peringkat 1 (poin tertinggi).
            Format Kolom Tabel: Posisi, Nama Tim / Pemain, Total Kill, Total Poin.
            """
            
            with st.spinner("Sedang memproses gambar dan menghitung poin..."):
                response = model.generate_content([prompt, *images])
                st.session_state['hasil_klasemen'] = response.text
                
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses: {e}")

if 'hasil_klasemen' in st.session_state:
    st.success("Perhitungan Selesai!")
    st.markdown(st.session_state['hasil_klasemen'])
