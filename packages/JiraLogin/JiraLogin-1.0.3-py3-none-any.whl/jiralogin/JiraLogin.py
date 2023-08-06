import getpass
import base64
import os
from jira import JIRA


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


class JiraLogin:
    def __init__(self, server):
        self.server = server
        if self.server[-1] == "/":
            self.server = self.server[:-1]
        self.__file_name = str(self.server).split("//")[1] + '.txt'
        self.path = (os.getenv('APPDATA') + "\\Jira\\")
        self.username = None
        self.__password = None

    def __create_local_credentials(self):
        """
        If the user hasn't signed into a specific server before or are receiving a 401, they will need to re-enter their
        credentials. This info is stored locally so that it can be easily retrieved for future use, however the password
        has been encoded as a minor obfuscation tactic (primarily to prevent people peering over your shoulder from
        seeing your password in plain text).
        """
        try:
            cls()
            if not os.path.exists(self.path):
                os.makedirs(self.path)

            print('Please enter your Jira (OneLogin) credentials for the follow database - ' + self.server +
                  '\n\nNote that you cannot paste your password and must manually enter it.')
            self.username = input("Username - ")
            self.__password = getpass.getpass("Password (characters hidden) - ")
            obfuscated_password = base64.b64encode(self.__password.encode("utf-8"))

            txt = open(self.path + self.__file_name, 'w+')
            txt.write(self.username + '\n' + obfuscated_password.decode('utf-8'))
            txt.close()
            cls()

            print('Signing into Jira...')
            self.__sign_in()

        except Exception as ex:
            input(str(ex) + "\n\n Press [Enter] to continue.")

    def __read_local_credentials(self):
        """
        Read the users stored username and password for the server. If none is found, use the above method to
        create them.
        """
        try:
            if not os.path.exists(self.path + self.__file_name):
                self.__create_local_credentials()

            with open(self.path + self.__file_name, 'r') as t:
                login_data = t.readlines()

            i = 0
            for line in login_data:
                if i == 0:
                    self.username = line.rstrip()
                if i == 1:
                    self.__password = base64.b64decode(line.encode('utf-8')).decode('utf-8')
                i += 1
            self.__sign_in()

        except Exception as ex:
            input(str(ex) + "\n\n Press [Enter] to continue.")

    def __sign_in(self):
        """
        Try signing in after receiving the users credentials for a specific server. If it fails, showcase a reasoning
        and have them sign in again.
        """
        try:
            options = {'server': self.server}
            self.__jira = JIRA(options, basic_auth=(self.username, self.__password), max_retries=1)

        except Exception as ex:
            print(str(ex))
            if 'JiraError HTTP 401' in str(ex):
                cls()
                input("\n'Unauthorized' error received from Jira, please re-enter your credentials."
                      "\n\nPress [Enter] to continue.")
                self.__create_local_credentials()
            elif 'CAPTCHA_CHALLENGE' in str(ex):
                cls()
                input('\n Too may failed login attempts, a Captcha challenge is now required to sign in. Manually'
                      ' log out then back into Jira (' + self.server + ') via any web browser, then re-enter your'
                      ' credentials.\n\nPress [Enter] to continue.')
                self.__create_local_credentials()
            else:
                input('\nSign in failed due to an unknown issue. Review the above error with Mason for assistance'
                      '\n\nPress [Enter] to re-enter credentials.')
                self.__create_local_credentials()

    def login(self):
        """
        :return: Jira object from the jira module which can be used to interact with your instance
        """
        print("Signing into Jira...")
        self.__read_local_credentials()
        del self.__password
        cls()
        return self.__jira
