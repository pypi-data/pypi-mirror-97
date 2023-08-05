"""Package of client-server for using server`s api"""
import socket
import pickle
from traceback import format_exc
import threading
import pathlib
from time import sleep
from wsqluse.wsqluse import Wsqluse
from wapi.auth import auth_module as am
from wapi.errors import NoSQLshellSupplied


class WApi:
    """Super class for API (Server&Client)"""

    def __init__(self, debug=False):
        self.status_ready = True
        self.debug = debug
        print("WAPI DEBUG -", debug)

    def send_data(self, sock, data):
        """Отправить сериализированные данные на WServer"""
        self.show_print('\nОтправка данных.', data, debug=True)
        self.show_print('\tPickling...', debug=True)
        pickled_data = pickle.dumps(data)
        self.show_print('\tДанные упакованы. Блокировка сокета', )
        self.show_print('\tОтправка данных')
        sock.send(pickled_data)
        self.show_print('\tДанные были отправлены')

    def get_file_data(self, filename):
        """Получение содержимого файла"""
        self.show_print('\nОткрытие файла', debug=True)
        with open(filename, 'rb') as fobj:
            self.show_print('\tЧтение файла', debug=True)
            data = fobj.read()
            self.show_print('\tВозвращение содержимого', debug=True)
            return data

    def get_response(self, sock):
        """Получить, показать и вернуть ответ"""
        response = self.get_data(sock)
        self.show_print('\tПолучен ответ', response, debug=True)
        return response

    def get_data(self, sock, data_size=4096):
        """Получить данные из сокета, объемом data_size. Если размер передаваемого объекта больше dataSize, -
        функция собирает объект по частям, пока не соберет его весь и возвращает результат"""
        self.show_print('\nОжидаем данные')
        data = self.unpickle_data(sock, data_size)
        return data

    def unpickle_data(self, sock, data_size):
        """Собирает большие файлы в цикле"""
        data = []
        # print('\tБлокировка сокета')
        while True:
            print('\tЖдем данные')
            packet = sock.recv(data_size)
            if not packet:
                break
            data.append(packet)
            try:
                data_arr = pickle.loads(b"".join(data))
                return data_arr
            except pickle.UnpicklingError:
                print(format_exc())
            except:
                print(format_exc())

    def save_file(self, data, filename):
        """Сохранение заданного содержимого (data) в файл filename"""
        print('\n\tСохранение файла', filename)
        with open(filename, 'wb') as fobj:
            fobj.write(data)

    def get_filesend_command(self, filepath):
        """Отправляет указанный файл по указанному сокету. Использует модуль pathlib для нормализации путей"""
        filepath = pathlib.Path(filepath)
        # Прочитать файл и вернуть содержимое
        filedata = self.get_file_data(filepath)
        send_command = {'uploadData': {'filename': filepath.name, 'mainDataBody': filedata}}
        return send_command

    def make_str_tuple(self, msg):
        return ' '.join(map(str, msg))

    def show_print(self, *msg, debug=False):
        msg = self.make_str_tuple(msg)
        if debug and self.debug:
            print(msg)
        elif not debug:
            print(msg)


class WITClient(WApi):
    """Универсальный клиент для общения с API WServer"""
    def __init__(self, ip, port, login, password, debug='False'):
        super().__init__(debug=debug)
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password
        self.sock = socket.socket()

    def send_file(self, filepath):
        send_command = self.get_filesend_command(filepath)
        self.send_data(send_command)

    def send_data(self, data):
        super().send_data(self.sock, data)

    def auth_me(self):
        """Авторизовать клиента на сервере"""
        command = {'authMe': {'login': self.login, 'password': self.password}}
        super().send_data(self.sock, command)
        response = self.get_response(self.sock)
        return response

    def make_connection(self):
        """Создать соединение с WServer"""
        print('Making connection with WServer on {}:{}'.format(self.ip, self.port))
        self.sock.connect((self.ip, self.port))
        print('Succes. Connection has been established.')

    def make_auth(self):
        """Отправить данные для авторизации"""
        auth_command = {'authMe': {'login': self.login, 'password': self.password}}
        self.send_data(auth_command)
        self.auth_data = self.get_data(self.sock)
        return self.auth_data


