from google import genai
from dotenv import load_dotenv
import os
from src.session_manager import SessionManager

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=key)
session_id = "test_1"
manager = SessionManager()

while (True):
    # keep getting response and store the questions in the session
    user_input = input("Please type your work: ")
    if user_input.lower() in ["quit", "exit"]:
        break
    MAX_TURNS = 5
    context = manager.get_context(session_id=session_id)[-MAX_TURNS:]
    history = "\n".join([
    f"User: {t['user']}\nAI: {t['ai_response']}"
    for t in context
    ])
    print("[past_work] : " + history)
    print("-----")
    full_prompt = f"{history}\nUser: {user_input}"


    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents= full_prompt
    )
    print(response.text)
    manager.add_turn(session_id=session_id, user_msg=user_input, ai_msg=response.text)
