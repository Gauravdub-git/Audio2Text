import customtkinter as ctk
import speech_recognition as sr
import threading
from tkinter import ttk

def live_audio_to_text(output_file):
    """
    Function to capture live audio input and transcribe it to text.
    Saves the transcription to the specified output file.
    """
    global running
    try:
        recognizer = sr.Recognizer()  # Initialize recognizer

        # Use the microphone as the audio source
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Ready! Start speaking.")

            while running:
                print("Listening...")
                try:
                    audio_data = recognizer.listen(source, timeout=1, phrase_time_limit=10)  # Increased phrase time limit to 10 seconds
                    print("Transcribing...")
                    text = recognizer.recognize_google(audio_data)  # Transcribe audio
                    print(f"You said: {text}")

                    with open(output_file, "a") as f:  # Append transcription to file
                        f.write(f"{text}\n")

                except sr.WaitTimeoutError:
                    # Skip if no speech detected within timeout
                    if not running:
                        break
                except sr.UnknownValueError:
                    print("Could not understand audio. Please try again.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")

    except KeyboardInterrupt:
        print("Exiting live transcription...")

def start_transcription():
    """Start live audio transcription in a separate thread."""
    global running, output_file, transcription_thread
    running = True

    if file_option.get() == "new":
        output_file = "new_transcription.txt"  # Use a new file
    else:
        output_file = "live_transcription.txt"  # Continue with the same file

    print(f"Transcribing to: {output_file}")

    # Run transcription in a separate thread
    transcription_thread = threading.Thread(target=live_audio_to_text, args=(output_file,))
    transcription_thread.start()

def stop_transcription():
    """Stop live audio transcription."""
    global running
    running = False
    print("Transcription paused.")

def create_gui():
    """Create a modern GUI for the transcription app."""
    ctk.set_appearance_mode("dark")  # Set dark mode
    ctk.set_default_color_theme("blue")  # Set theme

    root = ctk.CTk()
    root.title("Live Audio to Text Converter")
    root.geometry("500x400")

    global file_option
    file_option = ctk.StringVar(value="same")  # Default to continue with the same file

    ctk.CTkLabel(root, text="Live Audio to Text Converter", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

    ctk.CTkButton(root, text="Start Transcription", command=start_transcription, width=200).pack(pady=10)
    ctk.CTkButton(root, text="Stop Transcription", command=stop_transcription, width=200).pack(pady=10)

    ctk.CTkRadioButton(root, text="Continue in Same File", variable=file_option, value="same").pack(anchor="w", padx=50)
    ctk.CTkRadioButton(root, text="Create New File", variable=file_option, value="new").pack(anchor="w", padx=50)

    # Add an animation placeholder (e.g., a spinning progress bar)
    progress = ttk.Progressbar(root, mode="indeterminate")
    progress.pack(pady=20)

    def animate():
        """Start and stop progress bar animation based on running state."""
        if running:
            progress.start()
        else:
            progress.stop()
        root.after(100, animate)

    animate()

    ctk.CTkButton(root, text="Exit", command=root.quit, width=200).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    running = False  # Flag to control transcription state
    transcription_thread = None  # Thread for running transcription
    output_file = "live_transcription.txt"  # Default output file
    create_gui()
