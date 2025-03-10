Running MeTTa in Python
Introduction
As Python has a broad range of applications, including web development, scientific and numeric computing, and especially AI, ML, and data analysis, its combined use with MeTTa significantly expands the possibilities of building AI systems. Both ways can be of interest:

embedding Python objects into MeTTa for serving as sub-symbolic (and, in particular, neural) components within a symbolic system;
using MeTTa from Python for defining knowledge, rules, functions, and variables which can be referred to in Python programs to create prompt templates for LLMs, logical reasoning, or compositions of multiple AI agents.
We start with the use of MeTTa from Python via high-level API, and then we will proceed to a tighter integration.

Setup
Firstly, you need to have MeTTa’s Python API installed as a Python package. MeTTa itself can be built from source with Python support and installed in the development mode in accordance with the instructions in the github repository. This approach is more involved, but it will yield the latest version with a number of configuration options.

However, for a quick start, hyperon package available via pip under Linux or MacOs (possibly except for newest processors):

bash
pip install hyperon
MeTTa runner class
The main interface class for MeTTa in Python is MeTTa class, which represents a runner built on top of the interpreter to execute MeTTa programs. It can be imported from hyperon package and its instance can be created and used to run MeTTa code directly:

python
from hyperon import MeTTa
metta = MeTTa()
result = metta.run('''
   (= (foo) boo)
   ! (foo)
   ! (match &self (= ($f) boo) $f)
''')
print(result) # [[boo], [foo]]
Reset
[[boo], [foo]]
The result of run is a list of results of all evaluated expressions (following the exclamation mark !). Each of this results is also a list (each containing one element in the example above). These results are not printed to the console by metta.run. They are just returned. Thus, we print them in Python.

Let us note that MeTTa instance preserve their program space after run has finished. Thus, run can be executed multiple times:

python
from hyperon import MeTTa
metta = MeTTa()
metta.run('''
	(Parent Tom Bob)
	(Parent Pam Bob)
	(Parent Tom Liz)
	(Parent Bob Ann)
''')
print(metta.run('!(match &self (Parent Tom $x) $x)')) # [[Liz, Bob]]
print(metta.run('!(match &self (Parent $x Bob) $x)')) # [[Tom, Pam]]
Reset
[[Liz, Bob]]
[[Tom, Pam]]
Parsing MeTTa code
The runner has methods for parsing a program code instead of executing it. Parsing produces MeTTa atoms wrapped into Python objects (so they can be manipulated from Python). Creating a simple expression atom (A B) looks like

python
atom = metta.parse_single('(A B)')
The parse_single() method parses only the next single token from the text program, thus the following example will give equivalent results

python
from hyperon import MeTTa
metta = MeTTa()
atom1 = metta.parse_single('(A B)')
atom2 = metta.parse_single('(A B) (C D)')
print(atom1) # (A B)
print(atom2) # (A B)
Reset
(A B)
(A B)
The parse_all() method can be used to parse the whole program code given in the string and get the list of atoms

python
from hyperon import MeTTa
metta = MeTTa()
program = metta.parse_all('(A B) (C D)')
print(program) # [(A B), (C D)]
Reset
[(A B), (C D)]
Accessing the program Space
Let us recall that Atomspace (or just Space) is a key component of MeTTa. It is essentially a knowledge representation database (which can be thought of as a metagraph) and the associated MeTTa functions are used for storing and manipulating information.

One can get a reference to the current program Space, which in turn may be accessed directly, wrapped in some way, or passed to the MeTTa interpreter. Having the reference, one can add new atoms into it using the add_atom() method

python
metta.space().add_atom(atom)
Now let us call the run() method that runs the code from the program string containing a symbolic expression

python
from hyperon import MeTTa
metta = MeTTa()
atom = metta.parse_single('(A B)')
metta.space().add_atom(atom)
print(metta.run("!(match &self (A $x) $x)")) # [[B]]
Reset
[[B]]
The program passed to run contains only one expression !(match &self (A $x) $x). It calls the match function for the pattern (A $x) and returns all matches for the $x variable. The result will be [[B]], which means that add_atom has added (A B) expression extracted from the string by parse_single. The code

python
atom = metta.parse_single('(A B)')
metta.space().add_atom(atom)
is effectively equivalent to

python
metta.run('(A B)')
because expressions are not preceded by ! are just added to the program Space.

Please note that

python
atom = metta.parse_all('(A B)')
is not precisely equivalent to

python
metta.run('! (A B)')[0]
Although the results can be identical, the expression passed to run will be evaluated and can get reduced:

python
from hyperon import MeTTa
metta = MeTTa()
print(metta.run('! (A B)')[0])    # [(A B)]
print(metta.run('! (+ 1 2)')[0])  # [3]
print(metta.parse_all('(A B)'))   # [(A B)]
print(metta.parse_all('(+ 1 2)')) # [(+ 1 2)]
Reset
[(A B)]
[3]
[(A B)]
[(+ 1 2)]
parse_single or parse_all are more useful, when we want not to add atoms to the program Space, but when we want to get these atoms without reduction and to process them further in Python.

Besides add_atom (and remove_atom as well), Space objects have query method.

python
metta = MeTTa()
metta.run('''
	(Parent Tom Bob)
	(Parent Pam Bob)
	(Parent Tom Liz)
	(Parent Bob Ann)
''')
pattern = metta.parse_single('(Parent $x Bob)')
print(metta.space().query(pattern)) # [{ $x <- Pam }, { $x <- Tom }]
Reset
[ { $x <- Tom },
 { $x <- Pam } ]
