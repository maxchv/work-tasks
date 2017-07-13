DROP DATABASE IF EXISTS testforyou;
CREATE DATABASE IF NOT EXISTS testforyou
  DEFAULT CHARACTER SET utf8;
USE testforyou;

--

CREATE TABLE IF NOT EXISTS courses
(
  id      INTEGER      NOT NULL PRIMARY KEY AUTO_INCREMENT,
  name    VARCHAR(100) NOT NULL UNIQUE,
  code    VARCHAR(100) NOT NULL,
  created TIMESTAMP
);

CREATE INDEX courses_name_index
  ON courses (name);

-- procedures for courses
DELIMITER $

CREATE PROCEDURE create_course(IN _name VARCHAR(100), IN _code VARCHAR(100), OUT _id INT)
  BEGIN
    INSERT INTO courses (name, code) VALUES (_name, _code);
    SET _id = LAST_INSERT_ID();
  END $

CREATE PROCEDURE delete_course(IN _id INT)
  BEGIN
    DELETE FROM courses
    WHERE id = _id;
  END $

CREATE PROCEDURE update_course_by_id(IN _id INT, IN _name VARCHAR(100), _code VARCHAR(100))
  BEGIN
    IF (SELECT name
        FROM courses
        WHERE id = _id) IS NOT NULL
    THEN
      UPDATE courses
      SET name = _name, code = _code
      WHERE id = _id;
    END IF;
  END $

CREATE PROCEDURE select_course_by_id(IN _id INT)
  BEGIN
    SELECT
      id,
      name,
      code
    FROM courses
    WHERE id = _id;
  END $

CREATE PROCEDURE select_courses()
  BEGIN
    SELECT *
    FROM courses;
  END $

CREATE PROCEDURE courses_count(OUT _count INT)
  BEGIN
    SET _count = (SELECT count(*)
                  FROM courses);
  END $

DELIMITER ;

CALL create_course('Python-Base', 'P012345', @id);
CALL create_course('Python-Database', 'P234567', @id);
CALL create_course('HTML', 'H345678', @id);
CALL create_course('Java-Base', 'J456789', @id);
CALL create_course('JavaScript-Base', 'JS543210', @id);
CALL create_course('test', 'test', @id);

CALL update_course_by_id(@id, 'Python-Advance', 'P9876543');

CALL select_course_by_id(@id);

--

CREATE TABLE IF NOT EXISTS users
(
  id           INTEGER                    NOT NULL PRIMARY KEY AUTO_INCREMENT,
  name         VARCHAR(100)               NOT NULL,
  phone        VARCHAR(100)               NULL,
  mobile_phone VARCHAR(100)               NULL,
  status       SET ('active', 'inactive') NOT NULL,
  created      TIMESTAMP,
  updated      DATETIME,
  email        VARCHAR(255)               NOT NULL
);

CREATE INDEX users_name_index
  ON users (name);

-- procedures for table users
DELIMITER $
CREATE PROCEDURE create_user(IN  _name         VARCHAR(100),
                             IN  _phone        VARCHAR(100),
                             IN  _mobile_phone VARCHAR(100),
                             IN  _status       SET ('active', 'inactive'),
                             IN  _email        VARCHAR(255),
                             OUT _id           INT)
  BEGIN
    INSERT INTO users (name, phone, mobile_phone, status, updated, email)
    VALUES (_name, _phone, _mobile_phone, _status, CURRENT_TIMESTAMP(), _email);
    SET _id = LAST_INSERT_ID();
  END $

CREATE PROCEDURE delete_user(IN _id INT)
  BEGIN
    DELETE FROM users
    WHERE id = _id;
  END $

CREATE PROCEDURE update_user_by_id(IN _id           INT,
                                   IN _name         VARCHAR(100),
                                   IN _phone        VARCHAR(100),
                                   IN _mobile_phone VARCHAR(100),
                                   IN _status       SET ('active', 'inactive'),
                                   IN _email        VARCHAR(255))
  BEGIN
    IF (SELECT name
        FROM users
        WHERE id = _id) IS NOT NULL
    THEN
      UPDATE users
      SET name = _name, phone = _phone, mobile_phone = _mobile_phone,
        status = _status, email = _email, updated = CURRENT_TIMESTAMP()
      WHERE id = _id;
    END IF;
  END $

