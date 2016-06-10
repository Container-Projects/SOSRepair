__author__ = 'afsoona'

import os
import fnmatch
import logging
from settings import INTROCLASS_PATH, ALL_PATCHES
from profile.profile import *
from profile.tests import *
from fault_localization.suspicious_lines import *
from repository.snippet_preparation import *
from repository.db_manager import DatabaseManager
from repository.smt_solver import Z3
from repository.patch_generation import PatchGeneration
from utils.file_process import transform_file

logger = logging.getLogger(__name__)


def re_build_database(db_manager):
    db_manager.drop_tables()
    db_manager.initialize_tables()
    for root, dirs, files in os.walk(INTROCLASS_PATH):
        for items in fnmatch.filter(files, "*.c"):
            ff = os.path.join(root, items)
            ff = transform_file(ff)
            fl = CodeSnippetManager(ff)
            fl.detach_snippets()
            os.system('rm ' + ff)


def main():
    faulty_code = 'smallest.c'
    logger.info('***************************** %s' % faulty_code)
    faulty_code = transform_file(faulty_code)

    tests = Tests('', faulty_code)
    tests.initialize_testing()
    logger.debug('Tests %s' % str(tests))
    if len(tests.positives) == 0:
        print "No positive test!"
        return

    suspicious_lines = SuspiciousLines(faulty_code, '', tests)
    suspicious_lines.compute_suspiciousness()

    db_manager = DatabaseManager()
    # re_build_database(db_manager)

    fl = FaultLocalization(faulty_code)

    passing_patches = []
    os.system('rm -r patches')
    os.system('mkdir patches')
    for line, score in suspicious_lines.suspiciousness:
        logger.info("Suspicious line: %d ,score: %f" % (line, score))
        sb = fl.line_to_block(line)
        if not sb:
            logger.warning("No block found for line: %d" %line)
            continue
        logger.info("Suspicious block range %s" % str(sb.line_range))
        profile = Profile(faulty_code, sb)
        # profile.generate_file()
        # success = profile.generate_profile(tests.positives)
        success = profile.generate_gdb_script(tests.positives)
        logger.debug('Profile: ' + str(profile.input_list))
        if not success or not profile.input_list:
            continue

        z3 = Z3(sb, profile, db_manager)
        i = z3.fetch_valid_snippets()
        while i:
            res = z3.prepare_smt_query(i)
            for source, variables, mapping in res:
                patch_generation = PatchGeneration(source, variables, mapping)
                patch_generation.prepare_snippet_to_parse()
                ast = patch_generation.parse_snippet()
                patch_snippet = patch_generation.replace_vars(ast)
                patch_file = patch_generation.create_patch(sb, patch_snippet, patch_file='patches/patch'+str(len(passing_patches))+'.c')
                patch_test = Tests('', patch_file)
                success = patch_test.initialize_testing()
                if success and len(patch_test.negatives) == 0:
                    print "Found a patch!!! YAY"
                    passing_patches.append(patch_file)
                    if not ALL_PATCHES:
                        return
                    break
            i = z3.fetch_valid_snippets()


def main2():
    faulty_code = 'smallest.c'

    fl = CodeSnippetManager(faulty_code)
    fl.detach_snippets()

if __name__ == "__main__":
    main()