In contrast to match in MeTTa itself, query doesn't take the output pattern, but just returns options for variable bindings, which can be useful for further custom processing in Python. It would be useful to have a possibility to define patterns directly in Python instead of parsing them from strings.

MeTTa atoms in Python
Class Atom in Python (see its implementation) is used to wrap all atoms created in the backend of MeTTa into Python objects, so they can be manipulated in Python. An atom of any kind (metatype) can be created as an instance of this class, but classes SymbolAtom, VariableAtom, ExpressionAtom and GroundedAtom together with helper functions are inherited from Atom for convenience.

SymbolAtom
Symbol atoms are intended for representing both procedural and declarative knowledge entities for fully introspective processing. Such symbolic representations can be used and manipulated to infer new knowledge, make decisions, and learn from experience. It's a way of handling and processing abstract and arbitrary information.

The helper function S() is a convenient tool to construct an instance of SymbolAtom Python class. Its only specific method is get_name, since symbols are identified by their names. All instances of Atom has get_metatype method, which returns the atom metatype maintained by the backend.

python
from hyperon import S, SymbolAtom, Atom
symbol_atom = S('MyAtom')
print(symbol_atom.get_name()) # MyAtom
print(symbol_atom.get_metatype()) # AtomKind.SYMBOL
print(type(symbol_atom)) # SymbolAtom
print(isinstance(symbol_atom, SymbolAtom)) # True
print(isinstance(symbol_atom, Atom)) # True
Reset
MyAtom
AtomKind.SYMBOL
<class 'hyperon.atoms.SymbolAtom'>
True
True
Let us note that S('MyAtom') is a direct way to construct a symbol atom without calling the parser as in metta.parse_single('MyAtom'). It allows constructing symbols with the use of arbitrary characters, which can be not accepted by the parser.

VariableAtom
A VariableAtom represents a variable (typically in an expression). It serves as a placeholder that can be matched with, or bound to other Atoms. V() is a convenient method to construct a VariableAtom:

python
from hyperon import V
var_atom = V('x')
print(var_atom) # $x
print(var_atom.get_name()) # x
print(var_atom.get_metatype()) # AtomKind.VARIABLE
print(type(var_atom)) # VariableAtom
Reset
$x
x
AtomKind.VARIABLE
<class 'hyperon.atoms.VariableAtom'>
VariableAtom also has get_name method. Please note that variable names don't include $ prefix in internal representation. It is used in the program code for the parser to distinguish variables and symbols.

ExpressionAtom
An ExpressionAtom is a list of Atoms of any kind, including expressions. It has the get_children() method that returns a list of all children Atoms of an expression. E() is a convenient method to construct expressions, it takes a list of atoms as an input. The example below shows that queries can be constructed in Python and the resulting expressions can be processed in Python as well.

python
from hyperon import E, S, V, MeTTa

metta = MeTTa()
expr_atom = E(S('Parent'), V('x'), S('Bob'))
print(expr_atom) # (Parent $x Bob)
print(expr_atom.get_metatype()) # AtomKind.EXPR
print(expr_atom.get_children()) # [Parent, $x, Bob]
# Let us use expr_atom in the query
metta = MeTTa()
metta.run('''
	(Parent Tom Bob)
	(Parent Pam Bob)
	(Parent Tom Liz)
	(Parent Bob Ann)
''')
print(metta.space().query(expr_atom)) # [{ $x <- Pam }, { $x <- Tom }]
result = metta.run('! (match &self (Parent $x Bob) (Retrieved $x))')[0]
print(result) # [(Retrieved Tom) (Retrieved Pam)]
# Ignore 'Retrieved' in expressions and print Pam, Tom
for r in result:
	print(r.get_children()[1])
Reset
(Parent $x Bob)
AtomKind.EXPR
[Parent, $x, Bob]
[ { $x <- Tom },
 { $x <- Pam } ]
[(Retrieved Tom), (Retrieved Pam)]
Tom
Pam
GroundedAtom
GroundedAtom is a special subtype of Atom that makes a connection between the abstract, symbolically represented knowledge within AtomSpace and the external environment or the behaviors/actions in the outside world. Grounded Atoms often have an associated piece of program code that can be executed to produce specific output or trigger an action.

For example, this could be used to pull in data from external sources into the AtomSpace, to run a PyTorch model, to control an LLM agent, or to perform any other action that the system needs to interact with the external world, or just to perform intensive computations.

Besides the content, which a GroundedAtom wraps, there are three other aspects which can be customized:

the type of GroundedAtom (kept within the Atom itself);
the matching algorithm used by the Atom;
a GroundedAtom can be made executable, and used to apply sub-symbolic operations to other Atoms as arguments.
Let us start with basic usage. G() is a convenient method to construct a GroundedAtom. It can accept any Python object, which has copy method. In the program below, we construct an expression with a custom grounded atom and add it to the program Space. Then, we perform querying to retrieve this atom. GroundedAtom has get_object() method to extract the data wrapped into the atom.

python
from hyperon import *
metta = MeTTa()
entry = E(S('my-key'), G({'a': 1, 'b': 2}))
metta.space().add_atom(entry)
result = metta.run('! (match &self (my-key $x) $x)')[0][0]
print(type(result)) # GroundedAtom
print(result.get_object()) # {'a': 1, 'b': 2}
Reset
<class 'hyperon.atoms.GroundedAtom'>
{'a': 1, 'b': 2}
As the example shows, we can add a custom grounded object to the space, query and get it in MeTTa, and retrieve back to Python.

