# Music Recognition Project

Softwaredesign Abschlussprojekt von Til Neubauer, Jens Nockenberg und Otto Sandrini (ottosandrini & RnTPVGas)

## Inhaltsverzeichnis

- [Überblick](#Überblick)
- [Features](#features)
- [Installation](#installation)
- [Verwendung](#usage)

## Überblick

In unserem Abschlussprojekt versuchten wir eine Shazam ähnliche streamlit Applikation zu bauen.  Die Applikation sollte in der Lage sein Teile von Songs mit Songs in einer Datenbank zu vergleichen und identifizieren. Die Datenbank wurde mit tinydb umgesetzt und für die Erkennung der Songs wurde die abracadabra library verwendet. Es können auch über das Mikrofon Tonstücke aufgenommen und verglichen werden. Hierfür wurde unten angeführte recording library verwendet.

abracadabra: https://github.com/notexactlyawe/abracadabra/
recording library: https://github.com/stefanrmmr/streamlit-audio-recorder

## Features

- **Upload Music**:
    Im ersten Tab kann man Lieder in die Datenbank hochladen.
- **Recognize Music**:
    Im recognize Tab kann man Teile von Liedern hochladen. Diese werden dann automatisch mit der Datenbank abgeglichen und ein Ergebnis wird angezeigt. Es werden außerdem Duckduckgo Suchergebnisse für den Titel des gefundenen Liedes angezigt.
- **Record Music**:
    Hier kann man mit dem Mikrofon Tonstücke aufnehmen und vergleichen lassen. Nach dem drücken des Stop-buttons beim aufnehmen ist Geduld gefragt.

## Installation

Zum Start das Github Repository clonen:

    git clone https://github.com/ottosandrini/Abschlussprojekt_swd.git

abracadabra benötigt zusätzlich noch Programme, die in einem Unix System ganz einfach mit folgendem Befehl installiert werden können:

    sudo apt-get install gcc portaudio19-dev python3-dev ffmpeg

Nun kann man ein Python virtual environment starten, wenn man möchte. Man muss nun nämlich mit:

    pip install -r requirements.txt

alle benötigten Python Module installieren.

Nun sollte man in der Lage sein mit folgendem Befehl die Applikation zu starten:

    streamlit run main.py

## Verwendung

Wurde die Applikation wie zuvor beschrieben gestartet, sollte sich auf dem bevorzugten Browser das Programm öffnen.

Dort sollten sich 3 Reiter befinden: **Upload Music**, **Recognize Music** und **Record Music**

**Verwendung von Upload Music:**

In diesem Reiter kann man Songs vom typ **mp3** und **wav** zu der Bibliothek hinzufügen. Mit dem Feld **Browse Files** öffnet sich der Datenexplorer des Geräts um den Song auszuwählen, oder man fügt ihn per Drag&Drop im vorgesehenen Feld hinzu.
Ist dies erfolgt, kann man den gewählten Song abspielen und mit dem Feld **upload Song** hochladen. Dieser Song wird dann in dem lokalen Ordner **uploaded_songs** abgelegt und zusätlich in Form von Hashes mit einer zugeteilten ID in der tinyDB Datenbank abgelegt. 

**Verwendung von Recognize Music:**

Die Vorgehensweise beim hochladen eines Songabschnittes, vereinfach genannt **Schnipsel**, ist die gleiche wie bei Upload Music.
Auch hier werden die hochgeladenen Schnipsel im lokalen Ordner **uploaded_schnipsel** abgelegt.
In diesem Fall wird auch der Schnipsel in Hashes umgewandelt, jedoch werden diese Hashes automatisch mit allen Hashes in der tinyDB Datenbank abgeglichen und **Matches** erfasst und gespeichert.
Nun werden für diese Matches die Abweichungen abgeglichen und der Beste Match, also der mit der geringsten Abweichung mit Titel in der Anwendung ausgegeben.
Befindet sich der gesuchte Song nicht in der Datenbank, wird dennoch der Song mit der höchsten Übereinstimmung ausgegeben.
Zusätzlich werden unter dem ermittelten Song per **Duckandgo** Links zu diesem Songtitel ausgegeben

**Verwendung von Record Music:**

In diesem Reiter können Songabschnitte über das im Gerät verbaute Mikrofon aufgenommen werden. Je nach Browser kann es sein, dass hier zuerst die Genehmigung zur Verwendung des Mikrofons erteilt werden muss. In diesem Fall muss der Aufnahmevorgang erneut gestartet werden.
Wird die Aufnahme beendet, dauert es eine kurze Zeit diesen Abschnitt zu verarbeiten und Zwischenzuspeichern, anschließend wird der Abschnitt genau wie bei dem Reiter recognize music mit der Datenbank abgeglichen und der Match ausgegeben. 





