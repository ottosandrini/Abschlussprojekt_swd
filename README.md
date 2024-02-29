# Music Recognition Project

Softwaredesign Abschlussprojekt von Til Neubauer, Jens Nockenberg und Otto Sandrini (ottosandrini & RnTPVGas)

## Inhaltsverzeichnis

- [Überblick](#Überblick)
- [Features](#features)
- [Installation](#installation)
- [Verwendung](#usage)

## Überblick

In unserem Abschlussprojekt versuchten wir eine Shazam ähnliche streamlit Applikation zu bauen.  Die Applikation sollte in der Lage sein Teile von Songs mit Songs in einer Datenbank zu vergleichen und identifizieren. Die Datenbank wurde mit tinydb umgesetzt und für die erkennung der Songs wurde die abracadabra library verwendet. Es können auch über das Mikrofon Tonstücke aufgenommen und verglichen werden. Hierfür wurde unten angeführte recording library verwendet.

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

abracadabra benötigt zusätzlich noch programme, die in einem Unix System ganz einfach mit folgendem Befehl installiert werden können:

  sudo apt-get install gcc portaudio19-dev python3-dev ffmpeg

Nun kann man ein Python virtual environment starten, wenn man möchte. Man muss nun nämlich mit:

  pip install -r requirements.txt

alle benötigten Python Module installieren.

Nun sollte man in der Lage sein mit folgendem Befehl die Applikation zu starten:

  streamlit run main.py

## Verwendung




