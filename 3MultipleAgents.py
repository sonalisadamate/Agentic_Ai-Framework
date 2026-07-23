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
    agent1 = AssistantAgent(name="MathTeacher", anthropic_client =anthropic_client, system_message="You are a math teacher, Explain concepts")

    agent2 = AssistantAgent(name="Student",anthropic_client=anthropic_client, system_message="you are a curious student. Ask questions and show your thinking process")


    team = RoundRobinGroupChat(participants=[agent1, agent2], termination_condition=MaxMessageTermination)

    await Console(team.run_stream(task="what is multiplication and how it works"))







asyncio.run(main())