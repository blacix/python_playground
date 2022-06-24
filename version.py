import os
import sys
import re
import subprocess
from array import array

MIN_ARG_CNT = 2

VERSION_TYPES = ['APP_VERSION_MAJOR', 'APP_VERSION_MINOR', 'APP_VERSION_REV', 'APP_VERSION_PATCH',
                 'APP_VERSION_BUILD']

APP_VERSION = {VERSION_TYPES[i]: 0 for i in range(0, len(VERSION_TYPES))}


def increment_version(version_file, version_tags: []):
    print(version_tags)
    new_lines = []
    with open(version_file, 'r') as file:
        for line in file:
            new_line = ''
            # [^\S] matches any char that is not a non-whitespace = any char that is whitespace
            result = re.search("(.*#define)([^\S]+)(\S+)([^\S]+)(\d+)([^\S]*\n)", line)
            if result is not None:
                version_type = result[3]
                if version_type in version_tags and version_type in VERSION_TYPES:
                    # print(f"{version_type} {int(result[5]) + 1}")
                    # replace \\4 with a space and a tab and the new value
                    APP_VERSION[version_type] = int(result[5]) + 1
                    new_line = re.sub(pattern="(.*#define)([^\S]+)(\S+)([^\S]+)(\d+)([^\S]*\n)",
                                      repl=f"\\1\\2\\3 \t{APP_VERSION[version_type]}\\6",
                                      string=line)
                else:
                    APP_VERSION[version_type] = int(result[5])
                    new_line = line
                print(new_line.strip())
            else:
                new_line = line
            new_lines.append(new_line)

    with open(version_file, 'w') as file:
        file.writelines(new_lines)


def update_tags(r90_version):
    result = 0
    tag_name = f'R90_V{r90_version}'
    print(tag_name)
    proc = subprocess.Popen('git tag', stdout=subprocess.PIPE)
    output = proc.stdout.readlines()
    # print(output)
    if bytes(f'{tag_name}\n', 'utf-8') not in output:
        result = os.system(f'git tag {tag_name}')
        result = os.system(f'git push origin {tag_name}')
    else:
        print(f'tag {tag_name} already exists')

    return result


if __name__ == '__main__':
    if len(sys.argv) <= MIN_ARG_CNT:
        print(f'usage: {sys.argv[0]} version.h [version_type1 ... version_typen]')
        exit(-1)
    increment_version(sys.argv[1], sys.argv[MIN_ARG_CNT:len(sys.argv)])
    update_tags(
        f'{APP_VERSION["APP_VERSION_MAJOR"]}.{APP_VERSION["APP_VERSION_MINOR"]}.{APP_VERSION["APP_VERSION_BUILD"]}')
