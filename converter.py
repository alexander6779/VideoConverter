import yt_dlp
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import threading  # To run the download in a separate thread
import sys

# Counter for completed downloads
completed_downloads_count = 0

def get_image_path(file_name):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Temporary folder where PyInstaller extracts the files
    else:
        base_path = os.path.dirname(__file__)  # Folder where the script is located
    return os.path.join(base_path, file_name)

def read_urls(file):
    """Reads the file and returns URLs separated by ';'."""
    with open(file, 'r') as file_content:
        content = file_content.read()
    return [url.strip() for url in content.split(";") if url.strip()]

def download_video(url, options, progress_callback, total):
    """Downloads a video from the URL using the provided options."""
    update_message(1)
    with yt_dlp.YoutubeDL(options) as ydl:
        # Configure callback for progress
        ydl.params['progress_hooks'] = [progress_callback]
        ydl.download([url])
    global completed_downloads_count
    completed_downloads_count += 1
    if completed_downloads_count == total:
        update_message(2)  # Show completed message

def download_progress(d, bar):
    """Callback that is called during the download, updates the progress bar."""
    if d['status'] == 'downloading':
        progress = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)
        bar['value'] = progress * 100
        bar.update_idletasks()  # Update tkinter interface
        
def download_example_file():
    content = """https://www.youtube.com/watch?v=PnpEOtzb668;
    https://www.youtube.com/watch?v=LGRxyz2W2Og;
    https://www.youtube.com/watch?v=9YqecbxSr4A;
    https://www.youtube.com/watch?v=lPe09eE6Xio;
    https://www.youtube.com/watch?v=vJwKKKd2ZYE;
    https://www.youtube.com/watch?v=28hYUZMufDg;"""
    
    destination = filedialog.askdirectory(title="Select a folder to save the file")
    
    if destination:
        file_path = os.path.join(destination, "test.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder = filedialog.askdirectory(title="Select the download folder")
    return folder

def download():
    """Main function that handles reading and downloading the videos."""
    global completed_downloads_count
    completed_downloads_count = 0
    destination_folder = select_folder()
    
    if not destination_folder:
        print("No folder selected.")
        return
    file = input_file.get()
    urls = read_urls(file)  # Read all URLs from the file

    # Common configuration for all videos
    video_options = {
        'format': 'bestaudio/best',  # Download the best quality available
        'merge_output_format': 'mp4',  # Merge video and audio into MP4
        'outtmpl': f'{destination_folder}/%(title)s.%(ext)s',  # Save with the video title  
        'n_connections': 6,  # Download up to 6 videos at the same time
        'socket_timeout': 15,  # Reduced timeout to avoid delays
        'postprocessors': [],  # Avoid additional processing
        'no_post_overwrites': True,  # Disable existing file checks
        'concurrent_fragments': 3,  # Download fragments in parallel
        'ignoreerrors': True,  # Ignore download errors
    }
    
    completed_message.config(text="")
    progress_bar["val"] = 0
    
    update_message(0)
    # Start a thread for each video download
    for url in urls:
        download_thread = threading.Thread(target=download_video, args=(url, video_options, lambda d: download_progress(d, progress_bar), len(urls)))
        download_thread.start()

def select_file():
    file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    input_file.delete(0, tk.END)  # Clear the text field
    input_file.insert(0, file)  # Insert the selected file path

def update_message(state):
    if state == 0:
        completed_message.config(text="Starting the download.")
    elif state == 1:
        completed_message.config(text="Download in progress.")
    else:
        completed_message.config(text="Download complete! Check the selected download folder.")

# Create the main window
window = tk.Tk()
window.title("MP4 Converter")  # Window title
window.geometry("400x350")  # Window size
window.resizable(False, False)  # Disable resizing

# Load the icon in .png or .gif format
icon = tk.PhotoImage(file=get_image_path('mp4.png'))  # Or use .gif

# Set the window icon
window.tk.call('wm', 'iconphoto', window._w, icon)

# Center the window on the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 900
window_height = 650
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Create and pack the title (centered)
title = tk.Label(window, text="Video to MP4 Audio Converter", font=("Arial", 16))
title.pack(pady=10)

# Create and pack the introductory text
intro_text = tk.Label(window, text="""Instructions: 
                       
1. Select a file with YouTube URLs separated by ;.
2. Press "Select" to load the file.
3. Press "Download", choose a folder, and the download will start.
4. Once done, check the folder. If any file is missing, try another URL.""", font=("Arial", 11))
intro_text.pack(pady=15)

# Create and pack the button to select a test file
test_file_button = tk.Button(window, text="Download Example File", command=download_example_file)
test_file_button.pack(pady=10)  # Place the button next to the input

# Create a Frame for the input and the button
frame = tk.Frame(window)
frame.pack(pady=15)

# Create and pack the input field for the file
input_file = tk.Entry(frame, width=40)
input_file.pack(side="right", padx=5)  # Place the input to the left with margin

# Create and pack the button to select a file
select_button = tk.Button(frame, text="Select File", command=select_file)
select_button.pack(side="left", padx=5)  # Place the button next to the input

# Create and pack the progress bar
progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Create and pack the download button
download_button = tk.Button(window, text="Download", command=download)
download_button.pack(pady=10)

# Create and pack the completed message
completed_message = tk.Label(window, text="", font=("Arial", 12), fg="green")
completed_message.pack(pady=10)

# Function to stop the download if the window is closed
def on_close():
    print("The window has been closed. Stopping the process.")
    window.quit()

# Configure the close window event
window.protocol("WM_DELETE_WINDOW", on_close)

# Start the Tkinter main loop
window.mainloop()