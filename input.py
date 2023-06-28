import customtkinter


def save_action():
    text=entry.get()
    print(text)


# Config
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
label=customtkinter.CTkLabel(master=frame,text="What have you been doing for the last 30 minutes?",font=("Roboto",18))
label.pack(pady=12,padx=10)
# Entry
entry = customtkinter.CTkEntry(master=frame,width=300)
entry.pack(pady=12, padx=10)

# Button
button=customtkinter.CTkButton(master=frame,text="Submit",hover=True,command=save_action)
button.pack(padx=10,pady=10)

root.mainloop()