However, wrapping Python object directly to G() is typically not recommended. Python API for MeTTa implements a generic class GroundedObject with the field content storing a Python object of interest and the copy method. There are two inherited classes, ValueObject and OperationObject with some additional functionality. Methods ValueAtom and OperationAtom is a sugared way to construct G(ValueObject(...)) and G(OperationObject(...)) correspondingly. Thus, it would be preferable to use ValueAtom({'a': 1, 'b': 2}) in the code above, although one would need to write result.get_object().content to access the corresponding Python object (ValueObject has a getter value for content as well, while OperationObject uses op for this).

The constructor of GroundedObject accepts the content argument (a Python object) to be wrapped into the grounded atom and optionally the id argument (optional) for representing the atom and optionally for comparing atoms, when utilizing the content for this is not desirable. The ValueObject class adds the getter value for returning the content of the grounded atom.

Arguments of the OperationObject constructor include name, op, and unwrap. name serves as the id for the grounded atom, op (a function) defining the operation is used as the content of the grounded atom, and unwrap (a boolean, optional) indicates whether to unwrap the GroundedAtom content when applying the operation (see more on uwrap on the next page of this tutorial).

While there is a choice whether to use ValueAtom and OperationAtom classes for custom objects or to directly wrap them into G, grounded objects constructed in the MeTTa code are returned as such sugared atoms:

python
from hyperon import *
metta = MeTTa()
plus = metta.parse_single('+')
print(type(plus.get_object())) # OperationObject
print(plus.get_object().op) # some lambda
print(plus.get_object()) # + as a representation of this operation
calc = metta.run('! (+ 1 2)')[0][0]
print(type(calc.get_object())) # ValueObject
print(calc.get_object().value) # 3

metta.run('(my-secret-symbol 42)') # add the expression to the space
pattern = E(V('x'), ValueAtom(42))
print(metta.space().query(pattern)) # { $x <- my-secret-symbol }
Reset
<class 'hyperon.atoms.OperationObject'>
<function arithm_ops.<locals>.<lambda> at 0x7f38ae52f600>
+
<class 'hyperon.atoms.ValueObject'>
3
[ { $x <- my-secret-symbol } ]
As can be seen from the example, ValueAtom(42) can be matched against 42 appeared in the MeTTa program (although it is not recommended to use grounded atoms as keys for querying).

Apparently, there is a textual representation of grounded atoms, from which atoms themselves are built by the parser. But is it possible to introduce such textual representations for custom grounded atoms, so we could refer to them in the textual program code? The answer is yes. The Python and MeTTa API for this is described on the next page.



Pager
Parsing grounded atoms
Tokenizer
The MeTTa interpreter operates with the internal representation of programs in the form of atoms. Atoms can be constructed in the course of parsing or directly using the corresponding API. Let us examine what atoms are constructed by the parser. In the following program, we parse the expression (+ 1 S).

python
from hyperon import *
metta = MeTTa()
expr1 = metta.parse_single('(+ 1 S)')
expr2 = E(S('+'), S('1'), S('S'))
print('Expr1: ', expr1)
print('Expr2: ', expr2)
print('Equal: ', expr1 == expr2)
for atom in expr1.get_children():
    print(f'type({atom})={type(atom)}')
Reset
Expr1:  (+ 1 S)
Expr2:  (+ 1 S)
Equal:  False
type(+)=<class 'hyperon.atoms.GroundedAtom'>
type(1)=<class 'hyperon.atoms.GroundedAtom'>
type(S)=<class 'hyperon.atoms.SymbolAtom'>
The result of parsing differs from the expression (+ 1 S) composed of symbolic atoms. Indeed, the atoms constructed from + and 1 by the parser are grounded atoms - not symbols. At the same time, S('+') is already a symbol atom.

Transformation of the textual representation to grounded atoms is not hard-coded. It is done by the tokenizer on the base of a mapping from tokens in the form of regular expressions to constructors of corresponding grounded atoms.

The initial mapping is provided by the stdlib module, but it can be modified later. In the simple case, tokens are just strings. For example, the tokenizer is informed that if + is encountered in the course of parsing, the following atom should be constructed

python
OperationAtom('+', lambda a, b: a + b,
              ['Number', 'Number', 'Number'])
Here, ['Number', 'Number', 'Number'] is a sugared way to defined the type (-> Number Number Numer), which should also be represented as an atom.

Regular expressions are needed for such cases as parsing numbers. For example, integers are constructed on the base of the token r"[-+]?\d+", and the constructor needs to get the token itself, so the atom is created by the following function once the token is encountered

python
lambda token: ValueAtom(int(token), 'Number')
evaluate_atom
Once atoms are created, the interpreter doesn't rely on the tokenizer. Instances of MeTTa class have method evaluate_atom, which is the function accepting the atom to interpret.

python
from hyperon import *
metta = MeTTa()
expr1 = metta.parse_single('(+ 1 2)')
print(metta.evaluate_atom(expr1))
expr2 = E(OperationAtom('+', lambda a, b: a + b),
          ValueAtom(1), ValueAtom(2))
