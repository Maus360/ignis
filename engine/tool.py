import os
import logging
import pandas as pd

logger = logging.getLogger("ignis")


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
    def get_meta_data(self):
        pass
