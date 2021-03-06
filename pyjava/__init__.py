from .parser import PyJavaParser, parse_file, parse_str
from .tokenize import tokenize

# import unittest

# class UnitTests(unittest.TestCase):
#     def test_parser(self):
#         import os.path
#         import pprint
#         from textwrap import indent
#         self.maxDiff = None
#         with open(os.path.join(os.path.dirname(__file__), 'test.java'), 'rb') as file:
#             java_unit = parse_file(file, parser=JavaParser)
#         with open(os.path.join(os.path.dirname(__file__), 'test.javapy'), 'rb') as file:
#             javapy_unit = parse_file(file, parser=Parser)
#         self.assertEqual(java_unit, javapy_unit, f"java_unit != javapy_unit.\njava_unit:\n{indent(pprint.pformat(java_unit), '    ')}\njavapy_unit:\n{indent(pprint.pformat(javapy_unit), '    ')}")
#         java_unit_str = str(java_unit)
#         javapy_unit_str = str(javapy_unit)
#         self.assertEqual(java_unit_str, javapy_unit_str, f"str(java_unit) != str(javapy_unit).")
        
        

def main(args=None):
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Parse a pyjava file')
    parser.add_argument('file', type=argparse.FileType('rb'),
                        help='The javapy file to parse')
    parser.add_argument('--optional-semicolons', action='store_true',
                        help="Make semicolons optional")
    parser.add_argument('--out', metavar='FILE', type=Path,
                        help='Where to save the output. Special name "STDOUT" can be used to output to the console.')

    args = parser.parse_args(args)

    with args.file as file:
        unit = parse_file(file, optional_semicolons=args.optional_semicolons)

    if hasattr(args, 'out'):
        if str(args.out) == 'STDOUT':
            filename = args.file.name
            for stmt in unit:
                print(stmt)
        else:
            with args.out.open('w') as file:
                file.writelines(str(stmt) for stmt in unit)
                filename = file.name

    else:
        import os.path

        filename = os.path.join(os.path.dirname(args.file.name), os.path.splitext(args.file.name)[0] + '.py')

        with open(filename, 'w') as file:
            file.writelines(str(stmt) for stmt in unit)

    print("Converted", filename)

if __name__ == "__main__":
    main()