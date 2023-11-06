# gpt4-cli

## Overview

This Python script is designed to interact with OpenAI's GPT-4 model from the CLI. I wrote this to combine it with the power of bash and be able to concat files, generate data etc and send it to GPT-4 via the API directly instead of copy/pasting into the app. Also allows access to GPT-4 without the monthly subscription 🙂.

It takes a user input, either as a string or a file, and sends it to the GPT-4 model as a prompt. The model's response is then printed to the console.

## Installation

#### 1. Set Environment Variables

This executable requires the following environment variable to be set.

 `OPENAI_API_KEY` - OpenAI API key
 `GPT4_CLI_PATH_PREFIX` - Directory path to this folder

 #### 2. Create venv and install dependencies

```
python3 -m venv .
source bin/activate
pip3 install -r requirements.txt
```

 #### 3. Make globally accessible

Move into /usr/local/bin
 `ln -s $GPT4_CLI_PATH_PREFIX/src/gpt4 /usr/local/bin/gpt4`

## Usage

The script takes one parameter, either a string or a path to a file containing the prompt

```
# String prompt
gpt4 "How old is Osaka castle?"

# File path prompt
gpt4 ./prompts/prompt.txt
```

If your prompt contains spaces, enclose it in quotes. If you're using a file, ensure the path to the file is correct.