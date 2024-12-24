from __future__ import annotations as _annotations

import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

from dataclasses import dataclass
from typing import List
from datetime import datetime

from httpx import AsyncClient
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

import logfire
logfire.instrument_pydantic()
logfire.configure(send_to_logfire='if-token-present')

from devtools import debug

from database import db

db_folder = os.path.join(os.path.dirname(__file__), '..', 'database')
db_path = os.path.join(db_folder, 'research_data.db')


@dataclass
class BuilderDeps:
    client: AsyncClient

class ExampleResult(BaseModel):
    project_name: str = Field(description='Name of the generated example project')
    code_snippets: List[str] = Field(description='Code snippets demonstrating features')

example_builder_agent = Agent(
    'openai:gpt-4o',
    deps_type=BuilderDeps,
    result_type=ExampleResult,
    system_prompt=(
        'You are a development assistant. Use research data to generate example applications demonstrating how trending technologies can be implemented. Focus on clarity, scalability, and modern design patterns.'
    ),
)

@example_builder_agent.tool
async def generate_code_snippets(ctx: RunContext[BuilderDeps], topic: str) -> List[str]:
    """Generate example code snippets for a given topic."""
    prompt = f"Generate Python code snippets that demonstrate the use of {topic} in a web application."
    with logfire.span('Generating example code') as span:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert Python programmer specializing in web development. Provide detailed examples and explanations."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=150,  
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        data = response.choices[0].message
        span.set_attribute('Code generation response', data)

    return [data]

async def main():
    async with AsyncClient() as client:
        deps = BuilderDeps(client=client)
        rdb = db.ResearchDatabase(db_path=db_path)

        today = datetime.now().strftime("%d-%m-%Y")
        results = rdb.conn.execute('SELECT topic FROM research WHERE date = ?', (today,)).fetchall()
        topics = [row[0] for row in results]

    
        for topic in topics:
            result = await example_builder_agent.run(f'Generate example app for {topic}', deps=deps)
            print(f'Example Project: {result.data.project_name}')
            print('Code Snippets:')
            for snippet in result.data.code_snippets:
                print(snippet)

if __name__ == '__main__':
    asyncio.run(main())