class WITServer(WApi):
    """"Серверное API, создается на передаеваемом myip, myport и ждет клиентов. Клиентов обрабатывает в
    ассинхронном режиме. От клиентов ожидает данные вида:
        {'какая-то команда':{'какие то доп.ключи: 'какие то доп.значения'}
    Однако, он эти команды не исполняет, пока клиент не пройдет авторизацию (если только сервер не работает
    в режиме without_auth=True, тогда сервер выполняет команды клиента без аутентификации и авторизации."""

    def __init__(self, myip, myport, without_auth=False, mark_disconnect=True, debug=False, sqlshell = None):
        super().__init__(debug=debug)
        self.recieved_commands = []
        self.without_auth = without_auth
        self.mark_disconnect = mark_disconnect
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((myip, myport))
        self.connections = []
        self.server.listen(10)
        self.sqlshell = sqlshell
        self.my_ip = myip
        self.my_port = myport
        if not without_auth and not sqlshell:
            raise NoSQLshellSupplied

    def send_file(self, sock, filepath):
        send_command = self.get_filesend_command(filepath)
        self.send_data(sock, send_command)

    def launch_mainloop(self):
        """Слушает сокет, получив подключение вызывает параллельную обработку каждого соеднинения"""
        print('\nWaiting for new connections on {}:{}'.format(self.my_ip, self.my_port))
        while True:
            conn_dict = {}
            conn, addr = self.server.accept()
            # Добавить соединение (в виде ключа словаря) в список self.connections, для дальнейшей работы
            # self.without_auth = по умолчанию False, если при создании экз. WServer передать значение True, то
            # парольная авторизация для клиентов WClient будет не затребована.
            conn_dict[conn] = {'auth': self.without_auth}
            self.connections.append(conn_dict)
            print('\nGot a new connection! Dispatching...')
            threading.Thread(target=self.dispatcher, args=(conn, conn_dict)).start()

    def dispatcher(self, conn, conn_dict):
        """"Функция взаимодействия с сокетом, занятым каким либо подключением (conn). Вызывается параллельно основному
        потоку для достижения ассинхронности обрабатываемых подключений"""
        while True:
            ip = conn.getpeername()[0]
            print('\nЕсть клиент. Ip:', ip)
            try:
                print('\tWaiting for commands from client...')
                command = self.get_data(conn)
                if not command:
                    print('\t\tConnection was lost')
                    conn.close()
                    self.connections.remove(conn_dict)
                    if self.mark_disconnect and self.sqlshell:
                        am.set_disconnect_status(self.sqlshell, ip)
                    break
                print('\tПолучена команда:', command)
                # response = self.operate_command(conn_dict, command, conn)
                # self.send_response(conn, response)
                self.command_execute_queue(conn_dict, conn, command)
            except ConnectionResetError:
                print(format_exc())
                break

    def change_status(self, status_name, status):
        status_name = status

    def command_execute_queue(self, conn_dict, conn, command):
        while True:
            if self.status_ready:
                self.change_status(self.status_ready, False)
                response = self.operate_command(conn_dict, command, conn)
                self.send_response(conn, response)
                self.change_status(self.status_ready, True)
                break
            else:
                # print
                sleep(1)

    def send_response(self, conn, response):
        """Отправить ответ клиенту по получению от него комманды"""
        print('\nSending response', response)
        self.send_data(conn, response)

    def operate_command(self, conn_dict, command, connection):
        """Оперировать командой"""
        self.recieved_commands.append(command)
        response = self.check_auth(conn_dict, command, connection)
        return response

    def check_auth(self, conn_dict, command, connection):
        """Выполняет передававемую команду и возвращает ответ"""
        for comm, values in command.items():
            if conn_dict[connection]['auth']:
                response = self.execute_command(comm, values)
            else:
                if comm == 'authMe':
                    response, auth = am.auth_user(self.sqlshell, values['login'], values['password'], connection)
                    if auth:
                        conn_dict[connection]['auth'] = True
                else:
                    response = "Вы должны сначала авторизоваться! Комманда {'authMe':{'login':..., " \
                               "'password'=...}} "
            return response

    def execute_command(self, comm, values):
        self.show_print('Got command: {} with values {}'.format(comm, values), debug=True)
        return 'WITApi server execution is not realised yet!'

    def clear_recieved_commands(self):
        self.recieved_commands = []
