import sys
from configparser import ConfigParser
from chat_bot_using_gemini import ChatBot
from rich.markdown import Markdown
from rich.console import Console

def main():
    config = ConfigParser()
    config.read("D:/API_KEY/Gemini_api.ini")
    api_key = config['gemini_ai']['API_KEY']

    chatbot = ChatBot(api_key=api_key)
    chatbot.start_convertion()
    #chatbot.clear_conversation()

    print("Welcome to the JJ Gemini Chatbot CLI. Type 'quit' or 'exit' to exit")

    # print('{0}: {1}'.format(chatbot.CHATBOT_NAME, chatbot.history[-1]['text']))
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit" or user_input.lower() == 'exit':
            # print(Exiting Chatbot CLI')
            sys.exit("Exiting ChatBot CLI...")
        
        try:
            responce = chatbot.send_prompt(user_input)
            console = Console()
            ...
            response = chatbot.send_prompt(user_input)
            console.print(Markdown(response))
            #print(f"{chatbot.CHATBOT_NAME}: {responce}")
        except Exception as e:
            print(f"Error: {e}")

main()
