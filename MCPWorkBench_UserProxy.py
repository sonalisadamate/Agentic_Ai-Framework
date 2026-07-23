import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench
from mcp import StdioServerParameters

os.environ[
    "CLAUDE_API_KEY"] = "not adding api key as pushing the project to github"
async def main():
    filesystem_server_params = StdioServerParams(command= "npx",args=[
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/my path"],
    read_timeout_seconds=60

      )
    fs_workbench = McpWorkbench(filesystem_server_params)
    async with fs_workbench as fs_wb:

        anthropic_client = AnthropicChatCompletionClient(model="claude-3-7-sonnet-20250219")  # from autogen website

        math_tutor = AssistantAgent(name="MathTutor", anthropic_client=anthropic_client,workbench=fs_wb,system_message="You are helpful math tutor.help the user to solve problem step by step, you have to access file system"
                    "when user says 'Thanks Done' or similar, acknowledge and say 'Lesson Complete' to end session")

        user_proxy = UserProxyAgent(name="student")  # this is for human

        team = RoundRobinGroupChat(participants=[user_proxy, math_tutor],
                                   termination_condition=TextMentionTermination("Lesson Complete"))

        await Console(team.run_stream(task="i need help with algebra problem. Feel free to create fils to help with student learning"))
asyncio.run(main())