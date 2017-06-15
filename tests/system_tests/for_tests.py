import unittest
from tests.system_tests.code_runner import run_code

class ForTester(unittest.TestCase):

    def test_single_for_loop_with_initialization_condition_increment(self):
         code = """
             void main()
             {   int i;
                 for(i =0; i<5; i = i +1)
                     printf("%i ",i);
             }
             """
         target_output = "0 1 2 3 4 "
         scc_output = run_code(code)
         self.assertEqual(target_output, scc_output)

    def test_for_loop_with_no_initialization_inside_the_parentheses(self):
        code = """
             void main()
             {   int i = 0;
	                for(; i<5;i = i +1)
		            printf("%s","Hi ");
             }
             """

        target_output = "Hi Hi Hi Hi Hi "
        scc_output = run_code(code)
        self.assertEqual(target_output, scc_output)

    def test_for_loop_with_increment_inside_for_body(self):
            code = """
                 void main()
                 {   int i = 0;
    	                for( ; ; i = i +1)
    	                {
    		            printf("%i",i);
                            if (i == 6)
                                break;
    		            }
                 }
                 """
            target_output = "0 1 2 3 4 5 6 "
            scc_output = run_code(code)
            self.assertEqual(target_output, scc_output)

if __name__ == "__main__":
    unittest.main()