from dataclasses import dataclass
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler, SingleThreadedAgentRuntime, type_subscription,TopicId
import asyncio

@dataclass
class MessageModel:
    content: str

@type_subscription (topic_type= "Default")
class ReceiverAgent(RoutedAgent):
    @message_handler
    async def on_my_message(self, message : MessageModel, ctx : MessageContext) -> None:
        print()
        print(f"Receiver Agent : Received a message :: {message.content}")
        print()
      
    
class BroadCastAgent(RoutedAgent):
    def __init__(self, description):
        super().__init__(description)

    @message_handler
    async def on_my_message(self, message : MessageModel, ctx : MessageContext) ->None:
          print()
          print(f"SenderAgent : Received Message from runtime :: {message.content}")  
          await self.publish_message(MessageModel("Broadcats message_123"),topic_id=TopicId(type="Default", source=self.id.key))       
          print()

async def main() -> None:

    agentruntime = SingleThreadedAgentRuntime()
    
    receivertype =  "receiveragent"
    await ReceiverAgent.register(agentruntime, receivertype, lambda : ReceiverAgent("receiveragent    "))

    broadcastagenttype = "broadcastagentagent"
    await BroadCastAgent.register(agentruntime, broadcastagenttype, lambda : BroadCastAgent("BroadCastAgent"))

    agentruntime.start()
    broadcastagentid = AgentId(broadcastagenttype , "broadcastagent")
    await agentruntime.send_message(MessageModel(content="message from runtime"),broadcastagentid)
    
    await agentruntime.stop_when_idle()
    await agentruntime.close()
    

asyncio.run(main())
  