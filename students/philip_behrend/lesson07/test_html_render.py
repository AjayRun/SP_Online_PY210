"""
test code for html_render.py

This is just a start -- you will need more tests!
"""

import io
import pytest

# import * is often bad form, but makes it easier to test everything in a module.
from html_render import *


# utility function for testing render methods
# needs to be used in multiple tests, so we write it once here.
def render_result(element, ind=""):
    """
    calls the element's render method, and returns what got rendered as a
    string
    """
    # the StringIO object is a "file-like" object -- something that
    # provides the methods of a file, but keeps everything in memory
    # so it can be used to test code that writes to a file, without
    # having to actually write to disk.
    outfile = io.StringIO()
    # this so the tests will work before we tackle indentation
    if ind:
        element.render(outfile, ind)
    else:
        element.render(outfile)
    return outfile.getvalue()

########
# Step 1
########

def test_init():
    """
    This only tests that it can be initialized with and without
    some content -- but it's a start
    """
    e = Element()

    e = Element("this is some text")


def test_append():
    """
    This tests that you can append text

    It doesn't test if it works --
    that will be covered by the render test later
    """
    e = Element("this is some text")
    e.append("some more text")


def test_render_element():
    """
    Tests whether the Element can render two pieces of text
    So it is also testing that the append method works correctly.

    It is not testing whether indentation or line feeds are correct.
    """
    e = Element("this is some text")
    e.append("and this is some more text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # making sure the content got in there.
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    # make sure it's in the right order
    assert file_contents.index("this is") < file_contents.index("and this")

    # making sure the opening and closing tags are right.
    assert file_contents.startswith("<html")
    assert file_contents.endswith("</html>")

 # Does it pass right away? No, need to change None to ""
def test_render_element2():
    """
    Tests whether the Element can render two pieces of text
    So it is also testing that the append method works correctly.

    It is not testing whether indentation or line feeds are correct.
    """
    e = Element()
    e.append("this is some text")
    e.append("and this is some more text")
    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # making sure the content got in there.
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    # make sure it's in the right order
    assert file_contents.index("this is") < file_contents.index("and this")

    # making sure the opening and closing tags are right.
    assert file_contents.startswith("<html")
    assert file_contents.endswith("</html>")



 ########
 # Step 2
 ########

 # tests for the new tags
def test_html():
    e = Html("this is some text")
    e.append("and this is some more text")
    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents
    print(file_contents)
    assert file_contents.endswith("</html>")


def test_body():
    e = Body("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<body")
    assert file_contents.endswith("</body>")


def test_p():
    e = P("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<p")
    assert file_contents.endswith("</p>")

def test_sub_element():
    """
    tests that you can add another element and still render properly
    """
    page =  Html()
    page.append("some plain text.")
    page.append(P("A simple paragraph of text"))
    page.append("Some more plain text.")

    file_contents = render_result(page)
    print(file_contents) # so we can see it if the test fails

    # note: The previous tests should make sure that the tags are getting
    #       properly rendered, so we don't need to test that here.
    assert "some plain text" in file_contents
    assert "A simple paragraph of text" in file_contents
    assert "Some more plain text." in file_contents
    assert "some plain text" in file_contents
    # but make sure the embedded element's tags get rendered!
    assert "<p" in file_contents
    assert "</p>" in file_contents




#######
#Step 3
#######

def test_one_line_tag():
    e = OneLineTag("text here")
    e.append("mas palabras")
    file_contents = render_result(e).strip()
    assert "text here" in file_contents
    assert "mas palabras" in file_contents
    assert "\n" not in file_contents

def test_title():
    e = Title("some text")
    e.append("more of the same")
    
    file_contents = render_result(e).strip()

    assert "some text" in file_contents
    assert "more of the same" in file_contents

    assert file_contents.startswith("<title>")
    assert file_contents.endswith("</title>")

def test_attributes():
    e = P("A paragraph of text", style="text-align: center", id="intro")

    file_contents = render_result(e).strip()
    assert "A paragraph of text" in file_contents
    assert file_contents.startswith("<p")
    assert 'style="text-align: center"' in file_contents
    assert 'id="intro"' in file_contents 
    assert file_contents.endswith("</p>")
    print(file_contents)  # so we can see it if the test fails

def test_self_closing_tag():
    e = SelfClosingTag()
    file_contents = render_result(e).strip()
    assert file_contents.startswith('<')
    assert file_contents.endswith('/>')

def test_hr():
    e = Hr(width=400)
    file_contents = render_result(e).strip()
    assert file_contents.startswith('<hr')
    assert 'width="400"' in file_contents

def test_br():
    e = Br(width=400)
    file_contents = render_result(e).strip()
    assert file_contents.startswith('<br')
    assert 'width="400"' in file_contents

def test_A():
    e = A("http://google.com", "link to google")
    file_contents = render_result(e).strip()
    assert file_contents.startswith('<a')
    assert 'href=http://google.com' in file_contents

def test_ul():
    e = Ul()
    file_contents = render_result(e).strip()
    assert file_contents.startswith('<ul')
    assert file_contents.endswith('</ul>')

def test_li():
    e = Li()
    file_contents = render_result(e).strip()
    assert file_contents.startswith('<li')
    assert file_contents.endswith('</li>')

def test_h():
    e = H(2, "The text of the header")
    file_contents = render_result(e).strip()
    assert file_contents.startswith('<h2')
    assert "The text of the header" in file_contents
    assert file_contents.endswith('</h2>')

def test_meta():
    e = Meta(charset="UTF-8")
    file_contents = render_result(e).strip()

def test_head():
    e = Head("this is some text")
    e.append(" and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents
    assert("<meta charset=\"UTF-8\" />") in file_contents

    assert file_contents.startswith("<head")
    assert file_contents.endswith("</head>")



#####################
# indentation testing
#  Uncomment for Step 9 -- adding indentation
#####################


def test_indent():
    """
    Tests that the indentation gets passed through to the renderer
    """
    html = Html("some content")
    file_contents = render_result(html, ind="   ").rstrip()  #remove the end newline

    print(file_contents)
    lines = file_contents.split("\n")
    assert lines[1].startswith("   ")
    print(repr(lines[-1]))
    assert lines[-1].startswith("   <")


def test_indent_contents():
    """
    The contents in a element should be indented more than the tag
    by the amount in the indent class attribute
    """
    html = Element("some content")
    file_contents = render_result(html, ind="    ")

    print(file_contents)
    lines = file_contents.split("\n")
    assert lines[1].startswith(Element.ind)


def test_multiple_indent():
    """
    make sure multiple levels get indented fully
    """
    body = Body()
    body.append(P("some text"))
    html = Html(body)

    file_contents = render_result(html,ind = '    ')

    print(file_contents)
    lines = file_contents.split("\n")
    for i in range(3):  # this needed to be adapted to the <DOCTYPE> tag
        assert lines[i + 1].startswith(i * Element.ind + "<")

    assert lines[4].startswith(3 * Element.ind + "some")


def test_element_indent1():
    """
    Tests whether the Element indents at least simple content

    we are expecting to to look like this:

    <html>
        this is some text
    <\html>

    More complex indentation should be tested later.
    """
    e = Element("this is some text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # making sure the content got in there.
    assert("this is some text") in file_contents

    # break into lines to check indentation
    lines = file_contents.split('\n')
    # making sure the opening and closing tags are right.
    assert lines[0] == "<html >"
    # this line should be indented by the amount specified
    # by the class attribute: "indent"
    assert lines[1].startswith(Element.ind + "thi")
    assert lines[2] == "</html>"
    assert file_contents.endswith("</html>")
