def create_tables():
    queries = [
        'CREATE TABLE IF NOT EXISTS users (\
                id SERIAL PRIMARY KEY,\
                username VARCHAR,\
                email VARCHAR,\
                role VARCHAR,\
                password VARCHAR\
                )',

        'CREATE TABLE IF NOT EXISTS questions (\
                id SERIAL PRIMARY KEY,\
                title VARCHAR(70),\
                description VARCHAR(500),\
                user_id INTEGER REFERENCES users (id) ON DELETE CASCADE,\
                date_created TIMESTAMP, \
                FOREIGN KEY (user_id) REFERENCES users (id)\
                )',
        'CREATE TABLE IF NOT EXISTS answers (\
                id SERIAL PRIMARY KEY,\
                user_id INTEGER REFERENCES users (id) ON DELETE CASCADE,\
                question_id INTEGER REFERENCES questions (id) ON DELETE CASCADE,\
                description VARCHAR(500),\
                accepted BOOLEAN DEFAULT FALSE, \
                date_created TIMESTAMP, \
                FOREIGN KEY (user_id) REFERENCES users (id), \
                FOREIGN KEY (question_id) REFERENCES questions (id)\
                )',

        'CREATE TABLE IF NOT EXISTS tokens (\
                token_id SERIAL PRIMARY KEY,\
                token VARCHAR(200)\
                )'

    ]

    return queries


def drop_tables():
    """deletes the existing tables from the database"""
    queries = (
        'DROP TABLE IF EXISTS users CASCADE;',
        'DROP TABLE IF EXISTS questions CASCADE;',
        'DROP TABLE IF EXISTS answers CASCADE;',
        'DROP TABLE IF EXISTS tokens;'
    )

    return queries