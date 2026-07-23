import asyncio
import os

from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.anthropic import AnthropicChatCompletionClient

os.environ[
    "CLAUDE_API_KEY"] = "not adding api key as pushing the project to github"

async def main():
    #initialize openai or claude
    #make sure ti set your API key env variable
    anthropic_client = AnthropicChatCompletionClient(model="claude-3-7-sonnet-20250219")  # from autogen website
    #web browser plus resoning intelligence
    web_surfer_agent = MultimodalWebSurfer(name="WebSurfer",anthropic_client=anthropic_client, headless=False,animate_actions=True)

    agent_team = RoundRobinGroupChat(participants=[web_surfer_agent],max_turns=3)

    await Console(agent_team.run_stream(task="Navigate to Google and search for 'AutoGen framework Python'.Then summarise what you find"))

    await web_surfer_agent.close()
    await anthropic_client.close()


asyncio.run(main())