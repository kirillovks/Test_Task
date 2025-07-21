#!/bin/bash

LOGFILE="script.log"
echo "Скрипт запущен" >> "$LOGFILE"


# Проверка того, что аргумент передан
if [ -n "$1" ]; then
   echo "Аргумент передан" >> "$LOGFILE"
else
   echo "Ошибка: аргумент не передан" >> "$LOGFILE"
   exit 1
fi


# Проверка того, что аргумент - это директория
if [ -d "$1" ]; then
   echo "Аргумент '$1' является директорией" >> "$LOGFILE"
else
   echo "Ошибка: аргумент '$1' не является директорией" >> "$LOGFILE"
   exit 1
fi


# Проверяем наличие прав доступа к папке
if [ -r "$1" ]; then
    echo "Директория доступна для чтения" >> "$LOGFILE"
else
    echo "Ошибка: директория не доступна для чтения" >> "$LOGFILE"
    exit 1
fi


# Задаем переменные: путь к папке которую архивируем и название папки
FOLDER_PATH=$1
FOLDER_NAME=$(basename "$FOLDER_PATH")


# Создаем папку /backup, если ее еще нет
if [ -d "/backup" ]; then
    echo "Папка /backup уже существует" >> "$LOGFILE"
else
    mkdir /backup
    echo "Папка /backup создана" >> "$LOGFILE"
fi


# Проверяем, что архива с таким именем не существует
if [ -f "/backup/${FOLDER_NAME}.tar.gz" ]; then
    echo "Ошибка: этот архив уже существует" >> "$LOGFILE"
    exit 1
fi


# Создаем архив по имени папки и сохраняем его в /backup
tar czf "/backup/${FOLDER_NAME}.tar.gz" "$FOLDER_PATH"
echo "Архив /backup/${FOLDER_NAME}.tar.gz создан" >> "$LOGFILE"


# Удаляем архивы созданные более 7 дней назад
find /backup -name "*.tar.gz" -mtime +7 -delete
echo "Архивы созданные более 7 дней назад удалены" >> "$LOGFILE"


echo "Скрипт завершен" >> "$LOGFILE"
