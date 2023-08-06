# gemini_builder

This Python package makes creation of Gemini text documents for
[Project Gemini](https://gemini.circumlunar.space/) a little
easier.

To create a document, instantiate the Page class and add lines
using the appropriate methods. Finally, you can convert the
page to a string, print it, etc.

## Methods

The following methods are used to add content to the page:

### add_raw_line(raw_line)

Add any text as a line. Be cautious or you will screw everything up.

### add_text(line=None)

Add normal text as a line. Can also be used to add an empty line.

### add_heading(text, level=1)

Add a heading line. You can provide a level of 1, 2 or 3.

### add_link(url, label=None)

Add a link line. The URL must already be properly quoted.

### add_quote(quote)

Add a quote line.

### add_list(items)

Add a list. The items argument should be an iterable that returns strings.

### add_preformatted_lines(preformatted_lines, alt_text=None):

Add a block of preformatted lines. The preformatted_lines argument should be an iterable that returns strings. The optional alt_text argument will be added to the opening toggle line if present.

## Exceptions

The following exceptions can be thrown:

### GeminiBuilderException

Base class for all exceptions. Not instantiated.

### InvalidHeadingLevelException

You tried to add a heading with a level that is not 1, 2 or 3.

### NotIterableException

You tried to add a list but provided a non-iterable argument.

### InvalidTextLineException

You provided a text line that starts with one of the reserved characters. Use add_raw_line to add any raw content.

### PreformattedLineCannotStartLikeThisException

One of your pre-formatted lines begins with the reserved sequence for preformatted lines.