CREATE PROCEDURE select_user_by_id(IN _id INT)
  BEGIN
    SELECT
      id,
      name,
      phone,
      mobile_phone,
      status,
      email
    FROM users
    WHERE id = _id;
  END $

CREATE PROCEDURE find_users_by_name(IN _name VARCHAR(100))
  BEGIN
    SELECT
      id,
      name,
      phone,
      mobile_phone,
      status,
      email
    FROM users
    WHERE name LIKE concat('%', _name, '%');
  END $

CREATE PROCEDURE select_users()
  BEGIN
    SELECT *
    FROM users;
  END $

CREATE PROCEDURE users_count(OUT _count INT)
  BEGIN
    SET _count = (SELECT count(*)
                  FROM users);
  END $

DELIMITER ;

CALL create_user('Gary Busey', NULL, NULL, 'active', 'busey@mail.com', @id);
CALL create_user('Jeff Bridges', NULL, NULL, 'inactive', 'birdges@mail.com', @id);
CALL create_user('Michael Cimino', NULL, NULL, 'active', 'cimion@mail.com', @id);
CALL create_user('Rodger Corman', NULL, NULL, 'active', 'corman@mail.com', @id);
CALL create_user('Don Rikles', NULL, NULL, 'inactive', 'don@mail.com', @id);
CALL create_user('Harold J Stone', NULL, NULL, 'active', 'harold@mail.com', @id);
CALL create_user('Bruno Dumont', NULL, NULL, 'active', 'bruno@mail.com', @id);
CALL create_user('Alane Delhaye', NULL, NULL, 'active', 'alane@mail.com', @id);
CALL create_user('Bernard Pruvost', NULL, NULL, 'active', 'bernard@mail.com', @id);
CALL create_user('Lucie Caron', '+1(123)123 12 13', '+1(321)321 32 21', 'active', 'caron@mail.com', @id);
CALL create_user('Philip Jore', NULL, NULL, 'inactive', 'jore@mail.com', @id);
CALL create_user('Robert Wiene', NULL, NULL, 'active', 'wiene@mail.com', @id);
CALL create_user('Werner Krauss', NULL, NULL, 'active', 'krauss@mail.com', @id);

--

CREATE TABLE IF NOT EXISTS users_courses
(
  id        INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  user_id   INTEGER NOT NULL,
  course_id INTEGER NOT NULL,
  CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES users (id)
    ON DELETE CASCADE,
  CONSTRAINT course_fk FOREIGN KEY (course_id) REFERENCES courses (id)
    ON DELETE CASCADE
);
CREATE UNIQUE INDEX users_courses_index_together
  ON users_courses (user_id, course_id);
CREATE INDEX users_courses_index_user
  ON users_courses (user_id);
CREATE INDEX users_courses_index_course
  ON users_courses (course_id);

--

DELIMITER $
CREATE PROCEDURE add_course_to_user(IN _user_id INT, IN _course_id INT)
  BEGIN
    IF _user_id IN (SELECT id
                    FROM users)
       AND _course_id IN (SELECT id
                          FROM courses)
       AND _course_id NOT IN (SELECT course_id
                              FROM users_courses
                              WHERE user_id = _user_id)
    THEN
      INSERT INTO users_courses (user_id, course_id) VALUES (_user_id, _course_id);
    END IF;
  END$
CREATE PROCEDURE remove_all_course_from_user(IN _user_id INT)
  BEGIN
    IF _user_id IN (SELECT user_id
                    FROM users_courses)
    THEN
      DELETE FROM users_courses
      WHERE user_id = _user_id;
    END IF;
  END$
CREATE PROCEDURE select_all_user_courses(IN _user_id INT)
  BEGIN
    IF _user_id IN (SELECT id
                    FROM users)
    THEN
      SELECT
        c.id,
        c.name,
        code,
        c.created
      FROM courses c
        JOIN users_courses uc
        JOIN users u
          ON u.id = uc.user_id AND c.id = uc.course_id
      WHERE u.id = _user_id;
    END IF;
  END$
DELIMITER ;


CALL add_course_to_user(1, 1);
CALL add_course_to_user(1, 2);
CALL add_course_to_user(1, 3);

CALL add_course_to_user(2, 2);
CALL add_course_to_user(2, 3);
CALL add_course_to_user(2, 4);

CALL add_course_to_user(3, 5);

