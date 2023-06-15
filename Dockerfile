# Установка базового образа
FROM python:3.10

# Установка переменной среды PYTHONUNBUFFERED в значение 1
ENV PYTHONUNBUFFERED 1

# Установка рабочей директории внутри контейнера
WORKDIR /code

# Копирование зависимостей в контейнер
COPY requirements.txt /code/

# Установка зависимостей
RUN pip install -r requirements.txt

# Копирование остальных файлов проекта в контейнер
COPY . /code/
COPY ./certs/root.crt /certs/

# Запуск команды для сборки статических файлов
RUN python manage.py collectstatic --noinput

# Определение порта, который будет прослушиваться контейнером
EXPOSE 8000

# Запуск команды для запуска сервера Django
CMD gunicorn youtube.wsgi:application --bind 0.0.0.0:8000