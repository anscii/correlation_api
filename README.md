# Tiny pet project to try FastAPI

## HOW TO
1. Забрать себе этот репозиторий
2. `docker-compose up --build` из каталога, куда склонировали репозиторий
3. Открыть <http://localhost:8000/docs#/> в браузере

## Данные
При сборке в бд будут добавлены тестовые данные:
- пользователь с id=1
- типы данных "steps" и "avg_hr"
- небольшое количество данных для этого пользователя
Получения рассчитанной корреляции по этим данным: <http://localhost:8000/correlation/?x_data_type=steps&y_data_type=avg_hr&user_id=1>

## API
### Добавление нового пользователя:
<http://localhost:8000/docs#/user/user_create_user_user__post>

или
```
curl -X 'POST' \
  'http://localhost:8000/user/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "new_user": {
    "name": "test user 2"
  }
}'
```

### Добавление нового типа данных:
<http://localhost:8000/docs#/data_type/datatype_create_data_type_data_type__post>

или
```
curl -X 'POST' \
  'http://localhost:8000/data_type/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "new_data_type": {
    "name": "hrv"
  }
}'
```

### Добавление/изменение данных пользователя:
<http://localhost:8000/docs#/user/user_store_data_calculate__post>

или
```
curl -X 'POST' \
  'http://localhost:8000/calculate/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 1,
  "data": {
    "x_data_type": "steps",
    "y_data_type": "avg_hr",
    "x": [
      {
        "date": "2022-01-07",
        "value": 10000
      }
    ],
    "y": [
      {
        "date": "2022-01-07",
        "value": 78.13
      }
    ]
  }
}'
```

### Получение рассчитанной корреляции
<http://localhost:8000/correlation/?x_data_type=steps&y_data_type=avg_hr&user_id=1>

или
```
curl -X 'GET' \
  'http://localhost:8000/correlation/?x_data_type=steps&y_data_type=avg_hr&user_id=1' \
  -H 'accept: application/json'
```

