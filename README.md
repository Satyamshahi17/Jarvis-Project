# Jarvis – Python Voice Assistant

## Description

**Jarvis** is an AI-powered voice assistant built in Python. It listens for a wake word ("Jarvis"), understands commands, speaks back in Hindi, and can open apps or websites, play songs, fetch news, or answer general questions using **Google Gemini (LLM)**.

This assistant demonstrates real-world integration of speech recognition, APIs, TTS (Text-to-Speech), and AI models.

---

## Features

-  Listens for the wake word: `"Jarvis"`
-  Opens websites and apps like Google, YouTube, Spotify
-  Plays music using a custom song dictionary
-  Fetches and speaks top 5 news headlines (via GNews API)
-  Handles general queries using **Google Gemini AI**
-  Speaks responses in **Hindi** using Google Text-to-Speech (gTTS)
-  Opens Spotify app from your desktop

---

## Requirements

Install the required Python libraries using pip:

```bash
pip install speechrecognition
pip install pyttsx3
pip install pygame
pip install gtts
pip install requests
pip install google-generativeai

