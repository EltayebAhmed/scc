import unittest
from tests.system_tests.code_runner import run_code


class PointersTester(unittest.TestCase):
    def test_pointer(self):
        code = """
        void main() {
        int x = 1;
        int* y = &x;
        printf("%i",*y);
        }
        """
        target_output = "1"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_pointer_two(self):
        code = """
        void main() {
        int y = 1;
        int *x = &y;
        *x = 2;
        printf("%i",y);
        }
        """
        target_output = "2"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

if __name__ == "__main__":
    unittest.main()