import os
from langchain_groq import ChatGroq
import re
import io
import contextlib

llm = ChatGroq(
    api_key="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",
    model="mixtral-8x7b-32768",
)

def extract_code(input_str):
    pattern = r"```python\s*(.*?)\s*```"
    matches = re.findall(pattern, input_str, re.DOTALL)
    if matches:
        return str(matches[0].strip())
    else:
        return ""
    
def execute_code(extracted_code):
    output_stream = io.StringIO()
    error = None
    file_path = None

    with contextlib.redirect_stdout(output_stream):
        try:
            namespace = {}
            exec(extracted_code, namespace)
            file_path = namespace.get('file_path')
        except Exception as e:
            error = str(e)
            print("Execution Error:", error)
            
    output = output_stream.getvalue()

    if file_path and os.path.exists(file_path):
        with open(file_path, 'r') as f:
            file_content = f.read()
    else:
        file_content = ""

    return {
        "output": output,
        "error": error,
        "file_content": file_content
    }

def generate_code_output(prompt):
    result = llm.invoke(prompt)
    return extract_code(result.content)

userPrompt = input("Enter your prompt : ")

prompt = """
    You have to generate python code based on the given user prompt.
    Generate error free clean code and always add debug statements for future referrences.
    If you are ever asked to generate code that involves creation of files, always make sure to add
    the file path as file_path = "any_file_path.txt". This was just an exammple you can vary the file name
    but dont add things like /path/to in the file_path variable
    Here is the user prompt
    {user_prompt}
"""

while True:

    prompt = prompt.format(user_prompt = userPrompt)
    code = generate_code_output(prompt)
    print("Extracted Code:", code)

    exe = execute_code(code)
    print("Execution Result:", exe)

    if exe['error']:
        prompt = f"This is the code that you had generated {code} and it has the following error : {exe['error']}, Generate me python code to handle the error"
    else:
        break

final_code = generate_code_output(prompt)
final_exe = execute_code(final_code)
print("Final Execution Result:", final_exe)