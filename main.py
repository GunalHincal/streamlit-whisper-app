
#STREMLIT UYGULAMASI


import streamlit as st
import whisper
import os
from tempfile import NamedTemporaryFile

def transcribe_audio(audio_file):
    model = whisper.load_model("large")
    result = model.transcribe(audio_file)
    return result["text"]

# Streamlit arayüzü
st.set_page_config(page_title="Whisper Ses Transkripsiyon", layout="centered")
st.title("🎙️ Ses Dosyası Yükleyin ve Metne Çevirin")

uploaded_file = st.file_uploader("Bir ses dosyası yükleyin (MP3, WAV, MP4 vb.)", type=["mp3", "wav", "mp4"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_filename = temp_file.name
    
    st.write("🔄 Ses dosyanız işleniyor, lütfen bekleyin...")
    transcribed_text = transcribe_audio(temp_filename)
    os.remove(temp_filename)  # Geçici dosyayı temizle
    
    st.subheader("📝 Transkripsiyon Sonucu")
    st.text_area("Çıktı:", transcribed_text, height=250)
    
    st.download_button("📥 Metni İndir", transcribed_text, file_name="transcription.txt", mime="text/plain")