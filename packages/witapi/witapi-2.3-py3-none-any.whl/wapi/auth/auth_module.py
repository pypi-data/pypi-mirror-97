""" Модуль аутентификации пользователя. Аутенификаия проходит путем сравнения заданного логина/пароля (login/password)
с логином паролем, хранимыми в таблице tablename;
В таблице должны присутствовать поле <login_name> и <password_name>, задаваемые пользователем.
Для работы с БД используется служебный фреймворк WSQLuse (sqlhsell).
Так же передается словарь (conn_dict), в котором ключем является подключение к сокету (connection) а значением
еще один словарь с разными парами ключ-значение, в частности, ключ auth, принимающий True или False и отвечающий
на вопрос, аутентифицирован пользователь или нет. """
from wapi.auth import auth_settings as s


def auth_user(sqlshell, login, password, connection):
    response = auth_user_from_db(sqlshell, s.users_tablename, s.login_name, login, password)
    response = check_if_auth_succes(response)
    if response:
        ip = connection.getpeername()[0]
        user_id = save_conn_ip(sqlshell, s.users_tablename, s.login_name, login, ip)[0][0]
        print('Access granted! Got Id - ', user_id)
        return user_id, True
    else:
        print('Wrong password or login!')
        return 'Wrong password or login!', False

def set_disconnect_status(sqlshell, ip):
    print('Connection is ', ip)
    command = "UPDATE {} set connected=False where last_ip='{}'".format(s.users_tablename, ip)
    sqlshell.try_execute(command)

def save_conn_ip(sqlshell, tablename, login_name, login, ip):
    command = "UPDATE {} SET last_ip='{}', connected=True".format(tablename, ip)
    command += " where {}='{}'".format(login_name, login)
    user_id = sqlshell.try_execute(command)
    print('user_id', user_id)
    return user_id

def check_if_auth_succes(response):
    # Проверяет прошла аутентификация юзера в БД успешно
    try:
        response = response[0][0]
    except IndexError:
        response = None
    return response

def auth_user_from_db(sqlshell, tablename, login_name, login, password):
    # Аутентификация юзера, путем проверки в БД (через sqlshell) наличие логина (login) и совпадающего
    # пароля (password)
    command = "SELECT (password = crypt('{}', password)) ".format(password)
    command += "FROM {} ".format(tablename)
    command += "where {}='{}'".format(login_name, login)
    response = sqlshell.try_execute_get(command)
    return response
