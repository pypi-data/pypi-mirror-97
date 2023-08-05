from wapi.main import WITServer
from wapi.tests import test_cfg


if __name__ == '__main__':
    wserver = WITServer(test_cfg.external_ip, test_cfg.port, without_auth=True)
    wserver.launch_mainloop()


