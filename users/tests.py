from django.test import TestCase

from db.course import Course
from db.user import User


class CoursesTest(TestCase):
    def test_create_user(self):
        u = User(name='Gary Busey', email='busey@mail.com', status='active')
        _id = u.save()
        self.assertIsNotNone(_id, 'User id')
        u = User.get(id=_id)
        self.assertEqual(u.name, 'Gary Busey', 'User name')
        self.assertEqual(u.email, 'busey@mail.com', 'User email')
        self.assertEqual(u.status, 'active', 'User status')
        u.delete()

    def test_delete_user(self):
        u = User(name='Jeff Bridges', email='bridges@mail.com', status='inactive')
        _id = u.save()
        self.assertIsNotNone(_id, 'User id')
        u.delete()
        u = User.get(id=_id)
        self.assertIsNone(u, "Delete user")

    def test_update_user(self):
        u = User(name="unknown", email="unknown@mail.com", status="inactive")
        _id = u.save()

        u = User.get(id=_id)
        self.assertEqual(u.name, 'unknown', 'User name')
        self.assertEqual(u.email, 'unknown@mail.com', 'User email')
        self.assertEqual(u.status, 'inactive', 'User status')

        u.name = 'Michael Cimino'
        u.update()
        u = User.get(id=_id)
        self.assertEqual(u.name, 'Michael Cimino', 'Update user name')
        self.assertEqual(u.email, 'unknown@mail.com', 'Update user email')
        self.assertEqual(u.status, 'inactive', 'Update user status')

        u.email = "cimino@mail.com"
        u.update()
        u = User.get(id=_id)
        self.assertEqual(u.name, 'Michael Cimino', 'Update user name')
        self.assertEqual(u.email, 'cimino@mail.com', 'Update user email')
        self.assertEqual(u.status, 'inactive', 'Update user status')

        u.status = 'active'
        u.update()
        u = User.get(id=_id)
        self.assertEqual(u.name, 'Michael Cimino', 'Update user name')
        self.assertEqual(u.email, 'cimino@mail.com', 'Update user email')
        self.assertEqual(u.status, 'active', 'Update user status')

        self.assertIsNone(u.phone, "User phone is not null")
        u.phone = '+380123456789'
        u.update()
        u = User.get(id=_id)
        self.assertEqual(u.phone, '+380123456789', 'Update user phone')

        self.assertIsNone(u.mobile_phone, "User mobile phone is not null")
        u.mobile_phone = '+389876543210'
        u.update()
        u = User.get(id=_id)
        self.assertEqual(u.mobile_phone, '+389876543210', 'Update user mobile phone')

    def test_added_category(self):
        u = User(name="unknown", email="unknown@mail.com", status="inactive")

        courses = [Course.get(1), Course.get(2), Course.get(3)]

        u.courses = courses

        _id = u.save()

        u = User.get(id=_id)
        self.assertEqual(len(u.courses), len(courses), "Count courses")
        self.assertEqual(u.courses, courses, "Saving courses")
        u.delete()

    def test_update_courses(self):
        u = User(name="unknown", email="unknown@mail.com", status="inactive")
        _id = u.save()
        u = User.get(_id)
        self.assertFalse(u.courses, "Courses count")
        courses = [Course.get(1), Course.get(2), Course.get(3)]
        u.courses = courses
        u.update()
        u = User.get(_id)
        self.assertTrue(u.courses, "Courses count")
        self.assertEqual(u.courses, courses, "Update courses")
        u.delete()

    def test_delete_courses(self):
        u = User(name="unknown", email="unknown@mail.com", status="inactive")
        _id = u.save()
        u = User.get(_id)
        self.assertFalse(u.courses, "Courses count")
        courses = [Course.get(1), Course.get(2), Course.get(3)]
        u.courses = courses
        u.update()
        u = User.get(_id)
        self.assertTrue(u.courses, "Courses count")
        self.assertEqual(u.courses, courses, "Update courses")
        courses = [Course.get(4),]
        u.courses = courses
        u.update()
        u = User.get(_id)
        self.assertTrue(u.courses, "Courses count")
        self.assertEqual(u.courses, courses, "Update courses")
        u.courses = []
        u.update()
        self.assertFalse(u.courses, "Delete courses")
        u.delete()





