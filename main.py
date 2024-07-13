import os
from interpreter import KpopInterpreter


def run_kpop_code(code):
    interpreter = KpopInterpreter()
    interpreter.interpret(code)


def load_example(filename):
    with open(filename, 'r') as file:
        return file.read()


print("Welcome to the K-pop Programming Language Interpreter!")
print("Choose an option:")
print("1. Run an example")
print("2. Write your own code")

choice = input("Enter your choice (1 or 2): ")

if choice == '1':
    examples = [f for f in os.listdir() if f.endswith('.kpop')]
    print("\nAvailable examples:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    example_choice = int(input("Choose an example to run: ")) - 1
    code = load_example(examples[example_choice])
else:
    print(
        "\nEnter your code below. Type 'EXIT' on a new line to run the code.")
    code_lines = []
    while True:
        line = input()
        if line.strip().upper() == "EXIT":
            break
        code_lines.append(line)
    code = "\n".join(code_lines)

print("\nRunning K-pop code:\n")
run_kpop_code(code)
