import unittest
from tests.system_tests.code_runner import run_code

class IfTester(unittest.TestCase):
    def test_single_if_true(self):
        code = """
        void main() {
        if (1)
            printf("hello world");
        }
        """
        target_output = "hello world"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_single_if_false(self):
        code = """
        void main() {
        if (0)
            printf("hello world");
        }
        """
        target_output = ""
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_single_if_true_else(self):
        code = """
        void main() {
        if (1)
            printf("nominal output");
        else
            printf("bad output");
        printf("always printed");
        }
        """
        target_output = "nominal output" + "always printed"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_single_if_false_else(self):

        code = """
        void main() {
        if (0)
            printf("expr is true output");
        else
            printf("expr is false");
        printf("always printed");
        }
        """
        target_output = "expr is false" + "always printed"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_chained_if_else_all_true(self):
        code = """
        void main() {
        if (1)
            printf("first branch");
        else if(1)
            printf("second branch");
        else if (1)
            printf("third branch");
        else
            printf ("fall back branch");
        printf("always printed");
        }
        """
        target_output = "first branch" + "always printed"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_chained_if_else_all_false(self):
        code = """
        void main() {
        if (0)
            printf("first branch");
        else if(0)
            printf("second branch");
        else if (0)
            printf("third branch");
        else
            printf ("fall back branch");
        printf("always printed");
        }
        """
        target_output = "fall back branch" + "always printed"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_chained_if_else_middle_branch(self):
        code = """
        void main() {
        if (0)
            printf("first branch");
        else if(0)
            printf("second branch");
        else if (1)
            printf("third branch");
        else
            printf ("fall back branch");
        printf("always printed");
        }
        """
        target_output = "third branch" + "always printed"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_if_true_else_multiple_statement_body(self):
        code = """
        void main() {
        if (1){
            printf("if print 1");
            printf("if print 2");
            }
        else{
            printf ("else print 1");
            printf ("else print 2");
            }
        printf(" always printed");
        }
        """
        target_output = "if print 1" + "if print 2" + " always printed"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_if_false_else_multiple_statement_body(self):
        code = """
        void main() {
        if (0){
            printf("if print 1");
            printf("if print 2");
            }
        else{
            printf ("else print 1");
            printf ("else print 2");
            }
        printf(" always printed");
        }
        """
        target_output = "else print 1" + "else print 2" + " always printed"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)



if __name__ == "__main__":
    unittest.main()