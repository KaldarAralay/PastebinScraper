import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import time
import os
import re
import threading
import subprocess


class PasteDownloaderGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Paste Downloader")
        
        self.run_button = tk.Button(self.window, text="Run", command=self.start_download)
        self.run_button.pack(pady=10)
        
        self.stop_button = tk.Button(self.window, text="Stop", command=self.stop_download)
        self.stop_button.pack(pady=10)
        
        self.open_folder_button = tk.Button(self.window, text="Open Folder", command=self.open_output_folder)
        self.open_folder_button.pack(pady=10)
        
        self.dialog_box = tk.Text(self.window, width=60, height=10)
        self.dialog_box.pack(padx=10, pady=10)
        
        self.download_thread = None
        self.stop_event = threading.Event()
    
    def start_download(self):
        self.dialog_box.delete("1.0", tk.END)
        self.append_text("Download started.")
        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.stop_event.clear()  # Clear the stop event flag
        
        if self.download_thread is None or not self.download_thread.is_alive():
            self.download_thread = threading.Thread(target=self.download_pastes)
            self.download_thread.start()
    
    def stop_download(self):
        self.stop_event.set()
        self.run_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.append_text("Download stopped.")
    
    def open_output_folder(self):
        folder_path = os.path.abspath("pastes")
        if os.path.exists(folder_path):
            subprocess.Popen(f'explorer "{folder_path}"')
        else:
            messagebox.showerror("Folder Not Found", "The output folder does not exist.")
    
    def download_pastes(self):
        # URL of the pastebin.com archive
        url = 'https://pastebin.com/archive'

        # Directory to store the downloaded pastes
        output_directory = 'pastes'

        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Set the delay in seconds before each run
        delay_seconds = 180  # 3 minutes

        # Keep track of already downloaded paste IDs
        downloaded_pastes = set()

        while not self.stop_event.is_set():
            # Send a GET request to the archive page
            response = requests.get(url)
            self.append_text('Fetched archive page.')

            # Create a BeautifulSoup object to parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all the paste links in the archive
            paste_links = soup.select('.maintable tbody tr a')

            # Counter for new pastes downloaded
            new_pastes_downloaded = 0

            # Iterate over the paste links
            for link in paste_links:
                if self.stop_event.is_set():
                    break

                # Extract the paste ID from the link
                paste_id = link['href'].split('/')[-1]

                # Check if the paste has already been downloaded
                if paste_id in downloaded_pastes:
                    continue

                # Extract the paste name from the link text
                paste_name = link.text.strip()

                # Remove any invalid characters from the paste name
                paste_name = re.sub(r'[^\w\-_. ]', '_', paste_name)

                # Construct the raw paste URL
                raw_url = f'https://pastebin.com/raw/{paste_id}'
                self.append_text(f'Downloading paste: {paste_name}')

                # Send a GET request to the raw paste URL
                paste_response = requests.get(raw_url)

                # Generate the new file name with the original document title and paste ID
                new_file_name = f'{paste_name}-{paste_id}.txt'

                # Save the raw paste content to a file using UTF-8 encoding
                file_path = os.path.join(output_directory, new_file_name)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(paste_response.text)

                # Add the paste ID to the downloaded set
                downloaded_pastes.add(paste_id)

                # Save paste information to a separate file
                info_file_path = os.path.join(output_directory, 'paste_info.txt')
                with open(info_file_path, 'a', encoding='utf-8') as info_file:
                    paste_info = f'{paste_name} | {paste_id} | {time.ctime()} | {time.strftime("%Y-%m-%d %H:%M:%S")}\n'
                    info_file.write(paste_info)

                self.append_text(f'Saved paste: {new_file_name}')
                new_pastes_downloaded += 1

            if new_pastes_downloaded == 0:
                self.append_text('No new pastes downloaded.')

            if not self.stop_event.is_set():
                self.append_text(f'Waiting for {delay_seconds} seconds...')
                time.sleep(delay_seconds)
    
    def append_text(self, text):
        self.dialog_box.insert(tk.END, text + "\n")
        self.dialog_box.see(tk.END)
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = PasteDownloaderGUI()
    app.run()