# interpreter.py
import sys
from parser import parser
from lexer import lexer

class KpopInterpreterError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class KpopInterpreter:
    def __init__(self):
        self.variables = {}
        self.debug = False

    def log(self, message):
        if self.debug:
            print(f"DEBUG: {message}")

    def interpret(self, code):
        ast = parser.parse(code, lexer=lexer)
        #self.log(f"AST: {ast}")
        self.execute_program(ast)

    def execute_program(self, node):
        #self.log(f"Executing program: {node}")
        _, _, block = node
        self.execute_block(block)

    def execute_block(self, statements):
        for statement in statements:
            #self.log(f"Executing statement: {statement}")
            self.execute_statement(statement)

    def execute_statement(self, statement):
        try:
            statement_type = statement[0]
            if statement_type == 'assign':
                self.execute_assignment(statement)
            elif statement_type == 'fighting':
                self.execute_if(statement)
            elif statement_type == 'dance':
                self.execute_while(statement)
            elif statement_type == 'comeback':
                self.execute_for(statement)
            elif statement_type == 'saranghae':
                self.execute_print(statement)
            elif statement_type == 'record':
                self.execute_record(statement)
            elif statement_type == 'playback':
                self.execute_playback(statement)
            else:
                raise KpopInterpreterError(f"Unknown statement type: {statement_type}")
        except KpopInterpreterError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def execute_assignment(self, statement):
        _, var_name, value = statement
        evaluated_value = self.evaluate_expression(value)
        #self.log(f"Assigning {var_name} = {evaluated_value}")
        self.variables[var_name] = evaluated_value

    def execute_if(self, statement):
        _, condition, if_block, else_block = statement
        if self.evaluate_expression(condition):
            #self.log("Executing if block")
            self.execute_block(if_block)
        elif else_block:
            #self.log("Executing else block")
            self.execute_block(else_block)

    def execute_while(self, statement):
        _, condition, block = statement
        max_iterations = 1000  # Safety measure
        iterations = 0
        while self.evaluate_expression(condition) and iterations < max_iterations:
            #self.log(f"While loop iteration {iterations}")
            self.execute_block(block)
            iterations += 1
        if iterations == max_iterations:
            print("WARNING: Max iterations reached in while loop")

    def execute_for(self, statement):
        _, init, condition, update, block = statement
        #self.log(f"For loop init: {init}")
        self.execute_statement(init)
        max_iterations = 100  # Safety measure
        iterations = 0
        while self.evaluate_expression(condition) and iterations < max_iterations:
            #self.log(f"For loop iteration {iterations}")
            self.execute_block(block)
            #self.log(f"For loop update: {update}")
            if (update[0] == 'bts'):
                var_name = update[1][1]  # Get the variable name
                value = self.evaluate_expression(update)
                self.variables[var_name] = value
                #self.log(f"Updated {var_name} to {value}")
            else:
                self.execute_statement(update)
            iterations += 1
        if iterations == max_iterations:
            print("WARNING: Max iterations reached in for loop")

    def execute_print(self, statement):
        _, value = statement
        print(self.evaluate_expression(value))

    def evaluate_expression(self, expression):
        #self.log(f"Evaluating expression: {expression}")
        try :
            if isinstance(expression, tuple):
                if expression[0] == 'number':
                    return int(expression[1])
                elif expression[0] == 'string':
                    return str(expression[1])
                elif expression[0] == 'boolean':
                    return bool(expression[1])
                elif expression[0] == 'id':
                    return self.variables.get(expression[1], 0)
                elif expression[0] == 'ikon':
                    return self.evaluate_expression(expression[1]) == self.evaluate_expression(expression[2])
                elif expression[0] == 'bts':
                    return self.evaluate_expression(expression[1]) + self.evaluate_expression(expression[2])
                elif expression[0] == 'bp':
                    return self.evaluate_expression(expression[1]) - self.evaluate_expression(expression[2])
                elif expression[0] == 'twice':
                    return self.evaluate_expression(expression[1]) * self.evaluate_expression(expression[2])
                elif expression[0] == 'rv':
                    divisor = self.evaluate_expression(expression[2])
                    if divisor == 0:
                        raise KpopInterpreterError("Division by zero")
                    return self.evaluate_expression(expression[1]) / divisor
                elif expression[0] == 'shinee':
                    return int(expression[1])
                elif expression[0] == 'bb':
                    return self.evaluate_expression(expression[1]) > self.evaluate_expression(expression[2])
                elif expression[0] == 'jyp':
                    return self.evaluate_expression(expression[1]) < self.evaluate_expression(expression[2])
                elif expression[0] == 'sj':
                    return self.evaluate_expression(expression[1]) >= self.evaluate_expression(expression[2])
                elif expression[0] == 'skz':
                    return self.evaluate_expression(expression[1]) <= self.evaluate_expression(expression[2])
                else: 
                    raise KpopInterpreterError(f"Unknown operation: {expression[0]}")
                return expression
        except KpopInterpreterError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected Error : {e}")
            return None
        
    def execute_record(self, statement):
        _, var_name = statement
        user_input = input()
        self.variables[var_name] = user_input

    def execute_playback(self, statement):
        _, value = statement
        output = self.evaluate_expression(value)
        print(output, end='')
        sys.stdout.flush()
    
    def interpret(self, code):
        try:
            ast = parser.parse(code, lexer=lexer)
            if ast is None:
                raise KpopInterpreterError("Parsing failed")
            self.execute_program(ast)
        except KpopInterpreterError as e:
            print(f"Error e : {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Test the interpreter
if __name__ == "__main__":
    interpreter = KpopInterpreter()
    test_code = '''
    annyeong main() {
      idol x = shinee 10 kpop
      idol y = gg "Hello, K-pop!" kpop
      idol z = exo true kpop
      fighting(x ikon shinee 5) {
        saranghae(x bts 10) kpop
      } daebak {
        saranghae(y) kpop
      }
      dance(x bp shinee 0) {
        saranghae(x) kpop
        idol x = x bp shinee 1 kpop
      }
      comeback(idol i = shinee 0 kpop i bp shinee 5 kpop i bts shinee 1) {
        saranghae(i) kpop
      }
      idol x = shinee 1 kpop
      fighting(x bb shinee 5) {
        saranghae("x is greater than 5") kpop
      } daebak {
        fighting(x jyp shinee 5) {
        saranghae("x is lesser than 5") kpop
        }
      }
      idol name = gg "" kpop
        saranghae("What's your name? ") kpop
        record(name) kpop
        playback("Hello, ") kpop
        playback(name) kpop
        playback("! Welcome to K-pop Programming!\\n") kpop
    }
    '''
    try :
        interpreter.interpret(test_code)
    except Exception as e:
        print(f"An error occurred while running the program: {e}")