import os
import shutil
import logging
import pandas as pd
import numpy
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
        self.name = str(self.nn) + str(int(datetime.timestamp(self.nn.date)))
        self.filename = self.name + ".py"
        self.dataset = self.nn.dataset
        self.output_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            "sandboxes",
            self.name,
            "result.txt",
        )

    def get_meta_data(self):
        if not os.path.exists(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                "sandboxes",
                self.name,
            )
        ):
            self.prepare_sandbox()
            result = self.run()
        with open(self.output_file_path, "rb") as out:
            a = out.readlines()
            return a

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
            os.makedirs(
                os.path.join(
                    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                    "sandboxes/",
                    self.name,
                    "data/",
                ),
                exist_ok=True,
            )
            shutil.copyfile(
                self.dataset.file.name,
                os.path.join(
                    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                    "sandboxes/",
                    self.name,
                    "data/",
                    self.dataset.name,
                ),
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
                output.write(
                    "import os; import sys;"
                    "import pandas as pd;"
                    "data = pd.read_csv(os.path.join("
                    "os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"
                    f"'{self.name}',"
                    "'data/',"
                    f"'{self.dataset.name}'))\n" + self.nn.code
                )
        except Exception as e:
            logger.exception("error")

    def run(self):
        if os.path.exists(self.output_file_path):
            os.utime(self.output_file_path, None)
        else:
            open(self.output_file_path, "a").close()
        with open(self.output_file_path, "w") as output:
            print(f"from sandboxes.{self.name}.{self.name} import result")
            try:
                exec(f"from sandboxes.{self.name}.{self.name} import result")
                output.write(str(locals()["result"]))
            except Exception as e:
                logger.exception(e)
