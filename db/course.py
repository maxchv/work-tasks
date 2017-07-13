from db.base import BaseCrud


class Course(BaseCrud):
    # mysql procedures
    _insert = 'create_course'
    _delete = 'delete_course'
    _select = 'select_course_by_id'
    _select_all = 'select_courses'
    _update = 'update_course_by_id'
    _count = "courses_count"

    def __init__(self, **kwargs):
        self._id = kwargs.get("id")
        self._name = kwargs.get("name")
        self._code = kwargs.get("code")
        self._created = kwargs.get("created")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def created(self):
        return self._created

    def save(self, *args, **kwargs):
        super().save(self.name, self.code, None)
        return self.id

    def update(self, *args, **kwargs):
        super().update(self.id, self.name, self.code)

    def __str__(self):
        return "{} {} {}".format(self.id, self.name, self.code)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.code == other.code
