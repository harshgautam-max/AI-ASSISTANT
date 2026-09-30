# =================================================================
# Project Name: MY GIRL - AI Voice Assistant
# Creator: Harsh
# Description: Python based advanced AI assistant with Google Gemini
# =================================================================

from gtts import gTTS
import pygame
import os
import time
import speech_recognition as sr
import google.generativeai as genai
import pywhatkit      
import pyautogui      
import requests       

# --- 1. GEMINI AI SETUP (The Brain) ---
# GitHub par upload karte waqt yahan asli key NAHI dalni hai!
genai.configure(api_key="YOUR_API_KEY_HERE") 

system_instruction = """
Tumhara naam 'MY GIRL' hai. Tum ek bohot hi smart, caring aur friendly AI assistant ho.
Tumhe jisne banaya hai, unka naam Harsh hai. Tumhe Harsh se bohot respect aur ek achhe dost ki tarah baat karni hai.
Harsh ke har sawal ka jawab dena hai. Hamesha chote (1-2 lines) aur natural jawab dena.
Apne saare jawab hamesha pure Hindi script (देवनागरी) mein dena taaki voice engine easily bol sake.
"""

model = genai.GenerativeModel("gemini-3.5-flash", system_instruction=system_instruction)
chat_session = model.start_chat(history=[])

# --- 2. VOICE SETUP (The Mouth & Ears) ---
pygame.mixer.init()

def speak(text):
    print(f"\nMY GIRL: {text}")
    try:
        tts = gTTS(text=text, lang='hi', slow=False) 
        filename = "temp_voice.mp3"
        tts.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
        os.remove(filename)
    except Exception as e:
        print(f"Voice error: {e}")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening (Aaram se boliye, main sun rahi hoon...)..")
        r.adjust_for_ambient_noise(source, duration=1) 
        
        r.dynamic_energy_threshold = False 
        r.energy_threshold = 300 
        r.pause_threshold = 2.0 
        
        try:
            audio = r.listen(source, timeout=8) 
        except sr.WaitTimeoutError:
            return "none"

    try:
        print("Recognizing (Soch rahi hoon...)..")
        query = r.recognize_google(audio, language='hi-IN')
        print(f"Harsh ne kaha: {query}")
        return query.lower()
    except Exception:
        return "none"

# --- 3. MAIN LOOP (The Action Center) ---
if __name__ == "__main__":
    speak("Hello Harsh. Main online aa chuki hoon. Kahiye aaj hum kya karenge?")
    
    while True:
        query = take_command()
        
        if query == "none":
            continue
            
        # FEATURE 1: System Control
        if "volume badhao" in query or "aawaz badhao" in query:
            speak("Theek hai, aawaz badha rahi hoon.")
            pyautogui.press("volumeup", presses=10)
            
        elif "volume kam karo" in query or "aawaz kam karo" in query:
            speak("Aawaz kam kar di hai.")
            pyautogui.press("volumedown", presses=10)
            
        elif "mute" in query or "chup ho jao" in query:
            speak("System ko mute kar rahi hoon.")
            pyautogui.press("volumemute")

        # FEATURE 2: App Opening
        elif "notepad kholo" in query:
            speak("Notepad open kar rahi hoon.")
            os.system("notepad")
            
        elif "chrome kholo" in query or "browser kholo" in query:
            speak("Google Chrome khol rahi hoon.")
            os.system("start chrome") 

        # FEATURE 3: Web Automation (Music)
        elif "youtube par" in query and "chalao" in query:
            song = query.replace("youtube par", "").replace("chalao", "").strip()
            speak(f"Zaroor Harsh, aapke liye YouTube par {song} chala rahi hoon.")
            pywhatkit.playonyt(song) 

        # FEATURE 4: Live Data (Weather)
        elif "mausam" in query or "weather" in query:
            speak("Main internet se mausam ki jankari la rahi hoon...")
            try:
                res = requests.get("https://wttr.in/Delhi?format=%C+aur+tapman+%t+hai")
                speak(f"Harsh, abhi mausam {res.text}")
            except Exception as e:
                speak("Internet se mausam ki jankari nahi mil pa rahi hai.")

        # EXIT COMMAND
        elif "band ho jao" in query or "bye" in query or "so jao" in query:
            speak("Theek hai Harsh, main jaa rahi hoon. Apna khayal rakhna.")
            break
            
        # CONVERSATION WITH GEMINI
        else:
            try:
                response = chat_session.send_message(query)
                clean_text = response.text.replace("*", "") 
                speak(clean_text)
            except Exception as e:
                speak("Mera dimaag abhi connect nahi ho pa raha hai.")