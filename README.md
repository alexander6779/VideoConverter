# MP4 Converter - YouTube Video Downloader

This is a simple Python application that allows you to download YouTube videos as MP4 files using `yt-dlp`. The application provides a graphical user interface (GUI) using `Tkinter` to manage downloads easily.

## Features

- Download videos from YouTube by pasting URLs in a text file.
- Choose the folder where you want to save the downloaded files.
- Displays a progress bar showing download status.
- Handles multiple downloads concurrently for faster processing.
- Provides a button to download an example file with pre-configured URLs.

## Requirements

To run the project, you need the following dependencies installed:

- Python 3.x
- `yt-dlp` - A command-line program to download videos from YouTube and other sites.
- `Tkinter` - A standard GUI library for Python.

### Install dependencies

You can install the necessary Python packages using `pip`:

```bash
pip install yt-dlp
```

Tkinter is included by default with Python, so you shouldn't need to install it separately.

## Usage

### Download Example File:

Click the "Download Example File" button to download a sample file containing YouTube URLs separated by semicolons (`;`).

### Load Your URLs:

You can also create your own text file with YouTube video URLs separated by `;` and load it by clicking the "Select File" button.

### Select Download Folder:

Click the "Download" button and choose the folder where you want to save the downloaded videos.

### Monitor Progress:

The app will show the progress of the downloads in the progress bar.

### Completion:

Once the downloads are complete, a message will appear confirming that the downloads are finished.

## Instructions

- Select a file containing YouTube URLs separated by `;`.
- Press "Select" to load the file.
- Press "Download", choose a folder, and the download will start.
- When done, check the folder for the downloaded files. If any file is missing, try another URL.
