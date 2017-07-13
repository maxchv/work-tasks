import pymysql.cursors
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ConnectDB(object):
    @staticmethod
    def get_connection():
        db_config = settings.DB_CONFIG
        db_config['cursorclass'] = pymysql.cursors.DictCursor
        return pymysql.connect(**db_config)


def ddl_proc(proc_name, new=False):
    def connect(func):
        def wraper(self, *args, **kwargs):
            conn = ConnectDB.get_connection()
            try:
                with conn.cursor() as cursor:
                    args = func(self, *args, **kwargs)
                    proc = getattr(self, proc_name)
                    if proc and args:
                        cursor.callproc(proc, args)
                        conn.commit()
                        if new:  # if it is new record
                            n = len(args) - 1  # id argument should be last
                            # select id new record
                            param = "@_{proc}_{n}".format(proc=proc, n=n)
                            cursor.execute('select {param}'.format(param=param))
                            res = cursor.fetchone()
                            self.id = res.get(param)
            except Exception as e:
                logger.error(e)
            finally:
                conn.close()

        return wraper

    return connect


class BaseCrud(object):
    """
    Base class to manage crud operation

    Derived class should have class variables:

    Each variable contains stored procedure to operate
    crud command, for instance:

    class Course(object):
        _insert = 'create_course'
        _delete = 'delete_course'
        _select = 'select_course_by_id'
        _select_all = 'select_courses'
        _update = 'update_course_by_id'
        _count  = "courses_count"
        ...

    >>> c = Course(name='курс', code='код')
    >>> c.save()
    >>> print(c.name)
    курс
    >>> c.code
    код
    >>> c.code = "code 7"
    >>> c.update()
    >>> id = c.id
    >>> c = Course.get(id)
    >>> c.code
    code 7
    >>> c.delete()
    >>> Course.get(id)
    None
    """

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @ddl_proc(proc_name='_delete')
    def delete(self):
        return self.id,

    @ddl_proc(proc_name='_insert', new=True)
    def save(self, *args):
        return args

    @ddl_proc(proc_name='_update')
    def update(self, *args):
        return args

    @classmethod
    def all(klass):
        proc = klass._select_all
        conn = ConnectDB.get_connection()
        _all = ()
        try:
            with conn.cursor() as cursor:
                cursor.callproc(proc)
                _all = cursor.fetchall()
        except Exception as e:
            logger.error(e)
        finally:
            conn.close()

        return (klass(**record) for record in _all)

    @classmethod
    def get(klass, id):
        proc = klass._select
        conn = ConnectDB.get_connection()
        record = {}
        try:
            with conn.cursor() as cursor:
                cursor.callproc(proc, (id,))
                record = cursor.fetchone()
        except Exception as e:
            logger.error(e)
        finally:
            conn.close()

        return klass(**record) if record else None

    @classmethod
    def count(klass):
        proc = klass._count
        conn = ConnectDB.get_connection()
        count = 0
        try:
            with conn.cursor() as cursor:
                cursor.callproc(proc, (None,))
                param = "@_{proc}_0".format(proc=proc)
                cursor.execute('select {param}'.format(param=param))
                res = cursor.fetchone()
                count = res.get(param)
        except Exception as e:
            logger.error(e)
        finally:
            conn.close()

        return count
