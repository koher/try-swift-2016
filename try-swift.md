autoscale: true

# Three Stories about __Error Handling__ in Swift

## Yuta Koshizawa @koher

^ I am honored to be with you today at one of the finest Swift conferences in the world. Truth be told, I never attended a Swift conference and this is my first presentation about Swift. Today I want to tell you three stories of errors from my life. That's it. No big deal. Just three stories.

---

## The First Story

### Meeting the Optionals

^ The first story is about meeting the `Optional`s.

^ I believe that _optional types_ are one of the best features in Swift. So why did I get it?

^ It started before Swift was born.

---

### Error Handling in C

^ My first programming language was C except I had played BASIC in my childhood. Error handling in C was something like this.

```c
// [ C ]
int *numbers = (int *)malloc(sizeof(int) * 42);
if (numbers == NULL) {
    // Error handling here
}
```

^ It can be easily forgotten.

---

### Error Handling in C

^ The C compiler never warns or fails with codes without error handling even if we forget to handle errors.

```c
// [ C ]
int *numbers = (int *)malloc(sizeof(int) * 42);
// Easily forgets to handle errors
```

---

### Error Handling in Java

^ After that, I learned _checked exceptions_ in Java, which forced programmers to handle errors.

^ Think about a function to parse an integer from a string.

```java
// [ Java ]
static int toInt(String string)
  throws FormatException {
    ...
}
```

^ It returns an integer when the string is parsed correctly, or fails for strings whose formats are illegal.

```java
// [ Java ]
toInt("42");    // Success
toInt("Swift"); // Failure
```

---

### Error Handling in Java

^ It causes a compilation error without error handling.

```java
// [ Java ]
String string = ...;
int number = toInt(string); // Compilation error
```

---

### Error Handling in Java

^ We need to `try` and `catch` it.

```java
// [ Java ]
String string = ...;
try {
  int number = toInt(string);
  ...
} catch (FormatException e) {
  // Error handling
  ...
}
```

^ But sometimes we want to ignore errors. Text fields might force users to input only numbers. Even then, =>

---

### Error Handling in Java

^ we must write meaningless error handling to ignore the errors.

```java
// [ Java ]
String string = ...;
try {
  int number = toInt(string);
  ...
} catch (FormatException e) {
  // Error handling
  throw new Error("Never reaches here.");
}
```

^ I discussed this problem with my colleague at Qoncept, our company, and we concluded: we needed an explicit but easy way to ignore errors.

---

### Error Handling in Java

^ `!` after a method call was a good candidate. It's done by typing one key, still explicit and looks dangerous.

```java
// [ Java ]
String string = ...;
int number = toInt(string)!; // Ignores exceptions
  // This `!` was what we wanted.
```

---

### Optionals for Error Handling

^ Some years later, I did meet _optionals_ in Swift.

^ Swift provided _optionals_ mainly to eliminate `NullPointerException`s. But they were also used for error handling.

^ `toInt` is written this way using _optionals_.

```swift
// [ Swift ]
func toInt(string: String) -> Int? {
  ...
}
```

---

### Optionals for Error Handling

^ It causes a compilation error without error handling.

```swift
// [ Swift ]
let string: String = ...
let number: Int = toInt(string) // Compilation error
```

---

### Optionals for Error Handling

^ We can handle errors using _optional binding_.

```swift
// [ Swift ]
let string: String = ...
if let number = toInt(string) {
  ...
} else {
  // Error handling
  ...
}
```

---

### Optionals for Error Handling

^ How about ignoring errors?

^ When I learned _forced unwrapping_, I was so surprised because it was the one exactly we wanted.

```swift
// [ Swift ]
let string: String = ...
let number: Int = toInt(string)! // Ignores an error
```

---

### Optionals for Error Handling

^ Unlike _exceptions_, _optionals_ don't work well for functions and methods which have side effects. But I think the `@warn_unused_result` attribute can be the solution.

```swift
// [ Swift ]
@warn_unused_result
func updateBar(bar: Bar) -> ()? {
  ...
}
```

```swift
// [ Swift ]
foo.updateBar(bar) // Warning
```

---

### Optionals for Error Handling

^ Handing and ignoring errors can be done this way.

```swift
// [ Swift ]
if let _ = foo.updateBar(bar) {
  ...
} else {
  // Error handling
  ...
}
```

```swift
// [ Swift ]
_ = foo.updateBar(bar) // Ignores the error
```

^ If we had a kind of the `@error_unused_result` attribute, it would be better.

---

### Optionals for Error Handling

^ And, _optionals_ provide more flexible ways to handle errors. While _exceptions_ must be handled just after they are thrown, _optionals_ can be handled lazily.

^ We can assign an _optional_ into a variable, pass it to a function, and store it in a property.

```swift
// [ Swift ]
let string: String = ...
let number: Int? = toInt(string)

...

// Errors can be handled lazily
if let number = number {
  ...
} else {
  // Error handling
  ...
}
```

---

### Difficulty of Using Optionals

