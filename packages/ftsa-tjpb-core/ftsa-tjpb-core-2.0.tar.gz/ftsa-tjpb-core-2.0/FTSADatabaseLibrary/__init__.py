from DatabaseLibrary import DatabaseLibrary

from ftsa.core.properties import VERSION
from robot.api import logger


class FTSADatabaseLibrary(DatabaseLibrary):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        DatabaseLibrary.__init__(self)

    def _execute(self, query):
        logger.info(f'Executing SQL query string: {query}')
        output = super().execute_sql_string(query)
        logger.info(f'Result: {output}')
        return output

    def create_table(self, table_structure):
        """*FTSA Create Table in the Database*

        FTSA creates the table with the ``table_structure``.

        _Example:_
        | CREATE TABLE | ``table_structure=`` person(id integer, first_name varchar(40), last_name varchar(40)) |

        """
        return self._execute(f'CREATE TABLE {table_structure}')

    def drop_table(self, table_name):
        """*FTSA Drop Table in the Database*

        FTSA drops the table with the ``table_name``.

        _Example:_
        | DROP TABLE | ``table_name=`` person |

        """
        return self._execute(f'DROP TABLE {table_name}')

    def insert(self, table_name=None, values=None, script_file_name=None):
        """*FTSA Insert into Database*

        FTSA inserts to the database ``table_name`` some ``values``
        OR uses a ``script_file_name`` to perform it.

        _Examples:_
        | INSERT | ``table_name=`` person | ``values=`` (101, Joao, Goes) |
        | INSERT | ``script=`` insert_persons.sql | |

        """
        if script_file_name is not None:
            logger.info(f'Executing SQL query file: {script_file_name}')
            return self.execute_sql_script(sqlScriptFileName=script_file_name)
        else:
            return self._execute(f'INSERT INTO {table_name} VALUES {values}')

    def update(self, table_name=None, values=None, where=None, script_file_name=None):
        """*FTSA Update set to Database*

        FTSA updates to the database ``table_name`` some ``values`` with the given ``where`` condition
        OR uses a ``script_file_name`` to perform it.

        _Examples:_
        | UPDATE | ``table_name=`` person | ``values=`` (first_name='Jonas', last_name='Silva') | ``where=`` id=101 |
        | UPDATE | ``script=`` update_persons.sql | | |

        """
        if script_file_name is not None:
            logger.info(f'Executing SQL query file: {script_file_name}')
            return self.execute_sql_script(sqlScriptFileName=script_file_name)
        else:
            return self._execute(f'UPDATE {table_name} SET {values} WHERE {where}')

    def delete(self, table_name=None, where=None, script_file_name=None):
        """*FTSA Delete from Database*

        FTSA deletes from database ``table_name`` with the given ``where`` condition
        OR uses a ``script_file_name`` to perform it.

        _Examples:_
        | DELETE | ``table_name=`` person | ``where=`` id=101 |
        | DELETE | ``script=`` delete_persons.sql |  |

        """
        if script_file_name is not None:
            logger.info(f'Executing SQL query file: {script_file_name}')
            return self.execute_sql_script(sqlScriptFileName=script_file_name)
        else:
            return self._execute(f'DELETE FROM {table_name} WHERE {where}')

    def select(self, columns="*", table_name=None, where=None, script_file_name=None):
        """*FTSA Select from Database*

        FTSA selects columns ``columns`` from database ``table_name`` with the given ``where`` condition
        OR uses a ``script_file_name`` to perform it.

        _Examples:_
        | @{results} | SELECT | ``columns=`` * | ``table_name=`` person | ``where=`` first_name='Jonas' |
        | @{results} | SELECT | ``script=`` read_persons.sql |  |  |
        """
        if script_file_name is not None:
            logger.info(f'Executing SQL query file: {script_file_name}')
            return self.execute_sql_script(sqlScriptFileName=script_file_name)
        else:
            if where is None:
                return self.query(f'SELECT {columns} FROM {table_name}')
            else:
                return self.query(f'SELECT {columns} FROM {table_name} WHERE {where}')
