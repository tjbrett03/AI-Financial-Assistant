import openai
import os
import pandas as pd

def upload_file(file_path):
    """Uploads a file to OpenAI and returns the file ID."""
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            print("Error: OPENAI_API_KEY environment variable is not set.")
            return None

        with open(file_path, "rb") as file:
            response = openai.File.create(file=file, purpose="assistants")

        file_id = response["id"]
        print(f"File uploaded successfully. File ID: {file_id}")
        return file_id
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return None


def read_csv(file_path):
    """Reads a CSV file and returns its content as a string."""
    try:
        df = pd.read_csv(file_path)
        return df.to_string()
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return None


def send_request(file_content=None):
    user_input = input("You: ").strip()
    if not user_input:
        print("Warning: Please enter a message.")
        return

    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            print("Error: OPENAI_API_KEY environment variable is not set.")
            return

        messages = [{"role": "user", "content": user_input}]

        if file_content:
            messages.append({"role": "user", "content": f"Here is the CSV file content:\n{file_content}"})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        output_text = response["choices"][0]["message"]["content"]
        print(f"GPT: {output_text}\n")
    except Exception as e:
        print(f"Error: An error occurred: {str(e)}")


if __name__ == "__main__":
    file_content = None  # Store file content for chat inclusion

    while True:
        action = input("Type 'chat' to send a message or 'upload' to upload a CSV file: ").strip().lower()
        if action == "chat":
            send_request(file_content)
        elif action == "upload":
            file_path = input("Enter the CSV file path: ").strip()
            if os.path.exists(file_path):
                upload_file(file_path)
                file_content = read_csv(file_path)  # Read CSV for chat inclusion
            else:
                print("Error: File not found. Please enter a valid file path.")
