"""
    This file is used to create tables in on output
"""

create_tables_commands = (
    """
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        role VARCHAR(255) NOT NULL,
        password VARCHAR(500) NOT NULL,
        created_at timestamp with time zone DEFAULT now()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS questions(
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        body text NOT NULL,
        created_at timestamp with time zone DEFAULT now(),
        FOREIGN KEY (user_id)
            REFERENCES users (id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS answers(
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        answer_body TEXT NOT NULL,
        accepted bool DEFAULT false,
        created_at timestamp with time zone DEFAULT now(),
        FOREIGN KEY (question_id)
            REFERENCES  questions (id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (user_id)
            REFERENCES users (id)
            ON UPDATE CASCADE ON DELETE CASCADE            
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS tokens (
       id SERIAL PRIMARY KEY,
       token VARCHAR(255),
       created_at timestamp with time zone DEFAULT now()
    )
    """
)

migrations = create_tables_commands