^ It wasn't all romantic. My codes soon got full of _optionals_.

^ With _optionals_, it isn't easy to even square a number

```swift
// [ Swift ]
let a: Int? = ...
let square = a * a // Compilation error
```

^ or calculate a sum.

```swift
// [ Swift ]
let a: Int? = ...
let b: Int? = ...
let sum = a + b // Compilation error
```

---

### Difficulty of Using Optionals

^ Five lines for each to just `square` or `sum` with _optional binding_. It's awful.

```swift
// [ Swift ]
let a: Int? = ...
let square: Int?
if let a = a {
  square = a * a
} else {
  square = nil
}
```

```swift
// [ Swift ]
let a: Int? = ...
let b: Int? = ...
let sum: Int?
if let a = a, b = b {
  sum = a + b
} else {
  sum - nil
}
```

---

### Functional Operations for Optionals

^ Fortunately, Swift provides functional ways for such cases.

^ `map` is useful for `square`,

```swift
// [ Swift ]
let a: Int? = ...
let square: Int? = a.map { $0 * $0 }
```

^ and `flatMap` for `sum` to flatten the nested `Optional`s.

```swift
// [ Swift ]
let a: Int? = ...
let b: Int? = ...
let sum: Int? = a.flatMap { a in b.map { b in a + b } }
```

---

### Functional Operations for Optionals

^ More optional values make it complicated. A typical case is decoding JSONs.

^ Assume we have the APIs like SwiftyJSON ([^1]).

```swift
// [ Swift ]
let id: String? = json["id"].string
```

^ Any steps of decoding can fail.

```js
// [ JSON ]
// The `json` might not be an `Object`
[ "abc" ]
// It might not have a key named `"id"`
{ "foo": "abc" }
// The value might not be a `String`
{ "id": 42 }
```

---

### Functional Operations for Optionals

^ All return values are optionals. How can we initialize a `Person` with these optional values?

```swift
// [ Swift ]
struct Person {
  let id: String
  let firstName: String
  let lastName: String
  let age: Int
  let isAdmin: Bool
}

let id: String? = json["id"].string
let firstName: String? = json["firstName"].string
let lastName: String? = json["lastName"].string
let age: Int? = json["age"].int
let isAdmin: Bool? = json["isAdmin"].bool
```

---

### Functional Operations for Optionals

^ With `flatMap`, we get this awful pyramid.

```swift
// [ Swift ]
let person: Person? = id.flatMap { id in
  firstName.flatMap { firstName in
    lastName.flatMap { lastName in
      age.flatMap { age in
        isAdmin.flatMap { isAdmin in
          Person(id: id, firstName: firstName,
            lastName: lastName, age: age, isAdmin: isAdmin)
        }
      }
    }
  }
}
```

---

### Functional Operations for Optionals

^ Optional binding seems better.

```swift
// [ Swift ]
let person: Person?
if let id = id, firstName = firstName,
  lastName = lastName, age = age, isAdmin = isAdmin {
  person = Person(id: id, firstName: firstName,
    lastName: lastName, age: age, isAdmin: isAdmin)
} else {
  person = nil
}
```

^ But we have to repeat the parameter names so many times.

---

### Functional Operations for Optionals

^ In an applicative style, which is common in Haskell, it becomes much simpler.

```swift
// [ Swift ]
let person: Person? = curry(Person.init) <^> id
  <*> firstName <*> lastName <*> age <*> isAdmin
```

^ Applicative styles are available in Swift with the third-party library  "thoughtbot/Runes" ([^2]).

---

### Syntactic Sugars and Operators for Optionals

^ Additionally, Swift provided some syntactic sugars and operators to use _optionals_ easily.

```swift
// [ Swift ]
//let foo: Optional<Foo> = ...
let foo: Foo? = ...

// let baz: Baz? = foo.flatMap { $0.bar }.flatMap { $0.baz }
let baz: Baz? = foo?.bar?.baz

// let quxOrNil: Qux? = ...
// let qux: Qux
// if let q = quxOrNil {
//   qux = q
// } else {
//   qux = Qux()
// }
let quxOrNil: Qux? = ...
let qux: Qux = quxOrNil ?? Qux()
```

---

### Optionals in Swift

- `Foo? == Optional<Foo>`
- Forced Unwrapping: `!`
- `map`, `flatMap`
- Applicative styles: `<^>`, `<*>` ([^2])
- Optional chaining: `foo?.bar?.baz`
- Nil coalescing operator: `??`

^ `?` notations, _forced unwrapping_, `map`, `flatMap`, _optional chaining_, ...

^ Some languages had some of them. But combination of all made Swift different. It was safe, practical, theoretically subtle in a way that other languages couldn't achieve, and I found it fascinating.

---

^ Tony Hoare, the inventor of null references, said this.

> I couldn't resist the temptation to put in a null reference, simply because it was so easy to implement.
-- Tony Hoare

^ I think it is the dark side of programming. Falling to the dark side is easy. In exchange for a little unsafety, we can get free from the complication of types. But I want to stay Jedi. I believe it makes the evolution.

