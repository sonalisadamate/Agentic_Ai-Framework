import asyncio
import os
from turtledemo.chaos import f

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams

os.environ[
    "CLAUDE_API_KEY"] = "not adding api key as pushing the project to github"

os.environ["JIRA_URL"]="https://sonaleesadamate.atlassian.net/jira/software/projects/SCRUM/boards/1?filter=&groupBy=none"
os.environ["JIRA_USERNAME"]="sonali.sadamate23@gmail.com"
os.environ["JIRA_API_TOKEN"]="ATATT3xFfGF05NN47gOIF-vLBIBZhyrqnB2_s4W92lIX7CESLBoJq2ol3JR1LDYSCFqJ_FdiQlPJ_5l6KLSVqVSeA1kc9_pUItpspMIj_8Co88QVeJzuEMt248yDc59TkK7YFwtSMjx8ZhDRx5FgeOwgrz7L3C_DtFU2jNQjnnRPwI9taV8ZyWw=050069B5"

async def main():
    anthropic_client = AnthropicChatCompletionClient(model="claude-3-7-sonnet-20250219")  # from autogen website

    jira_server_params = StdioServerParams(command= "docker",    #f because data inside {}is accepted
                      args= [
                          "run", "-i", "--rm",
                          "--dns", "8.8.8.8", "--dns", "1.1.1.1",
                          "-e", f"JIRA_URL={os.environ['JIRA_URL']}",
                          "-e", f"JIRA_USERNAME={os.environ['JIRA_USERNAME']}",
                          "-e", f"JIRA_API_TOKEN={os.environ['JIRA_API_TOKEN']}",
                          "-e", f"JIRA_PROJECTS_FILTER={os.environ['JIRA_URL']}",
                          "ghcr.io/sooperset/mcp-atlassian:latest"

                      ])

    jira_workbench = McpWorkbench(jira_server_params)

    playwright_server_params = StdioServerParams(command= "npx",
      args= [
        "@playwright/mcp@latest"
      ])

    playwright_workbench = McpWorkbench(playwright_server_params)

    async with jira_workbench as jira_wb, playwright_workbench as playwright_wb: #as an object

        bug_analyst = AssistantAgent(name="BugAnalyst", anthropic_client=anthropic_client,
                       workbench=jira_wb,
                                     system_message=("""
                                       You are a Bug Analyst specializing in Jira defect analysis.

                       Your task is as follows:
                       Goal - - Your role is to analyze defects and create comprehensive test scenarios.
                        -Carefully read their descriptions and identify **recurring issues or common patterns**.
                       3. Based on these patterns, design a **detailed user flow** that exercises the core features of the application and can serve as a robust **smoke test scenario**.

                       Be very specific in your smoke test design:
                       - Provide clear, step-by-step manual testing instructions.
                       - Include exact **URLs or page routes** to visit.
                       - Describe **user actions** (clicks, form inputs, submissions).
                       - Clearly state the **expected outcomes or validations** for each step.

                       If you detect **zero bugs** in the recent Jira query, attempt to re-query or note it clearly.

                       When your analysis and scenario preparation is complete:
                       - Clearly output the final smoke testing steps.
                       - Finally, write: **'HANDOFF TO AUTOMATION'** to signal completion of your analysis.

                       Thank you for your thorough analysis.
                                       """))

        automation_analyst = AssistantAgent(name="AutomationAgent", anthropic_client=anthropic_client,
                                     workbench=playwright_wb,
                                            system_message=(
                                                "You are a Playwright automation expert. Take the user flow from BugAnalyst "
                                                "and convert it into executable Playwright commands. Use Playwright MCP tools to  "
                                                "execute the smoke test. Execute the automated test step by step and report "
                                                "results clearly, including any errors or successes. Take screenshots at key "
                                                "points to document the test execution."
                                                "Make sure expected results in the bug are validated in your flow"
                                                "Important : Use browser_wait_for to wait for success/error messages\n"
                                                "   - Wait for buttons to change state (e.g., 'Applying...' to complete)\n"
                                                "   - Verify expected outcomes as specified by BugAnalyst"
                                                " Always follow the exact timing and waiting instructions provided"
                                                "Complete ALL steps before saying 'TESTING COMPLETE, Execute each step fully, don't rush to completion"))
        team = RoundRobinGroupChat(participants=[bug_analyst,automation_analyst],
                            termination_condition=TextMentionTermination('TESTING COMPLETE'))

        await Console(team.run_stream(task="BugAnalyst:\n, "
                                           "1.search for recent bugs in CreditCardbanking project\n"
                                           "2.Then design a stable user flow that can be used as a smoke test"
                                           "3.use REAL URL's like: https://sonaleesadamate.atlassian.net/jira/software/projects/SCRUM/boards/1?filter=&groupBy=none"
                                           ""
                                           "AutomationAgent:\n"
                                           "once ready, automate this flow using playwright MCP and execute it."))





asyncio.run(main())