from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench


class McpConfig:




        def get_mysql_workbench():
            mysql_server_params = StdioServerParams(command="/Library/Frameworks/Python.framework/Versions/3.14/bin/uv",
                              args= [
                "--directory",
                "/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages",
                "run",
                "mysql_mcp_server"
            ],
                              env= {
                "MYSQL_HOST": "localhost",
                "MYSQL_PORT": "3306",
                "MYSQL_USER": "your_username",
                "MYSQL_PASSWORD": "your_password",
                "MYSQL_DATABASE": "your_database"
            }
            )

            return McpWorkbench(server_params=mysql_server_params)

        def get_rest_api_workbench():
            rest_api_server_params = StdioServerParams(command= "npx",
      args=[
        "-y",
        "dkmaker-mcp-rest-api"
      ],
      env= {
        "REST_BASE_URL": "https://rahulshettyacademy.com",

        "HEADER_Accept": "application/json"
      })

            return McpWorkbench(rest_api_server_params)

        def get_excel_workbench():
            excel_server_params= StdioServerParams(command= "npx",
            args=["--yes", "@negokaz/excel-mcp-server"],
            env= {
                "EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"
            },
                read_timeout_seconds=60)

            return McpWorkbench(excel_server_params)


        def get_file_system_workbench():
            file_system_params = StdioServerParams(command= "npx",
      args= [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "Users/indrajeetrajaramsadamate/documents/mcp-files"
        "read_timeout_seconds=60)"
      ])

            return McpWorkbench(file_system_params)