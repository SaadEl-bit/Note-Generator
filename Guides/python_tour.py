# -*- coding: utf-8 -*-
"""
================================================================================
  PYTHON SYNTAX TOUR — For Developers Coming from C and Java
================================================================================

  This file walks through the core Python programming tools:
    1. Variables & Types
    2. Operators
    3. Strings
    4. Control Flow (if / elif / else)
    5. Loops (for / while)
    6. Functions
    7. Collections (list, tuple, dict, set)
    8. List/Dict Comprehensions
    9. Lambda & Higher-Order Functions
   10. Classes & OOP
   11. Inheritance & Polymorphism
   12. Exception Handling
   13. File I/O
   14. Modules & Imports
   15. Decorators
   16. Generators & Iterators
   17. Context Managers (with statement)

  KEY DIFFERENCES VS C / JAVA (reminders scattered throughout):
    • No semicolons at line ends
    • Indentation replaces { } braces for blocks
    • No explicit type declarations (dynamic typing)
    • No need for main() unless you want entry-point guards
================================================================================
"""

# ─────────────────────────────────────────────────────────────────
# 0. ENTRY-POINT GUARD (equivalent of Java's main / C's main())
# ─────────────────────────────────────────────────────────────────
# In Python you use:  if __name__ == "__main__":
# Code OUTSIDE this block runs when the file is imported as a module too.
# Code INSIDE only runs when the file is executed directly.

def run_all():
    """Run every section in sequence."""
    section_variables()
    section_operators()
    section_strings()
    section_control_flow()
    section_loops()
    section_functions()
    section_collections()
    section_comprehensions()
    section_lambda_hof()
    section_oop()
    section_exceptions()
    section_file_io()
    section_decorators()
    section_generators()
    section_context_managers()
    print("\n✅  Tour complete!")


# ═══════════════════════════════════════════════════════════════════
# 1. VARIABLES & TYPES
# ═══════════════════════════════════════════════════════════════════
def section_variables():
    print("\n" + "═"*60)
    print("  §1 — VARIABLES & TYPES")
    print("═"*60)

    # ── No type keyword needed (unlike int x = 5; in C/Java) ──────
    x = 10          # int
    y = 3.14         # float
    z = 2 + 3j       # complex  (no direct C/Java equivalent)
    is_ok = True     # bool — capital T/F, NOT true/false like Java
    name = "Python"  # str — single or double quotes both valid
    nothing = None   # None — equivalent of null (Java) / NULL (C)

    print(f"int      : {x}  → type: {type(x)}")
    print(f"float    : {y}  → type: {type(y)}")
    print(f"complex  : {z}   → type: {type(z)}")
    print(f"bool     : {is_ok}  → type: {type(is_ok)}")
    print(f"str      : {name}  → type: {type(name)}")
    print(f"NoneType : {nothing}  → type: {type(nothing)}")

    # ── Multiple assignment (no C/Java equivalent) ────────────────
    a, b, c = 1, 2, 3
    print(f"\nMultiple assign: a={a}, b={b}, c={c}")

    # ── Swap values — Python style (no temp variable needed) ──────
    a, b = b, a
    print(f"After swap    : a={a}, b={b}")

    # ── Type conversion (casting) ─────────────────────────────────
    num_str = "42"
    num_int = int(num_str)      # like Integer.parseInt() in Java / atoi() in C
    num_float = float(num_str)
    back_to_str = str(num_int)  # like String.valueOf() in Java
    print(f"\nCasting: '{num_str}' → int {num_int}, float {num_float}")

    # ── Python integers have UNLIMITED precision ──────────────────
    big = 10 ** 100   # 1 googol — no overflow like in C/Java int
    print(f"Big int (10^100): {big}")


