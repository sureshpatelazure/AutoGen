from dataclasses import dataclass
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler, SingleThreadedAgentRuntime
import asyncio

@dataclass
class SimpleMessageType:
    content: str


class SingleAgent(RoutedAgent):
    def __init__(self, description) -> None:
        super().__init__(description)


    @message_handler
    async def hanlde_message(self, message : SimpleMessageType, ctx : MessageContext)->None:
           print(f"AgentId : {self.id.type} - {self.id.key}  received message: {message.content}")



async def main() -> None:

    agentruntime = SingleThreadedAgentRuntime()
    
    readeragenttype =  "readeragent"
    await SingleAgent.register(agentruntime, readeragenttype, lambda : SingleAgent("Reader"))

    writeragenttype = "writeragent"
    await SingleAgent.register(agentruntime, writeragenttype, lambda : SingleAgent("Writer"))

    agentruntime.start()
    readeragentid1 = AgentId(readeragenttype , "Reader 1")
    await agentruntime.send_message(SimpleMessageType("Reader 1 messag"), readeragentid1)

    readeragentid2 = AgentId(readeragenttype , "Reader 2")
    await agentruntime.send_message(SimpleMessageType("Reader2 Message"), readeragentid2)

    writeragentid = AgentId(writeragenttype , "writer")
    await agentruntime.send_message(SimpleMessageType("Writer Message"), writeragentid)

    await agentruntime.stop_when_idle()
    await agentruntime.close()
    

asyncio.run(main())




       