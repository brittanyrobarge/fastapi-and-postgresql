import os
from typing import List, Optional, Union
from psycopg_pool import ConnectionPool
from models.items import Error, ItemIn, ItemOut

DATABASE_URL = ConnectionPool(conninfo=os.environ["DATABASE_URL"])
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

pool = DATABASE_URL

class ItemRepository:
    def get_item(self, item_id: int) -> Optional[ItemOut]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT id,
                              type,
                              name,
                              cost,
                              measurement,
                              expiration_date,
                              store_name
                        FROM items
                        WHERE id = %s
                        """,
                        [item_id]
                    )
                    record = result.fetchone()
                    if record is None:
                        return None
                    return self.record_to_item_out(record)
        except:
            return {"message": f"Could not find that {item_id}"}

    def delete_item(self, item_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        DELETE FROM items
                        WHERE id = %s
                        """,
                        [item_id]
                    )
                    return (f"item {item_id} has succsefully been deleted")
        except:
            return (f"item {item_id} was not deleted")

    def update_inventory(self, item_id: int, item: ItemIn) -> Union[ItemOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        UPDATE items
                        SET type = %s,
                           name = %s,
                           cost = %s,
                           measurement = %s,
                           expiration_date = %s,
                           store_name = %s
                        WHERE id = %s
                        """,
                        [
                            item.type,
                            item.name,
                            item.cost,
                            item.measurement,
                            item.expiration_date,
                            item.store_name,
                            item_id
                        ]
                    )
                    return self.item_in_to_out(item_id, item)
        except:
            return {"message": f"Could not update {item.name}"}

    def get_all_items(self) -> Union[Error, List[ItemOut]]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT
                          id,
                          type,
                          name,
                          cost,
                          measurement,
                          expiration_date,
                          store_name
                        FROM items
                        ORDER BY id
                        """
                    )
                    return [
                        self.record_to_item_out(record)
                        for record in result
                    ]
        except:
            return {"message": "Could not retrive all items"}

    def add_item(self, item: ItemIn) -> Union[ItemOut, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO items(
                            type,
                            name,
                            cost,
                            measurement,
                            expiration_date,
                            store_name)
                        VALUES(
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s)
                        RETURNING (id, type, name, cost, measurement, expiration_date, store_name)
                        """,
                        [
                            item.type,
                            item.name,
                            item.cost,
                            item.measurement,
                            item.expiration_date,
                            item.store_name,
                        ]
                    )
                    id = result.fetchone()[0]
                    return self.item_in_to_out(id, item)
        except:
            return {"message": "could not add to fridge inventory."}

    def item_in_to_out(self, id: int, item: ItemIn):
        old_data = item.dict()
        return ItemOut(id=id, **old_data)

    def record_to_item_out(self, record):
        return ItemOut(
            id = record[0],
            type = record[1],
            name = record[2],
            cost = record[3],
            measurement = record[4],
            expiration_date = record[5],
            store_name = record[6],
        )
