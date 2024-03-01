import streamlit as st
import os 
from logik import songclass
from st_audiorec import st_audiorec
from logik import schnipselclass
from logik import vorschlaege 
from serpapi import GoogleSearch
import tempfile

st.write("Shazam auf Wish bestellt")
apikey = "2225a3954c27976ceae691cb28764bf93adcbdc7adf86d4cdda2eb6f0c0c6b67"         
tab1, tab2, tab3 = st.tabs(["Upload Music","Recognize Music", "Record Music"])

with tab1: # --- UPLOAD TAB ---
    st.header("Upload Music")

    if st.button("clear database", key="clear_database"):
        # This button clears the tinyDB database & deletes all files in /uploaded_songs
        uploaded_songs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploaded_songs")
        songclass.Song.cleardb()
        for filename in os.listdir(uploaded_songs_path):
            if os.path.isfile(os.path.join(uploaded_songs_path, filename)):
                os.remove(os.path.join(uploaded_songs_path, filename))
        st.warning("Database cleared!")
        print("Deleted all songs in /uploaded_songs")

    uploaded_song = st.file_uploader("Choose a file", type=['mp3', 'wav'])
        
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



with tab2: # --- RECOGNIZE TAB ---
    st.header("Recognize Music")
    uploaded_schnipsel = st.file_uploader("Choose a Schnipsel", type=['mp3', 'wav'])
    name = ""
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
            #schnipsel.print_hash()
            # attempt to recognize a song
            recognised_song = schnipsel.recognise_song()
            if recognised_song is not None:
                st.success("SUCCESS! Found a matching song")
                recognised_song = int(recognised_song)
                name = songclass.Song.get_song_name_by_id(recognised_song)
                name = name.split(".")[0]
                nmstr = "This song matches the Schnipsel closely: \n" + name
                st.write(nmstr)

            Search_keyword = name
            print(Search_keyword + "   --- SEARCH KEYWORD ---")
            st.write(f"Find out more about {Search_keyword}: ")
            params = {
              "engine": "duckduckgo",
              "q": Search_keyword,
              "kl": "us-en",
              "api_key": apikey
            }

            search = GoogleSearch(params)
            results = search.get_dict()
            if results:
                for i, result in enumerate(results['organic_results'][:5], start=1):
                    st.write(f"{i}. [{result['title']}]({result['link']})")


with tab3: # --- RECORD TAB ---
    st.header("Record Music")
    name = ""
    # Aufnahme des Musikabschnitts
    recording_choice = st.radio("Choose Recording Type:", ("Record Music Section", "Record Entire Song"))

    if recording_choice == "Record Music Section":
        st.subheader("Record Music Section")
        # Aufnahme des Musikabschnitts
        wav_audio_data = st_audiorec()

        if wav_audio_data is not None:
            st.audio(wav_audio_data, format='audio/wav')

            # Temporäre Datei erstellen, um den aufgenommenen Abschnitt zu speichern
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(wav_audio_data)
                temp_file_path = temp_file.name

            # Initialize Schnipsel Object
            schnipsel = schnipselclass.Schnipsel(temp_file_path)

            # Attempt to recognize a song
            recognised_song = schnipsel.recognise_song()

            # Löschen der temporären Datei
            os.unlink(temp_file_path)

            if recognised_song is not None:
                st.success("SUCCESS! Found a matching song")
                recognised_song = int(recognised_song)
                name = songclass.Song.get_song_name_by_id(recognised_song)
                name = name.split(".")[0]
                nmstr = "This song matches the Schnipsel closely: \n" + name
                st.write(nmstr)
                
            Search_keyword = name
            params = {
            "engine": "duckduckgo",
            "q": Search_keyword,
            "kl": "us-en",
            "api_key": apikey
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            st.write("Here is some more Information about your song: \n")
            if results is not None:
                for i, result in enumerate(results['organic_results'][:5], start=1):
                    st.write(f"{i}. [{result['title']}]({result['link']})")

                #code here
    else:
        st.subheader("Record Entire Song")
        # Audiodaten aufnehmen
        wav_song_data = st_audiorec()

        if wav_song_data is not None:
            # Audio wiedergeben
            st.audio(wav_song_data, format='audio/wav')

            # Eingabefeld für den Dateinamen
            record_filename = st.text_input("Enter Filename:", "recorded_song.wav")

            if st.button("Save Recorded Song", key="save_recorded_song"):
                # Den Dateipfad für die lokale Speicherung erstellen
                file_path = os.path.join("uploaded_songs", record_filename)
                # Songdatei speichern in file_path
                if os.path.exists(file_path):
                    st.error(f"Die Datei {record_filename} existiert bereits. Bitte ändern Sie den Dateinamen und speichern Sie die Datei erneut.")
                else:
                    # Die Audiodaten in die lokale Datei schreiben
                    with open(file_path, "wb") as f:
                        f.write(wav_song_data)
                    # Bestätigung anzeigen
                    st.success(f"Die Datei wurde erfolgreich gespeichert: {file_path}")

                # Überprüfen, wie viele Dateien vorhanden sind und eine eindeutige Song-ID generieren
                uploaded_songs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploaded_songs")
                songid = len([name for name in os.listdir(uploaded_songs_path) if os.path.isfile(os.path.join(uploaded_songs_path, name))])
                songid = songid + 1
                print(songid)
                
                # Initialisieren eines Song-Objekts mit den Daten des aufgenommenen Songs
                song = songclass.Song(record_filename, file_path, "Test", "Test", "Test", songid)
                song.store_data()
