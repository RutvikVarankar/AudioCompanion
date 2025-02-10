import pyttsx3
import speedtest

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def intSpeed():
    try:
        speak("Calculating internet speed, sir")
        wifi = speedtest.Speedtest()
        wifi.get_best_server()
        download_speed = wifi.download() / 1_000_000  # Convert to Mbps
        upload_speed = wifi.upload() / 1_000_000  # Convert to Mbps
        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
        speak (f"Your download speed is {download_speed:.2f} Mbps")
        speak (f"Your upload speed is {upload_speed:.2f} Mbps")
    except speedtest.ConfigRetrievalError as e:
        print("Failed to retrieve configuration. Please check your network.")
    except Exception as e:
        print(f"An error occurred: {e}")