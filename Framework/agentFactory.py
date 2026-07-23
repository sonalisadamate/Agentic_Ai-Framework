from autogen_agentchat.agents import AssistantAgent

from Framework import mcp_config
from Framework.mcp_config import McpConfig
from Framework.Scenario2 import anthropic_client


#factory is all about creating agents- only agents will be present here
#when there is class constructor should be present
class AgentFactory:     #self is accessible to everywhere
    def __init__(self):
        self.anthropic_client= anthropic_client
        self.mcp_config = McpConfig()



    def create_database_agent(self,system_message):

        database_agent = AssistantAgent(name="DatabaseAgent", anthropic_client=self.anthropic_client,
                                     workbench=self.mcp_config.get_mysql_workbench(),
                                     system_message=system_message)

    def create_api_agent(self, system_message):
        rest_api_workbench = self.mcp_config.get_rest_api_workbench()
        file_system_workbench = self.mcp_config.get_file_system_workbench()

        api_agent = AssistantAgent(name="APIAgent", anthropic_client = self.anthropic_client,
                                   workbench=[rest_api_workbench, file_system_workbench],
                                   system_message=system_message)

        return api_agent

    def create_excel_agent(self,system_message):

        excel_workbench = self.mcp_config.get_excel_workbench()

        excel_agent = AssistantAgent(name="ExcelAgent", anthropic_client=self.anthropic_client,
                                     workbench=excel_workbench,
                                     system_message=system_message)
        return excel_agent


