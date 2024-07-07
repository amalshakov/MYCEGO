# MYCEGO
- Тестовое задание на позицию “Full-stack разработчик” в компанию MYCEGO.
- Требуется написать код который по запросу из списка папок, собирает картинки из папок в один tiff файл.
- ТЗ - [ссылка](https://docs.google.com/document/d/1trG5aoepQetWPNQjqy_boUwlkyu2twfXTIxSJqzARlo/edit)
- Стек (python, pillow)
- Клонируйте репозиторий
```
git clone git@github.com:amalshakov/MYCEGO.git
```
- Создайте и активируйте виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```
- Установите зависимости
```
pip install -r requirements.txt
```
- Запустите программу (например через терминал)
```
python main.py
```
### Описание
- Алгоритм принимает на вход список папок (input_folders) с файлами (картинками):
- Пример входных данных:
```
input_folders = [
    "C:/Dev/mycego/test_db/1369_12_Наклейки 3-D_3",
    "C:/Dev/mycego/test_db/1388_2_Наклейки 3-D_1",
    "C:/Dev/mycego/test_db/1388_6_Наклейки 3-D_2",
    "C:/Dev/mycego/test_db/1388_12_Наклейки 3-D_3",
]
```
### Автор:
- Александр Мальшаков (ТГ [@amalshakov](https://t.me/amalshakov), GitHub [amalshakov](https://github.com/amalshakov/))