^ _Optionals_ were the evolution. They are type safe and still practical. That's the reason why I think _optionals_ in Swift are great.

---

## The Second Story

### Success or Failure

^ My second story is about success or failure.

^ Although _optionals_ were great, it lacked a way to report the causes of errors.

^ Mainly, it leads two problems.

^ 1. Hard to debug.

^ 2. Can't branch operations by the causes of errors.

---

### Problems of Optionals

^ For example,

```swift
// [ Swift ]
let a: Int? = toInt(aString)
let b: Int? = toInt(bString)
let sum: Int? = a.flatMap { a in b.map { b in a + b } }

guard let sum = sum else {
  // Which `a` or `b` failed to be parsed?
  // What string was the input?
  ...
}
```

^ even for such a simple operation, we want to know which of `a` or `b` failed to be parsed and what was the input.

---

### Problems of Optionals

^ Another example is decoding JSONs.

^ If we want to get `false` when the key "isAdmin" is omitted in the JSON, how can we do it by _optionals_?

```swift
// [ Swift ]
let isAdmin: Bool
if let admin = json["isAdmin"].bool {
  // { "isAdmin": true }
  isAdmin = admin
} else {
  // [ true ]
  // {}
  // { "isAdmin": 42 }
  isAdmin = ...
}
```

^ It can fail in three ways shown.

^ We want it to recover from only the second case =>

---

### Problems of Optionals

```swift
// [ Swift ]
let isAdmin: Bool
if let admin = json["isAdmin"].bool {
  // { "isAdmin": true }
  isAdmin = admin
} else {
  // [ true ]
  // {}                => false
  // { "isAdmin": 42 }
  isAdmin = ...
}
```

^  and fail for the others.

---

### Problems of Optionals

```swift
// [ Swift ]
let isAdmin: Bool
if let admin = json["isAdmin"].bool {
  // { "isAdmin": true }
  isAdmin = admin
} else {
  // [ true ]          => error
  // {}                => false
  // { "isAdmin": 42 } => error
  isAdmin = ...
}
```

^  `nil` cannot represent the difference.

---

### Alternatives of Optionals

^ I found three solutions.

1. _Tuples_
2. _Union types_
3. _Results_

---

### Tuples

^ With tuples, `toInt` can be written this way.

```swift
// [ Swift ]
func toInt(string: String) -> (Int?, FormatError?) {
  ...
}
```

^ It returns a `FormatError` in addition to the `Int` value. Libraries in Go sometimes employ this way.

---

### Tuples

^ But it makes four cases of results.

- `(value, nil  ) // Success`
- `(nil  , error) // Failure`
- `(value, error) // ???`
- `(nil  , nil  ) // ???`

^ I didn't want the last two.

---

### Union types

^ _Union types_ are provided in Ceylon, TypeScript and Python with _type hints_.

^ With _unions_, `Int|String` means the type `Int` or `String`. So we can return `Int` or `FormatError` directly.

```swift
// [ Swift ]
func toInt(string: String) -> Int|FormatError {
  ...
}
```

```swift
// [ Swift ]
switch toInt(...) {
  case let value as Int:
    ...
  case let error as FormatError:
    // Error handling
    ...
}
```

---

### Union types

^ In addition, it's interesting that _optionals_ in Ceylon and Python are a syntactic sugar of _unions_.

```java
// [ Ceylon ]
Integer? a = 42;
Integer|Null a = 42;
```

```bash
# [ Python ]
def foo() -> Optional[Foo]: ...
def foo() -> Union[Foo, None]: ...
```

^ _Unions_ are a straightforward way to extend _optionals_ in those languages.

---

### Union types

^ But the `Optional` in Swift was an _enumeration_.

```swift
// [ Swift ]
enum Optional<T> {
  case Some(T)
  case None
}
```

^ I thought it wasn't Swifty to extend _optionals_ by _unions_.

---

### Results

^ _Results_ came from Rust.

^ The `Result` can be declared this way.

```swift
// [ Swift ]
enum Result<T, E> {
  case Success(T)
  case Failure(E)
}
```

^ It's Swifty and a natural extension of the `Optional`.  

```swift
// [ Swift ]
enum Optional<T> {
  case Some(T)
  case None
}
```

---

### Results

^ With _results_, we can get error information,

```swift
// [ Swift ]
let a: Result<Int, FormatError> = toInt(aString)
let b: Result<Int, FormatError> = toInt(bString)
let sum: Result<Int, FormatError> = a.flatMap { a in b.map { b in a + b } }

switch sum {
  case let .Success(sum):
    ...
  case let .Failure(error):
    // Get the detailed error information from `error`
    ...
}
```

---

### Results

^ and branch operations by the causes of errors.

```swift
// [ Swift ]
let isAdmin: Bool
switch json["isAdmin"].bool {
  case let .Success(admin):
    isAdmin = admin
  case .Failure(.MissingKey):
    // {}                => false
    isAdmin = false
  case .Failure(.TypeMismatch, .NotObject):
    // [ true ]          => error
    // { "isAdmin": 42 } => error
    ...
}
```