# ═══════════════════════════════════════════════════════════════════
# 2. OPERATORS
# ═══════════════════════════════════════════════════════════════════
def section_operators():
    print("\n" + "═"*60)
    print("  §2 — OPERATORS")
    print("═"*60)

    a, b = 17, 5

    # ── Arithmetic ────────────────────────────────────────────────
    print(f"{a} + {b}  = {a + b}")
    print(f"{a} - {b}  = {a - b}")
    print(f"{a} * {b}  = {a * b}")
    print(f"{a} / {b}  = {a / b}   ← always float in Python 3 (unlike C int/int)")
    print(f"{a} // {b} = {a // b}  ← floor division (integer result)")
    print(f"{a} % {b}  = {a % b}   ← modulo")
    print(f"{a} ** {b} = {a ** b}  ← exponentiation (no Math.pow needed!)")

    # ── Comparison — same as C/Java ───────────────────────────────
    print(f"\n{a} == {b} → {a == b}")
    print(f"{a} != {b} → {a != b}")
    print(f"{a} >  {b} → {a > b}")
    print(f"{a} >= {b} → {a >= b}")

    # ── Logical — uses words, NOT symbols (unlike C/Java) ─────────
    # C/Java:  &&  ||  !
    # Python:  and  or  not
    x, y = True, False
    print(f"\nTrue and False → {x and y}")
    print(f"True or  False → {x or y}")
    print(f"not True       → {not x}")

    # ── Identity & Membership operators (Python-specific) ─────────
    lst = [1, 2, 3]
    print(f"\n3 in  [1,2,3]  → {3 in lst}")   # 'in' operator
    print(f"5 not in [1,2,3] → {5 not in lst}")

    s1 = "hello"
    s2 = "hello"
    s3 = s1
    print(f"\ns1 is s3 → {s1 is s3}")          # same object in memory
    print(f"s1 is s2 → {s1 is s2}")          # CPython may intern short strings
    print("(Use == for value comparison, 'is' for identity)")

    # ── Augmented assignment (same as C/Java) ─────────────────────
    n = 10
    n += 5;  print(f"\nn += 5  → {n}")
    n -= 3;  print(f"n -= 3  → {n}")
    n *= 2;  print(f"n *= 2  → {n}")
    n //= 3; print(f"n //= 3 → {n}")   # NOTE: no ++ / -- in Python!


# ═══════════════════════════════════════════════════════════════════
# 3. STRINGS
# ═══════════════════════════════════════════════════════════════════
def section_strings():
    print("\n" + "═"*60)
    print("  §3 — STRINGS")
    print("═"*60)

    s = "Hello, Python!"

    # ── Indexing & slicing (no C pointer arithmetic needed) ───────
    print(f"Original  : {s}")
    print(f"Index [0] : {s[0]}")        # 'H'
    print(f"Index [-1]: {s[-1]}")       # last char '!' — negative indexing!
    print(f"Slice [0:5]: {s[0:5]}")     # 'Hello'
    print(f"Slice [7:] : {s[7:]}")      # from index 7 to end
    print(f"Reverse   : {s[::-1]}")     # step -1 = reverse

    # ── Common methods ────────────────────────────────────────────
    print(f"\nUpper     : {s.upper()}")
    print(f"Lower     : {s.lower()}")
    print(f"Replace   : {s.replace('Python', 'World')}")
    print(f"Split     : {'one,two,three'.split(',')}")
    print(f"Strip     : {'  spaces  '.strip()}")
    print(f"Starts w/ : {s.startswith('Hello')}")
    print(f"Find      : {s.find('Python')}  ← index of substring")
    print(f"Length    : {len(s)}")  # len() instead of .length() in Java / strlen() in C

    # ── String formatting — 3 styles ──────────────────────────────
    name, age = "Ali", 21
    print(f"\n% format   : 'Name: %s, Age: %d'" % (name, age))   # C-style
    print(f".format()  : 'Name: {{}}, Age: {{}}'.format → 'Name: {name}, Age: {age}'")
    print(f"f-string   : f'Name: {{name}}, Age: {{age}}' → 'Name: {name}, Age: {age}'")  # Python 3.6+

    # ── Multi-line strings ────────────────────────────────────────
    multi = """Line 1
Line 2
Line 3"""
    print(f"\nMulti-line string:\n{multi}")

    # ── Raw strings (useful for file paths / regex) ───────────────
    raw = r"C:\Users\name\file.txt"   # backslash is NOT an escape
    print(f"\nRaw string: {raw}")


