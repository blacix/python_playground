import os
import sys
import re
import subprocess

ARG_TAG_START_INDEX = 2

VERSION_TAGS = ['APP_VERSION_MAJOR', 'APP_VERSION_MINOR', 'APP_VERSION_REV', 'APP_VERSION_PATCH',
                'APP_VERSION_BUILD']

APP_VERSION = {VERSION_TAGS[i]: 0 for i in range(0, len(VERSION_TAGS))}

# [^\S] matches any char that is not a non-whitespace = any char that is whitespace
C_DEFINE_PATTERN = r"(.*#define)([^\S]+)(\S+)([^\S]+)(\d+)([^\S]*\n)"


def _update_versions_file(version_file, tags: []):
    print(f'updating {str(tags)}')
    new_lines = []
    with open(version_file, 'r') as file:
        for line in file:
            new_line = ''
            result = re.search(C_DEFINE_PATTERN, line)
            if result is not None:
                version_type = result[3]
                if version_type in tags and version_type in VERSION_TAGS:
                    # print(f"{version_type} {int(result[5]) + 1}")
                    # replace \\4 with a space and a tab and the new value
                    APP_VERSION[version_type] = int(result[5]) + 1
                    new_line = re.sub(pattern=C_DEFINE_PATTERN,
                                      repl=f"\\1\\2\\3 {APP_VERSION[version_type]}\\6",
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


def commit_version_file(version_file: str, version_string: str):
    print(f'git add {version_file}')
    os.system(f'git add {version_file}')
    os.system(f'git commit -m "version: {version_string}"')
    os.system(f'git push')


def update_git_tag(tag_name):
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


def update_versions(sys_args: [], git_tag_prefix: str, project_ver_tags: []):
    if len(sys_args) < ARG_TAG_START_INDEX:
        print(f'usage: {sys_args[0]} version.h [version_type1 ... version_typen]')
        exit(-1)

    version_file = sys.argv[1]
    versions_to_increment = sys.argv[ARG_TAG_START_INDEX:len(sys.argv)]
    filtered_versions_to_increment = [item for item in
                                      filter(lambda x: x in VERSION_TAGS, versions_to_increment)]
    filtered_project_ver_tags = [item for item in
                                 filter(lambda x: x in VERSION_TAGS, project_ver_tags)]

    print(filtered_project_ver_tags)
    if len(filtered_project_ver_tags) != len(project_ver_tags):
        invalid_versions = [item for item in
                            filter(lambda x: x not in VERSION_TAGS, project_ver_tags)]
        print(f'print invalid version type {invalid_versions}')
        return -1

    print(filtered_versions_to_increment)
    if len(filtered_versions_to_increment) != len(versions_to_increment):
        invalid_versions = [item for item in
                            filter(lambda x: x not in VERSION_TAGS, versions_to_increment)]
        print(f'print invalid version type {invalid_versions}')
        return -1

    _update_versions_file(version_file, versions_to_increment)

    version_string = ".".join([str(APP_VERSION[item]) for item in
                               filter(lambda x: x in VERSION_TAGS, project_ver_tags)])

    print(version_string)
    # if len(versions_to_increment) > 0:
    #     git_tag = f'{git_tag_prefix}{version_string}'
    #     commit_version_file(version_file, git_tag)
    #     update_git_tag(git_tag)


if __name__ == '__main__':
    update_versions(sys.argv, 'V', ['APP_VERSION_MAJOR', 'APP_VERSION_MINOR', 'APP_VERSION_PATCH'])
