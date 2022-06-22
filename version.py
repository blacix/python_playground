import sys
import re

my_str = "#define MAJOR 1111\n"

default_increment = "PATCH"

MIN_ARG_CNT = 2

if __name__ == '__main__':
    if len(sys.argv) < MIN_ARG_CNT:
        print(f'usage: {sys.argv[0]} version.h [version_type1 ... version_typen]')
        exit(-1)
    version_file = sys.argv[1]
    if len(sys.argv) <= MIN_ARG_CNT:
        version_types_to_increment = [default_increment]
    else:
        version_types_to_increment = sys.argv[MIN_ARG_CNT:len(sys.argv)]
    print(version_types_to_increment)
    with open(version_file) as file:
        for line in file:
            # [^\S] matches any char that is not a non-whitespace = any char that is whitespace
            result = re.search("(.*#define)[^\S]+(\S+)[^\S]+(\d+)[^\S]*\n", line)
            if result is not None:
                version_type = result[2]
                if version_type in version_types_to_increment:
                    print(f"version_type: {version_type} {int(result[3]) + 1}")