# ═══════════════════════════════════════════════════════════════════
# 4. CONTROL FLOW
# ═══════════════════════════════════════════════════════════════════
def section_control_flow():
    print("\n" + "═"*60)
    print("  §4 — CONTROL FLOW (if / elif / else)")
    print("═"*60)

    # ── Basic if/elif/else — NO parentheses required, NO braces ───
    score = 75
    if score >= 90:
        grade = "A"
    elif score >= 75:           # 'elif' instead of 'else if' in C/Java
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "F"
    print(f"Score {score} → Grade {grade}")

    # ── Ternary / inline if-else (Python style) ───────────────────
    # Java:    result = (x > 0) ? "pos" : "neg";
    # Python:  result = "pos" if x > 0 else "neg"
    x = -5
    sign = "positive" if x > 0 else "negative"
    print(f"\nx = {x} is {sign}")

    # ── Truthiness (Python evaluates many types as bool) ──────────
    print("\nTruthiness check:")
    for val in [0, 1, "", "hi", [], [1, 2], None, True]:
        print(f"  bool({repr(val):10}) = {bool(val)}")

    # ── match / case — Python 3.10+ (like switch in C/Java) ───────
    status_code = 404
    match status_code:
        case 200:
            msg = "OK"
        case 404:
            msg = "Not Found"
        case 500:
            msg = "Server Error"
        case _:                  # default case
            msg = "Unknown"
    print(f"\nmatch {status_code} → '{msg}'")


# ═══════════════════════════════════════════════════════════════════
# 5. LOOPS
# ═══════════════════════════════════════════════════════════════════
def section_loops():
    print("\n" + "═"*60)
    print("  §5 — LOOPS (for / while)")
    print("═"*60)

    # ── for loop over a range (like for(int i=0;i<5;i++) in C) ────
    print("range(5):", end=" ")
    for i in range(5):
        print(i, end=" ")
    print()

    print("range(2,10,2):", end=" ")        # start, stop, step
    for i in range(2, 10, 2):
        print(i, end=" ")
    print()

    # ── Iterating over a list directly (Java enhanced for) ────────
    fruits = ["apple", "banana", "cherry"]
    print("\nDirect list iteration:")
    for fruit in fruits:
        print(f"  {fruit}")

    # ── enumerate() — gives index + value ────────────────────────
    print("\nenumerate():")
    for idx, fruit in enumerate(fruits):
        print(f"  [{idx}] {fruit}")

    # ── zip() — iterate two lists together ───────────────────────
    prices = [1.2, 0.5, 2.0]
    print("\nzip():")
    for fruit, price in zip(fruits, prices):
        print(f"  {fruit}: ${price}")

    # ── while loop ────────────────────────────────────────────────
    print("\nwhile loop (countdown):")
    n = 3
    while n > 0:
        print(f"  {n}...")
        n -= 1
    print("  Go!")

    # ── break / continue / else on loop ───────────────────────────
    print("\nbreak / continue / loop-else:")
    for i in range(10):
        if i == 3:
            continue        # skip 3
        if i == 6:
            break           # stop at 6
        print(i, end=" ")
    print()

    # Loop else: runs if loop completes WITHOUT hitting break
    for i in range(5):
        if i == 99:
            break
    else:
        print("Loop finished without break — loop-else executed")


