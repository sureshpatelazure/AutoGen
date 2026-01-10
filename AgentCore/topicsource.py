from dataclasses import dataclass
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler, SingleThreadedAgentRuntime, type_subscription,TopicId
from autogen_core import TypeSubscription
import asyncio

@dataclass
class MessageModel:
    content: str

class CoderAgent(RoutedAgent):
    def __init__(self, description) -> None:
       super().__init__(description)
       self.counter = 0

    @message_handler
    async def on_my_message(self, message : MessageModel, ctx : MessageContext) -> None:
        self.counter = self.counter + 1
        print()
        print(f"CoderAgent Received a message :: {message.content} , Counter :: {self.counter}")
        print()

class ReviewerAgent(RoutedAgent):
    def __init__(self, description) -> None:
       super().__init__(description)
       self.counter = 0

    @message_handler
    async def on_my_message(self, message : MessageModel, ctx : MessageContext) -> None:
        self.counter = self.counter + 1
        print()
        print(f"ReviewerAgent Received a message :: {message.content}, Counter :: {self.counter}")
        print()


async def main() -> None:
      agentruntime = SingleThreadedAgentRuntime()

       # register agent
      coderagent_type = "coderagent_jr"
      await CoderAgent.register(agentruntime, coderagent_type , lambda : CoderAgent("coderagent")) 

      revieweragent_type = "revieweragent_jr"
      await ReviewerAgent.register(agentruntime, revieweragent_type , lambda : ReviewerAgent("revieweragent"))

      # Add subscription
      topicnamedev = "bulkwordmerge_development"
      await agentruntime.add_subscription(TypeSubscription(topicnamedev,coderagent_type))
      await agentruntime.add_subscription(TypeSubscription(topicnamedev , revieweragent_type))

      topicnameqa = "bulkwordmerge_qa"
      await agentruntime.add_subscription(TypeSubscription(topicnameqa,coderagent_type))
      await agentruntime.add_subscription(TypeSubscription(topicnameqa , revieweragent_type))


      # AgentId
      topicsourcename = "addbulkwordmerge"

      # Start Runtime
      agentruntime.start()
      
      await agentruntime.publish_message(MessageModel("Dev Message from Runtime"), TopicId(topicnamedev, topicsourcename ))
      await agentruntime.publish_message(MessageModel("QA Message from Runtime"), TopicId(topicnameqa, topicsourcename ))

      await agentruntime.stop_when_idle()
      await agentruntime.close()

asyncio.run(main())

