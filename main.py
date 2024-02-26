import streamlit as st
import os 
from logik import songclass
from st_audiorec import st_audiorec
from logik import schnipselclass
from logik import vorschlaege 

st.write("abracadabra")
         
tab1, tab2, tab3 = st.tabs(["upload music","recognize music", "record music"])

with tab1: # --- UPLOAD TAB ---
    st.header("upload music")

    uploaded_song = st.file_uploader("Choose a file", type=['mp3'])
        
    if uploaded_song is not None:
        # Den Dateinamen extrahieren
        filename = uploaded_song.name

        # Die Audiodaten aus der hochgeladenen Datei lesen
        audio_data = uploaded_song.read()

        # Die lokal gespeicherte Audiodatei wiedergeben
        st.audio(audio_data)

        if st.button("upload Song", key="upload_Song"):
            # Den Dateipfad für die lokale Speicherung erstellen
            file_path = os.path.join("uploaded_songs", filename)
            # Song Datei speichern in file_path
            if os.path.exists(file_path):
                st.error(f"Die Datei {filename} existiert bereits. Bitte ändern Sie den Dateinamen und laden Sie die Datei erneut.")
            else:
                # Die Audiodaten in die lokale Datei schreiben
                with open(file_path, "wb") as f:
                    f.write(audio_data)
                # Bestätigung anzeigen
                st.success(f"Die Datei wurde erfolgreich gespeichert: {file_path}")
            
            # check number of files and generate a unique song ID
            uploaded_songs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploaded_songs")
            songid = len([name for name in os.listdir(uploaded_songs_path) if os.path.isfile(os.path.join(uploaded_songs_path, name))])
            songid = songid + 1
            print(songid)
            
            # Initialize a Song Object with data from Uploaded Song
            song = songclass.Song( filename, file_path, "Test", "Test", "Test", songid)
            song.store_data()


    if st.button("clear database", key="clear database"):
        # This button clears the tinyDB database & deletes all files in /uploaded_songs
        uploaded_songs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploaded_songs")
        songclass.Song.cleardb()
        for filename in os.listdir(uploaded_songs_path):
            if os.path.isfile(os.path.join(uploaded_songs_path, filename)):
                os.remove(os.path.join(uploaded_songs_path, filename))
        st.warning("Database cleared!")
        print("Deleted all songs in /uploaded_songs")

with tab2: # --- RECOGNIZE TAB ---
    st.header("recognize music")
    uploaded_schnipsel = st.file_uploader("Choose a Schnipsel", type=['mp3'])

    if uploaded_schnipsel is not None:
        filename = uploaded_schnipsel.name
        audio_data = uploaded_schnipsel.read()
        st.audio(audio_data)
        file_path = os.path.join("uploaded_schnipsel", filename)

        if st.button("upload Schnipsel", key="upload_schnipsel"):
            with open(file_path, "wb") as f:
                f.write(audio_data)
            st.success(f"Die Datei wurde erfolgreich gespeichert: {file_path}")
            # Initialize schnipsel Object
            schnipsel = schnipselclass.Schnipsel(file_path)
            # attempt to recognize a song
            recognised_song = schnipsel.recognise_song()
            if recognised_song is not None:
                st.success("SUCCESS! Found a matching song")

    Search_keyword = 'Nothing else matters'
    st.write(f"Here you can find something about {Search_keyword}: ")
    st.write(vorschlaege.duckduckgo_search(Search_keyword))
   



with tab3: # --- RECORD TAB ---
    st.header("record music")

    wav_audio_data = st_audiorec()
    if wav_audio_data is not None:
        st.audio(wav_audio_data, format='audio/wav')