# ═══════════════════════════════════════════════════════════════════
# 6. FUNCTIONS
# ═══════════════════════════════════════════════════════════════════
def section_functions():
    print("\n" + "═"*60)
    print("  §6 — FUNCTIONS")
    print("═"*60)

    # ── Basic function ────────────────────────────────────────────
    def greet(name):
        """Docstring: one-line description of the function."""
        return f"Hello, {name}!"

    print(greet("World"))

    # ── Default parameters (like C++ / Java overloading shortcut) ─
    def power(base, exponent=2):   # exponent defaults to 2
        return base ** exponent

    print(f"power(3)    = {power(3)}")      # uses default
    print(f"power(3, 3) = {power(3, 3)}")  # overrides default

    # ── Keyword arguments (call by name, any order) ───────────────
    def describe(name, age, city):
        return f"{name}, {age}, from {city}"

    print(describe(age=22, city="Rabat", name="Sara"))

    # ── *args — variable number of positional args (like varargs) ─
    def total(*numbers):
        return sum(numbers)

    print(f"total(1,2,3,4) = {total(1, 2, 3, 4)}")

    # ── **kwargs — variable keyword args ──────────────────────────
    def show_info(**info):
        for key, val in info.items():
            print(f"  {key}: {val}")

    print("show_info():")
    show_info(name="Karim", role="Engineer", level=3)

    # ── Multiple return values (returns a tuple) ──────────────────
    def min_max(lst):
        return min(lst), max(lst)   # implicit tuple packing

    lo, hi = min_max([3, 1, 8, 5])  # tuple unpacking
    print(f"\nmin/max of [3,1,8,5] = {lo}, {hi}")

    # ── Type hints (Python 3.5+, NOT enforced, just documentation) ─
    def add(a: int, b: int) -> int:
        return a + b

    print(f"add(4, 7) = {add(4, 7)}")


# ═══════════════════════════════════════════════════════════════════
# 7. COLLECTIONS
# ═══════════════════════════════════════════════════════════════════
def section_collections():
    print("\n" + "═"*60)
    print("  §7 — COLLECTIONS (list, tuple, dict, set)")
    print("═"*60)

    # ─────────────────── LIST (like ArrayList in Java / array in C) ─
    print("── LIST ──")
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"Original : {nums}")
    nums.append(7)              # add to end
    nums.insert(0, 0)           # insert at index
    nums.remove(1)              # remove first occurrence of 1
    popped = nums.pop()         # remove & return last element
    print(f"Modified : {nums}  (popped {popped})")
    nums.sort()
    print(f"Sorted   : {nums}")
    print(f"Reversed : {list(reversed(nums))}")
    print(f"Length   : {len(nums)}")
    print(f"Count 1s : {nums.count(1)}")
    print(f"Index of 5: {nums.index(5)}")

    # ─────────────────── TUPLE (immutable list) ───────────────────
    print("\n── TUPLE ──")
    point = (10, 20)             # cannot be changed after creation
    x, y = point                 # unpacking (like structured binding in C++)
    print(f"point = {point}, x = {x}, y = {y}")
    # point[0] = 99  ← This would raise TypeError: 'tuple' object does not support item assignment

    # ─────────────────── DICTIONARY (like HashMap in Java) ────────
    print("\n── DICTIONARY ──")
    student = {
        "name": "Youssef",
        "age": 20,
        "grades": [15, 18, 12]
    }
    print(f"Dict     : {student}")
    print(f"Name     : {student['name']}")
    print(f"Age      : {student.get('age', 0)}")     # .get() avoids KeyError
    student["city"] = "Casablanca"                   # add new key
    student["age"] = 21                              # update existing key
    del student["city"]                              # delete a key

    print(f"Keys     : {list(student.keys())}")
    print(f"Values   : {list(student.values())}")
    print(f"Items    : {list(student.items())}")

    print("Iterating:")
    for key, val in student.items():
        print(f"  {key}: {val}")

    # ─────────────────── SET (like HashSet in Java) ───────────────
    print("\n── SET ──")
    a = {1, 2, 3, 4, 5}
    b = {4, 5, 6, 7, 8}
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"Union        : {a | b}")
    print(f"Intersection : {a & b}")
    print(f"Difference   : {a - b}")
    print(f"Sym. Diff.   : {a ^ b}")
    print(f"3 in a       : {3 in a}")   # O(1) lookup


