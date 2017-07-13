from django.test import TestCase

from db.course import Course


class CoursesTest(TestCase):
    def test_create_course(self):
        c = Course(name="python-best", code="p123456")
        _id = c.save()
        c = Course.get(_id)
        self.assertEqual(c.name, 'python-best', "Course name")
        self.assertEqual(c.code, "p123456", "Course code")
        c.delete()

    def test_delete_course(self):
        c = Course(name='deleted course', code='dummy code')
        _id = c.save()
        self.assertEqual(c.name, 'deleted course', "Course name")
        self.assertEqual(c.code, "dummy code", "Course code")
        c.delete()
        c = Course.get(id=_id)
        self.assertIsNone(c, "Delete course")

    def test_update_course(self):
        c = Course(name='new course', code='course code')
        _id = c.save()
        c = Course.get(id=_id)
        self.assertEqual(c.name, 'new course', "Course name")
        self.assertEqual(c.code, "course code", "Course code")
        c.name = "updated course name"
        c.code = "updated course code"
        c.update()
        c = Course.get(id=_id)
        self.assertEqual(c.name, 'updated course name', "Update course name")
        self.assertEqual(c.code, "updated course code", "Update course code")
        c.delete()

