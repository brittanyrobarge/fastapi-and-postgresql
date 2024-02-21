steps = [
    [
        ## Create the table
        """
        CREATE TABLE items (
            id SERIAL PRIMARY KEY NOT NULL,
            type VARCHAR(20) NOT NULL,
            name VARCHAR(1000) NOT NULL,
            cost VARCHAR(10) NOT NULL,
            measurement VARCHAR(10) NOT NULL,
            expiration_date DATE NOT NULL,
            store_name VARCHAR(50) NOT NULL
        );
        """,
        ## Drop the table
        """
        DROP TABLE items;
        """

    ]
]
