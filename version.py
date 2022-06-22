import sys
import re

MIN_ARG_CNT = 2

VERSION_TYPES = ['APP_VERSION_MAJOR', 'APP_VERSION_MINOR', 'APP_VERSION_PATCH', 'APP_VERSION_BUILD']

if __name__ == '__main__':
    if len(sys.argv) <= MIN_ARG_CNT:
        print(f'usage: {sys.argv[0]} version.h [version_type1 ... version_typen]')
        exit(-1)
    version_file = sys.argv[1]
    version_types_to_increment = sys.argv[MIN_ARG_CNT:len(sys.argv)]
    print(version_types_to_increment)
    new_lines = []
    with open(version_file, 'r') as file:
        for line in file:
            new_line = ''
            # [^\S] matches any char that is not a non-whitespace = any char that is whitespace
            result = re.search("(.*#define)([^\S]+)(\S+)([^\S]+)(\d+)([^\S]*\n)", line)
            if result is not None:
                version_type = result[3]
                if version_type in version_types_to_increment and version_type in VERSION_TYPES:
                    # print(f"{version_type} {int(result[5]) + 1}")
                    # replace \\4 with a tab and the new value
                    new_line = re.sub(pattern="(.*#define)([^\S]+)(\S+)([^\S]+)(\d+)([^\S]*\n)",
                                    repl=f"\\1\\2\\3\t{int(result[5]) + 1}\\6",
                                    string=line)
                else:
                    new_line = line
                print(new_line.strip())
            else:
                new_line = line
            new_lines.append(new_line)

    with open(version_file, 'w') as file:
        file.writelines(new_lines)