^ _Results_ can be `map`ped and `flatMap`ped as well as _optionals_.

^ The library "antitypical/Result" ([^3]) provides such _results_ for Swift.

---

### Results

^ It would be convenient if _results_ had syntactic sugars like _optionals_.

^ Although I excluded _unions_, their vertical bar notations seem intuitive and easy to write. Also `flatMap` chains should be written like _optional chaining_.

```swift
// [ Swift ]
let foo: Result<Foo, Error> = ...
let baz: Result<Foo, Error>
  = foo.flatMap { $0.bar }.flatMap { $0.baz }
```

```swift
// [ Swift ]
let foo: Foo|Error = ...
let baz: Baz|Error = foo?.bar?.baz
```

^ They would make _results_ more powerful.

---

### Difficulty of Using Results

^ _Results_ seemed good. But soon I found some cases they did not work.

^ This is the example.

```swift
// [ Swift ]
let a: Result<Int, ErrorA> = ...
let b: Result<Int, ErrorB> = ...
let sum: Result<Int, ???>
  = a.flatMap { a in b.map { b in a + b } }
```

^ What should the second type parameter be? It can be both `ErrorA` and `ErrorB`.

---

### Difficulty of Using Results

^ One easy answer was using an _union_ of `ErrorA|ErrorB`. But that was the one I excluded.

```swift
// [ Swift ]
let a: Result<Int, ErrorA> = ...
let b: Result<Int, ErrorB> = ...
let sum: Result<Int, ErrorA|ErrorB>
  = a.flatMap { a in b.map { b in a + b } }
```

---

### Difficulty of Using Results

^ The next idea was nested _results_.

```swift
// [ Swift ]
let a: Result<Int, ErrorA> = ...
let b: Result<Int, ErrorB> = ...
let sum: Result<Int, Result<ErrorA, ErrorB>>
  = a.flatMap { a in b.map { b in a + b } }
```

^ It looked awful.

---

### Difficulty of Using Results

^ It got better with the vertical bar notations.

```swift
// [ Swift ]
let a: Int|ErrorA = ...
let b: Int|ErrorB = ...
let sum: Int|ErrorA|ErrorB
  = a.flatMap { a in b.map { b in a + b } }
```

---

### Difficulty of Using Results

^ But it was still bad when I had more _results_. They were nested too deeply and unintuitively.

```swift
// [ Swift ]
let id: String|ErrorA = ...
let firstName: String|ErrorB = ...
let lastName: String|ErrorC = ...
let age: Int|ErrorD = ...
let isAdmin: Bool| ErrorE = ...

let person: Person|(((ErrorA|ErrorB)|ErrorC)|ErrorD)|ErrorE
  = curry(Person.init) <^> id <*> firstName
    <*> lastName <*> age <*> isAdmin
```

---

### Difficulty of Using Results

^ Error handling was done this way.

```swift
// [ Swift ]
switch person {
  case let .Success(person):
    ...
  case let .Failure(.Success(.Success(.Success(.Success(.Failure(errorA)))))):
    ...
  case let .Failure(.Success(.Success(.Success(.Failure(errorB))))):
    ...
  case let .Failure(.Success(.Success(.Failure(errorC)))):
    ...
  case let .Failure(.Success(.Failure(errorD))):
    ...
  case let .Failure(.Failure(errorD)):
    ...
}
```

^ It was too complicated.

^ I thought about it for a long time. And finally, =>

---

### Results without an Error Type

^ I concluded that the second type parameter of _results_ was not important in practice.

```swift
// [ Swift ]
enum Result<T, E> {
  case Success(T)
  case Failure(E)
}
```

---

### Results without an Error Type

^ If the `Result` is declared this way, it loses the type of the error and seems unsafe.

```swift
// [ Swift ]
enum Result<T> {
  case Success(T)
  case Failure(ErrorType)
}
```

^ But, in most cases, we don't need to branch operations into each type of errors. We just need to care about one or two exceptional ones.

---

### Results without an Error Type

^ Think about networking operations. They fail in various ways. We want to retry the operation when it timeout. But not for "Forbidden", "Not found" and so on.

^ Then we branch the operation into the cases of `Success`, `Timeout` and the others. We don't need to list up all of possible errors.

```swift
// [ Swift ]
downloadJson(url) { json: Result<Json> in
  switch json {
    case let .Success(json): // success
      ...
    case let .Failure(.Timeout): // timeout
      // retry
      ...
    case let .Failure(error): // others
      // error
      ...
  }
}
```

---

### Results without an Error Type

^ Also, it's true for decoding JSONs. We want to recover only from `MissingKey`, and raise an error for the others.

```swift
// [ Swift ]
let isAdmin: Bool
switch json["isAdmin"].bool {
  case let .Success(admin): // success
    isAdmin = admin
  case .Failure(.MissingKey): // missing key
    // {}                => false
    isAdmin = false
  case let .Failure(error): // others
    // [ true ]          => error
    // { "isAdmin": 42 } => error
    ...
}
```

