# Описание Проекта: Solver Нонограмм Lunastory

Проект представляет собой автоматизированное решение нонограмм в мобильной игре Lunastory. Он использует компьютерное зрение для распознавания нонограмм и автоматического нажатия на клетки для их решения.

## Структура Проекта

1. `x_big_pictures_done.py` и `x_normal_done.py`:
   - Основные файлы, которые запускают процесс решения нонограмм.
   - Используют функции из других модулей для обнаружения пазлов, их решения и взаимодействия с экраном устройства.
   - Обрабатывает ошибки и печатает сообщения о переходе на следующий уровень.

2. `detect_cols.py`:
   - Содержит функцию `col_detector`, которая обнаруживает значения в колонках нонограммы.
   - Использует настройки OCR для распознавания чисел в обрезанных участках изображения.

3. `detect_rows.py`:
   - Функция `ptshp_image` выполняет предварительную обработку изображения для выделения цифр в строках нонограммы.
   - Применяет размытие и пороговое преобразование изображения для улучшения распознавания.
   - Содержит функцию `row_detector`, которая обнаруживает значения в колонках нонограммы.

4. `solve.py`:
   - Содержит функцию `solving`, которая формирует команды для автоматического нажатия на клетки нонограммы.
   - Использует команды ADB для отправки нажатий и ожидание между ними.
   - Перемешивает команды для избежания паттернов, которые могут запросить каптчу.

5. `x_big_pictures_done.py`:
   - Содержит функцию `main` для решения картин в режиме Big.
   - Обнаруживает уровни и решает нонограммы, используя функции из других модулей.
   - Навигирует между различными уровнями игры автоматически.

6. `x_normal_done.py`:
   - Содержит функцию `main` для обработки уровней в режиме Normal.
   - Обнаруживает круги для входа в выбор уровней, затем решает нонограммы.
   - Перемещается между уровнями, нажимая на соответствующие кнопки.

## Зависимости и Настройка

Для корректной работы проекта потребуется:
- Установка пакетов `opencv-python` и `pytesseract` для компьютерного зрения и распознавания текста.
- Наличие телефона Android и установленной туда игры Luna Story I [Luna Story I](https://play.google.com/store/apps/details?id=com.healingjjam.lunastory1)
- Настройка ADB (Android Debug Bridge) для взаимодействия с устройством.
- Наличие изображений и данных, используемых для распознавания нонограмм.

## Как Использовать

1. Запустите скрипт `x_big_pictures_done.py` или `x_normal_done.py`.
2. Убедитесь, что устройство подключено и ADB настроено.
3. Следите за выводом программы для отслеживания процесса решения.

## Заключение

Проект демонстрирует автоматизацию решения нонограмм в игре Lunastory, используя современные методы компьютерного зрения и автоматизации взаимодействия с устройствами.

## Пример использования

| DEMO Video |[![](http://markdown-videos-api.jorgenkh.no/youtube/Ief3IwF7r5I.gif)](https://youtu.be/Ief3IwF7r5I.gif)| <ul><li> Демонстрация прохождения уровней в режимах </li><li> NORMAL (10*10, 15*15, 20*20) </li><li> В режиме BIG (10*10, 20*20)  </li><li> (Видео ускорено в 3 раза) </li></ul>
|--|--|--|


Финальную картинку можете увидеть тут [![](screenshots/17,game_done.png)](screenshots/17,game_done.png)

## Требования

Необходимые пакеты Python можно установить с помощью следующей команды:

```sh
pip install -r requirements.txt
```

## Лицензия

Этот проект не требует лицензии, делайте с ним что хотите!