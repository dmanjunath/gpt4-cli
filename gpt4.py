import os
import sys
import logging
import time
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import openai

CHAT_MODEL = "gpt-4"
LOG_LEVEL = logging.INFO
LOG_FORMAT = 'Level=%(levelname)s, Function=%(funcName)s, Time=%(asctime)s, Message=%(message)s'


def setup_logging():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt='%m/%d %I:%M:%S %p')


def init_openai():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise Exception("OPENAI_API_KEY not defined")
    openai.api_key = openai_api_key
    openai.Engine.list()


def query_openai(prompt):
    completion = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=1600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
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
        self.input_str = user_input
        self.is_file = False
        self.file_path = ""
        self.file_contents = ""
        self._check_if_input_is_file()

    def _check_if_input_is_file(self):
        try:
            with open(self.input_str) as file:
                self.is_file = True
                self.file_path = self.input_str
                self.file_contents = file.read()
        except FileNotFoundError:
            pass

    def get_prompt(self):
        return self.file_contents if self.is_file else self.input_str


def main():
    setup_logging()
    init_openai()

    if len(sys.argv) == 1:
        raise SystemExit("Please provide a prompt string or link to file with prompt")

    user_input = " ".join(sys.argv[1:])
    prompt_config = PromptConfig(user_input)
    logging.debug(f"user_input: {prompt_config.get_prompt()}")

    query_openai(prompt_config.get_prompt())
    print("all done!")


if __name__ == "__main__":
    main()
