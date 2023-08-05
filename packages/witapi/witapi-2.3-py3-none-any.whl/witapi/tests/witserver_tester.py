from witapi.main import WITServer
from witapi.tests import test_cfg
from wsqluse.wsqluse import Wsqluse

if __name__ == '__main__':
    sqlhell = Wsqluse(test_cfg.db_name, test_cfg.db_user, test_cfg.db_pass, test_cfg.db_host)
    wserver = WITServer(test_cfg.external_ip, test_cfg.port, sqlshell=sqlhell, without_auth=False)
    wserver.launch_mainloop()


