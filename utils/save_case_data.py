from typing import Dict, List
import time

import pandas as pd


def save_case_data_in_excel_and_csv(detailed_case_data: List[Dict[str, str]], schema_name: str):
    """save data in form of csv and excel"""

    try:
        timestr = time.strftime("%Y%m%d-%H%M%S")

        case_data = pd.DataFrame(detailed_case_data)
        case_data.to_csv(f'./case_data/{schema_name}_{timestr}.csv')
        case_data.to_excel(f'./case_data/{schema_name}_{timestr}.xlsx')

    except Exception as ex:
        print(f"Could not save data, error: {ex}")
