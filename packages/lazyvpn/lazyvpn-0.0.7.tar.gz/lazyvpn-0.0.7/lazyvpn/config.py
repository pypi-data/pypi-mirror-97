"""
Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and* limitations under the License.*
"""
import argparse
import configparser
import getpass
import os
from typing import List

import keyring

from . import errors, ui

LAZY_VPN_KEYCHAIN_SERVICE_NAME = 'lazyvpn'
DEFAULT_VPN_REGION = [
    'ZillowGroup Seattle',
    'ZillowGroup Denver',
    'ZillowGroup Irvine',
    'ZillowGroup Cincinnati',
    'ZillowGroup Lincoln',
    'ZillowGroup New York',
    'ZillowGroup San Francisco',
]


class Config(object):
    """
       The Config Class gets the CLI arguments, writes out the okta config file,
       gets and returns username and password and the Okta API key.

       A lot of this code is modified from https://github.com/nimbusscale/okta_aws_login
       under the MIT license.
    """

    def __init__(self, gac_ui, create_config=True):
        """
        :type gac_ui: ui.UserInterface
        """
        self.ui = gac_ui
        self.FILE_ROOT = self.ui.HOME
        self.LAZYVPN_CONFIG = self.ui.environ.get('LAZYVPN_CONFIG', os.path.join(self.FILE_ROOT, '.lazyvpn_config'))

        self.conf_profile = 'DEFAULT'
        self.action_configure = False
        self.username = None
        self.company_vpn_region = None
        self.up = False
        self.down = False

        if create_config and not os.path.isfile(self.LAZYVPN_CONFIG):
            self.ui.notify('No lazy-vpn configuration file found, starting first-time configuration...')
            self.update_config_file()

    def get_args(self):
        """Get the CLI args"""
        parser = argparse.ArgumentParser(
            description="Create connection to VPN via Okta"
        )
        parser.add_argument('--profile', '-p', help='If set, the specified configuration profile will be used instead of the default.')
        parser.add_argument('--action-configure', '--configure', '-c', action='store_true', help="If set, will prompt user for configuration parameters and then exit.")
        parser.add_argument('--up', '-u', action='store_true', help='connect to vpn')
        parser.add_argument('--down', '-d', action='store_true', help='disconnect from vpn')
        args = parser.parse_args(self.ui.args)
        self.action_configure = args.action_configure
        self.conf_profile = args.profile or 'DEFAULT'
        if not self.action_configure and args.up == args.down:
            raise ValueError("Can't have both be UP and DOWN the same value")
        return args

    def _handle_config(self, config, profile_config, include_inherits=True):
        if "inherits" in profile_config.keys() and include_inherits:
            self.ui.message("Using inherited config: " + profile_config["inherits"])
            if profile_config["inherits"] not in config:
                raise errors.LazyVpnError(self.conf_profile + " inherits from " + profile_config["inherits"] + ", but could not find " + profile_config["inherits"])
            combined_config = {
                **self._handle_config(config, dict(config[profile_config["inherits"]])),
                **profile_config,
            }
            del combined_config["inherits"]
            return combined_config
        else:
            return profile_config

    def get_config_dict(self, include_inherits=True):
        """returns the conf dict from the okta config file"""
        # Check to see if config file exists, if not complain and exit
        # If config file does exist return config dict from file
        if os.path.isfile(self.LAZYVPN_CONFIG):
            config = configparser.ConfigParser()
            config.read(self.LAZYVPN_CONFIG)
            try:
                profile_config = dict(config[self.conf_profile])
                self.fail_if_profile_not_found(profile_config, self.conf_profile, config.default_section)
                return self._handle_config(config, profile_config, include_inherits)
            except KeyError:
                if self.action_configure:
                    return {}
                raise errors.LazyVpnError(
                    'Configuration profile not found! Use the --configure flag to generate the profile.')
            return config
        raise errors.LazyVpnError('Configuration file not found! Use the --configure flag to generate file.')

    def update_config_file(self):
        """
           Prompts user for config details for the okta_aws_login tool.
           Either updates existing config file or creates new one.
           Config Options:
                okta_username = Okta username
        """
        config = configparser.ConfigParser()
        if self.action_configure:
            self.conf_profile = self._get_conf_profile_name(self.conf_profile)

        defaults = {
            'okta_username': '',
            'company_vpn_region': DEFAULT_VPN_REGION[0]
        }

        # See if a config file already exists.
        # If so, use current values as defaults
        if os.path.isfile(self.LAZYVPN_CONFIG):
            config.read(self.LAZYVPN_CONFIG)
            if self.conf_profile in config:
                profile = config[self.conf_profile]
                for default in defaults:
                    defaults[default] = profile.get(default, defaults[default])

        # Prompt user for config details and store in config_dict
        config_dict = defaults
        config_dict['okta_username'] = self._get_okta_username(defaults['okta_username'])
        self.get_okta_password(config_dict['okta_username'])
        config_dict['company_vpn_region'] = self._get_company_vpn_region(DEFAULT_VPN_REGION)
        self.write_config_file(config_dict)

    def write_config_file(self, config_dict):
        config = configparser.ConfigParser()
        config.read(self.LAZYVPN_CONFIG)
        config[self.conf_profile] = config_dict
        # write out the conf file
        with open(self.LAZYVPN_CONFIG, 'w') as configfile:
            config.write(configfile)

    def _get_user_input_for_password(self, username, message):
        for x in range(0, 5):
            passwd_prompt = f"{message}: "
            password = getpass.getpass(prompt=passwd_prompt)
            if len(password) > 0:
                break
        # If the OS supports a keyring, offer to save the password
        if self.ui.input("Do you want to save this password in the keyring? (y/N) ") == 'y':
            try:
                keyring.set_password(
                    LAZY_VPN_KEYCHAIN_SERVICE_NAME, username, password)
                self.ui.info("Password for {} saved in keyring.".format(username))
            except RuntimeError as err:
                self.ui.warning("Failed to save password in keyring: " + str(err))
        return password

    def _get_user_input_with_default_value(self, message, default=None, hidden=False):
        """formats message to include default and then prompts user for input
        via keyboard with message. Returns user's input or if user doesn't
        enter input will return the default."""
        if default and default != '':
            prompt_message = message + " [{}]: ".format(default)
        else:
            prompt_message = message + ': '

        # print the prompt with print() rather than input() as input prompts on stderr
        user_input = self.ui.input(prompt_message, hidden)
        if user_input:
            return user_input
        return default

    def _get_user_input_with_predefined_list(self, message, default=[], hidden=False):
        """formats message to include default and then prompts user for input
        via keyboard with message. Returns user's input or if user doesn't
        enter input will return the default."""
        if default and len(default) > 0:
            prompt_message = message + ":\n"
            for index, entry in enumerate(default):
                prompt_message += f"{index} - {entry}\n"
        else:
            prompt_message = message + ': '

        # print the prompt with print() rather than input() as input prompts on stderr
        user_input = self.ui.input(prompt_message, hidden)
        if user_input:
            return default[int(user_input)]
        return default[0]

    def clean_up(self):
        """ clean up secret stuff"""
        del self.username

    def fail_if_profile_not_found(self, profile_config, conf_profile, default_section):
        """
        When a users profile does not have a profile named 'DEFAULT' configparser fails to throw
        an exception. This will raise an exception that handles this case and provide better messaging
        to the user why the failure occurred.
        Ensure that whichever profile is set as the default exists in the end users okta config
        """
        if not profile_config and conf_profile == default_section:
            raise errors.LazyVpnError(
                'DEFAULT profile is missing! This is profile is required when not using --profile')

    def _get_conf_profile_name(self, default_entry):
        """Get and validate configuration profile name. [Optional]"""
        ui.default.message(
            "If you'd like to assign the Okta configuration to a specific profile\n"
            "instead of to the default profile, specify the name of the profile.\n"
            "This is optional.")
        conf_profile = self._get_user_input_with_default_value(
            "Okta Configuration Profile Name", default_entry)
        return conf_profile

    def _get_okta_username(self, default_entry):
        """Get and validate okta username. [Optional]"""
        ui.default.message(
            "If you'd like to set your okta username in the config file, specify the username\n."
            "This is optional.")
        okta_username = self._get_user_input_with_default_value(
            "Okta User Name", default_entry)
        return okta_username

    def get_okta_password(self, okta_username):
        """Get and validate okta password. [Optional]"""
        ui.default.message(
            "Set Okta Password that will be used to connect to vpn")
        okta_password = self._get_user_input_for_password(
            okta_username, "Okta Pass Word")
        return okta_password

    def _get_company_vpn_region(self, default_list : List[str]):
        """ Get Okta AWS App name """
        ui.default.message(
            "Enter the VPN Region Name")
        company_vpn_region = self._get_user_input_with_predefined_list(
            "Please select VPN Region", default_list)
        return company_vpn_region
