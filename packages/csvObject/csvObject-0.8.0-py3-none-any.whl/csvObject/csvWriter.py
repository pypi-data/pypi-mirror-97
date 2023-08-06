import csv


def write_csv(write_out_path, name, headers, rows_to_write):
    """
    Purpose
    -------
    This writes out a csv file of row data with an optional header. If you don't want a header, pass None to headers

    Parameters
    ----------
    :param name: The file name
    :type name: str

    :param write_out_path: The write directory
    :type write_out_path: str

    :param headers: The headers for the columns you want to write
    :type headers: list

    :param rows_to_write: A list of row data to write, each columns row should be an individual element of a list.
    :type rows_to_write: list

    :return: Nothing, just write out the file to the specified directory named the specified name
    :rtype: None
    """

    if type(rows_to_write[0]) != list:
        rows_to_write = [[row] for row in rows_to_write]

    with open(f"{write_out_path}/{name}.csv", "w", newline="", encoding="utf-8") as csv_reader:
        csv_writer = csv.writer(csv_reader)

        if len(headers) > 0:
            csv_writer.writerow(headers)

        for row in rows_to_write:
            csv_writer.writerow(row)
