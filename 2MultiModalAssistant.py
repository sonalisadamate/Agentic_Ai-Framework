import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from openai.types.beta import assistant

#from chat gpt secret key
os.environ[
    "CLAUDE_API_KEY"] = "not adding api key as pushing the project to github"
async def main():

    anthropic_client = AnthropicChatCompletionClient(model="claude-3-7-sonnet-20250219")  # from autogen website
    assistant = AssistantAgent(name="MultiModalAssiatant", anthropic_client=anthropic_client)
    image = Image.from_file("")  #passing this image path to above LLM 18line to check 20th line what u can see
    multimodal_message = MultiModalMessage(content=["what do you see in this image", image], source="user")

    await Console(assistant.run_stream(task="multimodal_message"))



asyncio.run(main())