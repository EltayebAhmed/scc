import unittest
from tests.system_tests.code_runner import run_code

class FunceDefTester(unittest.TestCase):
    def test_simple_func_definition_assert_body_not_executed_without_call(self):
        code = """
        void aFunction(){
            printf("I should not be printed");
        }
        void main() {
            printf("hello world");
        }
        """
        target_output = "hello world"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_simple_func_def_and_call(self):
        code = """
        void afunction(){
            printf("-function was called-");
        }
        void main(){
            printf("main ");
            afunction();
            printf("  main again");
        }
        """
        target_output = "main " + "-function was called-" + "  main again"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_nested_func_def_and_call(self):
        code = """
        void functionB(){
            printf("B exec ");

        }
        void functionA(){
            printf("A in ");
            functionB();
            printf("A out ");
        }
        void main(){
            printf("main in ");
            afunction();
            printf("main out");
        }
        """
        target_output = "main in "+ "A in "+ "B exec " +  "A out "  + "main out"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)



if __name__ == "__main__":
    unittest.main()