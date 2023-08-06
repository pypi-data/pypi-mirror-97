from subprocess import call

import keyring

from lazyvpn import errors, ui
from lazyvpn.config import Config, LAZY_VPN_KEYCHAIN_SERVICE_NAME


class LazyVpn(object):

    envvar_list = [
        'OKTA_PASSWORD',
        'OKTA_USERNAME',
    ]

    def _run(self):
        # Generate one-time login code using the secret key
        self.handle_action_configure()
        username = self.conf_arg_dict['okta_username']
        password = keyring.get_password(LAZY_VPN_KEYCHAIN_SERVICE_NAME, username)
        if not password:
            password = self.config.get_okta_password(username)
        company_vpn_region = self.conf_arg_dict['company_vpn_region']
        if self.conf_arg_dict['up']:
            call(['bash', '-c', f'printf "{username}\n{password}\n2"  | /opt/cisco/anyconnect/bin/vpn -s connect "{company_vpn_region}"'])
        elif self.conf_arg_dict['down']:
            call(['bash', '-c', '/opt/cisco/anyconnect/bin/vpn -s disconnect'])

    def __init__(self, ui=ui.cli):
        self.ui = ui
        self.FILE_ROOT = self.ui.HOME
        self._cache = {}

    def handle_action_configure(self):
        # Create/Update config when configure arg set
        if not self.config.action_configure:
            return
        self.config.update_config_file()
        raise errors.LazyVpnExitSuccess()

    def run(self):
        try:
            self._run()
        except errors.LazyVpnExitBase as exc:
            exc.handle()

    def generate_config(self):
        """ generates a new configuration and populates
        various config caches
        """
        self._cache['config'] = config = Config(gac_ui=self.ui)
        conf_arg_dict = config.get_config_dict()
        conf_arg_dict.update(config.get_args().__dict__)
        self._cache['conf_arg_dict'] = conf_arg_dict

        for value in self.envvar_list:
            if self.ui.environ.get(value):
                key = value.lower()
                self.conf_arg_dict[key] = self.ui.environ.get(value)

        return config

    @property
    def config(self):
        if 'config' in self._cache:
            return self._cache['config']
        config = self.generate_config()
        return config

    @property
    def conf_arg_dict(self):
        """
        :rtype: dict
        """
        # noinspection PyUnusedLocal
        config = self.config
        return self._cache['conf_arg_dict']


if __name__ == "__main__":
    lazy_vpn = LazyVpn().run()
