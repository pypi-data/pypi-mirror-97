from . import tablemaker
import re
import collections
from threading import Lock
from .asciiMathConverter import convert
from .messages import error
from .javaScriptTagProcessing import picPathToDataURL # this should probably be stored in some utility destination instead - or the placement should be reversed

asciimath_delimiter_left="\$"
asciimath_delimiter_right="\$"

regexPlaceholderNumber = 0
regexNumberLock = Lock() # I do not think anyone will ever parallelize this, but here we go (assuming, that overwriting the used markdown will not cause problems - should be the same for one task)
usedMarkdown = None

# used to take parts out of a text toTransform with a regex, change them with some function applyThis and putting them back together
# with invertApplication = True everything else can be changed instead
# note that applyThis gets the found regex match if invertApplication is False, and otherwise the whole text with the found parts replaced with placeholders - this will cause errors if the placeholder is changed by one of these processing steps - however this should mostly be an issue with bad nesting of features, like verb tags inside an ascii math segment - and it retains the functionality of previous versions 
def apply_on_regex(toTransform, regex, applyThis, invertApplication = False):
    global regexPlaceholderNumber
    global regexNumberLock
    regexNumberLock.acquire()
    PLACEHOLDER = "HALLGRIMAPPLYONREGEXPLACEHOLDER" + str(regexPlaceholderNumber)
    regexNumberLock.release()
    regexPlaceholderNumber += 1
    found_parts = collections.deque()
    for m in re.finditer(regex, toTransform):
        found_parts.append(m)
    source = re.sub(regex, PLACEHOLDER, toTransform)
    if(invertApplication):
        source = applyThis(source)
        for a in range(len(found_parts)):
            found_parts.append(found_parts.popleft().groups()[0])
    else:
        for a in range(len(found_parts)):
            found_parts.append(applyThis(found_parts.popleft()))
    rests = collections.deque(source.split(PLACEHOLDER))
    final = collections.deque()
    for _ in range(min(len(rests), len(found_parts))):
            rest = rests.popleft()
            if rest != "":
                    final.append(rest)
            final.append(found_parts.popleft())
    final.extend(found_parts)
    final.extend(rests)
    final = "".join(final)
    return final

ASCII_MATH_TO_LATEX_REGEX = re.compile(asciimath_delimiter_left + '([\w\W]+?)'+ asciimath_delimiter_right, re.MULTILINE)
def ascii_math_to_latex_applicator(inp):
    return convert(inp.groups(2)[0], 'asciimath', 'latex')

IMAGE_INSERTION_REGEX = re.compile('\[image\]([\w\W]*?)(\[\/image\])', re.MULTILINE)
def image_insertion_applicator(inp):
    return ("<img src=\"" + picPathToDataURL(inp.groups()[0]) + "\">").replace("\\n","\n")

VERBATIM_REGEX = re.compile('\[verb\]([\w\W]+?)\[/verb\]', re.MULTILINE)
def verbatim_applicator(inp): # note that this is used in reverse i.e. this is applied to everything outside verb tags
    inp = apply_on_regex(inp, ASCII_MATH_TO_LATEX_REGEX, ascii_math_to_latex_applicator)
    inp = usedMarkdown(inp) # apply the markdown
    inp = tablemaker.prepareTables(inp) # apply tables
    inp = apply_on_regex(inp, IMAGE_INSERTION_REGEX, image_insertion_applicator) # insert images
    return inp

LINK_REGEX = re.compile('<a[\w\W]*?>[\w\W]*?</a>', re.MULTILINE)
def link_applicator(inp):
    currentLink = inp.group()
    return currentLink[0:2] + " target='_blank' class='HGMarkdownLink'" + currentLink[2:]

def pre_process_text(inp, markdown):
    """ Performs preprocessing on the text in the tasks. Currently consists of processing markdown with verbatim-tags, [table]-tags and asciiMath."""
    global usedMarkdown
    usedMarkdown = markdown
    inp = apply_on_regex(inp, VERBATIM_REGEX, verbatim_applicator, invertApplication = True)
    inp = apply_on_regex(inp, LINK_REGEX, link_applicator)
    return inp

