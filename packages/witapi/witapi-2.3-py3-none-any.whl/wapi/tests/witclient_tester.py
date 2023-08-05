from wapi.main import WITClient
from wapi.tests import test_cfg


if __name__ == '__main__':
    wclient = WITClient(test_cfg.interla_ip, test_cfg.port, test_cfg.login, test_cfg.port)
    wclient.make_connection()
    response = wclient.make_auth()
    print(response)
