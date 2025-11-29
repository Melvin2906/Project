import google.generativeai as genai

class GenAIExecption(Exception):
    """GenAI Exception base class"""

class ChatBot:
    """Chat can only have one candidate count"""
    CHATBOT_NAME = "My Gemini AI"

    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel('gemini-2.5-pro')
        self.conversation = None
        self._conversation_history = []

        self.preload_conversation()

    
    def send_prompt(self, prompt, temperature=0.1):
        if temperature < 0 or temperature > 1:
            raise GenAIExecption('Temperature must be between 0 and 1')
        
        if not prompt:
            raise GenAIExecption('Prompt cannot be empty')
        
        try:
            responce = self.conversation.send_message(
                content=prompt,
                generation_config=self._generation_config(temperature),
            )
            responce.resolve()

            # just return the cleaned text
            return responce.text.strip()
        except Exception as e:
            return f"Erreur Gemini: {e}"

    @property
    def history(self):
        conversation_history = [
            {'role': message.role, 'text': message.parts[0].text} for message in self.conversation.history
        ]
        return conversation_history

    def clear_conversation(self):
        self.conversation = self.model.start_chat(history=[])
    
    def start_convertion(self):
        self.conversation = self.model.start_chat(history=self._conversation_history)


    def _generation_config(self, temperature):
        return genai.types.GenerationConfig(
            temperature=temperature
        )

    def _construct_message(self, text, role='user'):
        return {
            'role': role,
            'parts': [text]
        }

    def preload_conversation(self, conversation_history=None):
        if isinstance(conversation_history, list):
            self._conversation_history = conversation_history
        else:
            self._conversation_history = [
                self._construct_message("Please format your responses in clear Markdown with headings, lists, and emphasis when useful.")
            ]
