from typing import List
import sqlite3

class ResearchDatabase:
    def __init__(self, db_path, str = 'research_data.db'):
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
        