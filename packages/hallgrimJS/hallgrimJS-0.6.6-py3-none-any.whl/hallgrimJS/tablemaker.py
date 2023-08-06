import re
import collections
from html import escape, unescape

AND_REPLACEMENT = "HALLGRIMTABLEAND"

and_regex = re.compile('&', re.MULTILINE)

table_start = re.sub(and_regex, AND_REPLACEMENT, escape('<table border="1">'))
table_end = re.sub(and_regex, AND_REPLACEMENT, escape('</table>'))
line_start = re.sub(and_regex, AND_REPLACEMENT, escape('<tr>'))
line_end = re.sub(and_regex, AND_REPLACEMENT, escape('</tr>'))
cell_start = re.sub(and_regex, AND_REPLACEMENT, escape('<td>\xa0\xa0')) # note: \xa0 are non-skipping spaces, which will also be displayed in the beginning and at the end of cells
cell_end = re.sub(and_regex, AND_REPLACEMENT, escape('\xa0\xa0</td>'))

def prepareTables(raw: str) -> str:
    """
    scans given string for use of [table]-tags and inserts necessary markup
    all '&' used in the table will be inserted as HALLGRIMTABLEAND due to
    conversion of '&' by IliasXMLCreator, these will have to be replaced later
    """
    # following regex finds text enclosed in the [table]-tag
    table_regex = re.compile('\[table\]([\w\W]+?)(\[\/table\])', re.MULTILINE) # [\w\W]+? contains ? so + is not greedy -> does not take string tu last end of table
    table_strings = collections.deque(); # for containing the ready table-strings
    latex_strings = collections.deque(); # for containing latex-content
    latex_regex=re.compile('\\\\\\(([\w\W]+?)\\\\\\)', re.MULTILINE) # the delimiters we are expecting are \( and \)
    for latex in re.finditer(latex_regex,raw): # filter out latex parts
        latex_strings.append(latex.group(0))
    raw=re.sub(latex_regex,'HALLGRIMTABLELATEX',raw)
    for table in re.finditer(table_regex,raw):
        tagged = collections.deque(); # for containing the areas of internal tags
        # following regex finds all internal tagged strings, assuming correct and non-intersecting (therefore unnested) tags
        internal_regex = re.compile('\[([\w\W]+?)\]([\w\W]+?)\[\/([\w\W]+?)\]', re.MULTILINE)
        for tag in re.finditer(internal_regex,table.group(1)): # group(1) is matching text without [table]-tags
            tagged.append(tag.group(0)) # group(0) contains both tags and the content
        untagged=re.sub(internal_regex, "HALLGRIMTABLETAGGED", table.group(1)) # temporarily replace all internal tags with HALLGRIMTABLETAGGED
        table_string = ""
        for line in collections.deque(untagged.split(";")): # for each row (split by ;)
            line_string = ""
            for cell in collections.deque(line.split(",")): # for each cell in row (split by ,)
                line_string += cell_start + cell + cell_end # add cell to row, reverse-engineered from XML, & replaced with HALLGRIMTABLEAND, also added NBS (\u00A0) for space between content and walls
            table_string += line_start + line_string + line_end # add row to table, reverse-engineered from XML, & replaced with HALLGRIMTABLEAND
        table_string = table_start + table_string + table_end # start and end of table, reverse-engineered from XML, & replaced with HALLGRIMTABLEAND
        untagged = collections.deque(table_string.split('HALLGRIMTABLETAGGED'))
        complete_table = collections.deque()
        for table_part in range(min(len(untagged), len(tagged))): # put string for table back together
            text = untagged.popleft()
            if text != "":
                complete_table.append(text)
            complete_table.append(tagged.popleft())
        complete_table.extend(untagged)
        complete_table.extend(tagged)
        table_strings.append("".join(complete_table))
    untabled = re.sub(table_regex, "HALLGRIMTABLEREMOVED", raw)
    untabled = collections.deque(untabled.split('HALLGRIMTABLEREMOVED'))
    full_table = collections.deque();
    for text_part in range(min(len(untabled),len(table_strings))): # put complete string (with HALLGRIMTABLELATEX tokens) back together
        text = untabled.popleft()
        if text != "":
            full_table.append(text)
        full_table.append(table_strings.popleft())
    full_table.extend(untabled)
    full_table.extend(table_strings)
    full_table = "".join(full_table)
    full_table = collections.deque(full_table.split('HALLGRIMTABLELATEX'))
    final = collections.deque()
    for latex_part in range(min(len(full_table),len(latex_strings))): # put latex back in
        text = full_table.popleft()
        if text != "":
            final.append(text)
        final.append(latex_strings.popleft())
    final.extend(full_table)
    final.extend(latex_strings)
    final = "".join(final)
    return final
        
