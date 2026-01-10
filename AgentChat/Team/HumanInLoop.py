import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient

ollama_client = OllamaChatCompletionClient(model="qwen3:0.6b")

assistant =  AssistantAgent("assistant",model_client=ollama_client)
user_proxy = UserProxyAgent("user_proxy", input_func=input)

termination = TextMentionTermination("APPROVE")

team  = RoundRobinGroupChat([assistant,user_proxy], termination_condition=termination)

asyncio.run(Console(team.run_stream( task = "Write a short poem about the beauty of nature.")));

asyncio.run(ollama_client.close())