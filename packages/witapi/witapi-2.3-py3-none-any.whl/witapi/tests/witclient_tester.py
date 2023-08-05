from witapi.main import WITClient
from witapi.tests import test_cfg


if __name__ == '__main__':
    wclient = WITClient(test_cfg.internal_ip, test_cfg.port, test_cfg.login, test_cfg.pw)
    wclient.make_connection()
    response = wclient.make_auth()
    print(response)
