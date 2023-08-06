import ast
import os
from pathlib import Path
import site
import subprocess
import sys
import unittest

from hypothesis import HealthCheck, given, settings
from hypothesmith import from_grammar

from bugbear import BugBearChecker, BugBearVisitor
from bugbear import (
    B001,
    B002,
    B003,
    B004,
    B005,
    B006,
    B007,
    B008,
    B009,
    B010,
    B011,
    B012,
    B013,
    B014,
    B015,
    B016,
    B301,
    B302,
    B303,
    B304,
    B305,
    B306,
    B901,
    B902,
    B903,
    B950,
)


class BugbearTestCase(unittest.TestCase):
    maxDiff = None

    def errors(self, *errors):
        return [BugBearChecker.adapt_error(e) for e in errors]

    def test_b001(self):
        filename = Path(__file__).absolute().parent / "b001.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B001(8, 0, vars=("bare `except:`",)),
            B001(40, 4, vars=("bare `except:`",)),
            B001(47, 0, vars=("`except ():`",)),
        )
        self.assertEqual(errors, expected)

    def test_b002(self):
        filename = Path(__file__).absolute().parent / "b002.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B002(15, 8), B002(20, 11)))

    def test_b003(self):
        filename = Path(__file__).absolute().parent / "b003.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B003(10, 0)))

    def test_b004(self):
        filename = Path(__file__).absolute().parent / "b004.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B004(3, 7), B004(5, 7)))

    def test_b005(self):
        filename = Path(__file__).absolute().parent / "b005.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B005(4, 0),
                B005(7, 0),
                B005(10, 0),
                B005(13, 0),
                B005(16, 0),
                B005(19, 0),
            ),
        )

    def test_b006_b008(self):
        filename = Path(__file__).absolute().parent / "b006_b008.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B006(26, 24),
                B006(30, 29),
                B006(34, 19),
                B006(38, 19),
                B006(42, 31),
                B008(51, 38),
                B006(67, 32),
                B008(95, 29),
                B008(99, 44),
            ),
        )

    def test_b007(self):
        filename = Path(__file__).absolute().parent / "b007.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B007(6, 4, vars=("i",)),
                B007(18, 12, vars=("k",)),
                B007(30, 4, vars=("i",)),
                B007(30, 12, vars=("k",)),
            ),
        )

    def test_b009_b010(self):
        filename = Path(__file__).absolute().parent / "b009_b010.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        all_errors = [
            B009(17, 0),
            B009(18, 0),
            B009(19, 0),
            B010(28, 0),
            B010(29, 0),
            B010(30, 0),
        ]
        self.assertEqual(errors, self.errors(*all_errors))

    def test_b011(self):
        filename = Path(__file__).absolute().parent / "b011.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors, self.errors(B011(8, 0, vars=("i",)), B011(10, 0, vars=("k",)))
        )

    def test_b012(self):
        filename = Path(__file__).absolute().parent / "b012.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        all_errors = [
            B012(5, 8),
            B012(13, 12),
            B012(21, 12),
            B012(31, 12),
            B012(44, 20),
            B012(66, 12),
            B012(78, 12),
            B012(94, 12),
            B012(101, 8),
            B012(107, 8),
        ]
        self.assertEqual(errors, self.errors(*all_errors))

    def test_b013(self):
        filename = Path(__file__).absolute().parent / "b013.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B013(10, 0, vars=("ValueError",)), B013(28, 0, vars=("re.error",))
        )
        self.assertEqual(errors, expected)

    def test_b014(self):
        filename = Path(__file__).absolute().parent / "b014.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B014(10, 0, vars=("Exception, TypeError", "", "Exception")),
            B014(16, 0, vars=("OSError, OSError", " as err", "OSError")),
            B014(27, 0, vars=("MyError, MyError", "", "MyError")),
            B014(41, 0, vars=("MyError, BaseException", " as e", "BaseException")),
            B014(48, 0, vars=("re.error, re.error", "", "re.error")),
            B014(
                55,
                0,
                vars=("IOError, EnvironmentError, OSError", "", "OSError"),
            ),
        )
        self.assertEqual(errors, expected)

    def test_b015(self):
        filename = Path(__file__).absolute().parent / "b015.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(B015(8, 0), B015(12, 0), B015(22, 4), B015(29, 4))
        self.assertEqual(errors, expected)

    def test_b016(self):
        filename = Path(__file__).absolute().parent / "b016.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(B016(6, 0), B016(7, 0), B016(8, 0))
        self.assertEqual(errors, expected)

    def test_b301_b302_b305(self):
        filename = Path(__file__).absolute().parent / "b301_b302_b305.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B301(39, 4),
                B301(40, 4),
                B301(41, 4),
                B301(42, 4),
                B302(43, 4),
                B302(44, 4),
                B302(45, 4),
                B302(46, 4),
                B305(47, 4),
                B305(48, 4),
            ),
        )

    def test_b303_b304(self):
        filename = Path(__file__).absolute().parent / "b303_b304.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B303(25, 4), B304(46, 4)))

    def test_b306(self):
        filename = Path(__file__).absolute().parent / "b306.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B306(9, 10)))

    def test_b901(self):
        filename = Path(__file__).absolute().parent / "b901.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B901(9, 8), B901(36, 4)))

    def test_b902(self):
        filename = Path(__file__).absolute().parent / "b902.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B902(29, 17, vars=("'i_am_special'", "instance", "self")),
                B902(32, 30, vars=("'cls'", "instance", "self")),
                B902(35, 4, vars=("(none)", "instance", "self")),
                B902(39, 12, vars=("'self'", "class", "cls")),
                B902(42, 22, vars=("*args", "instance", "self")),
                B902(48, 30, vars=("**kwargs", "instance", "self")),
                B902(51, 32, vars=("*, self", "instance", "self")),
                B902(54, 44, vars=("*, self", "instance", "self")),
                B902(68, 17, vars=("'self'", "metaclass instance", "cls")),
                B902(72, 20, vars=("'cls'", "metaclass class", "metacls")),
            ),
        )

    @unittest.skipIf(sys.version_info < (3, 8), "requires 3.8+")
    def test_b902_py38(self):
        filename = Path(__file__).absolute().parent / "b902_py38.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B902(29, 17, vars=("'i_am_special'", "instance", "self")),
                B902(32, 30, vars=("'cls'", "instance", "self")),
                B902(35, 4, vars=("(none)", "instance", "self")),
                B902(39, 12, vars=("'self'", "class", "cls")),
                B902(42, 22, vars=("*args", "instance", "self")),
                B902(48, 30, vars=("**kwargs", "instance", "self")),
                B902(51, 32, vars=("*, self", "instance", "self")),
                B902(54, 44, vars=("*, self", "instance", "self")),
                B902(68, 17, vars=("'self'", "metaclass instance", "cls")),
                B902(72, 20, vars=("'cls'", "metaclass class", "metacls")),
            ),
        )

    def test_b903(self):
        filename = Path(__file__).absolute().parent / "b903.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B903(32, 0), B903(38, 0)))

    def test_b950(self):
        filename = Path(__file__).absolute().parent / "b950.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B950(6, 92, vars=(92, 79))))

    def test_selfclean_bugbear(self):
        filename = Path(__file__).absolute().parent.parent / "bugbear.py"
        proc = subprocess.run(
            ["flake8", str(filename)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout.decode("utf8"))
        self.assertEqual(proc.stdout, b"")
        self.assertEqual(proc.stderr, b"")

    def test_selfclean_test_bugbear(self):
        filename = Path(__file__).absolute()
        proc = subprocess.run(
            ["flake8", str(filename)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout.decode("utf8"))
        self.assertEqual(proc.stdout, b"")
        self.assertEqual(proc.stderr, b"")


class TestFuzz(unittest.TestCase):
    @settings(suppress_health_check=[HealthCheck.too_slow])
    @given(from_grammar().map(ast.parse))
    def test_does_not_crash_on_any_valid_code(self, syntax_tree):
        # Given any syntatically-valid source code, flake8-bugbear should
        # not crash.  This tests doesn't check that we do the *right* thing,
        # just that we don't crash on valid-if-poorly-styled code!
        BugBearVisitor(filename="<string>", lines=[]).visit(syntax_tree)

    def test_does_not_crash_on_site_code(self):
        # Because the generator isn't perfect, we'll also test on all the code
        # we can easily find in our current Python environment - this includes
        # the standard library, and all installed packages.
        for base in sorted(set(site.PREFIXES)):
            for dirname, _, files in os.walk(base):
                for f in files:
                    if f.endswith(".py"):
                        BugBearChecker(filename=str(Path(dirname) / f))

    def test_does_not_crash_on_tuple_expansion_in_except_statement(self):
        # akin to test_does_not_crash_on_any_valid_code
        # but targets a rare case that's not covered by hypothesmith.from_grammar
        # see https://github.com/PyCQA/flake8-bugbear/issues/153
        syntax_tree = ast.parse(
            "grey_list = (ValueError,)\n"
            "black_list = (TypeError,)\n"
            "try:\n"
            "    int('1e3')\n"
            "except (*grey_list, *black_list):\n"
            "     print('error caught')"
        )
        BugBearVisitor(filename="<string>", lines=[]).visit(syntax_tree)


if __name__ == "__main__":
    unittest.main()
