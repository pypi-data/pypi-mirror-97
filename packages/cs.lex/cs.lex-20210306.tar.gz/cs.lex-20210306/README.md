Lexical analysis functions, tokenisers, transcribers:
an arbitrary assortment of lexical and tokenisation functions useful
for writing recursive descent parsers, of which I have several.
There are also some transcription functions for producing text
from various objects, such as `hexify` and `unctrl`.

*Latest release 20210306*:
* New cropped() function to crop strings.
* Rework cropped_repr() to do the repr() itself, and to crop the interiors of tuples and lists.
* cropped_repr: new inner_max_length for cropping the members of collections.
* cropped_repr: special case for length=1 tuples.
* New typed_str(o) object returning type(o).__name__:str(o) in the default case, useful for debugging.

Generally the get_* functions accept a source string and an offset
(usually optional, default `0`) and return a token and the new offset,
raising `ValueError` on failed tokenisation.

## Function `as_lines(chunks, partials=None)`

Generator yielding complete lines from arbitrary pieces of text from
the iterable of `str` `chunks`.

After completion, any remaining newline-free chunks remain
in the partials list; they will be unavailable to the caller
unless the list is presupplied.

## Function `common_prefix(*strs)`

Return the common prefix of the strings `strs`.

Examples:

    >>> common_prefix('abc', 'def')
    ''
    >>> common_prefix('abc', 'abd')
    'ab'
    >>> common_prefix('abc', 'abcdef')
    'abc'
    >>> common_prefix('abc', 'abcdef', 'abz')
    'ab'
    >>> # contrast with cs.fileutils.common_path_prefix
    >>> common_prefix('abc/def', 'abc/def1', 'abc/def2')
    'abc/def'

## Function `common_suffix(*strs)`

Return the common suffix of the strings `strs`.

## Function `cropped(s: str, max_length: int = 32, roffset: int = 1, ellipsis: str = '...')`

If the length of `s` exceeds `max_length` (default `32`),
replace enough of the tail with `ellipsis`
and the last `roffset` (default `1`) characters of `s`
to fit in `max_length` characters.

## Function `cropped_repr(o, roffset=1, max_length=32, inner_max_length=None)`

Compute a cropped `repr()` of `o`.

Parameters:
* `o`: the object to represent
* `max_length`: the maximum length of the representation, default `32`
* `inner_max_length`: the maximum length of the representations
  of members of `o`, default `max_length//2`
* `roffset`: the number of trailing characters to preserve, default `1`

## Function `cutprefix(s, prefix)`

Strip a `prefix` from the front of `s`.
Return the suffix if `s.startswith(prefix)`, else `s`.

Example:

    >>> abc_def = 'abc.def'
    >>> cutprefix(abc_def, 'abc.')
    'def'
    >>> cutprefix(abc_def, 'zzz.')
    'abc.def'
    >>> cutprefix(abc_def, '.zzz') is abc_def
    True

## Function `cutsuffix(s, suffix)`

Strip a `suffix` from the end of `s`.
Return the prefix if `s.endswith(suffix)`, else `s`.

Example:

    >>> abc_def = 'abc.def'
    >>> cutsuffix(abc_def, '.def')
    'abc'
    >>> cutsuffix(abc_def, '.zzz')
    'abc.def'
    >>> cutsuffix(abc_def, '.zzz') is abc_def
    True

## Function `format_as(format_s, format_mapping, error_sep=None)`

Format the string `format_s` using `str.format_mapping`,
return the formatted result.
This is a wrapper for `str.format_map`
which raises a more informative `FormatAsError` exception on failure.

Parameters:
* `format_s`: the format string to use as the template
* `format_mapping`: the mapping of available replacement fields
* `error_sep`: optional separator for the multipart error message,
  default from `FormatAsError.DEFAULT_SEPARATOR`:
  `'; '`

## Function `format_escape(s)`

Escape `{}` characters in a string to protect them from `str.format`.

## Class `FormatableMixin`

A mixin to supply a `format_as` method for classes with an
existing `format_kwargs` method.

