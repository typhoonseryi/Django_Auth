# Django_Auth
## Описание:
Требуется ограничить доступ к точке /api/v1/goods/ (POST) из предыдущего задания таким образом, чтобы к ней имели доступ только зарегистрированные пользователи с установленным флагом is_staff. Аутентификация должна проводиться по ключу, переданному в заголовке Authorization. Ключ должен быть строкой вида логин:пароль закодированной в base64. Другими словами, вам нужно реализовать HTTP Basic Auth для одной точки API. В случае если пользователь не имеет флага is_staff должен возвращаться пустой ответ со статусом 403. В случае если логин и/или пароль не валидны должен возвращаться пустой ответ со статусом 401.
