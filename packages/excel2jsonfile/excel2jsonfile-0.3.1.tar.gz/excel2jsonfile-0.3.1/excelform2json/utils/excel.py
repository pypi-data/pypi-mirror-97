from utils import messages
from openpyxl import load_workbook


class Excel:
    def __init__(self):
        pass

    def read_excel(self, file=None, sheet=None):
        """
        read a sheet from a provided excel_file file
        sets:
            self.work_book: a reference to the loaded work_book
            self.work_sheet: a reference to the loaded sheet
        :param file: The Excel file that contains the sheet
        :param sheet: The Excel sheet in the file to be loaded
        :return: result = 2 (one or more parameters not provided (None)), 3 (FileNotFound), 10 (IOError), 0 = ok
        """
        result = messages.message["ok"]
        if file is None or sheet is None:
            result = messages.message["internal_error"]
            result["info"] = "read_excel was called without an Excel file name >%s< and/or without a sheet name >%s<." \
                             % (file, sheet)
            return result, None, None

        try:
            print("file >%s<" % file)
            work_book = load_workbook(filename=file, data_only=True)
            print("sheet >%s<" % sheet)
            work_sheet = work_book[sheet]
        except FileNotFoundError or IOError as e:
            result = messages.message["excel_not_found"]
            result["info"] = "Could not read Excel >%s< sheet >%s<. Error: %s" % (file, sheet, str(e))
            print(result["info"])
            return result, None, None

        return result, work_book, work_sheet

    def search_value_in_row_index(self, work_sheet, search_string, row=1):
        """
        Thankfully copied from
        https://stackoverflow.com/questions/50491839/python-openpyxl-find-strings-in-column-and-return-row-number
        """
        for cell in work_sheet[row]:
            if cell.value == search_string:
                return cell.column, row
        return None, row