print(metta.evaluate_atom(expr2))
Reset
[3]
[3]
The example above shows that the parsed expression is interpreted in the same ways as the expression atom constructed directly. MeTTa.run simply parses the program code expression-by-expression and puts the resulting atoms in the program space or immediately interprets them when ! precedes the expression. Note that we could get the operation atom for + (which would be correctly typed) via metta.parse_single('+')

Creating new tokens
Access to the tokenizer is provided by the tokenizer() method of the MeTTa class. However, it may not be used directly. MeTTa class has the register_token method, which is intended for registering a new token. It accepts a regular expression and a function, which will be called to construct an atom each time the token is encountered. The constructed atom should not necessarily be a grounded atom, although it is the most typical case.

If the token is a mere string, and creation of different atoms depending on a regular expression is not supposed, register_atom can be used. It accepts a regular expression and an atom, and calls register_token with the given token and with the lambda simply returning the given atom.

The following example illustrates creation of an Atomspace and wrapping it into a GroundedAtom

python
from hyperon import *

metta = MeTTa()

# Getting a reference to a native GroundingSpace,
# implemented by the MeTTa core library.
grounding_space = GroundingSpaceRef()
grounding_space.add_atom(E(S("A"), S("B")))
space_atom = G(grounding_space)

# Registering a new custom token based on a regular expression.
# The new token can be used in a MeTTa program.
metta.register_atom("&space", space_atom)
print(metta.run("! (match &space (A $x) $x)"))
Reset
[[B]]
Parsing and interpretation
Although the interpreter works with the representation of programs in the form of atoms (as was mentioned above), and expressions should be parsed before being interpreted, the tokenizer can be changed in the course of MeTTa script execution. It is essential for the MeTTa module system (described in more detail in another tutorial).

import! is not only loads a module code into a space. It can also modify the tokenizer with tokens declared in the module. This is the reason why a MeTTa is not first entirely converted to atoms and then interpreted, but parsing and interpretation are intervened. Another approach would be to load all the atoms as symbols and resolve them at runtime, so the interpreter would verify if some symbols are grounded in subsymbolic data. This approach would have its benefits, and it might be chosen in the future versions of MeTTa. However, it would imply that introduction of new groundings to symbols has retrospective effect on the previous code.

We have also encountered creation of new tokens inside MeTTa programs with the use of bind! showing that token bindings don't have backward effect. The same is definitely true, when we create tokens using Python API:

python
from hyperon import *

# A function to be registered
def dup_str(s, n):
    r = ""
    for i in range(n):
        r += s
    return r

metta = MeTTa()
# Create an atom. "dup-str" is its internal name
dup_str_atom = OperationAtom("dup-str", dup_str)

# Interpreter will call this operation atom provided directly
print(metta.evaluate_atom(E(dup_str_atom, ValueAtom("-hello-"), ValueAtom(3))))

# Let us add a function calling `dup-str`
metta.run('''
  (= (test-dup-str) (dup-str "a" 2))
''')

# The parser doesn't know it, so dup-str will not be reduced
print(metta.run('''
 ! (dup-str "-hello-" 3)
 ! (test-dup-str)
'''))

# Now the token is registered. New expression will be reduced.
# However, `(= (test-dup-str) (dup-str "a" 2))` was added
# before `dup-str` token was introduced. Thus, it will still
# remain not reduced.
metta.register_atom("dup-str", dup_str_atom)
print(metta.run('''
! (dup-str "-hello-" 3)
! (test-dup-str)
'''))
Reset
["-hello--hello--hello-"]
[[(dup-str "-hello-" 3)], [(dup-str "a" 2)]]
[["-hello--hello--hello-"], [(dup-str "a" 2)]]
Kwargs for OperationAtom
Python supports variable number of arguments in functions. Such functions can be wrapped into grounded atoms as well.

python
from hyperon import *
def print_all(*args):
    for a in args:
        print(a)
    return [Atoms.UNIT]
metta = MeTTa()
metta.register_atom("print-all", OperationAtom("print-all", print_all))
metta.run('(print-all "Hello" (+ 40 2) "World")')
Reset
<empty string>
In cases when the function representing the operation has optional arguments with default values, the Kwargs keyword can be used to pass the keyword parameters. For example, let us define a grounded function find-pos which receives two strings and searches for the position of the second string in the first one. Let the default value for the second string be "a". Additionally, this function has the third parameter which specifies whether the search should start from the left or the right, with the default value being left=True.

python
from hyperon import *
def find_pos(x:str, y="a", left=True):
    if left:
        return x.find(y)
    pos = x[-1:].find(y)
    return len(x) - 1 - pos if pos >= 0 else pos
metta = MeTTa()
metta.register_atom("find-pos", OperationAtom("find-pos", find_pos))
print(metta.run('''
 ! (find-pos "alpha") ; 0
 ! (find-pos (Kwargs (x "alpha") (left False))) ; 4
 ! (find-pos (Kwargs (x "alpha") (y "c") (left False))) ; -1
'''))
Reset
[[0], [4], [-1]]
Hence, to set argument values using Kwargs, one needs to pass pairs of argument names and values.

Unwrapping Python objects from atoms
Above, we have introduced a summation operation as OperationAtom('+', lambda a, b: a + b),where a and b are Python numbers instead of atoms. a + b is also not an atom. Creating of operation atoms getting Python objects is convenient, because it eliminates the necessity to retrieve values from grounded atoms and wrap the result of the operation back to the grounded atom. However, sometimes it is needed to write functions that operate with atoms themselves, and these atoms may not be grounded atoms wrapping Python objects.

