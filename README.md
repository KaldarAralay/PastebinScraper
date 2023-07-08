# PastebinScraper

This is a Python application that uses a graphical user interface (GUI) to scrape and download posts ("pastes") from the Pastebin archive. It keeps track of downloaded pastes and ensures that no paste is downloaded more than once.

## Features

1. **GUI**: The application provides a graphical interface with buttons to start and stop the download process, as well as to open the folder where the pastes are stored.

2. **Real-time Status Updates**: The GUI includes a dialog box that provides real-time status updates on the downloading process, including the number of new pastes downloaded and when the next download cycle will occur.

3. **Periodic Download**: The application automatically downloads new pastes from the Pastebin archive every 3 minutes.

4. **Local Storage**: All downloaded pastes are stored locally in a directory named "pastes". Each paste is saved in a separate text file, and a separate file (`paste_info.txt`) is maintained with the metadata of each downloaded paste.

## Usage

To use this application, run the `Scraper.py` script. This will open the GUI. Click the "Run" button to start the download process and the "Stop" button to stop it. The "Open Folder" button can be used to open the output directory where the pastes are stored.

Please ensure that you have all the necessary Python dependencies installed (see `requirements.txt`).



![image](https://github.com/KaldarAralay/PastebinScraper/assets/3278231/6e66dd11-4d23-4ee3-9873-482a7f0f86f3)
