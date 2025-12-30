from v3 import main

def read_questions_from_file(file_path):
    questions = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('Q:'):
                question = line[3:].strip().lower()  # Convert question to lowercase
                questions.append(question)
    return questions

def prompt_user(question, answer):
    # Implement your logic to process the answer
    print(question)
    # You can perform any necessary processing or validation on the answer here
    return answer

def main_script():
    file_path = "Brain\\question.txt"
    questions = read_questions_from_file(file_path)
    for question in questions:
        prompt = "Please provide accurate and concise information about the topic in 30 words:"  # Replace with your desired prompt
        print(question)# Pass an empty answer initially
        response = main(question, prompt,word_limit=30)
        print("Response:", response)
        print("-----------------")

if __name__ == "__main__":
    main_script()
