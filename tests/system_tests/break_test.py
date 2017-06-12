import unittest
from tests.system_tests.code_runner import run_code


class BreakTest(unittest.TestCase):
    def test_with_while_loop(self):
        code = """
            void main(){
                while(1){
                    printf("H");
                    break;
                }
            }
        """
        target_output = "H"
        scc_output = run_code(code)
        self.assertEqual(target_output, scc_output)

    def test_with_variable_and_while(self):
        code = """
        void main() {
            int x=0;
            while (1){
                printf("Hello");
                break;
            }
            printf("%d",x);
        }
        """
        target_output = "Hello0"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)


if __name__ == "__main__":
    unittest.main()
