from dataclasses import dataclass
from datetime import datetime
import os
import pickle

persistence_file_name = "./progamdata.dat"


@dataclass
class ProgramData:
    last_notification_sent: datetime = None
    appointment: datetime = None

    @classmethod
    def load_from_disk(cls):
        if os.path.exists(persistence_file_name):
            with open(persistence_file_name, "rb") as f:
                data: ProgramData = pickle.load(f)
                return data
        else:
            return None

    def to_disk(self):
        with open(persistence_file_name, "wb") as f:
            pickle.dump(self, f)
