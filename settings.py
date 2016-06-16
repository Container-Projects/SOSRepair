__author__ = 'Afsoon Afzal'

import logging

#LIBCLANG_PATH = '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/libclang.dylib'
LIBCLANG_PATH = '/home/afsoon/llvm/build/lib/libclang.so'
#LIBCLANG_PATH = '/Users/afsoona/llvm/build/lib/libclang.dylib'

TESTS_DIRECTORY = '/home/afsoon/searchrepair/IntroClass/digits/tests/blackbox'
INTROCLASS_PATH = './IntroClass/digits'

Z3_COMMAND = '/home/afsoon/z3/build/z3'

LARGEST_SNIPPET = 7
SMALLEST_SNIPPET = 3

DATABASE = {
    'db_name': 'testdb',
    'user': 'afsoon',
    'password': None
}

ALL_PATCHES = False

LOGGING = {
    'filename': 'logs/repair.log',
    'level': logging.DEBUG
}

logging.basicConfig(**LOGGING)

MAX_SUSPICIOUS_LINES = 5
