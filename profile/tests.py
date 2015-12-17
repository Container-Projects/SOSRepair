__author__ = 'afsoona'

import os

from settings import TESTS_DIRECTORY
from utils.file_process import compare_files

class Tests():

    def __init__(self, program_directory, program_name):
        self.program_directory = program_directory
        self.program_name = program_name
        self.positives = []
        self.negatives = []


    def initialize_testing(self):
        program = os.path.join(self.program_directory, self.program_name + '.c')
        res = os.system('gcc -o ' + self.program_name + ' ' + program)
        if res != 0:
            raise Exception
        temp_output = os.path.join(self.program_directory, self.program_name + '_temp.out')
        test_files = os.listdir(TESTS_DIRECTORY)
        for file in test_files:
            if not file.endswith('.in'):
                continue
            test = os.path.join(TESTS_DIRECTORY, file)
            res = os.system('./' + self.program_name + ' < ' + test + ' > ' + temp_output)
            if res != 0:
                raise Exception
            out_file = file[0:-3]+'.out'
            if compare_files(os.path.join(TESTS_DIRECTORY, out_file), temp_output):
                self.positives.append(file)
            else:
                self.negatives.append(file)
        os.system('rm ' + temp_output + ' ' + self.program_name)
        return True

    def __str__(self):
        return "Positives: " + str(self.positives) + "\nNegative: " + str(self.negatives)

    def __unicode__(self):
        return "Positives: " + str(self.positives) + "\nNegative: " + str(self.negatives)