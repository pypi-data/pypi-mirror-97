# ============================
# Esquema que se utiliza para
# inicializar la base de datos
# ============================

instructions = [
    """
    CREATE TABLE class (
        name TEXT NOT NULL,
        teacher TEXT,
        link TEXT,
        PRIMARY KEY(name)
    )
    """,
    """
    CREATE TABLE bouquet (
        day INTEGER,
        hour INTEGER,
        minute INTEGER,
        class TEXT
    )
    """
]