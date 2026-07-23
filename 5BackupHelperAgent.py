import json
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from openai.types.beta import assistant
from tqdm import asyncio


os.environ[
    "CLAUDE_API_KEY"] = "not adding api key as pushing the project to github"

async def main():
    anthropic_client = AnthropicChatCompletionClient(model="claude-3-7-sonnet-20250219")  # from autogen website

    #create first assistant agent
    agent1 = AssistantAgent(name="Helper", anthropic_client =anthropic_client, system_message="You are a math teacher, Explain concepts")

    agent2 = AssistantAgent(name="BackupHelper",anthropic_client=anthropic_client, system_message="you are a curious student. Ask questions and show your thinking process")



    await Console(agent1.run_stream(task="my fav color is blue"))
    state = await agent1.save_state()
    with open("memory.json", "w") as f:
        json.dump(state,f, default=str)

    with open("memory.json", "r") as f:
        saved_state = json.load(f)

    await agent2.load_state(saved_state)
    agent2.run_stream(task="what is my fav color?")

    await anthropic_client.close()


asyncio.run(main())