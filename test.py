import openai
import os


def send_request():
    user_input = input("You: ").strip()
    if not user_input:
        print("Warning: Please enter a message.")
        return

    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            print("Error: OPENAI_API_KEY environment variable is not set.")
            return

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        output_text = response["choices"][0]["message"]["content"]
        print(f"GPT: {output_text}\n")
    except Exception as e:
        print(f"Error: An error occurred: {str(e)}")


if __name__ == "__main__":
    while True:
        send_request()
