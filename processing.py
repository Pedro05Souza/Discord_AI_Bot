from openai import OpenAI
import asyncio

async def on_bot_start_command(ctx):
    from base import BaseAI
    while True:
        await asyncio.sleep(10)
        data = BaseAI.get_data()
        if data:
            data = str(data)
            response = await generate_ai_actions(data)
            dict_users = await parse_ai_response(response)
            print(dict_users)
            BaseAI.clear_data()

async def generate_ai_actions(message_data):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    completion = client.chat.completions.create(
    model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
    messages=[
        {"role": "system", "content": "Please respond ONLY the user_id and a number between 0-10 for each user, the" +
         "higher the number the more disrepectful the user was, if more than one message give the average number of the messages. If more than one user, separate the responses with a comma. Only give integer numbers." +
         "Example: user1: 5 \n user2: 3"},
        {"role": "user", "content": message_data}
    ],
    temperature=0.2,
    max_tokens=15
    )
    return completion.choices[0].message.content

async def parse_ai_response(response: str):
    """Parses the ai response and returns a dictionary"""
    print(response)
