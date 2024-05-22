# Проект: "YaMDb"
yamdb - это проект, который собирает оценки и коментарии под разные произведения. 'Api для yamdb' - полноценный интерфейс для обмена данными,  
расширяющий функционал yamdb.
---
## Навигация
* ### [Stack](#stack)
* ### [Realized opportunities](#realized-opportunities)
* ### [Resources API YaMDb](#resources-api-yamdb)
* ### [Launching the project](#launching-the-project-)
* ### [Docks](#docks-)
* ### [User registration algorithm](#user-registration-algorithm)
* ### [Development team](#development-team)

---

## Stack
* Python
* Django
* Rest-framework
* Pillow
* Djoser

---

## Realized opportunities:
* Неаутентифицированным пользователям доступно чтение.
* Аутентифицированным пользователям доступно чтение, ревью произведений и добавление изменений.
* Модератор так же имеет право удалять и редактировать отзывы и комментарии.
* Админ имеет полные права над управлением проекта.
* Суперпользователь имеет такие же права как и админ.

---

## Resources API YaMDb
**AUTH**: аутентификация.

**USERS**: пользователи.

**TITLES**: произведения, к которым пишут отзывы.

**CATEGORIES**: категории произведений ('Фильмы', 'Книги', 'Музыка').

**GENRES**: жанры произведений.

**REVIEWS**: отзывы на произведения.

**COMMENTS**: комментарии к отзывам.

---

## Launching the project: 
 
Клонировать репозиторий и перейти в него в командной строке: 
 
```commandline
git clone https://github.com/diriabin/api_yamdb
``` 
 
```commandline
cd api_yamdb
``` 
 
Cоздать и активировать виртуальное окружение: 
 
```commandline 
python -m venv venv 
``` 
 
```commandline
source venv/scripts/activate 
``` 
 
Установить зависимости из файла requirements.txt: 
 
```commandline
pip install -r requirements.txt 
``` 
 
Выполнить миграции: 
 
```commandline
python manage.py migrate 
``` 
 
Запустить проект: 
 
``` commandline
python manage.py runserver 
``` 

---

## Docks 

[Документация](http://127.0.0.1:8000/redoc/) в которой описано, как должен работать API. 
Документация представлена в формате Redoc.

---

# User registration algorithm
Пользователь отправляет POST-запрос с параметром email на `/api/v1/auth/email/`.
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email (функция в разработке).
Пользователь отправляет POST-запрос с параметрами email и confirmation_code на `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
Эти операции выполняются один раз, при регистрации пользователя. В результате пользователь получает токен и может работать с API, отправляя этот токен с каждым запросом.

---

## Development team
* ### **Diriabin Artem**
  * github: https://github.com/diriabin
* ### **Porkulevich Semyon**
  * github: https://github.com/sadd9d9
* ### **Maslenko Nikita**
  * github: https://github.com/nickita0098
