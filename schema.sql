CREATE table if NOT EXISTS users
(
    email text NOT NULL PRIMARY KEY,
    name text NOT NULL,
    password text NOT NULL,
    avatar_url text NOT NULL,
    created_at INTEGER
);


CREATE table if NOT EXISTS ideas
(
    email text NOT NULL,
    id text PRIMARY KEY NOT NULL,
    content text NOT NULL,
    impact INTEGER NOT NULL,
    ease INTEGER NOT NULL,
    confidence INTEGER NOT NULL,
    average_score REAL NOT NULL,
    created_at INTEGER
);

CREATE table if NOT EXISTS revoked_tokens
(
    jti text NOT NULL
);