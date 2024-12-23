from __future__ import annotations as _annotations

import asyncio, os

from dotenv import load_dotenv
load_dotenv()

from dataclasses import dataclass
from typing import List

from httpx import AsyncClient
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

import logfire
logfire.instrument_pydantic()
logfire.configure(send_to_logfire='if-token-present')

from devtools import debug

# local imports and database
from database import db
db_folder = os.path.join(os.path.dirname(__file__), '..', 'database')
db_path = os.path.join(db_folder, 'research_data.db')

@dataclass
class ResearchDeps:
    client: AsyncClient

class ResearchResult(BaseModel):
    topics: List[str] = Field(description='List of trending technologies or frameworks')
    summaries: List[str] = Field(description='Summaries of each trending technology')

research_agent = Agent(
    'openai:gpt-4o',
    deps_type=ResearchDeps,
    result_type=ResearchResult,
    system_prompt=(
        'You are a research assistant for AI developers. Identify trending technologies, AI models, and frameworks.'
        'Summarize each topic in a short paragraph highlighting key features and relevance.'
    ),
)

@research_agent.tool
async def fetch_github_trends(ctx: RunContext[ResearchDeps]) -> List[str]:
    """Fetch trending repositories from GitHub."""
    url = 'https://api.github.com/search/repositories?q=stars:>5000&sort=stars'
    with logfire.span('Calling tech news function') as span:
        response = await ctx.deps.client.get(url)
        response.raise_for_status()
        data = response.json()
        span.set_attribute('tech response ', data)

    return [repo['name'] for repo in data['items'][:10]]

@research_agent.tool
async def fetch_tech_news(ctx: RunContext[ResearchDeps]) -> List[str]:
    """Fetch trending tech news articles."""
    url = 'https://hn.algolia.com/api/v1/search?query=AI&tags=story'
    with logfire.span('Calling tech news function') as span:
        response = await ctx.deps.client.get(url)
        response.raise_for_status()
        data = response.json()
        span.set_attribute('tech response ', data)

    return [story['title'] for story in data['hits'][:10]]

@research_agent.tool
async def fetch_devto_articles(ctx: RunContext[ResearchDeps]) -> List[str]:
    """Fetch trends from Dev.to."""
    url = 'https://dev.to/api/articles?per_page=10&top=1'
    with logfire.span('Calling Dev.to function') as span:
        response = await ctx.deps.client.get(url)
        response.raise_for_status()
        data = response.json()
        span.set_attribute('dev to reponse ', data)
    
    return [article['title'] for article in data[:10]]

async def main():
    async with AsyncClient() as client:
        deps = ResearchDeps(client=client)
        rdb = db.ResearchDatabase(db_path=db_path)
        
        result = await research_agent.run('Find trending AI frameworks and tools.', deps=deps)

        rdb.save_results(result.data.topics, result.data.summaries)
        rdb.close()
        
        print('Trending Topics:', result.data.topics)
        print('Summaries:', result.data.summaries)

if __name__ == '__main__':
    asyncio.run(main())
