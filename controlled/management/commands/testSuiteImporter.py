# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
import glob
import os
# Get models 
from controlled.models import *

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_programs(self):
        # read files from test suite directory
        directory = "testSuites/"
        list_dirs = os.listdir(directory)
        for dr in list_dirs:
            if dr.__contains__("TestSuite-"):
                program_name = dr.split("-")[1]
                codes = glob.glob(directory + dr + "/schema-*.sql")
                program_code = ""
                for c in codes:
                    with open(c) as reader:
                        create_tables = reader.read()
                        program_code = program_code + create_tables + "\n"
                # Creating A Program
                program = Program(name  = program_name, code = program_code)
                program.save()

                # Creating a Test Suite
                # "PROGRAM-AUTO-GENERATOR-REDUCED"
                testSuite_id = program_name + "-AUTO-DOMINOD-REDUCED"
                test_suite = TestSuite(test_suite_id = testSuite_id, program = program, other_label = "RD")
                test_suite.save()

                # Creating Test Cases
                testCases = glob.glob(directory + dr + "/tc*.sql")
                counter = 0
                for testcase in testCases:
                    with open(testcase) as reader:
                        first_line = reader.readline()
                        fline = "T"
                        #is_it = first_line == "FALSE"
                        #print(first_line + " is it FALSE ? ")
                        if first_line.__contains__("FALSE"):
                            fline = "F"
                        inserts = reader.read()
                        test_id = test_suite.test_suite_id + "-TC" + str(counter)
                        ts = TestCase(test_case_id = test_id, test_suite = test_suite, code = inserts, assertion = fline)
                        ts.save()
                        counter = counter + 1

    def handle(self, *args, **options):
        self._create_programs()

