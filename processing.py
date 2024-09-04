from openai import OpenAI
from errors import AIParseError, APIError
from discord.ext.commands import Context
import asyncio

async def on_bot_start_command(ctx: Context) -> None:
    from start import StartAI
    while True:
        await asyncio.sleep(10)
        data = StartAI.get_data()
        if data:
            response = await generate_ai_actions(data)
            dict_users = await parse_ai_response(response)
            StartAI.clear_data()

async def generate_ai_actions(message_data: dict) -> str:
    max_tokens = len(message_data.keys()) * 10
    message_data = str(message_data)
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    try:
        completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {"role": "system", "content": "Please respond ONLY the user_id and a number between 0-10 for each user, the" +
            "higher the number the more disrepectful the user was, if more than one message give the average number of the messages. If more than one user, separate the responses with a comma. Only give integer numbers." +
            "Example: user1: 5, \n user2: 3"},
            {"role": "user", "content": message_data}
        ],
        temperature=0.2,
        max_tokens=max_tokens
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise APIError(f"Error generating AI actions: {e}")

async def parse_ai_response(response: str) -> dict:
    """Parses the ai response and returns a dictionary"""
    try:
        response = response.split(",")
        dict_users = {}
        for user in response:
            user = user.split(":")
            dict_users[user[0]] = int(user[1])
        return dict_users
    except Exception as e:
        raise AIParseError(f"Error parsing AI response: {e}")