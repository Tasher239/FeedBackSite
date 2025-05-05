# FeedBackSite

Реализация формы обратной связи для сервисного портала на Django.

## Описание

Пользователь может:
- выбрать тип обращения (Пожелание, Проблема, Претензия, Другое)
- указать тему обращения
- описать суть обращения в текстовом поле
- прикрепить файл (опционально)

Сервер принимает данные, сохраняет в базу, загружает файл и возвращает подтверждение успешной отправки.

## Функциональность

- Модель `Feedback` с полями:
  - `request_type` (enum: wish, issue, claim, other)
  - `theme` (тема обращения)
  - `full_text` (текст обращения)
  - `file` (вложение, до 10 МБ)
  - `date` (дата создания)
- Форма `FeedbackForm` + валидация размера файла (макс 10 МБ).
- Endpoints:
  - список обращений: `feedback_list` (`/feedback/`)
  - создание нового обращения: `feedback_new_post` (`/feedback/new/`)
  - детальный просмотр: `FeedbackDetailView` (`/feedback/<pk>/`)
- Шаблоны на Bootstrap 5.

## Запуск

```bash
git clone <repo_url>
cd service_portal
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

