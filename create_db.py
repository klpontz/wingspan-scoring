import sqlite3

conn = sqlite3.connect('wingspan_scores.sqlite')
cur = conn.cursor()

cur.executescript('''
-- Users table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Expansions table
CREATE TABLE expansions (
    expansion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Game Sessions table
CREATE TABLE game_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_name VARCHAR(100) NOT NULL,
    description TEXT,
    num_players INTEGER NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Session Expansions table (many-to-many relationship between game_sessions and expansions)
CREATE TABLE session_expansions (
    session_expansion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    expansion_id INTEGER NOT NULL,
    FOREIGN KEY (session_id) REFERENCES game_sessions(session_id),
    FOREIGN KEY (expansion_id) REFERENCES expansions(expansion_id),
    UNIQUE(session_id, expansion_id)
);

-- User Game Sessions table
CREATE TABLE user_game_sessions (
    user_game_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    bird_points INTEGER NOT NULL,
    bonus_points INTEGER NOT NULL,
    end_of_round_points INTEGER NOT NULL,
    egg_points INTEGER NOT NULL,
    food_points INTEGER NOT NULL,
    tucked_points INTEGER NOT NULL,
    nectar_points INTEGER,
    total_points INTEGER NOT NULL GENERATED ALWAYS AS (
        bird_points + bonus_points + end_of_round_points + egg_points + food_points + tucked_points + nectar_points
    ) STORED,
    position INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (session_id) REFERENCES game_sessions(session_id)
);

-- Elo Ratings table
CREATE TABLE elo_ratings (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    rating INTEGER DEFAULT 1500,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (session_id) REFERENCES game_sessions(session_id),
    UNIQUE(user_id, session_id)
);

-- Indexes for faster queries
CREATE INDEX idx_user_game_sessions_session_user ON user_game_sessions(session_id, user_id);
CREATE INDEX idx_elo_ratings_user_session ON elo_ratings(user_id, session_id);
CREATE INDEX idx_game_sessions_game ON game_sessions(game_name);
CREATE INDEX idx_session_expansions_session_expansion ON session_expansions(session_id, expansion_id);
''')

cur.close()
conn.close()