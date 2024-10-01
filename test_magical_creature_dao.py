import pytest
import configparser
import pathlib
import mysql.connector

from acceso_a_datos.dao.magical_creatures.magical_creature_dao import MagicalCreatureDAO
from magical_creature import MagicalCreature
from mysql.connector import errorcode

@pytest.fixture(scope="module")
def db_conn():
    config=configparser.ConfigParser()
    config_path = pathlib.Path(__file__).parent.absolute() / "test_config.ini"
    config.read(config_path)
    db_config= config['database']
    try: 
        conn= mysql.connector.connect(
            user=db_config.get('user'),
            password=db_config.get('password'),
            host=db_config.get('host'),
        )
          
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
    def test_get_success(self, db_conn):
       
        # Insertar un registro de prueba
        with db_conn.cursor() as cursor:
            cursor.execute("INSERT INTO test_creatures.creatures (name, lives, magic_power) VALUES ('Test Creature', 100, 50)")
            db_conn.commit()
            inserted_id = cursor.lastrowid

        dao = MagicalCreatureDAO('test_config.ini')
        result = dao.get(inserted_id)

        assert result is not None
        assert isinstance(result, MagicalCreature)
        assert result.id == inserted_id
        assert result.name == 'Test Creature'
        assert result.lives == 100
        assert result.magic_power == 50
    