^ It's very rare to branch operations for all possible errors. And if we actually need it, =>

---

### Results without an Error Type

^ we can do it by _enumerations_ with _associated values_ which Swift has already provided.

```swift
// [ Swift ]
enum Foo {
  case Bar(A)
  case Baz
  case Qux(B)
}

func foo() -> Foo { ... }

switch foo() {
  case let Bar(a):
    ...
  case let Baz:
    ...
  case let Qux(b):
    ...
}
```

---

### Results without an Error Type

^ I implemented a library named "ResultK" ([^4]) to provide such _results_. It works well even if various types of errors are mixed together.

```swift
// [ Swift ]
let a: Result<Int> = ... // ErrorA
let b: Result<Int> = ... // ErrorB
let sum: Result<Int> // ErrorA or ErrorB
  = a.flatMap { a in b.map { b in a + b } }
```

---

### Results without an Error Type

^ How about syntactic sugars for them? `Int|` as `Result<Int>` might be good.

```swift
// [ Swift ]
let a: Int| = ...
let b: Int| = ...
let sum: Int|
  = a.flatMap { a in b.map { b in a + b } }
```

I'm afraid that such _results_ are the dark side. It makes _results_ untyped. But as far as I considered, it is the best way so far.

---

## The Third Story

### try

^ My third story is about `try`.

^ Swift 2.0 introduced the syntax similar to `try` / `catch` in Java.

---

### Automatic Propagation

^ My first impression was bad. I didn't want to go back to the Java age. But as I learned it, I figured out it was pretty good.

^ The Swift core team explained why they employed the `try` / `catch` syntax in the document named "Error Handling Rationale and Proposal" ([^5]).

```swift
// [ Swift ]
func toInt(string: String) throws -> Int {
  ...
}

do {
  let number = try toInt(string)
  ...
} catch let error {
  // Error handling here
  ...
}
```

---

### Automatic Propagation

^ In the rationale, the core team defined _manual propagation_ and _automatic propagation_ of errors. With _manual propagation_, errors are handled by a control flow statement manually while it jumps automatically to the handler when an error occurs with _automatic propagation_.

```swift
// [ Swift ]
// Manual propagation
switch(toInt(string)) {
  case let .Success(number):
    ...
  case let .Failure(error): // Handles an error manually
    ...
}

// Automatic propagation
do {
  let number = try toInt(string) // Jumps to `catch` automatically
  ...
} catch let error {
  ...
}
```

---

### Automatic Propagation

^ _Automatic propagation_ is useful especially when we want to handle multiple errors all together. Even with _manual propagation_, we can do it in a functional way using `map`, `flatMap` and applicative. But it's syntactically complicated and theoretically difficult. It's unreasonable to expect all programmers to understand them.

```swift
// [ Swift ]
// Manual propagation
let a: Result<Int> = toInt(aString)
let b: Result<Int> = toInt(bString)
switch a.flatMap { a in b.map { b in a + b } } {
  case let .Success(sum):
    ...
  case let .Failure(error):
    ...
}

// Automatic propagation
do {
  let a: Int = try toInt(aString)
  let b: Int = try toInt(bString)
  let sum: Int = a + b
  ...
} catch let error {
  ...
}
```

---

### Automatic Propagation

^ In the rationale, the core team referred to an interesting topic about Haskell's `do` notation.

^ It's a notation to simplify `flatMap` chains and nested `flatMap`s.

```swift
// [ Swift ]
let sum = toInt(aString).flatMap { a in
   toInt(bString).flatMap {
     .Some(a + b)
   }
}
```

```haskell
-- [ Haskell ]
sum = do
  a <- toInt aString
  b <- toInt bString
  Just (a + b)
```

^ The core team said it is a kind of _automatic propagation_. It means we anyway need _automatic propagation_ for both functional and non-functional error handling to write it in a simple notation.

^ So I understood it was good to introduce _automatic propagation_ to Swift.

---

### Marked Propagation

^ I also worried about untyped `throws`.

^ We can't specify types of errors with `throws` so far. I think it's reasonable as well as for _results_. What I was afraid of was another thing.

```swift
// [ Swift ]
func toInt(string: String) throws FormatError -> Int { // Compilation error
  ...
}
```

---

### Marked Propagation

^ Java has _unchecked exceptions_. The compiler reports nothing even if we don't handle them. C# and various dynamically typed languages have a similar mechanism too.

```java
// [ Java ]
class FormatException extends RuntimeException {
  ...
}
```

```java
// [ Java ]
static int toInt(String string) throws FormatException {
    ...
}
```

```java
// [ Java ]
String string = ...;
int number = toInt(string); // No compilation error
```

---

### Marked Propagation

^ In those languages, every line in a code might throw an unexpected error.

```java
// [ Java ]
void foo() { // What can `foo` throw?
  a(); // May throw an unchecked exception
  b(); // May throw an unchecked exception
  c(); // May throw an unchecked exception
  d(); // May throw an unchecked exception
  e(); // May throw an unchecked exception
  f(); // May throw an unchecked exception
  g(); // May throw an unchecked exception
}
```

