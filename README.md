# Foodgram, «Продуктовый помощник»

[![Django-app workflow](https://github.com/Redrikh/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/Redrikh/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

***
Тестовый проект доступен по адресу: http://130.193.52.11/
***

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Используемые технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)

## Пользовательские роли

* Anonymous: Может просматривать главную страницу и рецепты.
* User: Может читать всё, как и Аноним. Может создавать рецепты, добавлять к ним теги и ингридиенты. Может добавлять рецепты в избранное, в корзину и подписываться на авторов рецептов. Эта роль присваивается по умолчанию каждому новому пользователю.
* Admin: Полные права на управление всем контентом проекта. Может создавать и удалять теги, ингридиенты, рецепты, пользователей. Может назначать роли пользователям
* Суперюзер Django: Обладет правами администратора


### Регистрация нового пользователя
* Отправить POST-запрос с параметрами email, username, first_name и lastname на эндпоинт /api/users/.
* Для изменения пароля нужно отправить на /api/users/set_password/
```
{
  "new_password": "string",
  "current_password": "string"
}
```

### Рецепты
* Для получения списка рецептов надо отправить GET-запрос на /api/recipes/
* Для создания рецепта нужно отправить POST-запрос на /api/recipes/
```
{
  "ingredients": [
    {
      "id": {int},
      "amount": {int}
    }
  ],
  "tags": [
    {tags}
  ],
  "image": "{image}",
  "name": "{string}",
  "text": "{string}",
  "cooking_time": {int}
}
```
* Для просмотра, удаления или изменения рецепта нужно отправить GET, DELETE или PATCH запрос на /api/recipes/{id}/

### Теги
* Для просмотра всех тегов нужно отправить GET-запрос на /api/tags/
* Для просмотра конкретного тега нужно отправить GET-запрос на /api/tags/{id}/

### Ингридиенты
* Для просмотра всех ингридиентов нужно отправить GET-запрос на /api/ingredients/
* Для просмотра конкретного ингридиента нужно отправить GET-запрос на /api/ingredients/{id}

### Список покупок
* Для просмотра списка покупок нужно отправить GET-запрос на /api/recipes/download_shopping_cart/
* Для добавления рецепта в список покупок нужно отправить POST-запрос на /api/recipes/{id}/shopping_cart/
* Для удаления рецепта из списка покупок нужно отправить DELETE-запрос на /api/recipes/{id}/shopping_cart/

### Избранное
* Для добавления рецепта в избранное нужно отправить POST-запрос на /api/recipes/{id}/favorite/
* Для удаления рецепта из избранного нужно отправить DELETE-запрос на /api/recipes/{id}/favorite/

### Подписки на авторов
* Для просмотра подписок нужно отправить GET-запрос на /api/users/subscriptions/
* Для подписки на автора нужно отправить POST-запрос на /api/users/{id}/subscribe/
* Для удаления подписки на автора нужно отправить DELETE-запрос на /api/users/{id}/subscribe/

## Автор
Скворцов Евгений
