import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyttsx3
import json
from vosk import Model, KaldiRecognizer
import pyaudio
import webbrowser

model = Model("vosk-model-en-in-0.5")  # Replace with the path to your Vosk model directory

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate",150)

# Function to speak out the input text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's voice and convert it to text
def takeCommand():

    recognizer = KaldiRecognizer(model, 16000)

    # Setting up audio input
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening...")
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            query = result_dict.get("text", "")
            if query:
                print(f"You said: {query}")
                break

    # Cleaning up resources
    stream.stop_stream()
    stream.close()
    p.terminate()
    return query

# Dictionary of names and their corresponding email addresses
contacts = {
    "myself": "rutvik6404@gmail.com",
    "mom": "varankarshwetali17@gmail.com",
    "dad": "suryakantvarankar08@gmail.com",
    "shubham": "shubhamvarankar05@gmail.com",
    "swayam": "swayamwagre2@gmail.com",
    "sushant": "sushantbwagh2004@gmail.com",
    "rishikesh": "rajmanerishikesh@gmail.com",
    "harshal": "thakurharshal225@gmail.com",
    "vibha": "vibha.watkar@gmail.com",
    "saniya": "sandamsaniya@gmail.com"
}

# Function to send email
def sendEmail():
    print("Please tell me the name of the person you want to email.")
    speak("Please tell me the name of the person you want to email.")
    recipient_name = takeCommand()  # Get recipient name through voice

    # Retrieve the email address from the dictionary
    recipient_email = contacts.get(recipient_name, None)
    if not recipient_email:
        speak("Contact not found.")
        return

    print("What is the subject of the email?")
    speak("What is the subject of the email?")
    subject = takeCommand()  # Get email subject through voice

    print("What is the message?")
    speak("What is the message?")
    body = takeCommand()  # Get email body through voice

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = "rutvik6404@gmail.com"  # Replace with your email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Use your email provider's SMTP server
            server.starttls()
            server.login('rutvik6404@gmail.com', 'zozb gtsp qian ycly')  # Replace with your email and password
            server.send_message(msg)
            print("Email sent successfully.")
            speak("Email sent successfully.")
            webbrowser.open("https://mail.google.com/mail/u/0/?tab=rm&ogbl#sent")
    except Exception as e:
        print(f"Failed to send email: {e}")
        speak("Failed to send email.")

if __name__ == "__main__":
    sendEmail()
