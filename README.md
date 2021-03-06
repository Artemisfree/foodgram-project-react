# praktikum_new_diplom

## Описание
сайт Foodgram - «Продуктовый помощник». 
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное».
Перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.


## Технологии в проекте 
* Python
* Django Rest Framework

### Запуск проекта

Для начала убедитесь, что у вас установлен Docker командой:

```
docker -v
```

Клонируйте репозиторий и перейдите в него в командной строке


Перейдите в папку с проектом и создайте и активируйте виртуальное окружение:


```
source venv/Scripts/activate
```

```
python3 -m pip install --upgrade pip
```

Установите зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейдите в папку с файлом docker-compose.yaml:

```
cd infra
```

Разверните контейнеры:

```
docker-compose up -d --build
```

Выполните миграции, создайте суперпользователя, соберите статику:

```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
```

Создайте дамп (резервную копию) базы:

```
docker-compose exec web python manage.py dumpdata > fixtures.json
```
