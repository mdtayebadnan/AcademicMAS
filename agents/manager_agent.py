from spade import Agent
from spade.behaviour import CyclicBehaviour

class OrchestratorAgent(Agent):
    class OrchestratorBehaviour(CyclicBehaviour):
        async def run(self):
            message = await self.receive()
            if message:
                user_request = message.body
                print(f"Orchestrator received request: {user_request}")

                # Decide which agent to call based on the user input
                if "summarize" in user_request.lower():
                    await self.send_summarization_request(message)
                elif "citation" in user_request.lower():
                    await self.send_citation_request(message)
                elif "literature review" in user_request.lower():
                    await self.send_literature_review_request(message)
                else:
                    await self.send(message.make_reply("Sorry, I didn't understand the request."))

        async def send_summarization_request(self, message):
            # Send the request to Summarization Agent
            summarizer_jid = "summarizer@localhost"
            summarizer_agent = await self.search_for_agent(summarizer_jid)
            await summarizer_agent.send(message)

        async def send_citation_request(self, message):
            # Send the request to Citation Agent
            citation_agent_jid = "citation@localhost"
            citation_agent = await self.search_for_agent(citation_agent_jid)
            await citation_agent.send(message)

        async def send_literature_review_request(self, message):
            # Send the request to Literature Review Agent
            literature_review_jid = "literature_review@localhost"
            literature_review_agent = await self.search_for_agent(literature_review_jid)
            await literature_review_agent.send(message)

    async def setup(self):
        print("Orchestrator agent starting...")
        self.add_behaviour(self.OrchestratorBehaviour())

    async def search_for_agent(self, jid):
        # This is a simple function to look for an agent
        return await self.search(jid)