Unwrapping Python values from input atoms and wrapping the result back into a grounded atom is the default behavior of OperationAtom, which is controlled by the parameter unwrap. Let us consider an example of implementing + while setting this parameter to False.

python
def plus(atom1, atom2):
    from hyperon import ValueAtom
    sum = atom1.get_object().value + atom2.get_object().value
    return [ValueAtom(sum, 'Number')]

from hyperon import OperationAtom, MeTTa
plus_atom = OperationAtom("plus", plus,
    ['Number', 'Number', 'Number'], unwrap=False)
metta = MeTTa()
metta.register_atom("plus", plus_atom)
print(metta.run('! (plus 3 5)'))
Reset
[[8]]
When unwrap is False, a function should be aware of the hyperon module, which can be inconvenient for purely Python functions. Thus, this setting is desirable for functions processing or creating atoms themselves. For example, bind! takes an atom to be bound to a token. parse takes a string and return an atom of any metatype constructed by parsing this string. One can imagine different custom operations, which accept and return atoms. Say, if a crossover operation in genetic algorithms would be implemented as a grounded operation, it would accept two atoms (typically, expressions), traverse them to find crossover points, and construct a child expression.


-----
Embedding Python objects into MeTTa
py-atom
Introducing tokens for grounded atoms allows for both convenient syntax and direct representation of expressions with corresponding grounded atoms in a Space. However, wrapping all functions of rich Python libraries can be not always desirable. There is a way to invoke Python objects such as functions, classes, methods or other statements from MeTTa without additional Python code wrapping these objects into atoms.

py-atom allows obtaining a grounded atom for a Python object imported from a given module or submodule. Let us consider usage of numpy as an example, which should be installed. For instance, the absolute value of a number in MeTTa can be calculated by employing the absolute function from the numpy library:

metta
! ((py-atom numpy.absolute) -5) ; 5
Reset
[np.int64(5)]
Here, py-atom imports numpy library and returns an atom associated with the numpy.absolute function.

It is possible to designate types for the grounded atom in py-atom. For convenience, one can associate the result of py-atom with a token using bind!:

metta
! (bind! abs (py-atom numpy.absolute (-> Number Number)))
! (+ (abs -5) 10) ; 15
Reset
[()]
[np.int64(15)]
We specify here that the constructed grounded operation can accept an argument of type Number and its result will be of Number type.

When (abs -5) is executed, it triggers a call to absolute(-5). It can be seen that the results of executing Python objects imported via py-atom can then be directly utilized in other MeTTa expressions.

py-atom can actually execute some Python code, which shouldn't be a statement like x = 42, but should be an expression, which evaluation produces a Python object. In the following example, (py-atom "[1, 2, 3]") produces a Python list, which then passed to numpy.array.

metta
! (bind! np-array (py-atom numpy.array))
! (np-array (py-atom "[1, 2, 3]")) ; array([1, 2, 3])
Reset
[()]
[array([1, 2, 3])]
py-atom can be applied to functions accepting keyword arguments. Constructed grounded atoms will also support Kwargs (mentioned earlier), which allows for passing only the required arguments to the function while skipping arguments with default values. For example, there is numpy.arange in NumPy, which returns evenly spaced values within a given interval. numpy.arange can be called with a varying number of positional arguments:

metta
! (bind! np-arange (py-atom numpy.arange)) ; ()
! (np-arange 4) ; array([0, 1, 2, 3])
! (np-arange (Kwargs (step 2) (stop 8))) ; array([0, 2, 4, 6])
! (np-arange (Kwargs (start 2) (stop 10) (step 3))) ; array([2, 5, 8])
Reset
[()]
[array([0, 1, 2, 3])]
[array([0, 2, 4, 6])]
[array([2, 5, 8])]
py-dot
What if we wish to call functions from a submodule, say numpy.random? Accessing these functions via something like (py-atom numpy.random.randint) will work. However, it would be more efficient to get numpy.random itself as a Python object and access other objects in it. py-dot is introduced to carry out this operation.

metta
! (bind! np-rnd (py-atom numpy.random))
! ((py-dot np-rnd randint) 25)
Reset
[()]
[3]
In this case py-dot operates with two arguments: it takes the first argument, which is the grounded atom wrapping a Python object, and then searches for the value of an attribute within that object based on the name provided in the second argument.

This second argument can also contain objects in submodules. In the following example, we wrap numpy in the grounded atom:

metta
! (bind! np (py-atom numpy))
! ((py-dot np abs) -5)
! ((py-dot np random.randint) -25 0)
! ((py-dot np abs) ((py-dot np random.randint) -25 0))
Reset
[()]
[np.int64(5)]
[-18]
[np.int64(3)]
Here, when (py-dot np random.randint) is executed, it takes numpy object and searches for random in it and then for randint in random. The overall result is the grounded operation wrapping numpy.random.randint, which is then applied to some argument. Similar to py-atom, py-dot also permits the designation of types for the function, and supports Kwargs for arguments specification.

Binding np to (py-atom numpy) and accessing functions in it via (py-dot np abs) looks not more convenient than just using (py-atom numpy.abs), but is slightly more efficient if numpy.abs is accessed multiple times.

py-dot works for any Python object - not only modules:

metta
! ((py-dot "Hello World" swapcase)) ; "hELLO wORLD"
Reset
["hELLO wORLD"]
Notice the additional brackets to call swapcase. The equivalent Python code is "Hello World".swapcase(), which also contains (). One more pair of brackets in MeTTa is needed, because py-dot is also a function.

