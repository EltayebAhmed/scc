import unittest
from tests.system_tests.code_runner import run_code


class VariablesTester(unittest.TestCase):
    def test_simple_var_declaration(self):
        code = """
        void main() {
        int x;
        }
        """
        target_output = ""
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_simple_var_Assignment(self):
        code = """
            void main() {
            int x;
            x = 3;
            }
            """
        target_output = ""
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_simple_var_Assignment_in_Declaration(self):
        code = """
        void main() {
        int x = 3;
        }
        """
        target_output = ""
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_simple_var_Use(self):
        code = """
        void main() {
        int x = 3;
        printf("%i",x);
        }
        """
        target_output = "3"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_multiple_inline_declarations(self):
        code = """
        void main() {
        int x,y;
        }
        """
        target_output = ""
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_multiple_inline_declarations_and_Assignment(self):
        code = """
        void main() {
        int x = 2,y = 3;
        }
        """
        target_output = ""
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_multiple_inline_declarations_and_Assignment_different(self):
        code = """
        void main() {
        int x,y = 3;
        }
        """
        target_output = ""
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_multiple_inline_declarations_and_Assignment_and_Use(self):
        code = """
        void main() {
        int x = 2,y = 3;
        printf("%i %i",x,y);
        }
        """
        target_output = "2 3"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_nested_if_scope_Access_to_outside_scope(self):
        code = """
        void main() {
            int x = 99;
            if(x){
                printf("%d",x);
            }
        }
        """
        target_output = "99"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_nested_scope_access_to_scope_variables(self):
        code = """
        void main() {
        int x = 122;
            {

               printf("%i",x);
            }
        }
        """
        target_output = "122"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_access_to_global_variables(self):
        code = """
        int x;
        void main() {
            if(1){
                x = 2;
                printf("%i",x);
            }
        }
        """
        target_output = "2"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_access_of_multiple_scopes(self):
        code = """
        void main() {
            int z=1;
            {
                int x = 2;
               printf("%i  ",x);
            }

            {
                int y=7;
                printf("%i  %i",y,z);
            }
        }
        """
        target_output = "2  7  1"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_shadowing(self):
        code = """
        void main() {
            int x = 1;
            if(1){
                int x = 2;
               printf("%i",x);
            }
            printf("%i",x);
        }
        """
        target_output = "21"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_double_scopes(self):
        code = """
        void main() {
            int x = 0;
            {}

        }
        """
        target_output = ""
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)

    def test_variable_assignment_in_inner_scope(self):
        code = """
        void main() {
            int x = 12;
            printf("%d  ",x);
            { x = 3;
            printf("%d  ",x);
            }
        printf("%d",x);
        }
        """
        target_output = "12  3  3"
        scc_output = run_code(code)
        self.assertEquals(target_output, scc_output)



    if __name__ == "__main__":
        unittest.main()