import sqlite3

conn = sqlite3.connect('wingspan_scores.sqlite')
cur = conn.cursor()

cur.executescript('''
CREATE TABLE games (
    game_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    num_players INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE game_sessions (
    session_id SERIAL PRIMARY KEY,
    game_id INTEGER NOT NULL REFERENCES games(game_id),
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_game FOREIGN KEY (game_id) REFERENCES games(game_id)
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_game_sessions (
    user_game_session_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    session_id INTEGER NOT NULL REFERENCES game_sessions(session_id),
    bird_points INTEGER NOT NULL,
    bonus_points INTEGER NOT NULL,
    end_of_round_points INTEGER NOT NULL,
    egg_points INTEGER NOT NULL,
    food_points INTEGER NOT NULL,
    tucked_points INTEGER NOT NULL,
    nectar_points INTEGER NOT NULL,
    total_points INTEGER NOT NULL GENERATED ALWAYS AS (
        bird_points + bonus_points + end_of_round_points + egg_points + food_points + tucked_points + nectar_points
    ) STORED,
    position INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, user_id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_session FOREIGN KEY (session_id) REFERENCES game_sessions(session_id)
);

CREATE TABLE elo_ratings (
    rating_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    game_id INTEGER NOT NULL REFERENCES games(game_id),
    rating INTEGER DEFAULT 1500,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, game_id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_game FOREIGN KEY (game_id) REFERENCES games(game_id)
);

CREATE INDEX idx_user_game_sessions_session_user ON user_game_sessions(session_id, user_id);
CREATE INDEX idx_elo_ratings_user_game ON elo_ratings(user_id, game_id);
CREATE INDEX idx_game_sessions_game ON game_sessions(game_id);
''')