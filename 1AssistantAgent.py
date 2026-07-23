import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient

#from chat gpt secret key
os.environ[
    "CLAUDE_API_KEY"] = "not adding api key as pushing the project to github"

async def main():
    print("i am inside function")

    anthropic_client = AnthropicChatCompletionClient(model="claude-3-7-sonnet-20250219")  # from autogen website

    assistant = AssistantAgent( name="assistant", anthropic_client=anthropic_client )  #class
    await Console(assistant.run_stream(task="what is 25*8"))
    await anthropic_client.close()

asyncio.run(main())