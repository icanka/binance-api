DROP TABLE IF EXISTS webhooks;

DROP TABLE IF EXISTS user;

DROP TABLE IF EXISTS post;

CREATE TABLE
    webhooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        strategy_name TEXT NOT NULL,
        ticker TEXT NOT NULL,
        strategy_action TEXT NOT NULL,
        market_position TEXT NOT NULL,
        price TEXT NOT NULL,
        position_size TEXT NOT NULL,
        market_position_size TEXT NOT NULL,
        contracts TEXT NOT NULL,
        order_id TEXT NOT NULL
    );

CREATE TABLE
    user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );

CREATE TABLE
    post (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_id INTEGER NOT NULL,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        FOREIGN KEY (author_id) REFERENCES user (id)
    );