# ═══════════════════════════════════════════════════════════════════
# 8. LIST & DICT COMPREHENSIONS
# ═══════════════════════════════════════════════════════════════════
def section_comprehensions():
    print("\n" + "═"*60)
    print("  §8 — COMPREHENSIONS")
    print("═"*60)

    # ── List comprehension — compact loop-based list creation ─────
    # Java equivalent: stream().filter().map().collect(...)
    squares = [x**2 for x in range(1, 8)]
    print(f"Squares         : {squares}")

    evens = [x for x in range(20) if x % 2 == 0]
    print(f"Evens 0-19      : {evens}")

    words = ["hello", "WORLD", "Python"]
    lower = [w.lower() for w in words]
    print(f"Lowercased      : {lower}")

    # ── Nested list comprehension (matrix) ────────────────────────
    matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
    print(f"3×3 table       : {matrix}")

    # ── Dict comprehension ────────────────────────────────────────
    names  = ["Ali", "Sara", "Omar"]
    scores = [88, 95, 72]
    grade_map = {name: score for name, score in zip(names, scores)}
    print(f"\nDict comp       : {grade_map}")

    # ── Set comprehension ─────────────────────────────────────────
    data = [1, 2, 2, 3, 3, 3, 4]
    unique_squares = {x**2 for x in data}
    print(f"Set comp        : {unique_squares}")

    # ── Generator expression (memory-efficient, no [ ]) ───────────
    gen = sum(x**2 for x in range(1000))
    print(f"Sum of squares  : {gen}  ← computed lazily")


# ═══════════════════════════════════════════════════════════════════
# 9. LAMBDA & HIGHER-ORDER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════
def section_lambda_hof():
    print("\n" + "═"*60)
    print("  §9 — LAMBDA & HIGHER-ORDER FUNCTIONS")
    print("═"*60)

    # ── Lambda = anonymous single-expression function ─────────────
    # Java equivalent: (x) -> x * 2  (lambda expression)
    double = lambda x: x * 2
    add    = lambda a, b: a + b
    print(f"double(7) = {double(7)}")
    print(f"add(3, 5) = {add(3, 5)}")

    # ── map() — apply function to each element ────────────────────
    nums = [1, 2, 3, 4, 5]
    doubled = list(map(lambda x: x * 2, nums))
    print(f"\nmap double   : {doubled}")

    # ── filter() — keep elements where function returns True ───────
    evens = list(filter(lambda x: x % 2 == 0, nums))
    print(f"filter evens : {evens}")

    # ── sorted() with key function ────────────────────────────────
    words = ["banana", "fig", "apple", "kiwi", "cherry"]
    by_len  = sorted(words, key=lambda w: len(w))
    by_last = sorted(words, key=lambda w: w[-1])
    print(f"\nSorted by length : {by_len}")
    print(f"Sorted by last ch: {by_last}")

    # ── Functions as first-class citizens ─────────────────────────
    def apply(func, value):
        return func(value)

    print(f"\napply(double, 10) = {apply(double, 10)}")

    # ── Functions returning functions (closure) ────────────────────
    def multiplier(factor):
        return lambda x: x * factor    # 'factor' is captured in closure

    triple = multiplier(3)
    print(f"triple(7) = {triple(7)}")


