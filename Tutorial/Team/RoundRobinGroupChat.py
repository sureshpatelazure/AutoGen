import asyncio

from autogen_agentchat.agents import AssistantAgent
from  autogen_agentchat.base import TaskResult

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination

from autogen_agentchat.ui import Console
from autogen_core import CancellationToken

from autogen_ext.models.ollama import OllamaChatCompletionClient

ollama_clinet = OllamaChatCompletionClient(model="qwen3:0.6b")

# primary assistant agent
primary_agent = AssistantAgent(
    name= "primary",
    model_client=ollama_clinet,
    system_message= "You are helpful AI assistant."
)

#crtitic agent
critic_agent = AssistantAgent(
    name= "critic",
    model_client=ollama_clinet,
    system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed.",
    reflect_on_tool_use=True
)

text_termination = TextMentionTermination("APPROVE")

team = RoundRobinGroupChat([primary_agent, critic_agent],termination_condition=text_termination)

asyncio.run(Console(team.run_stream( task = "Write a short poem about the beauty of nature.")));
