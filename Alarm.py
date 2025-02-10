import os 

def alarm(alarm_time):

    alarm_time = alarm_time + ":00"

    task_name = "PythonAlarm"
    sound_file = r"C:/Users/Rutvik/OneDrive/Documents/Project/music.mp3"  # Change this to any sound file path

    schedule_command = f'schtasks /create /tn "{task_name}" /tr "cmd.exe /c start {sound_file}" /sc once /st {alarm_time} /f'
    os.system(schedule_command)

    print(f"Alarm set for {alarm_time}!")

if __name__ == "__main__":
    alarm("08:33")  # Set alarm for 8:00 AM