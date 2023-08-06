def get_file_content(filename_or_fileobj):
    if hasattr(filename_or_fileobj, 'read'):
        return filename_or_fileobj.read()
    else:
        with open(filename_or_fileobj, 'rb') as source:
            return source.read()
