import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient

ollama_client = OllamaChatCompletionClient(model="qwen3:0.6b")

async def get_weather(city:str)->str:
    # Simulate a weather fetching function
    return f"The current weather in {city} is sunny with a temperature of 25°C."

agent = AssistantAgent(
    name = "weatheragent",
    model_client =  ollama_client,
    tools = [get_weather],
    system_message= " You are a helpful weather assistant. You can provide current weather information for any city using the get_weather tool. ",
    reflect_on_tool_use=True,
    model_client_stream=True
)    

async def main() -> None:
    await Console(agent.run_stream(task = "What's the weather like in New York City today?"))
    await ollama_client.close()

asyncio.run(main())