'''
File name: parsers.py
Author: Michal Adamkiewicz
Date: 2014

This file implements the algebraic parsers using in logo.py
'''

import math

class HelperFunctions:
    "Convenient container for storing functions."
    def equ(x,y):
        if x==y:
            return 1
        return 0
   
    def mt(x,y):
        if x>y:
            return 1
        return 0

    
    def lt(x,y):
        if x<y:
            return 1
        return 0

class treeParser:
    "Customizable upon class creation number_variable only parser"

    operators=[{'@': HelperFunctions.equ,'<': HelperFunctions.lt,'>': HelperFunctions.mt},
   				{'+': lambda x, y: x+y,'-': lambda x, y: x-y,},
                {'*': lambda x, y: x*y , '/': lambda x, y: x/y},
                {'^': lambda x, y: x**y}]
    functions={'sin':math.sin,
                'cos':math.cos,
                'tan':math.tan,
                'asin':math.asin,
                'acos':math.acos,
                'atan':math.atan,
                'sqrt':math.sqrt}
    constants={'pi': math.pi, 'e': math.e}
    variables=[]

    def __init__(self,st):

        if(st[0]=='-'):
            st='0'+st

        found_match=self.operator_handle(st)
        if(found_match == 1): return

        #if passed has additioal parenthasis
        if(st[0]=='(' and st[-1]==')'):
            self.function= lambda x: x
            self.leaves=[self.__class__(st[1:-1])]
            return

        found_match=self.function_handle(st)
        if(found_match == 1): return

        self.singles_handle(st)

    def operator_handle(self,st):
        for level in self.operators:
            for op, func in level.items():
                braket_level=0
                for char in range(len(st)):

                    if(st[char]=='('): braket_level+=1
                    elif(st[char]==')'): braket_level-=1
                    elif(st[char]==op and braket_level==0): 
                        self.function=func
                        self.leaves=[]
                        self.leaves.append(self.__class__(st[:char]))
                        self.leaves.append(self.__class__(st[char-len(st)+1:]))
                        return 1

    def function_handle(self,st):
        for fu,func in self.functions.items():
            if(st[:len(fu)] == fu):
                self.function=func
                #todo multi argument
                # self.leaves=[self.__class__(st[len(fu)+1:-1])]
                self.leaves=list(map(self.__class__,st[len(fu)+1:-1].split(',')))
                return 1


    def singles_handle(self,st):
        #TODO: parse numbers better
        if(st in self.constants):
            self.function=self.constants[st]

        #Auto multyplication potencial?
        elif(st in self.variables):
            self.function=st

        else:
            self.function=float(st)


    def travel(self):

        if(type(self.function)==type(1.0)):
            def actual_function(*args):
                return self.function

        elif(self.function in self.variables):
            def actual_function(*args):
                return args[self.variables.index(self.function)]

        else:
            def actual_function(*args):
                return self.function(* map(lambda x: x.travel()(*args), self.leaves) )

        return actual_function

class DictParser(treeParser):
    'Customizable upon running parser'

    def singles_handle(self,st):

        #TODO: complex numbers
        if(st.lower() in self.constants):
            self.function=self.constants[st.lower()]
            return

        try:
            self.function=float(st)
        except ValueError:
            self.function=st


    def travel(self):

        if(type(self.function)==type(1.0)):
            def actual_function(**kargs):
                return self.function

        elif(type(self.function)==type(' ')):


            # if('[' in self.function and ']' in self.function):
            #     def actual_function(**kargs):
            #         return kargs[self.function.split('[')[0]][int(self.function.split('[',1)[1][:-1])]

            # else:
            #Next block indent changed to account for commented out code
            def actual_function(**kargs):
                return kargs[self.function]

        else:
            def actual_function(**kargs):
                return self.function(* map(lambda x: x.travel()(**kargs), self.leaves) )

        return actual_function

class HelperFunctions:
    "Convenient container for storing functions."
    def equ(x,y):
        if x==y:
            return 1
        return 0
   
    def mt(x,y):
        if x>y:
            return 1
        return 0

    
    def lt(x,y):
        if x<y:
            return 1
        return 0