Let us consider another example.

metta
! ((py-dot (py-atom "{5: \'f\', 6: \'b\'}") get) 5)
Reset
["f"]
Here, a dictionary {5: 'f', 6: 'b'} is created by py-atom, and then the value corresponding to the key 5 is retrieved from this dictionary using get accessed via py-dot.

py-list, py-tuple, py-dict
While it is possible to create Python lists and dictionaries using code evaluation by py-atom, it can be desirable to construct these data structures by combining atoms in MeTTa.

In this context, since passing dictionaries, lists or tuples as arguments to functions in Python is very common, such dedicated functions as py-dict, py-list and py-tuple were introduced.

metta
! ((py-atom max) (py-list (-5 5 -3 10 8))) ; 10
! ((py-atom numpy.inner)
     (py-list (1 2)) (py-list (3 4))) ; 1 * 3 + 2 * 4 = 11
Reset
[10]
[np.int64(11)]
In this example, py-list generates three Python lists: [-5, 5, -3, 10, 8] , [1,2] and [3,4], which are passed to max and numpy.inner.

Of course, one can use py-dict, py-list, and py-tuple independently - not just as function arguments:

metta
! (py-dict (("a" "b") ("b" "c"))) ; creates a dict {"a":"b", "b":"c"}
! (py-tuple (1 5)) ; creates a tuple (1, 5)
! (py-list (1 (2 (3 "3")))) ; creates a nested list [1, [2, [3, '3']]]
Reset
[{'a': 'b', 'b': 'c'}]
[(1, 5)]
[[1, [2, [3, '3']]]]
Pager
---


METTA LIBRARY FUNCTIONS 




Mathematical Operations¶
pow-math¶
Description: Calculates the power of a base raised to an exponent.

Parameters:
Base: The base number.

Power: The exponent.

Return: The result of the power function.

Example:

!(pow-math 2 3) ; Returns 8.0
sqrt-math¶
Description: Calculates the square root of a number.

Parameters:
Number: The number to calculate the square root of. Must be >= 0.

Return: The square root of the number.

Example:

!(sqrt-math 9) ; Returns 3.0
abs-math¶
Description: Calculates the absolute value of a number.

Parameters:
Number: The number to calculate the absolute value of.

Return: The absolute value of the number.

Example:

!(abs-math -5) ; Returns 5
log-math¶
Description: Calculates the logarithm of a number with a given base.

Parameters:
Base: The base of the logarithm.

Number: The number to calculate the logarithm of.

Return: The result of the logarithm function.

Example:

!(log-math 10 100) ; Returns 2.0
trunc-math¶
Description: Returns the integer part of the input value

Parameters:
Float: Input float value

Return: Integer part of float

Example:

!(trunc-math 5.6) ; Returns 5.0
ceil-math¶
Description: Returns the smallest integer greater than or equal to the input value

Parameters:
Float: Input float value

Return: Integer value greater than or equal to the input

Example:

!(ceil-math 5.2) ; Returns 6.0
floor-math¶
Description: Returns the smallest integer less than or equal to the input value

Parameters:
Float: Input float value

Return: Integer value less than or equal to the input

Example:

!(floor-math 5.8) ; Returns 5.0
round-math¶
Description: Returns the nearest integer to the input float value

Parameters:
Float: Input float value

Return: Nearest integer to the input

Example:

!(round-math 5.4) ; Returns 5.0
!(round-math 5.6) ; Returns 6.0
sin-math¶
Description: Returns result of the sine function for an input value in radians

Parameters:
Angle: Angle in radians

Return: Result of the sine function

Example:

!(sin-math 0) ; Returns 0.0
asin-math¶
Description: Returns result of the arcsine function for an input value

Parameters:
Float: Input float value

Return: Result of the arcsine function

Example:

!(asin-math 0) ; Returns 0.0
cos-math¶
Description: Returns result of the cosine function for an input value in radians

Parameters:
Angle: Angle in radians

Return: Result of the cosine function

Example:

!(cos-math 0) ; Returns 1.0
acos-math¶
Description: Returns result of the arccosine function for an input value

Parameters:
Float: Input float value

Return: Result of the arccosine function

Example:

!(acos-math 1) ; Returns 0.0
tan-math¶
Description: Returns result of the tangent function for an input value in radians

Parameters:
Angle: Angle in radians

Return: Result of the tangent function

Example:

!(tan-math 0) ; Returns 0.0
atan-math¶
Description: Returns result of the arctangent function for an input value

Parameters:
Float: Input float value

Return: Result of the arctangent function

Example:

!(atan-math 0) ; Returns 0.0
isnan-math¶
Description: Returns True if input value is NaN. False - otherwise

Parameters:
Number: Number

Return: True/False

Example:

!(isnan-math 0.0) ; Returns False
isinf-math¶
Description: Returns True if input value is positive or negative infinity. False - otherwise

Parameters:
Number: Number

Return: True/False

Example:

!(isinf-math 0.0) ; Returns False
min-atom¶
Description: Returns atom with min value in the expression. Only numbers allowed

Parameters:
Expression: Expression which contains atoms of Number type

Return: Min value in the expression. Error if expression contains non-numeric value or is empty

Example:

!(min-atom (2 6 7 4 9 3)) ; Returns 2.0
max-atom¶
Description: Returns atom with max value in the expression. Only numbers allowed

Parameters:
Expression: Expression which contains atoms of Number type