The `format_as` method is like an inside out `str.format` or
`object.__format__` method.
The `str.format` method is designed for formatting a string
from a variety of other objects supplied in the keyword arguments,
and the `object.__format__` method is for filling out a single `str.format`
replacement field from a single object.
By contrast, `format_as` is designed to fill out an entire format
string from the current object.

For example, the `cs.tagset.TagSetMixin` class
uses `FormatableMixin` to provide a `format_as` method
whose replacement fields are derived from the tags in the tag set.

### Method `FormatableMixin.format_as(self, format_s, error_sep=None, **control_kw)`

Return the string `format_s` formatted using the mapping
returned by `self.format_kwargs(**control_kw)`.

The class using this mixin must provide
a `format_kwargs(**control_kw)` method
to compute the mapping provided to `str.format_map`.

## Class `FormatAsError(builtins.LookupError,builtins.Exception,builtins.BaseException)`

Subclass of `LookupError` for use by `format_as`.

## Function `get_chars(s, offset, gochars)`

Scan the string `s` for characters in `gochars` starting at `offset`.
Return `(match,new_offset)`.

`gochars` may also be a callable, in which case a character
`ch` is accepted if `gochars(ch)` is true.

## Function `get_decimal(s, offset=0)`

Scan the string `s` for decimal characters starting at `offset` (default `0`).
Return `(dec_string,new_offset)`.

## Function `get_decimal_or_float_value(s, offset=0)`

Fetch a decimal or basic float (nnn.nnn) value
from the str `s` at `offset` (default `0`).
Return `(value,new_offset)`.

## Function `get_decimal_value(s, offset=0)`

Scan the string `s` for a decimal value starting at `offset` (default `0`).
Return `(value,new_offset)`.

## Function `get_delimited(s, offset, delim)`

Collect text from the string `s` from position `offset` up
to the first occurence of delimiter `delim`; return the text
excluding the delimiter and the offset after the delimiter.

## Function `get_dotted_identifier(s, offset=0, **kw)`

Scan the string `s` for a dotted identifier (by default an
ASCII letter or underscore followed by letters, digits or
underscores) with optional trailing dot and another dotted
identifier, starting at `offset` (default `0`).
Return `(match,new_offset)`.

Note: the empty string and an unchanged offset will be returned if
there is no leading letter/underscore.

Keyword arguments are passed to `get_identifier`
(used for each component of the dotted identifier).

## Function `get_envvar(s, offset=0, environ=None, default=None, specials=None)`

Parse a simple environment variable reference to $varname or
$x where "x" is a special character.

Parameters:
* `s`: the string with the variable reference
* `offset`: the starting point for the reference
* `default`: default value for missing environment variables;
   if `None` (the default) a `ValueError` is raised
* `environ`: the environment mapping, default `os.environ`
* `specials`: the mapping of special single character variables

## Function `get_hexadecimal(s, offset=0)`

Scan the string `s` for hexadecimal characters starting at `offset` (default `0`).
Return `(hex_string,new_offset)`.

## Function `get_hexadecimal_value(s, offset=0)`

Scan the string `s` for a hexadecimal value starting at `offset` (default `0`).
Return `(value,new_offset)`.

## Function `get_identifier(s, offset=0, alpha='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', number='0123456789', extras='_')`

Scan the string `s` for an identifier (by default an ASCII
letter or underscore followed by letters, digits or underscores)
starting at `offset` (default 0).
Return `(match,new_offset)`.

*Note*: the empty string and an unchanged offset will be returned if
there is no leading letter/underscore.

Parameters:
* `s`: the string to scan
* `offset`: the starting offset, default `0`.
* `alpha`: the characters considered alphabetic,
  default `string.ascii_letters`.
* `number`: the characters considered numeric,
  default `string.digits`.
* `extras`: extra characters considered part of an identifier,
  default `'_'`.

## Function `get_ini_clause_entryname(s, offset=0)`

Parse a `[`*clausename*`]`*entryname* string
from `s` at `offset` (default `0`).
Return `(clausename,entryname,new_offset)`.

