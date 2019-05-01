import os
import logging
import pandas as pd
import subprocess
import pwd
import subprocess
import sys
from datetime import datetime

logger = logging.getLogger("ignis")


def demote(user_uid, user_gid):
    def result():
        print("starting demotion")
        os.setgid(user_gid)
        os.setuid(user_uid)
        print("finished demotion")

    return result


class DatasetResolver(object):
    def __init__(self, file):
        self.file = file

    def get_meta_data(self):
        if self.is_valid() == False:
            return {"valid": False}
        return {
            "valid": self.is_valid(),
            "range": self.get_range(),
            "types": self.get_existing_types(),
        }

    def get_range(self):
        return " x ".join(list(map(str, self.df.shape)))

    def get_existing_types(self):
        print(self.df.dtypes.to_dict())
        return self.df.dtypes.to_dict()

    def is_valid(self):
        try:
            self.df = pd.read_csv(str(self.file))
            return True
        except Exception as e:
            logger.exception("error")
            return False

    def get_dataset(self):
        return self.df


class NNResolver(object):
    def __init__(self, nn):
        self.nn = nn
        self.name = str(self.nn) + str(datetime.timestamp(self.nn.date))
        self.filename = self.name + ".py"

    def get_meta_data(self):
        self.prepare_sandbox()
        result = self.run()
        with open(self.output_file_path, "rb") as out:
            return out.readlines()

    def prepare_sandbox(self):
        try:
            os.makedirs(
                os.path.join(
                    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                    "sandboxes/",
                    self.name,
                ),
                exist_ok=True,
            )
            with open(
                os.path.join(
                    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                    "sandboxes/",
                    self.name,
                    self.filename,
                ),
                "w",
            ) as output:
                output.write(self.nn.code)
        except Exception as e:
            logger.exception("error")
        print(self.nn.code)

    def run(self):
        # python_home = "/home/maus/.local/share/virtualenvs/kp-3crlKS4c"
        # activate_this = python_home + "/bin/activate_this.py"
        # exec(
        #     compile(open(activate_this, "rb").read(), activate_this, "exec"),
        #     dict(__file__=activate_this),
        # )
        command = "python " + os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            "sandboxes",
            self.name,
            self.filename,
        )
        print(command)
        self.output_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            "sandboxes",
            self.name,
            "result.txt",
        )
        if os.path.exists(self.output_file_path):
            os.utime(self.output_file_path, None)
        else:
            open(self.output_file_path, "a").close()
        with open(self.output_file_path, "w") as output:
            process = subprocess.Popen(
                "sudo -u kp " + command,
                shell=True,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdout=output,
            )
            process.wait()
            print("result")
