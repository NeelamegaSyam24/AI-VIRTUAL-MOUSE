import tkinter as tk

def show_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)

    width = 400
    height = 200

    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    splash.geometry(f"{width}x{height}+{x}+{y}")
    splash.configure(bg="#111111")

    label_title = tk.Label(
        splash,
        text="AI Gesture OS",
        font=("Arial", 20, "bold"),
        fg="white",
        bg="#111111"
    )
    label_title.pack(pady=40)

    label_sub = tk.Label(
        splash,
        text="Initializing AI Engine...",
        font=("Arial", 12),
        fg="gray",
        bg="#111111"
    )
    label_sub.pack()

    splash.after(2500, splash.destroy)
    splash.mainloop()