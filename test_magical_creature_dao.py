import pytest
import mysql.connector
from db_conn import DBConn

from magical_creature_dao import MagicalCreatureDAO
from magical_creature import MagicalCreature
from mysql.connector import errorcode

@pytest.fixture(scope="module")
def conn():
    db_conn=DBConn("test_config.ini")
    conn=db_conn.connect_to_mysql()

    try: 
          
        with conn.cursor() as cursor:
            # Crear la base de datos si no existe
            cursor.execute("CREATE DATABASE IF NOT EXISTS test_creatures")

            # Crear la tabla si no existe
            cursor.execute("CREATE TABLE IF NOT EXISTS test_creatures.creatures (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255), lives INT, magic_power INT)")
            
            # Borrar todas las filas 
            cursor.execute("DELETE FROM test_creatures.creatures")
        
        yield conn

        with conn.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS test_creatures")
            conn.close()   

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
             raise("Usuario o Password no válido")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise("La base de datos no existe.")
        else:
            raise(err)
    return None

class TestMagicalCreatureDao:
    def test_get_success(self, conn):
       
        # Insertar un registro de prueba
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO test_creatures.creatures (name, lives, magic_power) VALUES ('Test Creature', 100, 50)")
            conn.commit()
            inserted_id = cursor.lastrowid

        db_conn=DBConn("test_config.ini")
        dao = MagicalCreatureDAO(db_conn)
        result = dao.get(inserted_id)

        assert result is not None
        assert isinstance(result, MagicalCreature)
        assert result.id == inserted_id
        assert result.name == 'Test Creature'
        assert result.lives == 100
        assert result.magic_power == 50
    

