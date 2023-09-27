from typing import List, Dict

import pandas as pd

from utils.logging import get_basic_stdout_logger

logger = get_basic_stdout_logger()


class DataFrameProcessor:

    @classmethod
    def from_dict(cls, transformations: Dict[str, str]):
        """
        Takes a dictionary of transformations and creates a DataFrameProcessor object.
        Expect the format of the dictionary to be:
        {'transformation_name': 'transformation_function'}
        :param transformations: Dict
        :return: DataFrameProcessor
        """
        self = cls()
        for key, value in transformations.items():
            # Create a new method for each transformation
            func_str = value
            func = eval(func_str)
            setattr(self, key, func)
        return self

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        result = pd.DataFrame()
        for key in self.__dict__:
            try:
                result[key] = getattr(self, key)(df)
            except Exception as e:
                logger.error(f"Error during transformation '{key}': {e}", exc_info=True)
        return result
