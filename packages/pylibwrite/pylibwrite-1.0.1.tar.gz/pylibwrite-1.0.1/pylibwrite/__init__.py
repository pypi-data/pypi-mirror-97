import pickle
import glob
import re
import json
import pkgutil
import io


def main():

    dlib_list_b = pkgutil.get_data('pylibwrite', 'default_lib_list_392.pkl')
    dlib_list_d = io.BytesIO(dlib_list_b)
    dlib_list = pickle.load(dlib_list_d)

    change_libname_dict_b = pkgutil.get_data(
        'pylibwrite',
        'convert_libname.json')
    change_libname_dict_d = io.BytesIO(change_libname_dict_b)
    change_libname_dict = json.load(change_libname_dict_d)

    pyfiles = glob.glob("./*.py")
    libs = ['import', 'from']
    comment_element = ['"', "'", '#']

    def file_reader(file):
        for row in open(file, 'r'):
            yield row

    def detect_lib(line):  # 0 found
        for lib in libs:
            if lib in line:
                for celement in comment_element:
                    if celement in line:
                        return 1

                return 0
        return 1

    lib_list = []

    for file in pyfiles:

        pydata = file_reader(file)

        for line in pydata:
            detect = detect_lib(line)

            if detect == 0:
                lib_list.append(line)

    def pick_libname(libline):
        libline = re.sub('\n', '', libline)
        libline = libline.split(' ')

        for i in range(len(libline)):
            if len(libline[i]) == 0:
                continue

            if (libline[i] == 'import') or (libline[i] == 'from'):
                for j in range(i + 1, len(libline) - i + 2):
                    if len(libline[i]) == 0:
                        continue
                    else:
                        libname = libline[j]
                        libname = re.sub(r'\..*', '', libname)
                        return libname

    def detect_non_default_lib(libname):
        if libname in dlib_list:
            return 1
        else:
            return 0

    req_list = []
    lib_list = list(set(lib_list))

    for library in lib_list:
        detect = detect_non_default_lib(pick_libname(library))
        libname = pick_libname(library)

        if detect == 0:

            if change_libname_dict.get(libname):
                req_list.append(change_libname_dict[libname])
            else:
                req_list.append(libname)

    with open('./gen-requirements.txt', 'w') as f:
        for req in req_list:
            f.write(req + '\n')

        print('create gen-requirements.txt')


if __name__ == '__main__':
    main()