# ═══════════════════════════════════════════════════════════════════
# 10. CLASSES & OOP
# ═══════════════════════════════════════════════════════════════════
def section_oop():
    print("\n" + "═"*60)
    print("  §10 — CLASSES & OOP")
    print("═"*60)

    # ── Class definition ──────────────────────────────────────────
    # Java:   public class Animal { ... }
    # Python: class Animal:
    class Animal:
        # Class variable — shared across ALL instances (like static in Java)
        kingdom = "Animalia"

        # __init__ = constructor (like Animal() in Java)
        # 'self' = explicit 'this' — must be first param always
        def __init__(self, name: str, sound: str):
            self.name  = name    # instance variable
            self.sound = sound

        # Regular method — 'self' must be first param
        def speak(self):
            return f"{self.name} says {self.sound}!"

        # __str__ = like toString() in Java
        def __str__(self):
            return f"Animal(name={self.name})"

        # __repr__ — developer-friendly string
        def __repr__(self):
            return f"Animal({self.name!r}, {self.sound!r})"

        # Class method — receives class, not instance
        @classmethod
        def info(cls):
            return f"Kingdom: {cls.kingdom}"

        # Static method — no access to class or instance
        @staticmethod
        def breathes():
            return "Yes, animals breathe."

    # Instantiation — no 'new' keyword in Python!
    cat = Animal("Cat", "Meow")
    dog = Animal("Dog", "Woof")

    print(cat.speak())
    print(dog.speak())
    print(str(cat))
    print(repr(dog))
    print(Animal.info())
    print(Animal.breathes())

    # ── Inheritance ───────────────────────────────────────────────
    print("\n── Inheritance ──")

    class Dog(Animal):   # Dog extends Animal
        def __init__(self, name: str, breed: str):
            super().__init__(name, "Woof")   # call parent constructor
            self.breed = breed

        def speak(self):   # method overriding
            base = super().speak()
            return f"{base} (breed: {self.breed})"

        def fetch(self):
            return f"{self.name} fetches the ball!"

    rex = Dog("Rex", "German Shepherd")
    print(rex.speak())
    print(rex.fetch())
    print(f"Is Dog an Animal? {isinstance(rex, Animal)}")
    print(f"Is rex a Dog?     {isinstance(rex, Dog)}")

    # ── Multiple inheritance (possible in Python, not Java) ───────
    print("\n── Multiple Inheritance ──")

    class Flyable:
        def fly(self):
            return f"{self.name} is flying!"

    class FlyingDog(Dog, Flyable):
        pass   # 'pass' = empty body placeholder (no {} needed)

    fido = FlyingDog("Fido", "Labrador")
    print(fido.speak())
    print(fido.fly())
    print(f"MRO: {[c.__name__ for c in FlyingDog.__mro__]}")

    # ── Dunder (magic) methods ─────────────────────────────────────
    print("\n── Dunder Methods (like operator overloading) ──")

    class Vector:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __add__(self, other):          # v1 + v2
            return Vector(self.x + other.x, self.y + other.y)

        def __mul__(self, scalar):         # v * 3
            return Vector(self.x * scalar, self.y * scalar)

        def __len__(self):                 # len(v)
            return 2

        def __str__(self):
            return f"Vector({self.x}, {self.y})"

    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 * 3  = {v1 * 3}")
    print(f"len(v1) = {len(v1)}")


