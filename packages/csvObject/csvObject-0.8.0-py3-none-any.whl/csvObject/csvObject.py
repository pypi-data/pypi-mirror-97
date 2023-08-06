from distutils.util import strtobool
from pathlib import Path
import csv
import re


class CsvObject:
    """
    Simple Objected based approach to using data from a csv
    """

    def __init__(self, csv_path, column_types=None, set_columns=False, file_headers=True, encoding="utf-8-sig",
                 missing_to_zero=False, print_warnings=True):
        """
        This class reads in the data from the path provided with the specified encoding standard. It then sets the
        headers from the first row if headers exist, else it generates incremental column names as header names. It also
        loads the data and formats it into a column data structure and a row data structure. If a type or type list is
        provided, then the data can be typed as well; with the option of setting missing numeric data to zero
        missing_to_zero.

        :param csv_path: path to the load file
        :type csv_path: str

        :key column_types: A type, list of types to type the row's data, or None if a string representation of the data
            is sufficient
        :type column_types: type | list[type] | None

        :key file_headers: Equals True if the first row should be interpreted as a file header, False if not.
        :type file_headers: bool

        :key encoding: The encoding style of the file
        :type encoding: str

        :key missing_to_zero: Equals True if you want missing data in numeric columns of type int or float to be set to
            zero, False if not.
        :type missing_to_zero: bool

        :key print_warnings: Equals True if you want to log and print the column-row-value-type entries that were not
            successfully typed vus defaulting to string, False otherwise.
        :type print_warnings: bool
        """

        self.file_path = Path(csv_path)
        self.file_name = self.file_path.name

        self._file_headings = file_headers
        self._encoding = encoding

        self.headers = self._extract_headers()
        self.row_length = len(self.headers)

        self.missing_to_zero = missing_to_zero
        self.print_warnings = print_warnings
        self.invalid_typed = []

        self.column_types = self._determine_column_types(column_types)
        self.row_data, self.column_data, self.column_length = self._set_data(set_columns)

        if len(self.invalid_typed) > 0 and self.print_warnings:
            print(f"Warning: The following column-row-value-type where not correct so loaded as strings:\n"
                  f"{sorted(self.invalid_typed)}")

    def __repr__(self):
        """Add some human readable output from print"""
        if self.column_data:
            return f"{self.file_name}: Column:{self.column_length} by Rows:{self.row_length}"
        else:
            return f"{self.file_name}: Rows:{self.row_length}"

    def __getitem__(self, item):
        """
        This will allow you to index a given column of data via its numeric index or the header name. Can only be called
        if column data is set

        :param item: An index of a column to Isolate or the header name
        :type item: int | str

        :return: The column data of this index
        :rtype: list
        """

        assert self.column_data, "Get item only works if column data is set!"

        if isinstance(item, int):
            return self.column_data[item]
        elif isinstance(item, str):
            index = self.index_from_headers(item)
            return self.column_data[index]
        else:
            raise Exception(f"Get Item takes a int or a string, where the int is a column index and the string is the"
                            f"name of the header of the column you want to index.\nYet was passed {type(item)}")

    def index_from_headers(self, item):
        """Extract the index of a given header"""
        assert item in set(self.headers), f"String of {item} passed but this is not in headers!\n{self.headers}"
        return self.headers.index(item)

    def _extract_headers(self):
        """
        This will extract the headers from a given csv file if the file has headers, otherwise just Untitled

        :return: A list of Headers
        :rtype: list[str]
        """

        with open(self.file_path, "rt", encoding=self._encoding) as csv_file:
            for row in csv.reader(csv_file):
                if self._file_headings:
                    return [header if header != "" else f"Untitled_{index + 1}" for index, header in enumerate(row)]

                else:
                    return [f"Untitled_{i + 1}" for i in range(len(row[0]))]

    def _extract_data(self):
        """
        Returns a tuple of the the raw untyped row data minus the header, as well as the headers.

        :return: A tuple of raw untyped row data minus the header, as well as the headers
        """
        with open(self.file_path, "rt", encoding=self._encoding) as csv_file:
            raw_data = [row for row in csv.reader(csv_file)]

        # If we have read in a .txt, .tsv or .uniq file then we delimit our rows
        if self.file_path.suffix == ".txt":
            raw_data = [row[0].split() for row in raw_data if len(row) == 1]

        elif (self.file_path.suffix == ".tsv") or (self.file_path.suffix == ".tsv"):
            raw_data = [re.split(r"\t+", row[0]) for row in raw_data]

        # Csv files are the default so don't need handling
        elif self.file_path.suffix == ".csv":
            pass

        # Warning users that a file has been loaded that we haven't build a capture for
        else:
            print(f"Warning: {self.file_path.suffix} is not explicitly handled")

        if self._file_headings:
            return raw_data[1:]
        else:
            return raw_data

    def _determine_column_types(self, column_types):
        """
        Returns a list, where each element in the list represents the type of data in the column data

        :param column_types: A python type or list a list of types
        :type column_types: type | list[type]

        :return: A list types, where said types equal to the length of columns
        :rtype: list[type]
        """
        if isinstance(column_types, list):
            # List based typing
            if len(column_types) != len(self.headers):
                raise ValueError(f"You must provide as many column types as columns of data\nFound {len(column_types)}"
                                 f" but expected {len(self.headers)}")
            else:
                return [col_type if col_type != bool else self._string_to_bool for col_type in column_types]

        elif isinstance(column_types, type):
            # Uniform Typing of type column_types
            if column_types == bool:
                return [self._string_to_bool for _ in range(self.row_length)]
            else:
                return [column_types for _ in range(self.row_length)]

        elif not column_types:
            # None Typed operation
            return column_types

        else:
            raise TypeError(f"Column_types takes a list[types], type or None. Yet {type(column_types)} was found")

    def _format_column(self, row_data):
        """
        Reformat a list of rows to a list of columns

        Example
        --------
        row_data = [[1, 2, 3, 4], [5, 6, 7, 8]]
        column_data = [[1, 5], [2, 6], [3, 7], [4, 8]]

        :param row_data: A list of lists, where each list within the list is a list of entry's
        :type row_data: list[list]

        :return: A list of lists, where each list within the list is a list of entries found in a given column.
        :rtype: list[list]
        """
        return [[row[i] for row in row_data] for i in range(self.row_length)]

    def _type_data(self, row, index):
        """
        Set entry's to their provide type

        Further information
        ---------------------
        Where it is possible the system will type the data to the given type. A common point of failure is numeric data
        with missing values. If self.missing_to_zero is set to true, then in the case of this ValueError a zero will be
        added to the row data rather than an empty string.

        The principle here is to avoid crashing, so if a invalid type is found it simply adds the entry as a string and
        raises a warning at the end that some data wasn't typed correctly.

        :param row: A list of entries
        :type row: list

        :return: A typed list of entries
        :rtype: list
        """
        typed_row = []
        for i, (entry, entry_type) in enumerate(zip(row, self.column_types)):
            try:
                typed_row.append(entry_type(entry))
            except ValueError:
                if (entry_type == int or entry_type == float) and self.missing_to_zero:
                    typed_row.append(entry_type(0))
                else:
                    if [i + 1, index + 2, entry, entry_type] not in self.invalid_typed and self.print_warnings:
                        self.invalid_typed.append([i + 1, index + 2, entry, entry_type])
                    typed_row.append(entry)
        return typed_row

    def _check_row_length(self):
        """
        csv does not read in empty rows at the end of csv, so if we have 40 headers but only 26 columns for a given row
        then we will end up not being able to index call. This sets all rows with length less than the column length to
        be equal to it via blanks.

        :return: A list of rows, where each row is equal to the length of the number of columns
        :rtype: list[list]
        """

        row_data = []
        for row in self._extract_data():
            if len(row) < self.row_length:
                row_data.append(row + ["" for _ in range(self.row_length - len(row))])
            else:
                row_data.append(row)

        return row_data

    def _set_data(self, set_columns):
        """
        Set the row and column data of the csv, with the entries typed if types where provided

        :return: Two lists, where the first list is a list of entries in row format and the second a list a list of
            entries in column formant
        :rtype: tuple[list, list]
        """
        if self.column_types:
            row_data = [self._type_data(row, index) for index, row in enumerate(self._check_row_length())]
        else:
            row_data = self._check_row_length()

        if set_columns:
            return row_data, self._format_column(row_data), len(row_data)
        else:
            return row_data, None, len(row_data)

    @staticmethod
    def _string_to_bool(string_representation_of_bool):
        """
        Convert a string of False or True to a bool representation
        """
        return bool(strtobool(string_representation_of_bool))
