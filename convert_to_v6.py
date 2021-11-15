import sys

tags_to_remove = [
    "AlignConsecutiveMacros",
    "AlignConsecutiveBitFields",
    "AllowAllArgumentsOnNextLine",
    "AllowAllConstructorInitializersOnNextLine",
    "AllowShortEnumsOnASingleLine",
    "AllowShortBlocksOnASingleLine",
    "AllowShortLambdasOnASingleLine",
    "AllowShortIfStatementsOnASingleLine",
    "AlwaysBreakTemplateDeclarations",
    "AfterCaseLabel",
    "BeforeLambdaBody",
    "BeforeWhile",
    "BreakInheritanceList",
    "BreakConstructorInitializersBeforeComma",
    "DeriveLineEnding",
    "SortPriority",
    "IncludeIsMainSourceRegex",
    "IndentCaseBlocks",
    "IndentExternBlock",
    "InsertTrailingCommas",
    "IndentGotoLabels",
    "ObjCBinPackProtocolList",
    "ObjCBreakBeforeNestedBlockParam",
    "PenaltyBreakTemplateDeclaration",
    "SpaceAfterLogicalNot",
    "SpaceBeforeCpp11BracedList",
    "SpaceBeforeCtorInitializerColon",
    "SpaceBeforeInheritanceColon",
    "SpaceBeforeRangeBasedForLoopColon",
    "SpaceInEmptyBlock",
    "SpacesInConditionalStatement",
    "SpaceBeforeSquareBrackets",
    "Standard",
    "StatementMacros",
    "Q_UNUSED",
    "QT_REQUIRE_VERSION",
    "UseCRLF"
]


def process(input_file_name):
    print(f'processing: {input_file_name}')

    with open(input_file_name, 'r') as input_file, open(f'{input_file_name}_v6', 'w') as output_file:
        for line in input_file:
            if match_any_tag(line):
                line = comment_out(line)
            output_file.write(line)

    print(f'output: {output_file.name}')


def match_any_tag(line: str):
    for tag in tags_to_remove:
        if line.find(tag) >= 0:
            return True
    return False


def comment_out(line: str):
    stripped_line = line.strip()
    if len(stripped_line) < 1:
        return line
    if stripped_line[0] == '#':
        return line

    return f'# {line}'


if __name__ == '__main__':
    if len(sys.argv) == 2:
        process(sys.argv[1])
    else:
        print(f'usage : {sys.argv[1]} <input_clang_file> ')