# ═══════════════════════════════════════════════════════════════════
# 11. EXCEPTION HANDLING
# ═══════════════════════════════════════════════════════════════════
def section_exceptions():
    print("\n" + "═"*60)
    print("  §11 — EXCEPTION HANDLING")
    print("═"*60)

    # ── try / except / else / finally ─────────────────────────────
    # Java:   try { } catch(Exception e) { } finally { }
    # Python: try:  except Exception as e:  finally:
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"Caught: {e}")
    else:
        print("No exception — this runs only if try succeeded")
    finally:
        print("Finally always runs (like Java's finally)")

    # ── Multiple except clauses ───────────────────────────────────
    def safe_parse(value):
        try:
            return int(value)
        except ValueError:
            return f"Cannot convert '{value}' to int"
        except TypeError:
            return "Wrong type entirely"

    print(f"\nsafe_parse('42')  = {safe_parse('42')}")
    print(f"safe_parse('abc') = {safe_parse('abc')}")
    print(f"safe_parse(None)  = {safe_parse(None)}")

    # ── Raising exceptions ────────────────────────────────────────
    def validate_age(age):
        if age < 0:
            raise ValueError(f"Age cannot be negative: {age}")
        if age > 150:
            raise ValueError(f"Unrealistic age: {age}")
        return age

    try:
        validate_age(-5)
    except ValueError as e:
        print(f"\nRaised ValueError: {e}")

    # ── Custom exceptions ─────────────────────────────────────────
    class InsufficientFundsError(Exception):
        def __init__(self, amount, balance):
            super().__init__(f"Cannot withdraw {amount}, balance is {balance}")
            self.amount  = amount
            self.balance = balance

    try:
        raise InsufficientFundsError(500, 200)
    except InsufficientFundsError as e:
        print(f"Custom exception: {e}")


