import streamlit as st
import os 
from logik import songclass
from st_audiorec import st_audiorec

st.write("abracadabra")
         
tab1, tab2 = st.tabs(["upload music","recognize music"])

with tab1:
    st.header("upload music")

    uploaded_song = st.file_uploader("Choose a file", type=['mp3'])
        
    if uploaded_song is not None:
        # Den Dateinamen extrahieren
        filename = uploaded_song.name

        # Die Audiodaten aus der hochgeladenen Datei lesen
        audio_data = uploaded_song.read()

        # Die lokal gespeicherte Audiodatei wiedergeben
        st.audio(audio_data)

        if st.button("upload Song", key="upload Song"):

            # Den Dateipfad für die lokale Speicherung erstellen
            file_path = os.path.join("uploaded_songs", filename)

            if os.path.exists(file_path):
                st.error(f"Die Datei {filename} existiert bereits. Bitte ändern Sie den Dateinamen und laden Sie die Datei erneut.")
            else:
                # Die Audiodaten in die lokale Datei schreiben
                with open(file_path, "wb") as f:
                    f.write(audio_data)

                # Bestätigung anzeigen
                st.success(f"Die Datei wurde erfolgreich gespeichert: {file_path}")
            
            song = songclass.Song( filename, file_path, "Test", "Test", "Test")
            song.store_data()

with tab2:
    st.header("record music")

    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        st.audio(wav_audio_data, format='audio/wav')
