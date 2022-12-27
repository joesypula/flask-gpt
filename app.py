import os
import re
import ssl
import json
import logging
from logging.handlers import RotatingFileHandler
import openai
import config
from flask import Flask, render_template, request, make_response

app = Flask(__name__)

# Initialize an empty list to store the conversation
conversation = []

# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set up a rotating file handler
handler = RotatingFileHandler("logs/conversation.log", maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)

# Set up a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Create an openaiapikey.txt file and save your api key.
openai.api_key = config.API_KEY


def get_response_from_openai(prompt, engine='text-davinci-003', temp=0.9, top_p=1.0, tokens=1000, freq_pen=0.0,
                             pres_pen=0.5):
    """
    Makes a request to the OpenAI API and returns the response.
    """
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temp,
            max_tokens=tokens,
            top_p=top_p,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            stop=[" User:", " AI:"])
        return response['choices'][0]['text'].strip()
    except Exception as e:
        print('Error communicating with OpenAI:', e)
        return "Sorry, there was an error getting a response from the OpenAI API."


def get_bot_response(user_text, context):
    """
    Processes the user's input, gets a response from the OpenAI API, and appends the conversation to the conversation list.
    """
    # Sanitize the user's input
    user_text = user_text.strip()
    if not user_text:
        return "Please enter some text."

    # Remove any special characters or HTML tags from the user's input
    # Allow the ? character in the user's input
    user_text = re.sub(r'[^\w\s\?]', '', user_text)
    user_text = re.sub(r'<[^>]+>', '', user_text)

    prompt = context + user_text
    bot_response = get_response_from_openai(prompt)
    conversation.append(("User:", user_text))
    conversation.append(("Bot:", bot_response))
    return bot_response


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get():
    user_text = request.args.get('msg')
    context = request.args.get('context')
    src_ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    bot_response = get_bot_response(user_text, context)
    log_message = {
        "src_ip": src_ip,
        "user_agent": user_agent,
        "user_input": user_text,
        "bot_response": bot_response,
    }
    logger.info(json.dumps(log_message))
    return bot_response


@app.route("/save_conversation")
def save_conversation():
    conversation_str = ""
    for message in conversation:
        conversation_str += f"{message[0]} {message[1]}\n"
    return conversation_str


@app.route("/clear_conversation")
def clear_conversation():
    conversation.clear()
    src_ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    log_message = {
        "src_ip": src_ip,
        "user_agent": user_agent,
        "action": "conversation cleared"
    }
    logger.info(json.dumps(log_message))
    make_response("Conversation cleared.")
    return "Conversation history cleared."


if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain('certificate.pem', 'key.pem')
    app.run(debug=False, host="0.0.0.0", port=443, ssl_context=ssl_context)