Return: Max value in the expression. Error if expression contains non-numeric value or is empty

Example:

!(max-atom (2 6 7 4 9 3)) ; Returns 9.0
random-int¶
Description: Returns random int number from range defined by two numbers

Parameters:
Range start: Range start

Range end: Range end

Return: Random int number from defined range

Example:

!(random-int 2 9) ; Returns any int number between 2 to 9
random-float¶
Description: Returns random float number from range defined by two numbers

Parameters:
Range start: Range start

Range end: Range end

Return: Random float number from defined range

Example:

!(random-float 2 9) ; Returns any number in the interval [2, 9)


Non-deterministic Computation¶
collapse-bind¶
Description: Evaluates a MeTTa operation and returns an expression containing all alternative evaluations in the form (Atom Bindings).

Parameters:
Atom: The MeTTa operation to be evaluated.

Return: An expression of alternative evaluations with bindings.

Example:

(= (bin) 0)
(= (bin) 1)
!(collapse-bind (bin)) ; Returns (0 { }), (1 { }) nondeterministically
superpose-bind¶
Description: Takes the result of collapse-bind and returns only the result atoms, discarding the bindings.

Parameters:
Expression: An expression in the form (Atom Bindings).

Return: A non-deterministic list of atoms.

Example:

!(superpose-bind ((A (Grounded ...)) (B (Grounded ...)))) ; returns the equivalent of (superpose (A B))
superpose¶
Description: Turns a tuple into a nondeterministic result.

Parameters:
Tuple: Tuple to be converted.

Return: Argument converted to nondeterministic result

Example:

!(superpose (A B C)) ; returns A, B, C nondeterministically
collapse¶
Description: Converts a nondeterministic result into a tuple.

Parameters:
Atom: Atom which will be evaluated.

Return: Tuple

Example:

!(collapse (superpose (A B C))) ; returns (A B C)


Type System¶
is-function¶
Description: Checks if a type is a function type.

Parameters:
Type: The type atom to be checked.

Return: True if the type is a function type, False otherwise.

Example:

!(is-function (-> Atom Atom)) ; Returns True
!(is-function Atom) ; Returns False
type-cast¶
Description: Attempts to cast an atom to a specific type within an atomspace context.

Parameters:
Atom: The atom to cast.

Type: The target type.

Space: The atomspace to use as context.

Return: The atom if casting is successful, or an Error atom if not.

Example:

(: type1 Type)
!(type-cast A type1 &self) ; A
!(type-cast 1 type1 &self) ; Error 1 BasType
match-types¶
Description: Checks if two types can be unified and returns one value if so, another - otherwise.

Parameters:
Type1: The first type.

Type2: The second type.

Then: Atom to be returned if types can be unified.

Else: Atom to be returned if types cannot be unified.

Return: Third or fourth argument

Example:

!(match-types Atom Atom "Matched!" "Didn't match") ; Returns "Matched!"
!(match-types Atom Number "Matched!" "Didn't match") ; Returns "Didn't match"
first-from-pair¶
Description: Gets a pair as a first argument and returns first atom from pair.

Parameters:
Pair: Pair.

Return: First atom from a pair.

Example:

!(first-from-pair (A B)) ; Returns A
match-type-or¶
Description: Checks if two types can be unified and returns result of OR operation between first argument and type checking result.

Parameters:
Folded: Boolean value

Next: First type.

Type: Second type.

Return: True or False

Example:

!(match-type-or True Number Number) ; Returns True
!(match-type-or False Number Number) ; Returns True
!(match-type-or True Number Bool) ; Returns True
!(match-type-or False Number Bool) ; Returns False


List Manipulation¶
filter-atom¶
Description: Filters a list of atoms based on a predicate.

Parameters:
List: The list of atoms to filter.

Variable: The variable to use in the predicate.

Filter: The predicate to apply (an expression that returns True or False).

Return: A new list containing only the atoms that satisfy the predicate.

Example:

!(filter-atom (1 2 3 4 5) $x (> $x 3)) ; Returns (4 5)
map-atom¶
Description: Applies a function to each atom in a list, creating a new list with the results.

Parameters:
List: The list of atoms to map over.

Variable: The variable to use in the mapping expression.

Map: The expression to apply to each atom.

Return: A new list with the mapped values.

Example:

!(map-atom (1 2 3) $x (+ $x 1)) ; Returns (2 3 4)
foldl-atom¶
Description: Folds (reduces) a list of values into a single value, using a binary operation. This is a left fold.

Parameters:
List: The list of values to fold.

Init: The initial value.

A: The variable to hold the accumulated value.

B: The variable to hold the current element of the list.

Op: The binary operation to apply (an expression using A and B).

Return: The final accumulated value.

Example:

!(foldl-atom (1 2 3 4) 0 $acc $x (+ $acc $x)) ; Returns 10 (1+2+3+4)



Atomspace Interaction¶
add-reduct¶
Description: Reduces an atom and adds it to the atomspace.

Parameters:
Space: The atomspace to add the atom to.

Atom: The atom to be added.

Return: Unit atom

Example:

!(add-reduct &self (= (add) (+ 1 3))); This will add (= (add) 4) to the working space, &self
add-atom¶
Description: Adds an atom into the atomspace without reducing it.

Parameters:
Space: Atomspace to add atom into

Atom: Atom to be added

Return: Unit atom

Example:

!(add-atom &self (= (add) (+ 1 3))); This will add (= (add) (+ 1 3)) to the working space, &self
get-type¶
Description: Returns type notation of input atom.

