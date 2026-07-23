import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.anthropic import AnthropicChatCompletionClient

os.environ[
    "CLAUDE_API_KEY"] = "not adding api key as pushing the project to github"

async def main():
    anthropic_client = AnthropicChatCompletionClient(model="claude-3-7-sonnet-20250219")  # from autogen website

    researcher = AssistantAgent("ResearcherAgent", anthropic_client=anthropic_client, system_message="you are a researcher.your role is to gather information and provide research finding""do not write articles or create content-just provide research data and facts")

    writer = AssistantAgent("WriterAgent", anthropic_client=anthropic_client, system_message="you are a writer.your role is to take research information "and "create well written articles. Wait for researcher to be provided, then write the content")

    critic = AssistantAgent("CriticAgent", anthropic_client=anthropic_client,system_message="you are a a critic .your role is to review written content and provide feedback. Say 'Terminate' when satisfied with the final result")

    text_termination = TextMentionTermination("TERMINATE")
    max_messages_termination = MaxMessageTermination(max_message=15)
    termination = text_termination | max_messages_termination

    #Selector group figuessout which Agent has to run
    team = SelectorGroupChat(participants=[critic,writer,researcher],anthropic_client=anthropic_client,termination_condition= termination,allow_repeated_speaker=True)

    await Console(team.run_stream(task="Research renewable energy trends and write a brief articlle about the future of solar energy"))