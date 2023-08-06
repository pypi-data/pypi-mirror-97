#! /usr/bin/python3
#
# Copyright © 2021 Martin Ibert
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

class GeminiBuilderException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class InvalidHeadingLevelException(GeminiBuilderException):

    def __init__(self, level):
        self.message = "Heading level " + str(level) + " invalid"

class NotIterableException(GeminiBuilderException):

    def __init__(self):
        self.message = "Argument is not iterable"

class InvalidTextLineException(GeminiBuilderException):

    def __init__(self):
        self.message = "Text line cannot start like this"

class PreformattedLineCannotStartLikeThisException(GeminiBuilderException):

    def __init__(self):
        self.message = "Preformatted line cannot start like this"

class Page:

    def __init__(self):
        self.__lines__ = []

    def __str__(self):
        if self.__lines__:
            return "\r\n".join(self.__lines__) + "\r\n"
        else:
            return ""

    def add_raw_line(self, raw_line):
        self.__lines__.append(raw_line)

    def add_text(self, line=None):
        if line is None:
            line = ""
        elif line.startswith("#") or line.startswith(">") or line.startswith("=>") or line.startswith("* ") or line.startswith("```"):
            raise InvalidTextLineException
        self.add_raw_line(line)

    def add_heading(self, text, level=1):

        if level != 1 and level != 2 and level != 3:
            raise InvalidHeadingLevelException(level)

        self.add_raw_line("#" * level + " " + text)

    def add_link(self, url, label=None):

        line = "=> " + url
        if label is not None:
            line += " " + label
        
        self.add_raw_line(line)

    def add_quote(self, quote):
        self.add_raw_line(">" + quote)

    def add_list(self, items):

        iterable = None
        try:
            iterable = iter(items)
        except TypeError:
            raise NotIterableException

        for item in iterable:
            self.add_raw_line("* " + item)

    def add_preformatted_lines(self, preformatted_lines, alt_text=None):

        try:
            iterator = iter(preformatted_lines)
        except TypeError:
            raise NotIterableException

        raw_line = "```"
        if alt_text is not None:
            raw_line += alt_text
        self.add_raw_line(raw_line)
        for raw_line in iterator:
            if(raw_line.startswith("```")):
                raise PreformattedLineCannotStartLikeThisException
            self.add_raw_line(raw_line)
        self.add_raw_line("```")

# main

if __name__ == "__main__":
    
    page = Page()

    page.add_heading("Hello, world!")
    page.add_heading("Wassup?", 2)
    page.add_heading("Lorum", 3)
    page.add_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    page.add_heading("Mary", 3)
    page.add_text("Mary had a little lamb,")
    page.add_text("Whose fleece was white as snow.")
    page.add_text("And everywhere that Mary went,")
    page.add_text("The lamb was sure to go.")
    page.add_heading("Quote", 3)
    page.add_quote("Always look on the bright side of life!")
    page.add_list(["first", "second", "third"])
    page.add_link("http://01n.de/", "Are we live yet?")
    page.add_link("https://google.de/")
    page.add_preformatted_lines(("10 PRINT \"HELLO WORLD\"", "20 GOTO 10"), "Endless loop")
    try:
        page.add_heading("Four", 4)
        raise InvalidHeadingLevelException
    except InvalidHeadingLevelException:
        pass
    try:
        page.add_text("=>")
        raise InvalidTextLineException
    except InvalidTextLineException:
        pass
    

    print(page)