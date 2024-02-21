steps = [
    [
        # "Up" SQL statement
        """
        ALTER TABLE items
        ADD user_id integer NOT NULL DEFAULT(1) REFERENCES accounts(id);
        """,
        # "Down" SQL statement
        """
        DROP COLUMN user_id;
        """
    ],
]
