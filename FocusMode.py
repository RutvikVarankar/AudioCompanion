import time
import datetime
import ctypes, sys
import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",150)

# Function to speak out the input text
def speak(text):
    engine.say(text)
    engine.runAndWait()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def enable_focus_mode():
    if is_admin():
        current_time = datetime.datetime.now().strftime("%H:%M")
        Stop_time = input("Enter time example:- [10:10]:- ")
        a = current_time.replace(":",".")
        a = float(a)
        b = Stop_time.replace(":",".")
        b = float(b)
        Focus_Time = b-a
        Focus_Time = round(Focus_Time,3)
        host_path ="C:\Windows\System32\drivers\etc\hosts"
        redirect = "127.0.0.1"
        
        print(current_time)
        time.sleep(2)

        # Prompt user for websites to block
        website_list = []
        print("Enter the websites you want to block (type 'done' when finished):")
        speak("Enter the websites you want to block  (type 'done' when finished):")
        while True:
            website = input("Website: ")
            if website.lower() == 'done':
                break
            if website not in website_list:
                website_list.append(f"www.{website}.com")
                website_list.append(f"{website}.com")

        if (current_time < Stop_time):
            with open(host_path,"r+") as file: #r+ is writing+ reading
                content = file.read()
                time.sleep(2)
                for website in website_list:    
                    if website in content:
                        pass
                    else:
                        file.write(f"{redirect} {website}\n")
                        print("DONE")
                        time.sleep(1)
                print("FOCUS MODE TURNED ON !!!!")

        while True:     
            current_time = datetime.datetime.now().strftime("%H:%M")
            if (current_time >= Stop_time):
                with open(host_path,"r+") as file:
                    content = file.readlines()
                    file.seek(0)
                    for line in content:
                        if not any(website in line for website in website_list):
                            file.write(line)
                    file.truncate()
                    print("Websites are unblocked !!")
                    file = open("focus.txt","a")
                    file.write(f",{Focus_Time}")        #Write a 0 in focus.txt before starting
                    file.close()
                    break 

    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
