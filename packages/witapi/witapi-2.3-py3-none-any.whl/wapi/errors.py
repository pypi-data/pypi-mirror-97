class NoSQLshellSupplied(Exception):
    def __init__(self):
        text = 'Внимание! Функцию аутентификации юзеров можно включать лишь тогда, когда WITServer передан ' \
               'объект wsqluse (фреймворк для работы с БД), а так-же должна быть правильно настроенна БД.' \
               'В противном случае, WITServer сможет работать только в режиме without_auth=True'
        super().__init__(text)
