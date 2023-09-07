from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import openai


messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant specialized in providing information about BellaVista Italian Restaurant.",
    },
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "stop":
        break

    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    assistant_message = response["choices"][0]["message"]["content"]
    print(f"Assistant: {assistant_message}")

    messages.append({"role": "assistant", "content": assistant_message})