^ Then, no one knows what errors can be actually thrown even by a function she implemented. It's so bad. Impossible to complete error handling, and we tend to be careless about it.

---

### Marked Propagation

^ I thought it could be reproduced in Swift.

^ Swift doesn't have _unchecked exceptions_. But once we add `throws` to a function, it's hard to know which line in the function can throw an error. And because we don't need to specify the type of the error, we get careless about what kinds of errors the function `throws`.

```swift
// [ Swift ]
func foo() throws { // What can `foo` throw?
  a() // Can throw an error?
  b() // Can throw an error?
  c() // Can throw an error?
  d() // Can throw an error?
  e() // Can throw an error?
  f() // Can throw an error?
  g() // Can throw an error?
}
```

---

### Marked Propagation

^ But Swift forces to add the keyword `try` when we call a function with `throws`. The core team called it _marked propagation_.

```swift
// [ Swift ]
func foo() throws {
  a()
  try b() // May throw an error
  c()
  d()
  try e() // May throw an error
  f()
  g()
}
```

^ With `try`, it's obvious which lines can throw an error. And, we can check what kinds of errors can be thrown.

^ If `throws` were typed, it would be safer. But I think _marked propagation_ removed the worst part of untyped `throws`, and untyped `throws` is a reasonable trade-off between type safety and simplicity.

---

### Marked Propagation

^ _Marked propagation_ also helps us to read codes. With _automatic propagation_, it's hard to understand the control flow from where it jumps to `catch` clauses. It's referred as an implicit control flow problem in the rationale. _Marked propagation_ makes it clearer.

```java
// [ Java ]
try {
  foo();
  bar();
  baz();
} catch (QuxException e) {
  // Where did it come from?
}
```

```swift
// [ Swift ]
do {
  foo()
  try bar()
  baz()
} catch let error {
  // Came from `bar()`
}
```

---

### Marked Propagation

- Careless about error types
- Implicit control flow

^ _Marked propagation_ is a solution for these. I thought it was evolutional.

---

### Marked Automatic Propagation for Optionals

^ Now we have a question. _Marked automatic propagation_ seems good. Why don't we use it for _optionals_?

^ In the rationale, the core team said _optionals_ should be used for _simple domain errors_. They defined _simple domain errors_ as the errors which should be handled immediately. `toInt` was an example they gave. They concluded that the combination of _optionals_ and _manual propagation_ was suitable for those errors.

```swift
// [ Swift ]
// Simple domain error with manual propagation
guard let number = toInt(string) {
  // Error handling here
  ...
}
```

---

### Marked Automatic Propagation for Optionals

^ But I think _automatic propagation_ is also useful for _optionals_. We get `nil` not only as errors but also just as empty values. Our codes are full of _optionals_. Handling them manually costs a lot.

^ I propose _automatic propagation_ for _optionals_ this way.

```swift
// [ Swift ]
// Manual propagation
let a: Int? = toInt(aString)
let b: Int? = toInt(bString)
if let sum = (a.flatMap { a in b.map { b in a + b } }) {
    ...
} else {
    ...
}

// Automatic propagation
do {
  let a: Int = try toInt(aString)
  let b: Int = try toInt(bString)
  let sum: Int = a + b
  ...
} catch {
  ...
}
```

^ In this syntax, `try` is a kind of _unwrapping_. We must `catch` it or return an optional value.

^ I think this syntax is consistent.

---

### Results and try

^ This can be extended to _results_.

^ `throws` and _results_ can be theoretically interchanged. If `throws` were a syntactic sugar of returning a result, =>

```swift
// [ Swift ]
func toInt(string: String) throws -> Int {
  ...
}
```

```swift
// [ Swift ]
func toInt(string: String) -> Result<Int> {
  ...
}
```

---

### Results and try

^ we could connect the both worlds of `throws` and _results_ seamlessly.

```swift
// [ Swift ]
do {
  let a: Int = try toInt(aString)
  let b: Int = try toInt(bString)
  let sum: Int = a + b
  ...
} catch {
  ...
}
```

```swift
// [ Swift ]
let a: Result<Int> = toInt(aString)
let b: Result<Int> = toInt(bString)
switch a.flatMap { a in b.map { b in a + b } } {
  case let .Success(sum):
    ...
  case let .Failure(error):
    ...
}
```

^ _Results_ provide a more flexible way to handle errors like _optionals_. They can be handled lazily. So interoperability between them are important.

^ Let me show an example.

---

### Results and try

^ I implemented the library "ListK" ([^6]) which provides lazily evaluated `List`s. It makes it possible to create infinite lists.

^ In spite that they are infinite, we can `map` them because the operations are evaluated lazily.

```swift
// [ Swift ]
let infinite: List<Int> = List { $0 } // [0, 1, 2, 3, 4, ...]
let square: List<Int> = infinite.map { $0 * $0 } // [0, 1, 4, 9, 16, ...]
```

