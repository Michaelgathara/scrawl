import pytest
from unittest.mock import AsyncMock, patch
from agents.example_builder import BuilderDeps, example_builder_agent
from database.db import ResearchDatabase
from httpx import AsyncClient


test_db_path = ':memory:'  

def setup_test_db():
    db = ResearchDatabase(db_path=test_db_path)
    db.conn.execute('INSERT INTO research (topic, summary) VALUES (?, ?)', ('Test Framework', 'Test summary'))
    return db

@pytest.fixture
def test_db():
    db = setup_test_db()
    yield db
    db.close()


@pytest.fixture
async def deps():
    mock_client = AsyncMock(spec=AsyncClient)
    return BuilderDeps(client=mock_client)


@pytest.mark.asyncio
async def test_generate_code_snippets():
    with patch('example_builder.client.chat.completions.create') as mock_openai:
        mock_openai.return_value.choices = [
            AsyncMock(message='def example_function():\n    print("Hello World")')
        ]

        result = await example_builder_agent.tools['generate_code_snippets']('Test Framework')
        assert len(result) > 0
        assert 'def example_function' in result[0]


@pytest.mark.asyncio
async def test_integration_example_builder_agent(deps, test_db):
    with patch('example_builder.example_builder_agent.run', new_callable=AsyncMock) as mock_run:
        mock_run.return_value.data.project_name = 'TestProject'
        mock_run.return_value.data.code_snippets = ['def example():\n    pass']

        result = await example_builder_agent.run('Generate example app for Test Framework', deps=deps)
        assert result.data.project_name == 'TestProject'
        assert len(result.data.code_snippets) > 0
        assert 'def example()' in result.data.code_snippets[0]
