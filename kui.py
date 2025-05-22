import streamlit as st
import pandas as pd
import joblib
from streamlit_lottie import st_lottie
import json
from PIL import Image


# Fungsi konversi jawaban ke skor
def jawaban_ke_skor(jawaban):
    return {'Tidak Setuju': 0.0, 'Netral': 5.0, 'Setuju': 10.0}[jawaban]

# Fungsi load lottie json animation
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

@st.cache_resource

def load_resources():
    model = joblib.load('random_forest_model.pkl')
    gender_encoder = joblib.load('gender_encoder.pkl')
    interest_encoder = joblib.load('interest_encoder.pkl')
    target_encoder = joblib.load('target_encoder.pkl')
    return model, gender_encoder, interest_encoder, target_encoder

# Set page config
st.set_page_config(page_title="Prediksi Tipe Kepribadian", layout="wide")

model, gender_encoder, interest_encoder, target_encoder = load_resources()

if 'page' not in st.session_state:
    st.session_state['page'] = "Form Input"

page = st.sidebar.radio("Navigasi", ["Form Input", "Hasil Prediksi"],
                        index=["Form Input", "Hasil Prediksi"].index(st.session_state['page']))

if page != st.session_state['page']:
    st.session_state['page'] = page

if st.session_state['page'] == "Form Input":
    st.title("🧠 Aplikasi Prediksi Tipe Kepribadian 16 MBTI")
    st.markdown("Silakan isi form di bawah ini untuk memprediksi tipe kepribadian kamu.")

    with st.form("prediction_form"):
        st.header("📋 Form Input Pengguna")

        col1, col2 = st.columns(2)
        with col1:
            age = st.slider("Usia", 10, 100, 21)
            gender = st.radio("Jenis Kelamin", ['Male', 'Female'])
        with col2:
            education = st.selectbox("Tingkat Pendidikan", [
                'Sarjana / SMA / Tidak Berpendidikan',
                'Pascasarjana atau lebih tinggi'
            ])
            interest = st.selectbox("Minat Utama", ['Arts', 'Technology', 'Sports'])

        education_bin = 1 if education == 'Pascasarjana atau lebih tinggi' else 0

        pilihan = ['Tidak Setuju', 'Netral', 'Setuju']
        st.divider()
        st.markdown("### 🧠 Kuesioner Kepribadian")

        questions = [
            "Saya suka berkelompok",
            "Saya lebih suka memikirkan gambaran besar daripada detail",
            "Saya mengambil keputusan berdasarkan logika bukan perasaan",
            "Saya suka merencanakan segala sesuatu dengan rapi",
            "Saya merasa nyaman dengan hal-hal yang sudah terjadwal",
            "Saya senang mencoba hal-hal baru dan berbeda",
            "Saya mudah memperhatikan hal-hal kecil yang orang lain lewatkan",
            "Saya biasanya berpikir sebelum bertindak",
            "Saya suka suasana yang tenang dan tidak bising",
            "Saya cenderung mengandalkan perasaan dalam mengambil keputusan",
            "Saya suka beradaptasi dengan situasi daripada mengikuti aturan ketat",
            "Saya merasa lebih nyaman saat ada jadwal yang jelas"
        ]

        responses = []
        for i, question in enumerate(questions, 1):
            responses.append(st.radio(f"{i}. {question}", pilihan, key=i))

        submitted = st.form_submit_button("🔍 Prediksi")

    if submitted:
        gender_encoded = gender_encoder.transform([gender])[0]
        interest_encoded = interest_encoder.transform([interest])[0]
        scores = [jawaban_ke_skor(j) for j in responses]

        df = pd.DataFrame([[ 
            age,
            gender_encoded,
            education_bin,
            scores[0],
            scores[1],
            scores[2],
            scores[3],
            interest_encoded
        ]], columns=[
            'Age', 'Gender', 'Education',
            'Introversion Score', 'Sensing Score', 'Thinking Score',
            'Judging Score', 'Interest'
        ])

        prediction = model.predict(df)
        result = target_encoder.inverse_transform(prediction)[0]

        st.session_state['prediction_result'] = result
        st.session_state['page'] = "Hasil Prediksi"
        st.rerun()

elif st.session_state['page'] == "Hasil Prediksi":
    st.title("📊 Hasil Prediksi & Rekomendasi Karir")

    result = st.session_state.get('prediction_result', None)
    if not result:
        st.warning("Mohon isi form terlebih dahulu di halaman Form Input.")
    else:
        st.success(f"🎉 Tipe kepribadian kamu adalah: **{result}**")

        try:
            lottie_success = load_lottiefile("success_animation.json")
            st_lottie(lottie_success, height=700)
        except:
            st.info("(Animasi tidak tersedia)")

        col1, col2, col3 = st.columns([3, 2, 3])

        with col2:
            st.image("career.png", caption="Rekomendasi Karir",width=300)

        rekomendasi_karir = {
            "INTJ": ["Ilmuwan", "Insinyur Sistem", "Analis Strategi", "Dosen", "Polisi"],
            "INTP": ["Peneliti", "Programmer", "Data Scientist", "Analis", "Penulis Teknologi"],
            "ENTJ": ["CEO", "Manajer Proyek", "Pengacara", "Konsultan Bisnis"],
            "ENTP": ["Wirausahawan", "Marketing", "Product Manager", "Jurnalis"],
            "INFJ": ["Psikolog", "Konselor", "Guru", "Penulis", "Pekerja Sosial"],
            "INFP": ["Penulis", "Desainer", "Seniman", "HRD", "Editor"],
            "ENFJ": ["Pemimpin Organisasi", "Guru", "Public Speaker", "Manajer HR", "Konsultan"],
            "ENFP": ["Aktor", "Pekerja Sosial", "Public Relation", "Event Organizer", "Marketing Kreatif"],
            "ISTJ": ["Akuntan", "Admin", "Pegawai Negeri", "Teknisi", "Manajer Proyek"],
            "ISFJ": ["Perawat", "Guru", "HR Admin", "Customer Service", "Asisten Medis"],
            "ESTJ": ["Manajer Operasional", "Supervisor", "Tentara", "Polisi", "Manajer Proyek"],
            "ESFJ": ["Perawat", "Event Coordinator", "Marketing Support", "Guru", "Customer Service"],
            "ISTP": ["Teknisi", "Ahli Mesin", "Pilot", "Ahli Logistik", "Polisi"],
            "ISFP": ["Fotografer", "Desainer Interior", "Musisi", "Chef", "Seniman"],
            "ESTP": ["Sales", "Pengusaha", "Detektif", "Trader", "Event Organizer"],
            "ESFP": ["Entertainer", "Host", "Public Relations", "Aktor", "Perawat"],
            "Default": ["Pilih karir yang sesuai dengan minat dan keahlian kamu."]
        }

        karir = rekomendasi_karir.get(result, rekomendasi_karir["Default"])

        st.info(f"💼 Rekomendasi karir untuk tipe kepribadian **{result}**:")
        for k in karir:
            st.write(f"- {k}")

    if st.button("🔙 Kembali ke Form Input"):
        st.session_state['page'] = "Form Input"
        st.rerun()
