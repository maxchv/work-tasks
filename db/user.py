from db.base import BaseCrud, ConnectDB
import logging

from db.course import Course

logger = logging.getLogger(__name__)


class User(BaseCrud):
    # mysql procedures
    _insert = 'create_user'
    _delete = 'delete_user'
    _select = 'select_user_by_id'
    _select_all = 'select_users'
    _update = 'update_user_by_id'
    _count = "users_count"
    _find = 'find_users_by_name'

    def __init__(self, **kwargs):
        self._id = kwargs.get("id")
        self._name = kwargs.get("name")
        self._phone = kwargs.get("phone")
        self._mobile_phone = kwargs.get("mobile_phone")
        self._status = kwargs.get('status')
        self._email = kwargs.get('email')
        self._created = kwargs.get('created')
        self._updated = kwargs.get('updated')
        self._courses = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    @property
    def mobile_phone(self):
        return self._mobile_phone

    @mobile_phone.setter
    def mobile_phone(self, value):
        self._mobile_phone = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value if value in ('active', 'inactive') else 'inactive'

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def created(self):
        return self._created

    @property
    def updated(self):
        return self._updated

    def __load_course(self):
        if self.id:
            proc = "select_all_user_courses"
            conn = ConnectDB.get_connection()
            _all = {}
            try:
                with conn.cursor() as cursor:
                    cursor.callproc(proc, (self.id,))
                    _all = cursor.fetchall()
            except Exception as e:
                logger.error(e)
            finally:
                conn.close()
            self._courses = [Course(**record) for record in _all]

    @property
    def courses(self):
        if not self._courses:  # lazy load
            self.__load_course()
        return self._courses

    @courses.setter
    def courses(self, value):
        # FIXME: make custom list
        self._courses = value

    def __update_courses(self):
        self.__clear_courses()
        proc = "add_course_to_user"
        conn = ConnectDB.get_connection()
        for c in self.courses:
            try:
                with conn.cursor() as cursor:
                    cursor.callproc(proc, (self.id, c.id))
                    conn.commit()
            except Exception as e:
                logger.error(e)
        conn.close()

    def __clear_courses(self):
        proc = "remove_all_course_from_user"
        conn = ConnectDB.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc(proc, (self.id,))
                conn.commit()
        except Exception as e:
            logger.error(e)
        finally:
            conn.close()

    @classmethod
    def filter(cls, **kwargs):
        username = kwargs.get('name')
        if username is None:
            raise Exception('Filter accept only name')
        proc = cls._find
        conn = ConnectDB.get_connection()
        _all = {}
        try:
            with conn.cursor() as cursor:
                cursor.callproc(proc, (username,))
                _all = cursor.fetchall()
        except Exception as e:
            logger.error(e)
        finally:
            conn.close()

        return (cls(**record) for record in _all)

    def save(self, *args, **kwargs):
        super().save(self.name, self.phone, self.mobile_phone, self.status, self.email, self.id)
        self.__update_courses()
        return self.id

    def update(self, *args, **kwargs):
        super().update(self.id, self.name, self.phone, self.mobile_phone, self.status, self.email)
        self.__update_courses()

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.id, self.name, self.phone,
                                          self.mobile_phone, self.status, self.email)

    def __repr__(self):
        return self.__str__()


