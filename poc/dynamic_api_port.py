from nguylinc_python_utils.misc import rename_substring_in_files

if __name__ == "__main__":
    path = "/private/var/folders/_r/8ww7zn494k9clc7hxb66cvt00000gr/T/_MEIGCwL8b/static"
    port = 52095
    rename_substring_in_files(path, "http://127.0.0.1:34200", f"http://127.0.0.1:{port}", ["js"])
