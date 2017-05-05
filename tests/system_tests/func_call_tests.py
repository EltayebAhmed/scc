import unittest
from tests.system_tests.code_runner import run_code

class FuncCallTester(unittest.TestCase):
    def test_simple_func_call(self):
        code = """
        void main() {printf("hello world");}
        """
        target_output = "hello world"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_func_call_multiple_parameters(self):
        code = """
        void main(){printf("number : %d %s", 12, "string 2");}
        """
        target_output = "number : 12 string 2"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

if __name__ == "__main__":
    unittest.main()