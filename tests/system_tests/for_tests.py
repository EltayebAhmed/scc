import unittest
from tests.system_tests.code_runner import run_code

class ForWhileTests(unittest.TestCase):
    def test_single_for_loop(self):
        code = """
        void main()
        {   int i;
            for(i =0; i<5; i = i +1)
                printf("%i ",i);
        }
        """
        target_output = "0 1 2 3 4 "
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)


if __name__ == "__main__":
    unittest.main()