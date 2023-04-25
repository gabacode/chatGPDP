# ChatGPDP

Chat with your favourite fictional characters!

This is a fake scenario and should not be taken seriously.

Change the initial prompt to change your fictional character's desired behavior.

If you're interested in chatting with your own PDF documents, check the [chatPDF](https://github.com/gabacode/chatPDF) project!

## General Notes

- Get a GPT API key from [OpenAI](https://platform.openai.com/account/api-keys) if you don't have one already.

- Set your API key from the top menu `Options -> Settings`.

- You can change your fictional character's desired behavior via the `Options -> Change Personality` menu.

- Save and load conversations from the `File` menu.

- If you're encountering any issues, try starting a new conversation via the `File -> New Chat` menu.

- Ask any questions to your favourite fictional character!

- Enjoy!

## Installation

### Windows 7 and greater

- Download and install the [latest Windows Installer](https://github.com/gabacode/chatGPDP/releases/latest).

### macOS Catalina and greater

- Coming soon...

### All the Operating Systems...

- [Install Python](https://www.python.org/downloads/) >=3.9.

- Install the dependencies:

```bash
pip install -r requirements.txt
```

- Run the app:

```bash
python3 app.py
```

---

## Building

You can build your own executable by running the `build` scripts.

Go to the main folder of the project and run:

## On Linux and macOS

```bash
./build.sh
```

## On Windows

```bash
build.bat
```

Your compiled file will be inside the `/dist` folder.

## Why this project?

We shouldn't really need a reason to publish a project like this, but particular times call for particular measures.

GPDP stands for "Giving Power to Democratic Participation", it's a censorship-resistant (for now) way of accessing to OpenAI's [GPT-3.5 models](https://platform.openai.com/docs/models/gpt-3-5) while their GDPR compliance is being evaluated.

Also, being open source, means that you can understand and learn how to build a similar bot, giving you a degree of "freedom" in setting your initial prompt, to experiment with different bot personalities, and satisfying your curiosity.

Being an embedded and portable solution, means that you can share your conversations across different devices, and even with your friends.

Feel free to post on this repository for [feedback and suggestions](https://github.com/gabacode/chatGPDP/issues).

Use this technology responsibly, and don't forget to have fun!

Peace.

