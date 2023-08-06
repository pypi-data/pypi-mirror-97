import os
import time
from subprocess import run

from PySide2.QtCore import Slot
from PySide2.QtCore import Property
from PySide2.QtCore import QObject


class GitAnnex(QObject):
    
    autostart_config_path = "~/.config/git-annex/autostart"
    
    def get_url_filepath(self):
        with open(os.path.expanduser(self.autostart_config_path)) as config:
            repo_path = config.read().strip()
        return os.path.join(repo_path, ".git/annex/url")
    
    @Slot()
    def start(self):
        """
        Start

        We remove the url file and wait for it to reappear so that we can be
        sure the later file is the correct one.
        """
        url_filepath = self.get_url_filepath()
        print("starting git annex daemon")
        if os.path.exists(url_filepath):
            os.remove(url_filepath)
        run("git-annex assistant --autostart", shell=True)
        while not os.path.isfile(url_filepath):
            time.sleep(1)
    
    @Slot()
    def stop(self):
        print("stopping git annex daemon")
        run("git-annex assistant --autostop", shell=True)
    
    @Slot(result=str)
    def url(self):
        """
        Find the url to connect to assuming a single repo
        """
        with open(self.get_url_filepath()) as url_file:
            return url_file.read().strip()
