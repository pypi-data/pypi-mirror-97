import pymysql
import logging
from datetime import date
import base64
import os

_sql_session = None
logger = logging.getLogger('netyce')


def sql_connect(host='127.0.0.1', port=3306, db='YCE', user='justread', password=None):
    """To set up the SQL connection

    Args:
        host: the IP or hostname of the node to connect to. ['127.0.0.1']
        port: [3306]
        db: default database to use. ['YCE']
        user: the user to connect with. ['justread']
        password: the password matching the user.

    Returns:
        the pymysql object
    """

    global _sql_session

    if _sql_session:
        return _sql_session

    password = password or base64.b64decode(os.environ.get(user))

    connection_dict = {
        'host': host,
        'user': user,
        'port': port,
        'password': password,
        'database': db,
    }
    connection = pymysql.connect(binary_prefix=True, **connection_dict)
    _sql_session = connection.cursor()
    return _sql_session


def sql_disconnect():
    global _sql_session
    if _sql_session:
        try:
            _sql_session.close()
        finally:
            _sql_session = None


def sql_query_one(query, **kwargs):
    """execute a query and read a single line of output

    Args:
        query: the query to be executed
        kwargs: args to pass to the sql_connect function

    Returns:
        the tuple fetched from the database

    """
    s = sql_connect(**kwargs)
    s.execute(query)
    return s.fetchone()


def sql_query_all(query, **kwargs):
    """execute a query and read all lines of output

    Args:
        query: the query to be executed
        kwargs: args to pass to the sql_connect function

    Returns:
        the tuple of tuples fetched from the database

    """
    s = sql_connect(**kwargs)
    s.execute(query)
    return s.fetchall()


def sql_query_many(query, size, **kwargs):
    """execute a query and read the desired amount of lines of output

    Args:
        query: the query to be executed
        size: the amount of lines to receive back
        kwargs: args to pass to the sql_connect function

    Returns:
        the tuple of tuples fetched from the database,
        limited on the amount of lines desired

    """
    s = sql_connect(**kwargs)
    s.execute(query)
    return s.fetchmany(size=size)


def init_log(file_level='WARNING', console_level='WARNING', logfile=None):
    """Initializes the logging for an output file and console.

    Args:
        file_level: One of the options: 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'
          Fallback value is 'WARNING'
        console_level: One of the options: 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'
          Fallback value is 'WARNING'
        logfile: Provide the complete path to store the logfile. Else cwd with a date.

    Returns:
        nothing.

    Raises:
        nothing.

    """

    global logger
    possible_levels = ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG')
    # should be the minimal to control the file and console handler
    # This is not used in another way, since no output is defined.
    logger.setLevel('DEBUG')

    if logfile:
        dir_logfile = os.path.dirname(logfile)
        if dir_logfile:
            os.makedirs(dir_logfile, exist_ok=True)
        path_logfile = logfile
    else:
        path = os.path.join(os.getcwd(), "logs")
        os.makedirs(path, exist_ok=True)
        path_logfile = '%s/%s.log' % (path, date.today())

    file_level = file_level.upper()
    console_level = console_level.upper()

    if file_level not in possible_levels:
        print("LOG LEVEL %r doesnt exist, Fallback is 'WARNING'" % file_level)
        file_level = "WARNING"

    if console_level not in possible_levels:
        print("LOG LEVEL %r doesnt exist, Fallback is 'WARNING'" % console_level)
        console_level = "WARNING"

    fh = logging.FileHandler('%s' % path_logfile)
    fh.setLevel(file_level)
    fh_formatter = logging.Formatter('%(asctime)s %(name)-12s - %(levelname)-8s - %(message)s',
                                     datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(fh_formatter)

    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    con_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    ch.setFormatter(con_formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("log path: %s" % path_logfile)
