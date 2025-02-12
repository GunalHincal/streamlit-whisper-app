
#STREMLIT UYGULAMASI


import streamlit as st
import whisper
import os
import ffmpeg
from tempfile import NamedTemporaryFile

def convert_to_wav(input_file):
    """ Ses dosyasını WAV formatına çevirir. """
    output_file = "converted_audio.wav"
    try:
        ffmpeg.input(input_file).output(output_file, format="wav").run(overwrite_output=True)
        return output_file
    except Exception as e:
        st.error(f"Ses dönüştürme hatası: {e}")
        return None

def transcribe_audio(audio_file):
    """ Whisper modelini kullanarak ses dosyasını metne çevirir. """
    model = whisper.load_model("large")
    result = model.transcribe(audio_file)
    return result["text"]

# Streamlit arayüzü
st.set_page_config(page_title="Whisper Ses Transkripsiyon", layout="centered")
st.title("🎙️ Ses Dosyası Yükleyin ve Metne Çevirin")

uploaded_file = st.file_uploader(
    "Bir ses dosyası yükleyin (MP3, WAV, MP4, M4A, OGG, CAF, AAC, FLAC vb.)", 
    type=["mp3", "wav", "mp4", "m4a", "ogg", "caf", "aac", "flac"]
)

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_filename = temp_file.name
    
    # Ses dosyasını WAV formatına dönüştür
    wav_filename = convert_to_wav(temp_filename)
    
    if wav_filename:
        st.write("🔄 Ses dosyanız işleniyor, lütfen bekleyin...")
        transcribed_text = transcribe_audio(wav_filename)
        os.remove(wav_filename)  # Geçici dosyayı temizle
        
        st.subheader("📝 Transkripsiyon Sonucu")
        st.text_area("Çıktı:", transcribed_text, height=250)
        
        st.download_button("📥 Metni İndir", transcribed_text, file_name="transcription.txt", mime="text/plain")
    
    os.remove(temp_filename)  # Orijinal dosyayı temizle
