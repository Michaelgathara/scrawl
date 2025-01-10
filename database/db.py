from typing import List
import sqlite3

class ResearchDatabase:
    def __init__(self, db_path: str = 'research_data.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                              CREATE TABLE IF NOT EXISTS research(
                                id INTEGER PRIMARY KEY,
                                topic TEXT,
                                date TEXT,
                                summary TEXT
                                )
                              ''')
    def save_results(self, topics: List[str], summaries: List[str]):
        with self.conn:
            self.conn.executemany(
                'INSERT INTO research (topic, summary) VALUES (?, ?)',
                zip(topics, summaries)
            )
    
    def close(self):
        self.conn.close()
        
class BrowserUseDatabase:
    def __init__(self, db_path: str = 'browser_use_data.db') -> None:
        self.conn = sqlite3.connect(db_path)
        self.create_table()
    
    def create_table(self):
        with self.conn:
            self.conn.execute('''
                              CREATE TABLE IF NOT EXISTS browser(
                                  id INTEGER PRIMARY KEY,
                                  visited_urls TEXT,
                                  screenshot_paths TEXT,
                                  action_names TEXT,
                                  errors TEXT,
                                  model_actions TEXT
                              )
                              ''')
    
    def save_results(self, visited_urls: List[str], screenshot_paths: List[str], action_names: List[str], errors: list, model_actions: List[dict]):
        # https://github.com/browser-use/browser-use/blob/main/browser_use/agent/views.py#L111 for the types.
        # TODO: check the types for errors
        
        with self.conn:
            self.conn.executemany(
                'INSERT INTO browser (visited_urls, screenshot_paths, action_names, errors, model_actions) VALUES (?, ?, ?, ?, ?)',
                zip(visited_urls, screenshot_paths, action_names, errors, model_actions)
            )
    
    def close(self):
        self.conn.close()
        