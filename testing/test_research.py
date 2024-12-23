import pytest
import sqlite3
from unittest.mock import AsyncMock, patch
from agents.research import ResearchDeps, research_agent
from database.db import ResearchDatabase
from httpx import AsyncClient

test_db_path = ':memory:'  

def setup_test_db():
    db = ResearchDatabase(db_path=test_db_path)
    return db

@pytest.fixture
def test_db():
    db = setup_test_db()
    yield db
    db.close()

@pytest.fixture
async def deps():
    mock_client = AsyncMock(spec=AsyncClient)
    return ResearchDeps(client=mock_client)

@pytest.mark.asyncio
async def test_fetch_github_trends(deps):
    mock_response = {
        'items': [{'name': 'Repo1'}, {'name': 'Repo2'}]
    }
    deps.client.get = AsyncMock(return_value=AsyncMock(json=AsyncMock(return_value=mock_response)))
    result = await research_agent.tool['fetch_github_trends'](deps, {})
    assert result == ['Repo1', 'Repo2']

@pytest.mark.asyncio
async def test_fetch_tech_news(deps):
    mock_response = {
        'hits': [{'title': 'News1'}, {'title': 'News2'}]
    }
    deps.client.get = AsyncMock(return_value=AsyncMock(json=AsyncMock(return_value=mock_response)))
    result = await research_agent.tool['fetch_tech_news'](deps, {})
    assert result == ['News1', 'News2']

@pytest.mark.asyncio
async def test_fetch_devto_articles(deps):
    mock_response = [{'title': 'Article1'}, {'title': 'Article2'}]
    deps.client.get = AsyncMock(return_value=AsyncMock(json=AsyncMock(return_value=mock_response)))
    result = await research_agent.tool['fetch_devto_articles'](deps, {})
    assert result == ['Article1', 'Article2']

@pytest.mark.asyncio
async def test_integration_research_agent(deps, test_db):
    with patch('research.research_agent.run', new_callable=AsyncMock) as mock_run:
        mock_run.return_value.data.topics = ['AI Framework']
        mock_run.return_value.data.summaries = ['Summary of AI Framework']

        result = await research_agent.run('Find trending AI frameworks and tools.', deps=deps)
        test_db.save_results(result.data.topics, result.data.summaries)

        rows = test_db.conn.execute('SELECT * FROM research').fetchall()
        assert len(rows) == 1
        assert rows[0][1] == 'AI Framework'
        assert rows[0][2] == 'Summary of AI Framework'

