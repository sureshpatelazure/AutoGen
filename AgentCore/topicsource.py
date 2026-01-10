from dataclasses import dataclass
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler, SingleThreadedAgentRuntime, type_subscription,TopicId
from autogen_core import TypeSubscription
import asyncio

@dataclass
class MessageModel:
    content: str

class CoderAgent(RoutedAgent):
    @message_handler
    async def on_my_message(self, message : MessageModel, ctx : MessageContext) -> None:
        print()
        print(f"CoderAgent Received a message :: {message.content}")
        print()

class ReviewerAgent(RoutedAgent):
    @message_handler
    async def on_my_message(self, message : MessageModel, ctx : MessageContext) -> None:
        print()
        print(f"ReviewerAgent Received a message :: {message.content}")
        print()


async def main() -> None:
      agentruntime = SingleThreadedAgentRuntime()

       # register agent
      coderagent_type = "coderagent_jr"
      await CoderAgent.register(agentruntime, coderagent_type , lambda : CoderAgent("coderagent")) 

      revieweragent_type = "revieweragent_jr"
      await ReviewerAgent.register(agentruntime, revieweragent_type , lambda : ReviewerAgent("revieweragent"))

      # Add subscription
      topicname = "bulkwordmerge_development"
      await agentruntime.add_subscription(TypeSubscription(topicname,coderagent_type))
      await agentruntime.add_subscription(TypeSubscription(topicname , revieweragent_type))

      # AgentId
      topicsourcename = "addbulkwordmerge"

      # Start Runtime
      agentruntime.start()
      
      await agentruntime.publish_message(MessageModel("Message from Runtime"), TopicId(topicname, topicsourcename ))
      await agentruntime.stop_when_idle()
      await agentruntime.close()

asyncio.run(main())

