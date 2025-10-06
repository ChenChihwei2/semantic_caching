class SessionManager:
    def __init__(self):
        self.sessions = {}
        
    # You get the message and the session_id and append the message onto existing place
    def add_turn(self, session_id, user_msg, ai_msg):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append({"user": user_msg, "ai_response": ai_msg})

    def get_context(self, session_id):
        return self.sessions.get(session_id, [])
