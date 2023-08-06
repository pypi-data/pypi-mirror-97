import os
import re

import pandas as pd


class DataFrameCreator:
    def __init__(self):
        pass

    def __call__(self, path_to_image):
        pass


class CreateDFDummy(DataFrameCreator):
    def __init__(self, num_of_entries=100):
        super().__init__()
        self.num_of_entries = num_of_entries

    def __call__(self, path_to_image):
        df = pd.DataFrame({"id": range(self.num_of_entries)})
        df["fold"] = df.apply(lambda row: row["id"] % 10, 1)
        df["is_even"] = df.apply(lambda row: (row["id"] % 2) == 0, 1)
        return df


class CreateDFFromCSV(DataFrameCreator):
    def __init__(self, path_to_csv, sep=",", **argv):
        super().__init__()
        self.path_to_csv = path_to_csv
        self.sep = sep
        self.argv = argv

    def __call__(self, path_to_image):
        if isinstance(self.path_to_csv, list):
            df = pd.DataFrame()
            for path in self.path_to_csv:
                tmp_df = pd.read_csv(path, sep=self.sep, **self.argv)
                tmp_df["__from_csv__"] = path
                df = df.append(tmp_df)
            return df
        else:
            return pd.read_csv(self.path_to_csv, sep=self.sep, **self.argv)


class CreateDFFromFolder(DataFrameCreator):
    def __init__(self, file_of_interest):
        super().__init__()
        self.file_of_interest = file_of_interest

        regex = ""
        tmp = file_of_interest
        self.var_names = []
        counter_unnamed = 0
        while len(tmp) > 0:
            var_start = tmp.find("{")
            var_unnamed_start = tmp.find("(")
            if (
                var_unnamed_start != -1
                and (var_unnamed_start < var_start or var_start == -1)
                and (var_unnamed_start == 0 or tmp[var_unnamed_start - 1] != "\\")
            ):
                regex += tmp[: var_unnamed_start + 1]
                tmp = tmp[var_unnamed_start + 1 :]
                self.var_names.append("unnamed_" + str(counter_unnamed))
                counter_unnamed += 1
            elif var_start == -1:  # No Variable could be found
                regex += tmp
                tmp = ""
            else:
                # ignore this var start
                if var_start > 0 and tmp[var_start - 1] == "\\":
                    regex += tmp[:var_start]
                    tmp = tmp[var_start:]
                else:
                    regex += tmp[:var_start]
                    tmp = tmp[var_start:]
                    var_end = tmp.find("}")
                    self.var_names.append(tmp[1:var_end])
                    # self.regex += '(?=.*)'
                    # regex += '(^[^/]*)'
                    regex += "(.*)"
                    tmp = tmp[var_end + 1 :]
        self.regex = re.compile(regex)

    def __call__(self, path_to_image):
        rows = {name: [] for name in self.var_names}
        rows["__path__"] = []
        for root, _, files in os.walk(path_to_image):
            for file in files:
                path = os.path.join(root, file)[len(path_to_image) :]
                if path.startswith("/"):
                    path = path[1:]
                result = self.regex.search(path)
                if result is not None:
                    path_as_variable = False
                    row = {}
                    for vname, var in zip(self.var_names, result.groups()):
                        row[vname] = var
                        if var is not None and var.find("/") != -1:
                            path_as_variable = True
                    if path_as_variable is False:
                        for k in row:
                            rows[k].append(row[k])
                        rows["__path__"].append(path)

        return pd.DataFrame(rows)
