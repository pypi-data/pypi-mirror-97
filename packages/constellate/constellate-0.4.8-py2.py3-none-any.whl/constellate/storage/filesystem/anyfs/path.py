from pathlib import PurePath


def get_immediate_parent_folder_if_file(filePath) -> PurePath:
    path = PurePath(filePath)
    return path if path.is_dir() else PurePath.parent


def get_basename_without_extension(filePath) -> str:
    path = PurePath(filePath)
    extension = path.suffix
    extensionLenght = +len(path.name) if len(extension) == 0 else -len(extension)
    baseName = path.name[:extensionLenght]
    return baseName


def get_path_without_extension(filePath) -> str:
    """
    Get path without the extension
    @param filePath File Path
    @return File path without the new extension
            Eg: /path/to/file.txt -> /path/to/file
    """
    path = PurePath(filePath)
    parent = path.parent
    baseName = get_basename_without_extension(filePath)
    return str(PurePath(parent, baseName))


def get_path_with_extension(filePath, newExtension) -> PurePath:
    """
    Get path with the new extension instead
    @param filePath File Path
    @param newExtension Extension to use in the file path
    @return File path with the new extension
    """
    path = get_path_without_extension(filePath)
    return PurePath(f"{path}.{newExtension}")


def get_path_with_parent_and_extension(filePath, newParent, newExtension) -> PurePath:
    """
    Get path with the new extension instead
    @param filePath File Path
    @param newParent Parent path to use in the file path
    @param newExtension Extension to use in the file path
    @return File path with the new parent/extension
    """
    basename = get_basename_without_extension(filePath)
    return PurePath(newParent, f"{basename}.{newExtension}")


def get_purepath(filePath) -> PurePath:
    return PurePath(filePath)


def get_file_extension(filePath) -> str:
    """
    Get file extension, dotless
    """
    path = PurePath(filePath)
    return path.suffix[1:].casefold().lower()


def is_hidden_file(filePath) -> str:
    basename = get_basename_without_extension(filePath)
    return basename.startswith(".")


def escape_occurences(source, escape_string) -> str:
    """
    Escape all characters with the escape string.
    @param source String to escape
    @param escape_string String to escape the first string with
    @return Escaped string
    """
    assert isinstance(source, str), "source must be a str"

    escaped_string = list()
    for c in source:
        escaped_string.append(escape_string)
        escaped_string.append(c)

    return "".join(escaped_string)


def escape_path(path) -> str:
    """
    Escape all characters with the escape string.
    @param path String to escape
    @param anEscapeString String to escape the first string with
    @return Escaped string
    """
    return escape_occurences(path, "\\")


def same_path(path1, path2) -> bool:
    """
    Case sensitive path check
    Assume linux fs path (ie case sensitive paths)
    """
    return str(path1) == str(path2)
