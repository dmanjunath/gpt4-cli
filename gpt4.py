import os
import logging
import argparse
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from openai import OpenAI

CHAT_MODEL = "gpt-4"
LOG_LEVEL = logging.INFO
LOG_FORMAT = 'Level=%(levelname)s, Function=%(funcName)s, Time=%(asctime)s, Message=%(message)s'


def setup_logging():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, datefmt='%m/%d %I:%M:%S %p')


def init_openai():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise Exception("OPENAI_API_KEY not defined")
    client = OpenAI()
    return client


def query_openai(client, prompt):
    completion = client.chat.completions.create(
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

    answer = ''
    for part in completion:
        answer = (part.choices[0].delta.content or "")
        print(answer, end='', flush=True)

    print("\n")
    return completion


class PromptConfig:
    def __init__(self):
        self.is_file = False
        self.file_path = ""
        self.file_contents = ""
        self.thread = ""
        self.parse_args()
        self._check_if_input_is_file()

    def parse_args(self):
        parser = argparse.ArgumentParser(description='GPT4 CLI.')
        parser.add_argument('user_input', type=str, help='Enter prompt text or path to file with prompt')
        parser.add_argument('--thread', type=str, help='Optional thread name')

        # hack to combine all non-recognized args into user_input
        args, unknown = parser.parse_known_args()
        self.user_input = (args.user_input + ' ' + ' '.join(unknown).strip()).strip()
        logging.debug(f"user_input: {self.user_input}")
        
        self.thread = args.thread
        logging.debug(f"thread: {self.thread}")

    def _check_if_input_is_file(self):
        try:
            with open(self.user_input) as file:
                self.is_file = True
                self.file_path = self.user_input
                self.file_contents = file.read()
        except FileNotFoundError as e:
            # logging.debug("file not found", e)
            pass

    def get_prompt(self):
        return self.file_contents if self.is_file else self.user_input

class DataStore:
    def __init__(self):
        self.filename = "KEY_TO_STRING.csv"

    def store(self, id, string):
        with open(self.filename, 'a') as f:
            f.write(f'{id},{string}\n')

    def retrieve(self, id):
        with open(self.filename, 'r') as f:
            for line in f:
                line_id, line_string = line.strip().split(',')
                if line_id == id:
                    return line_string
        return None

def map_thread_to_id(thread, client):
    data_store = DataStore()
    id = data_store.retrieve(thread)
    if id is None:
        empty_thread = client.beta.threads.create()
        return empty_thread.id
    
    return id

def main():
    setup_logging()
    client = init_openai()

    prompt_config = PromptConfig()
    logging.debug(f"user_input: {prompt_config.get_prompt()}")

    query_openai(client, prompt_config.get_prompt())


if __name__ == "__main__":
    main()