---

### Results and try

^ But, unlike `Array`'s `map`, it doesn't work well for a function with `throws`.

```swift
// [ Swift ]
func toInt(string: String) throws -> Int {
  ...
}

let strings: List<String> = ... // ["0", "1", "2", ...]
do {
  // Never finishes
  let numbers: List<Int> = try strings.map(transform: toInt)
} catch let error {
  ...
}
```

^ This `map` operation never finishes because it cannot be evaluated lazily.

---

### Results and try

^ `map` with `rethrows` can be regarded as overloaded two methods by _results_.

```swift
// [ Swift ]
// By throws
func map<U>(transform: T throws -> U) rethrows -> List<U>

// By `Result`
func map<U>(transform: T -> U) -> List<U>
func map<U>(transform: T -> Result<U>) -> Result<List<U>> // throws
```

^ The last one cannot be evaluated lazily because it must decide `Success` or `Failure` immediately.

---

### Results and try

^ What I want for my `List` is this.

```swift
// [ Swift ]
// By throws
func map<U>(transform: T throws -> U) rethrows -> List<U>

// By `Result`
func map<U>(transform: T -> U) -> List<U>
func map<U>(transform: T -> Result<U>) -> Result<List<U>> // throws
func map<U>(transform: T -> Result<U>) -> List<Result<U>> // <-This
```

---

### Results and try

^ Then we can `map` infinite `List`s with _automatic propagation_ by a function with `throws` this way.

```swift
// [ Swift ]
func toInt(string: String) throws -> Int {
  ...
}

do {
  let a: List<String> = ... // ["0", "1", "2", ...]
  let b: List<Result<Int>> = strings.map(transform: toInt)
    // [Result(0), Result(1), Result(2), ...]
  let c: List<Result<Int>> = numbers.take(10)
    // [Result(0), Result(1), ..., Result(9)]
  let d: Result<List<Int>> = sequence(first10)
    // Result([0, 1, ..., 9])
  let e: List<Int> = try d // [0, 1, ..., 9]
  ...
} catch let error {
  // Handling `FormatError`
  ...
}
```

---

### Results and try

^ Let me show you one downside of `throws` as `Result`.

^ With Swift 2.x, we get compilation errors at where we just omit `try`.

```swift
// Swift 2.x
let a = toInt(aString) // Compilation error here
let b = toInt(bString)
let sum = a + b
```

^ But with `throws` as `Result`, we get compilation errors where we try to use the result value.

```swift
// Swift with my proposal
let a = toInt(aString)
let b = toInt(bString)
let sum = a + b // Compilation error here
```

^ It's confusing and nonintuitive. But totally, I think `throws` as `Result` is better.

---

### Asynchronous Operations and try

^ Moreover, I think `try` can be used for other purposes besides error handling. An example is asynchronous operations.

^ JavaScript natively supports the `Promise` for asynchronous operations. Its `then` method is theoretically equivalent to `map` and `flatMap`. I implemented the `Promise` library "PromiseK" ([^7]) with them for Swift.

```swift
// [ Swift ]
let a: Promise<Int> = asyncGetInt(...)
let b: Promise<Int> = asyncGetInt(...)
let sum: Promise<Int> = a.flatMap { a in b.map { b in a + b } }
```

^ It's just like the `Result`.

```swift
// [ Swift ]
let a: Result<Int> = failableGetInt(...)
let b: Result<Int> = failableGetInt(...)
let sum: Result<Int> = a.flatMap { a in b.map { b in a + b } }
```

^ The only difference is asynchronous or failable.

---

### Asynchronous Operations and try

^ The future JavaScript will support the `async` / `await` syntax based on the one in C#. That syntax is backed by the `Promise` and makes it easier to write `then` chains.

^ I think we'll need to discuss the `async` / `await` syntax in Swift because asynchronous operations are one of the hottest topics in programming today.

```csharp
// [ C# ]
async Task<int> AsyncGetInt(...) {
  ...
}

async void PrintSum() {
  int a = await AsyncGetInt(...);
  int b = await AsyncGetInt(...);
  Console.WriteLine(a + b);
}
```

```swift
// [ Swift ]
func asyncGetInt(...) async -> Promise<Int> {
  ...
}

func printSum() async {
  let a: Int = await asyncGetInt(...)
  let b: Int = await asyncGetInt(...)
  print(a + b)
}
```

---

### Asynchronous Operations and try

^ The `async` / `await` syntax in C# is used like the upper one. This `Task` class in C# is equivalent to the `Promise`.

```csharp
// [ C# ]
async Task<int> AsyncGetInt(...) {
  ...
}

async void PrintSum() {
  int a = await AsyncGetInt(...);
  int b = await AsyncGetInt(...);
  Console.WriteLine(a + b);
}
```

^ If we had this syntax in Swift, it would be something like the lower one.

```swift
// [ Swift ]
func asyncGetInt(...) async -> Promise<Int> {
  ...
}

func printSum() async {
  let a: Int = await asyncGetInt(...)
  let b: Int = await asyncGetInt(...)
  print(a + b)
}
```

