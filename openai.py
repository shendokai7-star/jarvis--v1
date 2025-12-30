import openai

# Initialize OpenAI GPT-4
openai.api_key = ''

def get_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    print("Hello! I am your AI assistant. How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        response = get_response(user_input)
        print("AI Assistant:", response)

if __name__ == "__main__":
    main()
