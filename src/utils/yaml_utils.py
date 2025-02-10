def read_file(file_path: str) -> str:
    """
    Читает содержимое файла по заданному пути.

    :param file_path: Путь к файлу, который нужно прочитать.
    :type file_path: str
    :return: Содержимое файла в виде строки.
    :rtype: str
    :raises FileNotFoundError: Если файл по указанному пути не существует.
    :raises PermissionError: Если нет разрешения на чтение файла.
    """
    with open(file_path) as f:
        result = f.read()
    return result
