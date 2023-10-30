import os
import sys
import logging
import time

# patch to mute urllib3 warning, requirement for openai
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import openai


CHAT_MODEL = "gpt-4"
LOG_LEVEL = logging.INFO

def setup_logging():
    log_format = 'Level=%(levelname)s, Function=%(funcName)s, Time=%(asctime)s, Message=%(message)s'
    logging.basicConfig(level=LOG_LEVEL, format=log_format, datefmt='%m/%d %I:%M:%S %p')

def init_openai():
    # check if OPENAI env var exists
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    if OPENAI_API_KEY == None:
        raise Exception("OPENAI_API_KEY not defined")
    openai.api_key = OPENAI_API_KEY
    openai.Engine.list()  # check we have authenticated

def query_openAI(prompt):
    completion = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}"}
        ],
        temperature=0,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=True
    )

    # adapted from https://github.com/tmgthb/Stream-responses
    answer = ''
    for event in completion:
        print(answer, end='', flush=True)
        event_text = event['choices'][0]['delta']
        answer = event_text.get('content', '')
        time.sleep(0.1)

    print("\n")
    return completion

class PromptConfig:
    def __init__(self, user_input):
        self.input_str: str = user_input # can either be a prompt string or a path to a file

        # file related properties
        self.is_file: bool = False
        self.file_path: str = ""
        self.file_contents: str = ""

        self.check_if_input_is_file()

    def check_if_input_is_file(self):
        try:
            with open(self.input_str) as f:
                self.is_file = True
                self.file_path = self.input_str
                self.file_contents = f.read()
        except FileNotFoundError:
            pass

    def get_prompt(self):
        return self.input_str if self.is_file is False else self.file_contents


def main():
    setup_logging()
    init_openai()
    args = sys.argv
    if len(args) == 1:
        print("Please provide a prompt string or link to file with prompt")
        exit(1)

    user_input = args[1]
    if len(args) >= 3:
        user_input = " ".join(args[1:])

    prompt_config = PromptConfig(user_input) # either a prompt string or a file
    logging.debug(f"user_input: {prompt_config.get_prompt()}")

    query_openAI(prompt_config.get_prompt())
    print("all done!")

main()