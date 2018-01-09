#
#   File utilities
#   Created on 2018-01-06

from os import path, walk
from FileItem import FileItem


def find_files(dir_path):
    """
    Routine for finding all files in a directory
    :param dir_path: the path to find files in
    :return: List of files found in the path sorted in descending order of file size
    """
    files_found = []
    #   Check if path exists
    if not path.exists(dir_path):
        print(dir_path + " does not exist!")
        return files_found

    #   Check if it is a directory
    if not path.isdir(dir_path):
        print(dir_path + " is not a directory!")
        return files_found

    for root, dirs, files in walk(dir_path):
        for file_name in files:
            entry = FileItem(file_name, root, path.getsize(path.join(root, file_name)))
            files_found.append(entry)

    return sorted(files_found, key=lambda x: x.file_size, reverse=False)


def main():
    files = find_files("/home/sheldon/PycharmProjects/autocode/")
    print files


if __name__ == '__main__':
    main()
