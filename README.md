# ChatGPDP

Chat with your favourite fictional characters!

This is a fake scenario and should not be taken seriously.

Change the text in the `initial_prompt.txt` file to change your fictional character's desired behavior.

## Instructions

---
### Windows 7 and greater

- Download and install the [latest Windows Installer](https://github.com/gabacode/chatGPDP/releases/latest).

- Get a GPT API key from [OpenAI](https://platform.openai.com/account/api-keys) if you don't have one already.

- Set your API key from the top menu `Options -> Set API key`.

- You can change your fictional character's desired behavior via the `Options -> Change Personality` menu.

- If you're encountering any issues, try starting a new conversation via the `File -> New Chat` menu.

- Ask any questions to your favourite fictional character!

- Enjoy!

---

### Linux, macOS etc...

While the .deb and .dmg packages are being released, you can launch ChatGPDP with Python >=3.9

- Install the requirements

```bash
pip install -r requirements.txt
```

- Get a GPT API key from [OpenAI](https://platform.openai.com/account/api-keys) if you don't have one already.

- Paste your API key in a file called `.env` in the root directory of the project, or via the top menu Options -> Set API key.

- Run the app.

```bash
python3 app.py
```

- Ask any questions to your favourite fictional character!

- Enjoy!

## Why?

We shouldn't really need a reason to publish a project like this, but particular times call for particular measures.

GPDP stands for "Giving Power to Democratic Participation", it's a censorship-resistant (for now) way of accessing to OpenAI's [GPT-3.5 models](https://platform.openai.com/docs/models/gpt-3-5) while their GDPR compliance is being evaluated.

Also, being open source, means that you can understand and learn how to build a similar bot, giving you a degree of "freedom" in setting your initial prompt, to experiment with different bot personalities, and satisfying your curiosity.

Being an embedded and portable solution, means that you can share your conversations across different devices, and even with your friends.

Feel free to post on this repository for [feedback and suggestions](https://github.com/gabacode/chatGPDP/issues).

Use this technology responsibly, and don't forget to have fun!

Peace.