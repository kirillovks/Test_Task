## REST API на Python с использованием FastAPI 
### (Преобразование цветных изображений в черно-белые)

Данный REST API сервис на базе FastAPI позволяет преобразовать ваше цветное PNG/JPEG изображение в черно-белое

---

## Установка и запуск

### 1. *Клонирование репозитория*
```bash
git clone https://github.com/kirillovks/Test_Task.git
cd RestAPI_Task
```

### 2. *Запуск с Docker / Docker Compose*

#### 2.1 Docker
1. Создайте .env файл с содержимым (из этого файла будет подтягиваться номер порта):
```bash
PORT={ваш порт}
```
2. Соберите Docker образ 
```bash
docker build -t {название контейнера} .
```
2. Запуск контейнера
```bash
docker run -d --name {название образа} --env-file .env --restart unless-stopped {название контейнера}
```

 - #### 2.2 Docker Compose

1. Создайте .env файл с содержимым (из этого файла будет подтягиваться номер порта):
```bash
PORT={номер порта}
```
2. Запустите Docker Compose сервисы 
```bash
docker-compose up -d
```

### 3. *Использование*

API будет доступно на `http://localhost:{ваш порт}`

Документация FastAPI: `http://localhost:{ваш порт}/docs`

---

### Документация API

POST /upload — загрузка изображения (file) во временную папку tmp/ (только форматы JPEG и PNG) размером до 5 Мб

Пример запроса:

```bash
curl -X POST -F "file=@image.jpg" http://localhost:{ваш порт}/upload
```

GET /process — применение черно-белого фильтра к последнему загруженному изображению и сохранение в папку images/ в формате PNG

Пример запроса:

```bash
curl -X GET http://localhost:{ваш порт}/process -OJ
```

---

### Содержание репозитория

Все запросы и ошибки логируются в *logs/api_image_filter.log*

В файле *requirements.txt* представлены все необходимые Python-библиотеки

Папка ***tmp/*** предназначена для временного хранения оригинальных изображений

В папке ***images/*** хранятся обработанные изображения
