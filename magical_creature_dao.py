import mysql.connector
from interface_dao import DataAccessDAO
from magical_creature import MagicalCreature
from db_conn import DBConn

class MagicalCreatureDAO(DataAccessDAO):
    def __init__(self, db_conn: DBConn):
        self.db_conn=db_conn.connect_to_mysql()
        self.db_name=db_conn.get_data_base_name()

    def get(self, id: int) -> MagicalCreature:
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query= f"SELECT id, name, lives, magic_power FROM {self.db_name}.creatures WHERE id=%s"
                cursor.execute(query, ( id,))
                row = cursor.fetchone()
                if row:
                    return MagicalCreature(row[0], row[1], row[2], row[3])
                return None
            except mysql.connector.Error as err:
                raise err
            
    def get_all(self) -> list:
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query=f"SELECT id, name, lives, magic_power FROM {self.db_name}.creatures"
                cursor.execute(query, )
                rows = cursor.fetchall()
                return [MagicalCreature(row[0], row[1], row[2], row[3]) for row in rows]
            except mysql.connector.Error as err:
                print(err)

    def create(self, creature: MagicalCreature):
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query= f"INSERT INTO {self.db_name}.creatures (name, lives, magic_power) VALUES (%s, %s, %s)"
                cursor.execute(query, ( creature.name, creature.lives, creature.magic_power))
                conn.commit()
            except mysql.connector.Error as err:
                raise err

    def update(self, creature: MagicalCreature):
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query=f"UPDATE {self.db_name}.creatures SET name=%s, lives=%s, magic_power=%s WHERE id=%s"
                cursor.execute(query, ( creature.name, creature.lives, creature.magic_power, creature.lives))
                conn.commit()
            except mysql.connector.Error as err:
                raise err

    def delete(self, creature_id: int):
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query=f"DELETE FROM {self.db_name}.creatures WHERE id=%s"
                cursor.execute(query, (creature_id,))
                conn.commit()
            except mysql.connector.Error as err:
                raise err