from __future__ import annotations as _annotations

import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from httpx import AsyncClient
from database import db
from agents.research import ResearchDeps, research_agent
from agents.example_builder import BuilderDeps, example_builder_agent

db_folder = os.path.join(os.path.dirname(__file__), 'database')
db_path = os.path.join(db_folder, 'research_data.db')
examples_folder = os.path.join(os.path.dirname(__file__), 'examples', 'ai_example_projects')
os.makedirs(examples_folder, exist_ok = True)

async def save_example(project_name: str, snippets: list[str]):
    project_path = os.path.join(examples_folder, project_name)
    os.makedirs(project_path, exist_ok = True)
    
    for i, snippet in enumerate(snippets):
        # TODO: could be cool to name the file actually something useful here
        file_path = os.path.join(project_path, f'example_{i + i}.py') 
        with open(file_path, 'w', encoding = "utf-8") as file:
            file.write(snippet)

async def run_agents():
    async with AsyncClient() as client:
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
            await save_example(builder_result.data.project_name, builder_result.data.code_snippets)

        print("Example Builder Agent Completed.")
        rdb.close()

if __name__ == '__main__':
    asyncio.run(run_agents())
