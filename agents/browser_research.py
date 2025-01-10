from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

llm = ChatOpenAI(model="gpt-4o")

async def main():
    agent = Agent(
        task="Find the most popular programming frameworks within the last month, Return me the top 5",
        llm = llm,
        save_conversation_path="logs/agent_conversations.json",
    )
    result = await agent.run()
    print(result)

asyncio.run(main())