## Function `get_ini_clausename(s, offset=0)`

Parse a `[`*clausename*`]` string from `s` at `offset` (default `0`).
Return `(clausename,new_offset)`.

## Function `get_nonwhite(s, offset=0)`

Scan the string `s` for characters not in `string.whitespace`
starting at `offset` (default `0`).
Return `(match,new_offset)`.

## Function `get_other_chars(s, offset=0, stopchars=None)`

Scan the string `s` for characters not in `stopchars` starting
at `offset` (default `0`).
Return `(match,new_offset)`.

## Function `get_qstr(s, offset=0, q='"', environ=None, default=None, env_specials=None)`

Get quoted text with slosh escapes and optional environment substitution.

Parameters:
* `s`: the string containg the quoted text.
* `offset`: the starting point, default `0`.
* `q`: the quote character, default `'"'`. If `q` is `None`,
  do not expect the string to be delimited by quote marks.
* `environ`: if not `None`, also parse and expand `$`*envvar* references.
* `default`: passed to `get_envvar`

## Function `get_qstr_or_identifier(s, offset)`

Parse a double quoted string or an identifier.

## Function `get_sloshed_text(s, delim, offset=0, slosh='\\', mapper=<function slosh_mapper at 0x108d571f0>, specials=None)`

Collect slosh escaped text from the string `s` from position
`offset` (default `0`) and return the decoded unicode string and
the offset of the completed parse.