Parameters:
Atom: Atom to get type for

Return: Type notation or %Undefined% if there is no type for input Atom

Example:

!(get-type 1) ; Returns Number
get-type-space¶
Description: Returns type notation of input Atom relative to a specified atomspace.

Parameters:
Space: Atomspace where type notation for input atom will be searched

Atom: Atom to get type for

Return: Type notation or %Undefined% if there is no type for input Atom in provided atomspace

Example:

(: a A)
!(get-type-space &self a); Returns A because we defined the type of a to be A in the working space, &self
get-metatype¶
Description: Returns metatype of the input atom

Parameters:
Atom: Atom to get metatype for

Return: Metatype of input atom

Example:

!(get-metatype True); Returns Grounded
!(get-metatype (a b)); Return Expression
if-equal¶
Description: Checks if first two arguments are equal and evaluates third argument if equal, fourth argument - otherwise.

Parameters:
Arg1: First argument

Arg2: Second argument

Then: Atom to be evaluated if arguments are equal

Else: Atom to be evaluated if arguments are not equal

Return: Evaluated third or fourth argument

Example:

!(if-equal 1 1 "Equal" "Not Equal"); Returns "Equal"
!(if-equal 1 2 "Equal" "Not Equal"); Returns "Not Equal"
new-space¶
Description: Creates new Atomspace which could be used further in the program as a separate from &self Atomspace

Parameters:
None

Return: Reference to a new space

Example:

!(new-space); Returns reference to the new space
remove-atom¶
Description: Removes atom from the input Atomspace

Parameters:
Space: Reference to the space from which the Atom needs to be removed

Atom: Atom to be removed

Return: Unit atom

Example:

!(remove-atom &self (= (add) 4)); Removes (= (add) 4) from the working space, &self
get-atoms¶
Description: Shows all atoms in the input Atomspace

Parameters:
Space: Reference to the space

Return: List of all atoms in the input space

Example:

!(get-atoms &self); Returns all atoms inside &self
match¶
Description: Searches for all declared atoms corresponding to the given pattern inside space and returns the output template

Parameters:
Space: Atomspace to search pattern

Pattern: Pattern atom to be searched

Output: Output template typically containing variables from the input pattern

Return: If match was successfull it outputs template with filled variables using matched pattern. Empty - otherwise

Example:

(= (add) (+ 1 2))
(= (add) (+ 4 2))
!(match &self (= (add) (+ $x $y)) $x); Returns 1, 4



Quoting¶
quote¶
Description: Prevents an atom from being reduced.

Parameters:
Atom: The atom to be quoted.

Return: The quoted atom (which will not be evaluated).

Example:

!(quote (+ 1 2)) ; Returns (+ 1 2) instead of 3
unquote¶
Description: Removes the quote from a quoted atom.

Parameters:
QuotedAtom: The atom to unquote.

Return: The original, unquoted atom.

Example:

!(unquote (quote (+ 1 2))) ; Returns 3
noreduce-eq¶
Description: Checks equality of two atoms without reducing them.

Parameters:
A: First atom

B: Second atom

Return: True if not reduced atoms are equal, False - otherwise

Example:

!(noreduce-eq (+ 1 2) (+ 1 2)) ; Returns True
!(noreduce-eq (+ 1 2) 3) ; Returns False


Set Operations¶
unique¶
Description: Returns unique entities from non-deterministic input.

Parameters:
Arg: Non-deterministic set of values

Return: Unique values from input set

Example:

!(unique (superpose (a b c d d))) ; Returns [a, b, c, d]
union¶
Description: Returns union of two non-deterministic inputs.

Parameters:
Arg1: Non-deterministic set of values

Arg2: Another non-deterministic set of values

Return: Union of sets

Example:

!(union (superpose (a b b c)) (superpose (b c c d))) ; Returns [a, b, b, c, b, c, c, d]
intersection¶
Description: Returns intersection of two non-deterministic inputs.

Parameters:
Arg1: Non-deterministic set of values

Arg2: Another non-deterministic set of values

Return: Intersection of sets

Example:

!(intersection (superpose (a b c c)) (superpose (b c c c d))) ; Returns [b, c, c]
subtraction¶
Description: Returns subtraction of two non-deterministic inputs.

Parameters:
Arg1: Non-deterministic set of values

Arg2: Another non-deterministic set of values

Return: Subtraction of sets

Example:

!(subtraction (superpose (a b b c)) (superpose (b c c d))) ; Returns [a, b]
unique-atom¶
Description: Function takes tuple and returns only unique entities

Parameters:
List: List of values

Return: Unique values from input set

Example:

!(unique-atom (a b c d d)) ; Returns (a b c d)
union-atom¶
Description: Function takes two tuples and returns their union

Parameters:
List1: List of values

List2: List of values

Return: Union of sets

Example:

!(union-atom (a b b c) (b c c d)) ; Returns (a b b c b c c d)
intersection-atom¶
Description: Function takes two tuples and returns their intersection

Parameters:
List1: List of values

List2: List of values

Return: Intersection of sets

Example:

!(intersection-atom (a b c c) (b c c c d)) ; Returns (b c c)
subtraction-atom¶
Description: Function takes two tuples and returns their subtraction

Parameters:
List1: List of values

List2: List of values

Return: Subtraction of sets

Example:

!(subtraction-atom (a b b c) (b c c d)) ; Returns (a b)