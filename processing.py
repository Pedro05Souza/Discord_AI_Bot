from openai import OpenAI
from errors import AIParseError, APIError
from discord.ext.commands import Context
from concurrent.futures import ThreadPoolExecutor
from actions import Action
import asyncio

executor = ThreadPoolExecutor(max_workers=1)

async def on_bot_start_command(ctx: Context) -> None:
    from start import StartAI
    while True:
        await asyncio.sleep(10)
        data = StartAI.get_data()
        if data:
            response = executor.submit(generate_ai_response, data).result()
            dict_users = await parse_ai_response(response)
            await generate_ai_actions(dict_users, ctx)
            StartAI.clear_data()

def generate_ai_response(message_data: dict) -> str:
    from start import StartAI
    max_tokens = len(message_data.keys()) * 10
    message_data = str(message_data)
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    try:
        completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {"role": "system", "content": "Please respond ONLY the user_id and a number between 0-10 for each user, the" +
            "higher the number the more disrepectful the user was, if more than one message give the average number of the messages. If more than one user, separate the responses with a comma. Only give integer numbers." +
            "Example: 668666843900149791: 5, \n 856676215007346730: 3. If the message comes with asterisks it means the user said a bad word."},
            {"role": "user", "content": message_data}
        ],
        temperature=0.2,
        max_tokens=max_tokens,
        )
        return completion.choices[0].message.content
    except Exception as e:
        StartAI.clear_data()
        raise APIError(f"Error generating AI actions: {e}")

async def parse_ai_response(response: str) -> dict:
    """Parses the ai response and returns a dictionary"""
    try:
        response = response.split(",")
        dict_users = {}
        for user in response:
            user = user.split(":")
            dict_users[user[0]] = int(user[1]) * 10
        return dict_users
    except Exception as e:
        raise AIParseError(f"Error parsing AI response: {e}")
    
async def generate_ai_actions(users: dict, ctx: Context) -> None:
    for user in users.keys():
        user = Action(ctx.guild.get_member(int(user)), ctx, users[user])
        print(user)