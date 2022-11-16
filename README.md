# museum_api

Первым делом после клонирования репозитория необходимо установить requirements.txt

linux:
  *папка проекта*
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  
В файле db.py в 4 строке нужно настроить данные для подключения к базе данных MySQL

API использует для работы сервер uvicorn (он есть в файле requirements.txt, устанавливать отдельно его не нужно)
Linux:
  *папка проекта*
  source venv/bin/activate
  uvicorn main:app --host *указываете хост* --port 80 *этот порт обязателен*
  
API запущен и готов принимать запросы
