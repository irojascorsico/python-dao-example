import mysql.connector
from mysql.connector import errorcode
from interface_dao import DataAccessDAO
from magical_creature import MagicalCreature
import configparser
import pathlib

class MagicalCreatureDAO(DataAccessDAO):
    def __init__(self, config_file):
        # Crear una instancia de ConfigParser
        self.config=configparser.ConfigParser()
        # Configurar la ruta 
        config_path = pathlib.Path(__file__).parent.absolute() / config_file
        # Leer el archivo
        self.config.read(config_path)
        # Definir una variable db_config que contiene los datos de la sección [database] del archivo.
        self.db_config=self.config['database']

    def get(self, id: int) -> MagicalCreature:
        with self.__connect_to_mysql() as conn:
            try:
                cursor = conn.cursor()
                query= "SELECT id, name, lives, magic_power FROM creatures WHERE id=%s"
                cursor.execute(query, (id,))
                row = cursor.fetchone()
                if row:
                    return MagicalCreature(row[0], row[1], row[2], row[3])
                return None
            except mysql.connector.Error as err:
                raise err
            
    def get_all(self) -> list:
        with self.__connect_to_mysql() as conn:
            try:
                cursor = conn.cursor()
                query="SELECT id, name, lives, magic_power FROM creatures"
                cursor.execute(query)
                rows = cursor.fetchall()
                return [MagicalCreature(row[0], row[1], row[2], row[3]) for row in rows]
            except mysql.connector.Error as err:
                print(err)

    def create(self, creature: MagicalCreature):
        with self.__connect_to_mysql() as conn:
            try:
                cursor = conn.cursor()
                query= "INSERT INTO creatures (name, lives, magic_power) VALUES (%s, %s, %s)"
                cursor.execute(query, (creature.name, creature.lives, creature.magic_power))
                conn.commit()
            except mysql.connector.Error as err:
                raise err

    def update(self, creature: MagicalCreature):
        with self.__connect_to_mysql() as conn:
            try:
                cursor = conn.cursor()
                query="UPDATE creatures SET name=%s, lives=%s, magic_power=%s WHERE id=%s"
                cursor.execute(query, (creature.name, creature.lives, creature.magic_power, creature.lives))
                conn.commit()
            except mysql.connector.Error as err:
                raise err

    def delete(self, creature_id: int):
        with self.__connect_to_mysql() as conn:
            try:
                cursor = conn.cursor()
                query="DELETE FROM creatures WHERE id=%s"
                cursor.execute(query, (creature_id,))
                conn.commit()
            except mysql.connector.Error as err:
                raise err

    def __connect_to_mysql(self):
        # Conectar a una base de datos MySQL Server
        try: 
            return mysql.connector.connect(
                user=self.db_config.get('user'),
                password=self.db_config.get('password'),
                host=self.db_config.get('host'),
                database=self.db_config.get('database')
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise("Usuario o Password no válido")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise("La base de datos no existe.")
            else:
                raise(err)
        return None