# ═══════════════════════════════════════════════════════════════════
# 12. FILE I/O
# ═══════════════════════════════════════════════════════════════════
def section_file_io():
    print("\n" + "═"*60)
    print("  §12 — FILE I/O")
    print("═"*60)

    import os

    filename = "demo_output.txt"

    # ── Write to file ─────────────────────────────────────────────
    with open(filename, "w", encoding="utf-8") as f:   # 'w' = write (creates/overwrites)
        f.write("Line 1: Hello from Python\n")
        f.write("Line 2: File I/O is straightforward\n")
        f.writelines(["Line 3: Item A\n", "Line 4: Item B\n"])
    print(f"Written to '{filename}'")

    # ── Append to file ────────────────────────────────────────────
    with open(filename, "a", encoding="utf-8") as f:   # 'a' = append
        f.write("Line 5: Appended line\n")

    # ── Read entire file ──────────────────────────────────────────
    with open(filename, "r", encoding="utf-8") as f:   # 'r' = read (default)
        content = f.read()
    print(f"\nFull content:\n{content.strip()}")

    # ── Read line by line ──────────────────────────────────────────
    print("Line by line:")
    with open(filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            print(f"  [{i}] {line.rstrip()}")

    # ── Check existence / delete ──────────────────────────────────
    print(f"\nFile exists: {os.path.exists(filename)}")
    os.remove(filename)
    print(f"After delete: {os.path.exists(filename)}")


# ═══════════════════════════════════════════════════════════════════
# 13. DECORATORS
# ═══════════════════════════════════════════════════════════════════
def section_decorators():
    print("\n" + "═"*60)
    print("  §13 — DECORATORS")
    print("═"*60)

    # Decorator = a function that wraps another function
    # Like Aspect-Oriented Programming (AOP) in Java Spring

    import time
    import functools

    # ── Simple decorator ──────────────────────────────────────────
    def timer(func):
        @functools.wraps(func)      # preserves original func metadata
        def wrapper(*args, **kwargs):
            start  = time.perf_counter()
            result = func(*args, **kwargs)
            end    = time.perf_counter()
            print(f"  [{func.__name__}] ran in {(end-start)*1000:.3f} ms")
            return result
        return wrapper

    @timer   # syntactic sugar — equivalent to:  slow_sum = timer(slow_sum)
    def slow_sum(n):
        return sum(range(n))

    result = slow_sum(1_000_000)
    print(f"Sum = {result}")

    # ── Decorator with parameters ─────────────────────────────────
    def repeat(times):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for _ in range(times):
                    result = func(*args, **kwargs)
                return result
            return wrapper
        return decorator

    @repeat(3)
    def say(msg):
        print(f"  {msg}")

    say("Hello!")


# ═══════════════════════════════════════════════════════════════════
# 14. GENERATORS & ITERATORS
# ═══════════════════════════════════════════════════════════════════
def section_generators():
    print("\n" + "═"*60)
    print("  §14 — GENERATORS & ITERATORS")
    print("═"*60)

    # Generator = function that uses 'yield' to lazily produce values
    # Equivalent of Java's Iterator pattern, but far simpler

    def countdown(n):
        """Yields n, n-1, ..., 1"""
        while n > 0:
            yield n     # pauses here, returns n, resumes on next()
            n -= 1

    print("countdown(5):", end=" ")
    for val in countdown(5):
        print(val, end=" ")
    print()

    # ── Infinite generator ────────────────────────────────────────
    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    print("First 10 Fibonacci:")
    fib = fibonacci()
    print([next(fib) for _ in range(10)])

    # ── Generator expression (like list comp but lazy) ────────────
    big_squares = (x**2 for x in range(10**6))  # NO memory allocation yet!
    print(f"\nFirst 5 lazy squares: {[next(big_squares) for _ in range(5)]}")

    # ── Custom iterator class (like Java Iterable) ────────────────
    class Range:
        """Simplified version of Python's built-in range()."""
        def __init__(self, stop):
            self.current = 0
            self.stop    = stop

        def __iter__(self):     # makes the class iterable
            return self

        def __next__(self):     # called each iteration
            if self.current >= self.stop:
                raise StopIteration
            val = self.current
            self.current += 1
            return val

    print("\nCustom Range(5):", list(Range(5)))


# ═══════════════════════════════════════════════════════════════════
# 15. CONTEXT MANAGERS (with statement)
# ═══════════════════════════════════════════════════════════════════
def section_context_managers():
    print("\n" + "═"*60)
    print("  §15 — CONTEXT MANAGERS (with statement)")
    print("═"*60)

    # 'with' ensures __enter__ and __exit__ are called (like try-finally)
    # This is how Python handles resource management safely.
    # Java equivalent: try-with-resources (AutoCloseable)

    from contextlib import contextmanager

    @contextmanager
    def managed_resource(name):
        print(f"  ► Acquiring resource: {name}")
        try:
            yield name.upper()          # value available in 'as' clause
        finally:
            print(f"  ◄ Releasing resource: {name}")

    print("Using a context manager:")
    with managed_resource("database connection") as resource:
        print(f"  Working with: {resource}")

    # ── Multiple context managers ─────────────────────────────────
    print("\nNested context managers (one line):")
    with managed_resource("socket") as s, managed_resource("lock") as l:
        print(f"  Got: {s} and {l}")

    print("\n" + "─"*60)
    print("  QUICK REFERENCE — Key Python vs C/Java Differences")
    print("─"*60)
    table = [
        ("No semicolons",        "x = 5        ",  "x = 5;"),
        ("No braces for blocks", "if x:\\n    …",   "if(x){…}"),
        ("Indentation = block",  "    (4 spaces)",  "{"),
        ("No type declaration",  "x = 10       ",  "int x = 10;"),
        ("Print",                "print(x)     ",  "System.out.println(x); / printf"),
        ("Boolean: T/F caps",    "True / False ",  "true / false"),
        ("Null",                 "None         ",  "null / NULL"),
        ("Not / And / Or",       "not / and / or", "! / && / ||"),
        ("Integer division",     "//           ",  "/ (with ints)"),
        ("Power",                "**           ",  "Math.pow()"),
        ("String interpolation", "f'val={x}'   ",  "String.format() / printf"),
        ("No ++/--",             "x += 1       ",  "x++ / x--"),
        ("No 'new' keyword",     "Dog('Rex')   ",  "new Dog('Rex')"),
        ("This = self",          "self.name    ",  "this.name"),
    ]
    print(f"  {'Concept':<25} {'Python':<20} {'C / Java'}")
    print("  " + "-"*58)
    for concept, python, cjava in table:
        print(f"  {concept:<25} {python:<20} {cjava}")


# ─────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_all()
