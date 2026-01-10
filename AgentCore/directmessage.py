from dataclasses import dataclass
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler, SingleThreadedAgentRuntime
import asyncio

@dataclass
class MessageModel:
    content: str


class ReceiverAgent(RoutedAgent):
    @message_handler
    async def on_my_message(self, message : MessageModel, ctx : MessageContext) -> MessageModel:
        print()
        print(f"Receiver Agent : Received message from Sender Agent :: {message.content}")
        print()
        return MessageModel(content=f"message from receievr agent")
      
    
class SenderAgent(RoutedAgent):
    def __init__(self, description, receiveragenttype):
        super().__init__(description)
        self.receiveragentid = AgentId(receiveragenttype, self.id.key)

    @message_handler
    async def on_my_message(self, message : MessageModel, ctx : MessageContext) ->None:
          print()
          print(f"SenderAgent : Received Message from runtime :: {message.content}")  
          response = await self.send_message(MessageModel("message from sender agent"), self.receiveragentid)
          print(f"SenderAgent : Received response from ReceiverAgnt ::  {response.content}")
          print()

async def main() -> None:

    agentruntime = SingleThreadedAgentRuntime()
    
    receiveragnttype =  "ReceiverAgent"
    await ReceiverAgent.register(agentruntime, receiveragnttype, lambda : ReceiverAgent("receiveragent    "))

    senderagenttype = "SenderAgent"
    await SenderAgent.register(agentruntime, senderagenttype, lambda : SenderAgent("SenderAgent", receiveragnttype))

    agentruntime.start()
    senderagentid = AgentId(senderagenttype , "SenderAgent")
    await agentruntime.send_message(MessageModel(content="message from runtime"),senderagentid)
    
    await agentruntime.stop_when_idle()
    await agentruntime.close()
    

asyncio.run(main())
  