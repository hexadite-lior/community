# Copyright (C) 2012 Michael Boman (@mboman)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Based on information from http://antivirus.about.com/od/windowsbasics/tp/autostartkeys.htm

# Additional keys added from SysInternals Administrators Guide

from lib.cuckoo.common.abstracts import Signature

class Autorun(Signature):
    name = "persistence_autorun"
    description = "Installs itself for autorun at Windows startup"
    severity = 3
    categories = ["persistence"]
    authors = ["Michael Boman", "nex", "securitykitten"]
    minimum = "2.0"

    regkeys_re = [
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run$",
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\RunOnce$",
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\RunServices$",
        ".*\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\RunOnceEx$",
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\RunServicesOnce$",
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Windows\\ NT\\\\CurrentVersion\\\\Winlogon$",
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Windows\\ NT\\\\CurrentVersion\\\\Winlogon\\\\Notify$",
        ".*\\\\Software\\\\Microsoft\\\\Windows\\ NT\\\\CurrentVersion\\\\Winlogon\\\\Userinit$",
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Policies\\\\Explorer\\\\Run$",
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Active\\ Setup\\\\Installed Components\\\\.*",
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Windows\\ NT\\\\CurrentVersion\\\\Windows\\\\Appinit_Dlls.*",
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Explorer\\\\SharedTaskScheduler.*",
        ".*\\\\Software\\\\Microsoft\\\\Windows\\ NT\\\\CurrentVersion\\\\Image\\ File\\ Execution\\ Options.*",
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Windows\\ NT\\\\CurrentVersion\\\\Winlogon\\\\Shell$",
        ".*\\\\System\\\\CurrentControlSet\\\\Services.*",
        ".*\\\\SOFTWARE\\\\Classes\\\\Exefile\\\\Shell\\\\Open\\\\Command\\\\\\(Default\\).*",
        ".*\\\\Software\\\\Microsoft\\\\Windows NT\\\\CurrentVersion\\\\Windows\\\\load$",
        ".*\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\ShellServiceObjectDelayLoad$",
    ]

    files_re = [
        ".*\\\\win\.ini$",
        ".*\\\\system\\.ini$",
        ".*\\\\Start\\ Menu\\\\Programs\\\\Startup",
    ]

    def on_complete(self):
        for indicator in self.regkeys_re:
            regkey = self.check_key(pattern=indicator, regex=True, actions=["regkey_written"])
            if regkey:
                self.mark_ioc("registry", regkey)

        for indicator in self.files_re:
            filepath = self.check_file(pattern=indicator, regex=True, actions=["file_written"])
            if filepath:
                self.mark_ioc("file", filepath)

        return self.has_marks()
