import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from openai.types.beta import assistant
from tqdm import asyncio


os.environ[
    "CLAUDE_API_KEY"] = "not adding api key as pushing the project to github"

async def main():
    anthropic_client = AnthropicChatCompletionClient(model="claude-3-7-sonnet-20250219")  # from autogen website

    assistant = AssistantAgent(name="MathTutor", anthropic_client=anthropic_client, system_message="You are helpful math tutor.help the user to solve problem"
                    "when user says 'Thanks Done' or similar, acknowledge and say 'Lesson Complete' to end session")

    user_proxy = UserProxyAgent(name="student")  #this is for human

    team = RoundRobinGroupChat(participants=[user_proxy,assistant], termination_condition=TextMentionTermination("Lesson Complete"))

    await Console(team.run_stream(task="i need help with algebra problem"))


asyncio.run(main())

#Human -Agent-(save) , Agent2