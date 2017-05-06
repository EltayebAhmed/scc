import unittest
from tests.system_tests.code_runner import run_code

class ExpressionsTest(unittest.TestCase):
	def test_plus(self):
		code = """
		void main(){
			printf("1+2 = %d",1+2);
		}
		"""

		target_output = "1+2 = "+str(1+2)
		scc_output = run_code(code)

		self.assertEquals(target_output,scc_output)

	def test_plus_multiple_times(self):
		code = """
		void main(){
			printf("1+2+13 = %d",1+2+13);
		}
		"""

		target_output = "1+2+13 = "+str(1+2+13)
		scc_output = run_code(code)

		self.assertEquals(target_output,scc_output)

	def test_minus(self):
		code = """
		void main(){
			printf("2-1 = %d",2-1);
		}
		"""

		target_output = "2-1 = "+str(2-1)
		scc_output = run_code(code)

		self.assertEquals(target_output,scc_output)

	def test_minus_multiple_times(self):
		code = """
		void main(){
			printf("2-1-13 = %d",2-1-13);
		}
		"""

		target_output = "2-1-13 = "+str(2-1-13)
		scc_output = run_code(code)

		self.assertEquals(target_output,scc_output)

	
	def test_mul(self):
		code = """
		void main(){
			printf("2*3 = %d",2*3);
		}
		"""

		target_output = "2*3 = "+str(2*3)
		scc_output = run_code(code)

		self.assertEquals(target_output,scc_output)


	def test_mul_multiple_times(self):
		code = """
		void main(){
			printf("2*3*13 = %d",2*3*13);
		}
		"""

		target_output = "2*3*13 = "+str(2*3*13)
		scc_output = run_code(code)

		self.assertEquals(target_output,scc_output)

	def test_int_div(self):
		code = """
		void main(){
			printf("4//2 = %d",4//2);
		}
		"""

		target_output = "4//2 = "+str(4//2)
		scc_output = run_code(code)

		self.assertEquals(target_output,scc_output)

	def test_int_div_multiple_times(self):
		code = """
		void main(){
			printf("4//2//2 = %d",4//2//2);
		}
		"""

		target_output = "4//2//2 = "+str(4//2//2)
		scc_output = run_code(code)

		self.assertEquals(target_output,scc_output)


	def test_mul_div(self):
		code = """
			void main(){
				printf("5*6//2 = %d",5*6//2);
			}
		"""

		target_output = "5*6//2 = "+str(5*6//2)
		scc_output = run_code(code)

		self.assertEquals(target_output,scc_output)

	def test_precedence(self):
		code = """
		void main(){
			printf("1+2*3+4*(1+3)*2 = %d",1+2*3+4*(1+3)*2);
		}
		"""
		target_output = "1+2*3+4*(1+3)*2 = "+str(1+2*3+4*(1+3)*2)
		scc_output = run_code(code)

		self.assertEquals(target_output,scc_output)

	def test_unary_op(self):
		code = """
		void main(){
			printf("2--1 = %d",2--1);
		}
		"""

		target_output = "2--1 = "+str(2--1)
		scc_output = run_code(code)

		self.assertEquals(target_output,scc_output)


if __name__ == "__main__":
    unittest.main()