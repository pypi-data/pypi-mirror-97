import time
from enum import Enum
from dateutil import parser
import datetime
from typing import Dict, List, Generic, TypeVar
import tkinter
import tkinter.filedialog as fd
from coopui.IAtomicUserInteraction import IAtomicUserInteraction
from pprint import pprint
import pandas as pd
from cooptools.pandasHelpers import clean_a_dataframe

T = TypeVar('T')

class CliAtomicUserInteraction(IAtomicUserInteraction):

    def __init__(self):
        pass

    def notify_user(self, text: str, sleep_sec: int = 1):
        print(text)
        if sleep_sec > 0:
            time.sleep(sleep_sec)

    def request_string(self, prompt: str, default:str = None, cancel_text: str = None):
        if default:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"(enter for default [{default}]):"

        if cancel_text:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"({cancel_text} to cancel):"

        inp = input(prompt).strip()

        if len(inp) == 0 and default:
            return default
        elif cancel_text and inp in (cancel_text, cancel_text.upper()):
            return None
        else:
            return inp

    def request_int(self, prompt: str, min: int = None, max: int = None, default: int = None):
        cancel_text = 'x'
        default_prompt_text = f", <enter> for {default}" if default else ""
        cancel_default_prompt = f"({cancel_text} to cancel{default_prompt_text})"

        if min and max:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[between {min} and {max} (inclusive)]{cancel_default_prompt}:"
        elif min:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[greater than or equal to {min}]{cancel_default_prompt}:"
        elif max:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[less than or equal to {max}]{cancel_default_prompt}:"
        else:
            prompt = prompt + cancel_default_prompt




        while True:
            try:
                ret = input(prompt)

                if ret == "":
                    return default

                if ret in (cancel_text, cancel_text.upper(), None):
                    return None

                parsed = self.int_tryParse(ret)
                if parsed is None:
                    raise ValueError(f"Invalid integer value {ret}")

                if min and parsed < min:
                    raise Exception(f"Must be a greater than {min}")

                if max and parsed > max:
                    raise Exception(f"Must be a less than {max}")

                return parsed

            except Exception as e:
                self.notify_user(f"Invalid Integer entry: {e}")

    def request_enum(self, enum, prompt:str=None, cancel_text: str = 'CANCEL SELECTION'):
        if prompt is None:
            prompt = f"Enter {enum.__name__}:"

        if issubclass(enum, Enum):
            enum_num = self.request_from_dict({x.value: x.name for x in enum}, prompt, cancel_text)
            if enum_num is None:
                return None
            else:
                return enum(enum_num)
        else:
            raise TypeError(f"Input must be of type Enum but {type(enum)} was provided")


    def request_float(self, prompt: str, min: float = None, max: float = None, default: float = None):
        cancel_text = 'x'
        default_prompt_text = f", <enter> for {default}" if default else ""
        cancel_default_prompt = f"({cancel_text} to cancel{default_prompt_text})"


        if min and max:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[between {min} and {max} (inclusive)]{cancel_default_prompt}:"
        elif min:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[greater than or equal to {min}]{cancel_default_prompt}:"
        elif max:
            prompt = prompt.replace(":", " ")
            prompt = prompt + f"[less than or equal to {max}]{cancel_default_prompt}:"
        else:
            prompt = prompt + cancel_default_prompt

        while True:
            try:
                ret = input(prompt)

                if ret == "":
                    return default

                if ret in (cancel_text, cancel_text.upper(), None):
                    return None

                inp = float(ret)
                if min and inp < min:
                    raise Exception(f"Must be a greater than or equal to {min}")

                if max and inp > max:
                    raise Exception(f"Must be a less than or equal to {max}")

                return inp
            except Exception as e:
                self.notify_user(f"invalid float entry: {e}")

    def request_guid(self, prompt: str):
        while True:
            inp = input(prompt)
            if (len(inp)) == 24:
                return inp
            else:
                self.notify_user("Invalid Guid...")

    def request_date(self, prompt: str = None, cancel_text='x'):
        if prompt is None:
            prompt = "Date"

        prompt.replace(":", "")

        prompt = prompt + f"({cancel_text} to cancel, <Enter> for current date):"

        while True:
            inp = input(f"{prompt}")
            try:
                if inp == '':
                    date_stamp = datetime.datetime.now().date()
                    print(f"using: {date_stamp}")
                elif inp in (cancel_text, cancel_text.upper()):
                    return None
                else:
                    date_stamp = parser.parse(inp).date()
                break
            except:
                print("invalid date format")

        return date_stamp

    def request_datetime(self, prompt: str = None, cancel_text='x', include_ms: bool = False):
        if prompt is None:
            prompt = "Datetime"

        prompt.replace(":", "")

        prompt = prompt + f"({cancel_text} to cancel, <Enter> for current datetime):"

        while True:
            inp = input(f"{prompt}")
            try:
                if inp == '':
                    date_stamp = datetime.datetime.now()
                    print(f"using: {date_stamp}")
                elif inp in (cancel_text, cancel_text.upper()):
                    return None
                else:
                    date_stamp = parser.parse(inp)
                break
            except:
                print("invalid date format")

        if not include_ms:
            date_stamp = datetime.datetime.combine(date_stamp, datetime.datetime.min.time())

        return date_stamp

    def request_from_list(self, selectionList: List[T], prompt=None, cancel_text: str = 'CANCEL SELECTION') -> T:
        ret = self.request_from_dict({ii: item for ii, item in enumerate(selectionList)}, prompt, cancel_text)
        if ret is None:
            return ret

        return selectionList[ret]

    def request_from_objects(self, selectionList: List[T], objectIdentifier: str, prompt=None, cancel_text: str = 'CANCEL SELECTION') -> T:
        item_id = self.request_from_list([str(vars(obj)[objectIdentifier]) for obj in selectionList], prompt=prompt, cancel_text=cancel_text)
        if item_id is None:
            return item_id

        return next(item for item in selectionList if str(vars(item)[objectIdentifier]) == item_id)

    def request_from_dict(self, selectionDict: Dict[int, str], prompt=None, cancel_text: str = 'CANCEL SELECTION') -> int:
        if prompt is None:
            prompt = ""

        cancel = 'X'

        while True:
            print(prompt)
            for key in selectionDict:
                print(f"{key} -- {selectionDict[key]}")

            if cancel_text is not None:
                print(f"{cancel} -- {cancel_text}")

            inp = input("").upper()
            if cancel_text is not None and inp == cancel:
                return None

            inp = self.int_tryParse(inp)

            if (inp or type(inp) == int) and selectionDict.get(inp, None) is not None:
                return inp
            else:
                print("Invalid Entry...")

    def request_index_from_df(self, df: pd.DataFrame, prompt: str = None, cancel_text: str = 'CANCEL SELECTION', hide_columns: List[str] = None, return_columns: List[str] = None):
        if prompt is None:
            prompt = "Select an index from the dataframe:"

        cancel = 'X'

        while True:
            print_out = df
            if hide_columns:
                print_out = print_out[[x for x in print_out.columns if x not in hide_columns]]

            self.pretty_print_dataframe(print_out, prompt)

            if cancel_text is not None:
                print(f"{cancel} -- {cancel_text}")

            inp = input("").upper()
            if cancel_text is not None and inp == cancel:
                return None

            ind = self.int_tryParse(inp)
            if (ind in df.index) and return_columns is None:
                return ind
            elif (ind in df.index) and len(return_columns) > 0:
                return (df.at[ind, x]for x in return_columns if x in df.columns)
            else:
                print("Invalid Entry...")


    def request_open_filepath(self, title:str=None, filetypes=None):
        root = tkinter.Tk()

        if filetypes is None:
            filetypes = ()

        in_path = fd.askopenfilename(title=title, filetypes=filetypes)
        root.destroy()

        if in_path == '':
            in_path = None

        return in_path

    def pd_column_replacement(self, df, required_columns) -> Dict:
        missing_columns = [column for column in required_columns if column not in df.columns]
        additional_columns = [column for column in df.columns if column not in required_columns]

        if len(missing_columns) == 0 or len(additional_columns) == 0:
            return {}

        resp = self.request_yes_no(
            prompt=f"The following columns are missing from dataset:  [{[col for col in missing_columns]}]. "
                   f"\nWould you like to substitute from additional columns: [{[col for col in additional_columns]}]",
            cancel_text=None)

        if resp is False:
            return {}

        remaining_to_evaluate = missing_columns
        replacements = {}
        while len(remaining_to_evaluate) > 0:
            options = [x for x in additional_columns if x not in replacements.keys()]
            replacement = self.request_from_list(options, f"Any replacement for column [{remaining_to_evaluate[0]}]")
            if replacement is not None:
                replacements[replacement] = remaining_to_evaluate[0]
            remaining_to_evaluate.pop(0)

        return replacements


    def request_data_from_csv_with_specified_columns(self, column_type_definition: Dict, title:str=None, allow_partial:bool=False, fill_missing: bool=False) -> pd.DataFrame:

        # Direct user of what is required
        required_columns = [key for key, value in column_type_definition.items()]

        while True:
            if allow_partial:
                text = "AT LEAST A SUBSET OF"
            else:
                text = "ALL OF"
            self.notify_user(f"Please select a .csv file containing {text} the columns:\n\t" + "\n\t".join(required_columns), sleep_sec=0)

            # Request Filepath from user
            filepath = self.request_open_filepath(title=title, filetypes=(("CSV Files","*.csv"),))

            # Get file contents
            if filepath is None or filepath == '':
                return None

            try:
                df = pd.read_csv(filepath)
                if df is None:
                    return None

                # Return
                self.notify_user(f"The selected file has the following columns:\n\t" + "\n\t".join(df.columns),
                                 sleep_sec=0)
                return clean_a_dataframe(df,
                                         column_type_definition=column_type_definition,
                                         allow_partial_columnset=allow_partial,
                                         fill_missing=fill_missing,
                                         column_name_replacement=lambda: self.pd_column_replacement(df, required_columns)
                                              )
            except Exception as e:
                self.notify_user(text=f"Error when reading the csv file: {str(e)}")


    def request_save_filepath(self):
        root = tkinter.Tk()
        in_path = fd.asksaveasfilename()
        root.destroy()

        if in_path == '':
            in_path = None

        return in_path

    def request_you_sure(self, prompt=None, cancel_text: str = 'CANCEL SELECTION'):
        return self.request_from_dict({1: "Yes", 2: "No"}, prompt, cancel_text=cancel_text)

    def request_bool(self, prompt=None, cancel_text: str = 'CANCEL SELECTION'):
        ret = self.request_from_dict({1: "True", 2: "False"}, prompt, cancel_text=cancel_text)
        if ret == 1:
            return True
        elif ret == 2:
            return False
        elif ret is None:
            return None
        else:
            raise NotImplementedError(f"Unhandled return [{ret}] from request_from_dict")

    def request_yes_no(self, prompt:str=None, cancel_text: str = 'CANCEL SELECTION') -> bool:
        ret = self.request_from_dict({1: "Yes", 2: "No"}, prompt, cancel_text=cancel_text)

        if ret == 1:
            return True
        elif ret == 2:
            return False
        elif ret is None:
            return None
        else:
            raise NotImplementedError(f"Unhandled return [{ret}] from request_from_dict")

    def float_as_currency(self, val: float):
        return "${:,.2f}".format(round(val, 2))

    def int_tryParse(self, value):
        try:
            return int(value)
        except:
            return None

    def pprint_items(self, items, header:str=None):
        if header:
            print(header)
        pprint(items)

    @staticmethod
    def pretty_print_dataframe(df: pd.DataFrame, title: str = None, display_width: int = 2000, display_max_columns: int=2000):
        if title:
            print(title)

        with pd.option_context('display.max_rows', 500,
                               'display.max_columns', display_max_columns,
                               'display.width', display_width,
                               'display.float_format', lambda x: '%.3f' % x):
            print(f"{df}\n")
