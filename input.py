# Code for desktop input application, whose data is later used for the website
import customtkinter
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

DATE_FORMAT = "%H:%M"
load_dotenv()

def main():
    def get_start_end(time):
        end_hours, end_minutes = time.split(":")
        if end_minutes != "00" or end_minutes != "30":
            if 0 < int(end_minutes) < 30:
                end_minutes = "00"
            elif 30 < int(end_minutes) < 60:
                end_minutes = "30"
        end = f"{end_hours}:{end_minutes}"
        return (datetime.strptime(end, DATE_FORMAT) - timedelta(hours=0, minutes=30)).strftime(DATE_FORMAT), end

    def save_action():
        text = entry.get()
        current_time = datetime.now().strftime(DATE_FORMAT)
        start, end = get_start_end(current_time)

        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_DATABASE"),
            user=os.environ.get("DB_USERNAME"),
            password=os.environ.get("DB_PASSWORD"))

        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO ACTIVITY (TEXT,START_AT,END_AT,DAY_DATE) VALUES ('{text}','{start}','{end}',CURRENT_DATE)")
        conn.commit()

        # Close connection and the app window
        cur.close()
        conn.close()
        root.destroy()

    # App color
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    # Window
    root = customtkinter.CTk()
    root.title("Input")
    root.geometry("500x350")
    # Frame
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(padx=20, pady=20, fill="both", expand=True)
    # Main Label
    label = customtkinter.CTkLabel(master=frame, text="What have you been doing for the last 30 minutes?",
                                   font=("Roboto", 18))
    label.pack(pady=12, padx=10)
    # Entry
    entry = customtkinter.CTkEntry(master=frame, width=300)
    entry.pack(pady=12, padx=10)
    # Button
    button = customtkinter.CTkButton(master=frame, text="Submit", hover=True, command=save_action)
    button.pack(padx=10, pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()