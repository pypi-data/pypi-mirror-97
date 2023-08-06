# Abnormal expressions
Abnormal expressions (abnex) is an alternative to regular expressions (regex).
This is a Python library but the abnex syntax could be ported to other languages.

# Examples
## Matching an email address
- Regex
  - `([\w\._-]+)@([\w\.]+)`
- Abnex
  - `{[w"._-"]1++}"@"{[w"."]1++}`
- Abnex (spaced)
  - `{[w "._-"]1++} "@" {[w "."]1++}`

- Abnex (expanded)
  ```
  {
    [w "._-"]1++
  }
  "@"
  {
    [w "."]1++
  }
  ```
  ## A more advanced pattern:
  `{{{[a-z '_']1++} {[a-z 0-9 '_-.']0++}} '@' {{[a-z 0-9]1++} '.' {[a-z 0-9]1++} {[a-z 0-9 '-_.']0++}} {[a-z 0-9]1++}}`.

# Why is Abnex Better?
- It's easier to read, write and understand.
- You can use spaces inside of the expression, you can also "expand" it, i.e. write it over multiple lines and use indention.
- You don't have to use a backslashes all the time
- More logical/common symbols like `!` for _not_, `{}` for _groups_, `1++`, `0++`, `0+` for: _one or more_, _zero or more_, _zero or one_.
- It's easier to see if a symbol is an actual symbol you are searching for or if it's a regex character, ex:
  - Regex: `[\w-]+@[\w-_]+`
  - Abnex: `[w "-"]1++ "@" [w "-"]1++`

# Documentation
### Regex on right after -> is the abnex equivalent
## Anchors
- Start of string, or start of line in multi-line pattern
  - `^` -> `->`
- End of string, or end of line in multi-line pattern
  - `$` -> `<-`
- Start of string
  - `\A` -> `s>`
- End of string
  - `\Z` -> `<s`
- Word boundary
  - `\b` -> `:`
- Not word boundary
  - `\B` -> `!:`
- Start of word
  - `\<` -> `w>`
- End of word
  - `\>` -> `<w`

## Character Classes
- Control character
  - `\c` -> `c`
- White space
  - `\s` -> `_`
- Not white space
  - `\S` -> `!_`
- Digit
  - `\d` -> `d`
- Not digit
  - `\D` -> `!d`
- Word
  - `\w` -> `w`
- Not word
  - `\W` -> `!w`
- Hexade­cimal digit
  - `\x` -> `x`
- Octal digit
  - `\o` -> `o`

## Quantifiers
- 0 or more
  - `*` -> `0++`
- 1 or more
  - `+` -> `1++`
- 0 or 1
  - `?` -> `0+`

## Groups and Ranges
- Any character except new line (\n)
  - `.` -> `*`
- a or b
  - `a|b` -> `"a"|"b"`
- Group
  - `(...)` -> `{...}`
- Passive (non-c­apt­uring) group
  - `(?:...)` -> `{#...}`
- Range (a or b or c)
  - `[abc]` -> `['abc']` or `["a" "b" "c"]`
- Not in set
  - `[^...]` -> `[!...]`
- Lower case letter from a to Z
  - `[a-q]` -> `[a-z]`
- Upper case letter from A to Q
  - `[A-Q]` -> `[A-Q]`
- Digit from 0 to 7
  - `[0-7]` -> `[0-7]`

# Standards
What is the recommended way to write abnexes

- Use spaces between characters in character sets:
  - Correct: `[w "_-"]`
  - Incorrect: `[w"_-"]`
- Put multiple exact characters between the same quotes in character sets:
  - Correct: `["abc"]`
  - Incorrect: `["a" "b" "c"]`, especially incorrect: `["a""b""c"]`
- Put spaces between groups:
  - Correct: `{w} "." {w}`
  - Incorrect: `{w}"."{w}`

### Examples:
Match for an email address:
- Regex:
  - `[\w-\._]+@[\w-\.]+`
- Abnex (following standards):
  - `{[w "-._"]1++} "@" {[w "-."]1++}`
- Abnex (not following standards):
  - `{[w"-._"]1++}"@"{[w"-."]1++}`
  
# Functions (In Python)
__Abnex has most functions from the `re` library, but it also has som extra functionality like: `last()` & `contains()`.__

## Common functions between re and abnex
### Regex on right after -> is the abnex equivalent
- `match()` -> `match()`
- `findall()` -> `all()`
- `split()` -> `split()`
- `sub()` -> `replace()`
- `subn()` -> `replace_count()`
- `search()` -> `first()`
## Special to abnex
- `holds()`: whether or not a string matches an expression (bool).
- `contains()`: wheter or not a string contains a match (bool).
- `last()`: the last match in a string.
