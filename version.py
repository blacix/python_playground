import os
import sys
import re
import subprocess

ARG_TAG_START_INDEX = 2

VERSION_TAGS = ['APP_VERSION_MAJOR', 'APP_VERSION_MINOR', 'APP_VERSION_REV', 'APP_VERSION_PATCH',
                'APP_VERSION_BUILD']

APP_VERSION = {VERSION_TAGS[i]: 0 for i in range(0, len(VERSION_TAGS))}
C_DEFINE_PATTERN = r"(.*#define)([^\S]+)(\S+)([^\S]+)(\d+)([^\S]*\n)"


def increment_version(version_file, tags: []):
    print(tags)
    new_lines = []
    with open(version_file, 'r') as file:
        for line in file:
            new_line = ''
            # [^\S] matches any char that is not a non-whitespace = any char that is whitespace
            result = re.search(C_DEFINE_PATTERN, line)
            if result is not None:
                version_type = result[3]
                if version_type in tags and version_type in VERSION_TAGS:
                    # print(f"{version_type} {int(result[5]) + 1}")
                    # replace \\4 with a space and a tab and the new value
                    APP_VERSION[version_type] = int(result[5]) + 1
                    new_line = re.sub(pattern=C_DEFINE_PATTERN,
                                      repl=f"\\1\\2\\3 \t{APP_VERSION[version_type]}\\6",
                                      string=line)
                else:
                    APP_VERSION[version_type] = int(result[5])
                    new_line = line
                print(new_line.strip())
            else:
                new_line = line
            new_lines.append(new_line)

    if len(tags) > 0:
        with open(version_file, 'w') as file:
            file.writelines(new_lines)


def update_tags(tag_name):
    result = 0
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
    if len(sys.argv) < ARG_TAG_START_INDEX:
        print(f'usage: {sys.argv[0]} version.h [version_type1 ... version_typen]')
        exit(-1)

    version_tags = sys.argv[ARG_TAG_START_INDEX:len(sys.argv)]
    increment_version(sys.argv[1], version_tags)
    if len(version_tags) > 0:
        update_tags(
            f'V{APP_VERSION["APP_VERSION_MAJOR"]}.{APP_VERSION["APP_VERSION_MINOR"]}.{APP_VERSION["APP_VERSION_BUILD"]}')
