CREATE TABLE IF NOT EXISTS games (
    app_id INTEGER PRIMARY KEY,
    name VARCHAR(256),
    last_modified INTEGER,
    BOOLEAN has_acheievements DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS achievements (
    name TEXT NOT NULL,
    app_id INTEGER NOT NULL,
    display_name TEXT,
    description TEXT,
    icon_url VARCHAR(256),
    icon_url_gray VARCHAR(256),
    hidden BOOLEAN,
    PRIMARY KEY(name, app_id),
    CONSTRAINT fk_game FOREIGN KEY(app_id) REFERENCES games(app_id)
);

CREATE TABLE IF NOT EXISTS users (
    account_id INTEGER PRIMARY KEY,
    steam_id VARCHAR(32),
    profile_url VARCHAR(256),
    avatar_url VARCHAR(256),
    avatar_medium_url VARCHAR(256),
    avatar_full_url VARCHAR(256),
    last_log_off INTEGER,
    real_name VARCHAR(256),
    account_create TIMESTAMP WITH TIME ZONE,
    country_code VARCHAR(2)
);

CREATE TABLE IF NOT EXISTS games_users (
    account_id INTEGER NOT NULL,
    app_id INTEGER NOT NULL,
    PRIMARY KEY(account_id, app_id),
    CONSTRAINT fk_user FOREIGN KEY(account_id) REFERENCES users(account_id),
    CONSTRAINT fk_game FOREIGN KEY(app_id) REFERENCES games(app_id)
);

CREATE TABLE IF NOT EXISTS users_achievements (
    account_id INTEGER NOT NULL,
    achievement_name VARCHAR(256) NOT NULL,
    app_id INTEGER NOT NULL,
    unlock_time TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY(account_id, achievement_name),
    CONSTRAINT fk_user FOREIGN KEY(account_id) REFERENCES users(account_id),
    CONSTRAINT fk_achievement FOREIGN KEY(achievement_name, app_id) REFERENCES achievements(name, app_id)
);
