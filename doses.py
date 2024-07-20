from datetime import datetime
import pandas as pd

from config import doses_file_path



def add(people_id, medicine_id):
    doses = pd.read_csv(doses_file_path)
    new_row = pd.DataFrame(
        {
            "people_id": [people_id],
            "medicines_id": [medicine_id],
            "dose_datetime": [datetime.now()],
        }
    )
    new_doses = pd.concat([doses, new_row])
    new_doses.to_csv(doses_file_path, index=False)
