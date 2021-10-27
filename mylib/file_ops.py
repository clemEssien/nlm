import os
 

class file_ops:

    def write_to_file(file_path, flag, content):
        with open(file_path, flag) as f:
            f.write(content)

    def remove_file(file):
        os.remove(file)

    def remove_files_in_directory(dir_path):
        for f in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, f))