Parameters:
* `delim`: end of string delimiter, such as a single or double quote.
* `offset`: starting offset within `s`, default `0`.
* `slosh`: escape character, default a slosh ('\').
* `mapper`: a mapping function which accepts a single character
  and returns a replacement string or `None`; this is used the
  replace things such as '\t' or '\n'. The default is the
  `slosh_mapper` function, whose default mapping is `SLOSH_CHARMAP`.
* `specials`: a mapping of other special character sequences and parse
  functions for gathering them up. When one of the special
  character sequences is found in the string, the parse
  function is called to parse at that point.
  The parse functions accept
  `s` and the offset of the special character. They return
  the decoded string and the offset past the parse.

The escape character `slosh` introduces an encoding of some
replacement text whose value depends on the following character.
If the following character is:
* the escape character `slosh`, insert the escape character.
* the string delimiter `delim`, insert the delimiter.
* the character 'x', insert the character with code from the following
  2 hexadecimal digits.
* the character 'u', insert the character with code from the following
  4 hexadecimal digits.
* the character 'U', insert the character with code from the following
  8 hexadecimal digits.
* a character from the keys of `mapper`

## Function `get_tokens(s, offset, getters)`

Parse the string `s` from position `offset` using the supplied
tokeniser functions `getters`.
Return the list of tokens matched and the final offset.

Parameters:
* `s`: the string to parse.
* `offset`: the starting position for the parse.
* `getters`: an iterable of tokeniser specifications.

Each tokeniser specification `getter` is either:
* a callable expecting `(s,offset)` and returning `(token,new_offset)`
* a literal string, to be matched exactly
* a `tuple` or `list` with values `(func,args,kwargs)`;
  call `func(s,offset,*args,**kwargs)`
* an object with a `.match` method such as a regex;
  call `getter.match(s,offset)` and return a match object with
  a `.end()` method returning the offset of the end of the match

## Function `get_uc_identifier(s, offset=0, number='0123456789', extras='_')`

Scan the string `s` for an identifier as for `get_identifier`,
but require the letters to be uppercase.

## Function `get_white(s, offset=0)`

Scan the string `s` for characters in `string.whitespace`
starting at `offset` (default `0`).
Return `(match,new_offset)`.

## Function `hexify(bs)`

A flavour of `binascii.hexlify` returning a `str`.

## Function `htmlify(s, nbsp=False)`

Convert a string for safe transcription in HTML.

Parameters:
* `s`: the string
* `nbsp`: replaces spaces with `"&nbsp;"` to prevent word folding,
  default `False`.

## Function `htmlquote(s)`

Quote a string for use in HTML.

## Function `is_dotted_identifier(s, offset=0, **kw)`

Test if the string `s` is an identifier from position `offset` onward.

## Function `is_identifier(s, offset=0, **kw)`

Test if the string `s` is an identifier
from position `offset` (default `0`) onward.

## Function `isUC_(s)`

Check that a string matches the regular expression `^[A-Z][A-Z_0-9]*$`.

## Function `jsquote(s)`

Quote a string for use in JavaScript.

## Function `lc_(value)`

Return `value.lower()`
with `'-'` translated into `'_'` and `' '` translated into `'-'`.

I use this to construct lowercase filenames containing a
readable transcription of a title string.

See also `titleify_lc()`, an imperfect reversal of this.

## Function `match_tokens(s, offset, getters)`

Wrapper for `get_tokens` which catches `ValueError` exceptions
and returns `(None,offset)`.

## Function `parseUC_sAttr(attr)`

Take an attribute name `attr` and return `(key,is_plural)`.

Examples:
* `'FOO'` returns `('FOO',False)`.
* `'FOOs'` or `'FOOes'` returns `('FOO',True)`.
Otherwise return `(None,False)`.

## Function `phpquote(s)`

Quote a string for use in PHP code.

## Function `skipwhite(s, offset=0)`

Convenience routine for skipping past whitespace;
returns the offset of the next nonwhitespace character.

## Function `slosh_mapper(c, charmap=None)`

Return a string to replace backslash-`c`, or `None`.

## Function `stripped_dedent(s)`

Slightly smarter dedent which ignores a string's opening indent.

Algorithm:
strip the supplied string `s`, pull off the leading line,
dedent the rest, put back the leading line.

This supports my preferred docstring layout, where the opening
line of text is on the same line as the opening quote.

Example:

    >>> def func(s):
    ...   """ Slightly smarter dedent which ignores a string's opening indent.
    ...       Strip the supplied string `s`. Pull off the leading line.
    ...       Dedent the rest. Put back the leading line.
    ...   """
    ...   pass
    ...
    >>> from cs.lex import stripped_dedent
    >>> print(stripped_dedent(func.__doc__))
    Slightly smarter dedent which ignores a string's opening indent.
    Strip the supplied string `s`. Pull off the leading line.
    Dedent the rest. Put back the leading line.

## Function `strlist(ary, sep=', ')`

Convert an iterable to strings and join with `sep` (default `', '`).

## Function `tabpadding(padlen, tabsize=8, offset=0)`

Compute some spaces to use a tab padding at an offfset.

## Function `texthexify(bs, shiftin='[', shiftout=']', whitelist=None)`

Transcribe the bytes `bs` to text using compact text runs for
some common text values.

This can be reversed with the `untexthexify` function.

This is an ad doc format devised to be compact but also to
expose "text" embedded within to the eye. The original use
case was transcribing a binary directory entry format, where
the filename parts would be somewhat visible in the transcription.

The output is a string of hexadecimal digits for the encoded
bytes except for runs of values from the whitelist, which are
enclosed in the shiftin and shiftout markers and transcribed
as is. The default whitelist is values of the ASCII letters,
the decimal digits and the punctuation characters '_-+.,'.
The default shiftin and shiftout markers are '[' and ']'.

String objects converted with either `hexify` and `texthexify`
output strings may be freely concatenated and decoded with
`untexthexify`.

Example:

    >>> texthexify(b'&^%&^%abcdefghi)(*)(*')
    '265e25265e25[abcdefghi]29282a29282a'

Parameters:
* `bs`: the bytes to transcribe
* `shiftin`: Optional. The marker string used to indicate a shift to
  direct textual transcription of the bytes, default: `'['`.
* `shiftout`: Optional. The marker string used to indicate a
  shift from text mode back into hexadecimal transcription,
  default `']'`.
* `whitelist`: an optional bytes or string object indicating byte
  values which may be represented directly in text;
  the default value is the ASCII letters, the decimal digits
  and the punctuation characters `'_-+.,'`.

## Function `titleify_lc(value_lc)`

Translate `'-'` into `' '` and `'_'` translated into `'-'`,
then titlecased.

See also `lc_()`, which this reverses imperfectly.

## Function `typed_str(o, use_cls=False, use_repr=False, max_length=None)`

Return "type(o).__name__:str(o)" for some object `o`.

Parameters:
* `use_cls`: default `False`;
  if true, use `str(type(o))` instead of `type(o).__name__`
* `use_repr`: default `False`;
  if true, use `repr(o)` instead of `str(o)`

I use this a lot when debugging. Example:

    from cs.lex import typed_str as s
    ......
    X("foo = %s", s(foo))

## Function `unctrl(s, tabsize=8)`

Return the string `s` with `TAB`s expanded and control characters
replaced with printable representations.

## Function `untexthexify(s, shiftin='[', shiftout=']')`

Decode a textual representation of binary data into binary data.

This is the reverse of the `texthexify` function.

Outside of the `shiftin`/`shiftout` markers the binary data
are represented as hexadecimal. Within the markers the bytes
have the values of the ordinals of the characters.

Example:

    >>> untexthexify('265e25265e25[abcdefghi]29282a29282a')
    b'&^%&^%abcdefghi)(*)(*'

Parameters:
* `s`: the string containing the text representation.
* `shiftin`: Optional. The marker string commencing a sequence
  of direct text transcription, default `'['`.
* `shiftout`: Optional. The marker string ending a sequence
  of direct text transcription, default `']'`.

# Release Log



*Release 20210306*:
* New cropped() function to crop strings.
* Rework cropped_repr() to do the repr() itself, and to crop the interiors of tuples and lists.
* cropped_repr: new inner_max_length for cropping the members of collections.
* cropped_repr: special case for length=1 tuples.
* New typed_str(o) object returning type(o).__name__:str(o) in the default case, useful for debugging.

*Release 20201228*:
Minor doc updates.

*Release 20200914*:
* Hide terribly special purpose lastlinelen() in cs.hier under a private name.
* New common_prefix and common_suffix function to compare strings.

*Release 20200718*:
get_chars: accept a callable for gochars, indicating a per character test function.

*Release 20200613*:
cropped_repr: replace hardwired 29 with computed length

*Release 20200517*:
* New get_ini_clausename to parse "[clausename]".
* New get_ini_clause_entryname parsing "[clausename]entryname".
* New cropped_repr for returning a shortened repr()+"..." if the length exceeds a threshold.
* New format_escape function to double {} characters to survive str.format.

*Release 20200318*:
* New lc_() function to lowercase and dash a string, new titleify_lc() to mostly reverse lc_().
* New format_as function, FormatableMixin and related FormatAsError.

*Release 20200229*:
New cutprefix and cutsuffix functions.

*Release 20190812*:
Fix bad slosh escapes in strings.

*Release 20190220*:
New function get_qstr_or_identifier.

*Release 20181108*:
new function get_decimal_or_float_value to read a decimal or basic float

*Release 20180815*:
No semantic changes; update some docstrings and clean some lint, fix a unit test.

*Release 20180810*:
* New get_decimal_value and get_hexadecimal_value functions.
* New stripped_dedent function, a slightly smarter textwrap.dedent.

*Release 20171231*:
New function get_decimal. Drop unused function dict2js.

*Release 20170904*:
Python 2/3 ports, move rfc2047 into new cs.rfc2047 module.

*Release 20160828*:
* Use "install_requires" instead of "requires" in DISTINFO.
* Discard str1(), pointless optimisation.
* unrfc2047: map _ to SPACE, improve exception handling.
* Add phpquote: quote a string for use in PHP code; add docstring to jsquote.
* Add is_identifier test.
* Add get_dotted_identifier.
* Add is_dotted_identifier.
* Add get_hexadecimal.
* Add skipwhite, convenince wrapper for get_white returning just the next offset.
* Assorted bugfixes and improvements.

*Release 20150120*:
cs.lex: texthexify: backport to python 2 using cs.py3 bytes type

*Release 20150118*:
metadata updates

*Release 20150116*:
PyPI metadata and slight code cleanup.