^ I want to change it in Swift to wrapping a return value in a `Promise` implicitly.

---

### Asynchronous Operations and try

```swift
// [ Swift ]
func asyncGetInt(...) async -> Int { // <- Changed Here
  ...
}

func printSum() async {
  let a: Int = await asyncGetInt(...)
  let b: Int = await asyncGetInt(...)
  print(a + b)
}
```

```swift
// [ Swift ]
func asyncGetInt(...) async -> Promise<Int> {
  ...
}

func printSum() async {
  let a: Int = await asyncGetInt(...)
  let b: Int = await asyncGetInt(...)
  print(a + b)
}
```

^ Now we can see the common relations between `async` / `await` and `throws` / `try`.

---

### Asynchronous Operations and try

```swift
// [ Swift ]
func asyncGetInt(...) async -> Int {     // async
  ...
}

func printSum() async {                  // async
  let a: Int = await asyncGetInt(...)    // await
  let b: Int = await asyncGetInt(...)    // await
  print(a + b)
}
```

```swift
// [ Swift ]
func failableGetInt(...) throws -> Int { // throws
  ...
}

func printSum() throws {                 // throws
  let a: Int = try failableGetInt(...)   // try
  let b: Int = try failableGetInt(...)   // try
  print(a + b)
}
```

^ The `async` / `await` syntax is backed by the `Promise`, and by my proposal, the `throws` / `try` syntax is backed by the `Result`. It perfectly makes sense. `async`, `await`, `Promise` and `throws`, `try`, `Result` represent a common concept only different in a point: asynchronous or failable.

---

### Asynchronous Operations and try

^ It's possible to unite them by using `try` as `await` and just returning `Promise` values.

```swift
// [ Swift ]
func asyncGetInt(...) async -> Int {     // async
  ...
}

do {
  let a: Int = await asyncGetInt(...)    // await
  let b: Int = await asyncGetInt(...)    // await
  print(a + b)
}
```

```swift
// [ Swift ]
func asyncGetInt(...) -> Promise<Int> {  // Promise
  ...
}

do {
  let a: Int = try asyncGetInt(...)      // try
  let b: Int = try asyncGetInt(...)      // try
  print(a + b)
}
```

^ It's good to have independent keywords like `async` because it makes easier to read the codes. But it needs other extra keywords endlessly when we want to add new features.

^ I'm wondering which one is better. I wanted to show you the possibilities of `try`.

---

### Let's Discuss Error Handling

^ I introduced my several ideas.

- `Result<T>` instead of `Result<T, E>`
- Automatic propagation for `Optional`s
- Interoperation between `throws` and `Result`
- `try` for asynchronous operations

... and let me know your opinions

^ I'm not very sure that they are all good. I wondered if I should talk about them because they were not a part of Swift. Just my ideas. But I thought it was important to begin discussions. So I decided to talk about them. I want to discuss error handling in Swift through this conference. So please let me know your opinions. And I will join in the swift-evolution mailing list because now I have time. I don't need any more time to prepare my presentation.

---

^ I'm dreaming of the world in which everyone has been educated in programming. I had even tried to design my own programming language suitable for education.

^ One morning, I met Swift. Swift seemed suited for my purpose. Now I plan to write a free online book for everyone to learn wide programming concepts, from "Hello, world!!" to monads, all in Swift.

^ Through my experience of designing programming languages, I can say that it is a struggle against unsafety and complexity. It can be said in other words: =>

---

# Stay Typed. Stay Practical.

^ "Stay Typed. Stay Practical." [^8]

^ I'm sure it makes the evolution as I talked through my presentation. Stay Typed. Stay Practical. And I have always wished that for Swift's designers. And now, as Swift became open source, it's us to make the Swift's evolution. I wish that for us.

^ Stay Typed, Stay Practical.

^ Thank you all very much.

[^1]: "SwiftyJSON", [https://github.com/SwiftyJSON/SwiftyJSON](https://github.com/SwiftyJSON/SwiftyJSON)

[^2]: "thoughtbot/Runes", [https://github.com/thoughtbot/Runes](https://github.com/thoughtbot/Runes)

[^3]: "antitypical/Result", [https://github.com/antitypical/Result](https://github.com/antitypical/Result)

[^4]: "ResultK", [https://github.com/koher/ResultK](https://github.com/koher/ResultK)

[^5]: "Error Handling Rationale and Proposal", [https://github.com/apple/swift/blob/master/docs/ErrorHandlingRationale.rst](https://github.com/apple/swift/blob/master/docs/ErrorHandlingRationale.rst)

[^6]: "ListK" [https://github.com/koher/ListK](https://github.com/koher/ListK)

[^7]: "PromiseK" [https://github.com/koher/PromiseK](https://github.com/koher/PromiseK)

[^8]: "Steve Jobs' Commencement address (2005)" [http://news.stanford.edu/news/2005/june15/jobs-061505.html](http://news.stanford.edu/news/2005/june15/jobs-061505.html)