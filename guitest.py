import os
import openai
import tkinter as tk
from tkinter import filedialog
import pandas as pd

# Global variable to store CSV content
file_content = None


def upload_file(file_path):
    """Uploads a file to OpenAI and returns the file ID."""
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            update_status("Error: OPENAI_API_KEY environment variable is not set.")
            return None

        with open(file_path, "rb") as file:
            response = openai.File.create(file=file, purpose="assistants")

        file_id = response["id"]
        update_status(f"File uploaded successfully. File ID: {file_id}")
        return file_id
    except Exception as e:
        update_status(f"Error uploading file: {str(e)}")
        return None

def read_csv(file_path):
    """Reads a CSV file and returns its content as a string."""
    try:
        df = pd.read_csv(file_path)
        return df.to_string()
    except Exception as e:
        update_status(f"Error reading CSV file: {str(e)}")
        return None

def send_request_ui(message, file_content=None):
    """
    Sends the provided message (with optional CSV file content) to OpenAI
    and returns the generated response.
    """
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            return "Error: OPENAI_API_KEY environment variable is not set."
        messages = [{"role": "user", "content": message}]
        messages.insert(0, {"role": "system",
                            "content": "You are my financial assistant. When a CSV file is provided, please summarize my finances. Tell me what categories I spent the most on, give me the monetary value and a percentage of total spending. also tell me what days i spent the most money on, what weeks i spent the most money on, and my total spending for each month. when listing remember to sort by highest spending first"})

        if file_content:
            messages.append({"role": "user", "content": f"Here is the CSV file content:\n{file_content}"})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        output_text = response["choices"][0]["message"]["content"]
        return output_text
    except Exception as e:
        return f"Error: {str(e)}"


def update_status(text):
    """Update the status label with the provided text."""
    status_label.config(text=text)


def choose_file():
    """Opens a file dialog to select a CSV, uploads it, and reads its content."""
    global file_content
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select a .CSV file",
        filetypes=[("CSV Files", "*.csv")]
    )
    if file_path and os.path.exists(file_path):
        upload_file(file_path)
        file_content = read_csv(file_path)
        update_status("CSV file processed successfully.")
    else:
        update_status("Error: File not found.")

def send_chat():
    """Retrieves the chat message, sends it to OpenAI, and displays the conversation."""
    user_message = chat_entry.get().strip()
    if not user_message:
        chat_display.insert(tk.END, "Please enter a message.\n")
        return
    # Display the user's message
    chat_display.insert(tk.END, "You: " + user_message + "\n")
    # Send the message (and CSV content if available) to OpenAI
    response = send_request_ui(user_message, file_content)
    chat_display.insert(tk.END, "GPT: " + response + "\n")
    chat_entry.delete(0, tk.END)

root = tk.Tk()
root.title("AI Enhanced Finance Tracking Application")

# file upload
file_frame = tk.Frame(root)
file_frame.pack(fill=tk.X, padx=10, pady=5)

upload_button = tk.Button(file_frame, text="Upload CSV", command=choose_file)
upload_button.pack(side=tk.LEFT, padx=5)

status_label = tk.Label(file_frame, text="No file uploaded yet.")
status_label.pack(side=tk.LEFT, padx=5)


chat_frame = tk.Frame(root)
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

chat_display = tk.Text(chat_frame, height=15)
chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

chat_entry = tk.Entry(chat_frame)
chat_entry.pack(fill=tk.X, padx=5, pady=5)

send_button = tk.Button(chat_frame, text="Send", command=send_chat)
send_button.pack(pady=5)

root.mainloop()
