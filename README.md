Перед стартом необхідно налаштувати параметри з'єднання
з базою данних mysql у модулі testforyou/settings.py (див. словник DB_CONFIG)
та виконати скрипт users.sql, що лежить у теці sql.
База даних за замовчуванням testforyou.


ТЕХНІЧНІ ВИМОГИ ДО ЗАДАЧІ:

1) WEB Framework на твій вибір
   (**Django**/Flask/Tornado або будь-який інший)
2) Стандарти написання коду (**PEP8**)
3) НЕ використовувати ORM
4) База даних - **MySQL**
5) Доступ до даних має бути через **процедури**
6) Має бути присутній один скрипт (SQL) для
   створення бази даних, таблиць і процедур (базу
   назвати “Users”)
7) В межах проекту має бути реалізована
   **дворівнева структура** (Web рівень та рівень
   доступу до даних)
8) Має бути чітка і логічна організація класів
9) Буде плюсом реалізація **кешування**
