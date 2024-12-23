from __future__ import annotations as _annotations

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from httpx import AsyncClient
from database import db
from agents.research import ResearchDeps, research_agent
from agents.example_builder import BuilderDeps, example_builder_agent

# Database setup
db_folder = os.path.join(os.path.dirname(__file__), 'database')
db_path = os.path.join(db_folder, 'research_data.db')

async def run_agents():
    async with AsyncClient() as client:
        # Initialize database
        rdb = db.ResearchDatabase(db_path=db_path)

        # ------------------ Research Agent ------------------
        print("Running Research Agent...")
        research_deps = ResearchDeps(client=client)
        research_result = await research_agent.run('Find trending AI frameworks and tools.', deps=research_deps)

        # Save research results to database
        rdb.save_results(research_result.data.topics, research_result.data.summaries)
        print("Research Agent Completed. Results saved to database.")

        # ---------------- Example Builder Agent ----------------
        results = rdb.conn.execute('SELECT topic FROM research').fetchall()
        topics = [row[0] for row in results]

        # Run example builder agent
        print("Running Example Builder Agent...")
        builder_deps = BuilderDeps(client=client)
        for topic in topics:
            builder_result = await example_builder_agent.run(f'Generate example app for {topic}', deps=builder_deps)
            print(f'Example Project: {builder_result.data.project_name}')
            for snippet in builder_result.data.code_snippets:
                print(snippet)

        print("Example Builder Agent Completed.")
        rdb.close()

if __name__ == '__main__':
    asyncio.run(run_agents())
