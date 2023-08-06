# This module contains the functionality for replacing the javaScript-relevant tags inside of tasks.
# hg_js_tag_processor is called by javaScriptUtils.py to replace the tags.
# The javaScript-functions contained may also just be called by any user, as their importation is solely based on
# a call being contained in the processed javaScript-part.
import re
import os
import base64
import sys
from .messages import info, error, abort

from .JSComponents.JSVariableTable import VARIABLE_TABLE_ROW_SEPARATOR, VARIABLE_TABLE_COLUMN_SEPARATOR
from .JSComponents.JSGraphEditor import graphNodeTypes

# loads picture under given path and returns the dataURL for it without enclosing quotes
def picPathToDataURL(path):
    imageType = os.path.splitext(path)[1][1:]
    with open(path, "rb") as fl:
        return "data:image/" + imageType + ";base64," + str(base64.encodestring(fl.read()))[2:-3]

CHECK_BOX_SEPARATOR = "HGCHECKBOXSEPARATOR"

def escapeLineBreaks(text):
    return text.replace("\n","\\n")

def InterleaveWithTags(text, eType, tagIDs, placeholder):
    """Splits the text at the placeholder string and inserts html-elements of the given type with the given tagIDs as 'HGID's. Most of the time span and div are use, depending on whether the element is supposed to be inline or separated. May fail if number of tagIDs and placeholders in the text not the same."""
    taskParts = text.split(placeholder)
    pos = 0
    text = ""
    while(pos < len(tagIDs)):
        text += taskParts[pos]
        text += "<" + eType + " HGID=\"" + str(tagIDs[pos]) + "\"></" + eType + ">"
        pos = pos + 1
    text += taskParts[-1]
    return text

def readID(found, counter, tagType, pos = 0):
    if(found.groups()[pos] and len(found.groups()[pos])>2):
        gotID = found.groups()[pos][1:-1]
        if(not (gotID in counter)):
            counter[gotID] = 0
        counter[gotID] += 1;
        return gotID
    else:
        abort("Missing ID for tag of type " + tagType + "! Conversion aborted.") # this should never happen, the regexes should catch this case
      

# One might want to consider somehow doing all the insertions with some common function, as they all have very similar structure.
# As they only share a very small minority of their lines each, this would probably not even result in a reduction of code size.
def hg_js_tag_processor(task):
    """Replaces tags for different inputs with replacable HTML-Elements and creates code for conversion."""
    converters = ""
    converters += """
    if(typeof HGFeedbackMap == 'undefined'){
      HGFeedbackMap = {};
      HGFeedbackOnlyList = [];
    }
    """
    IDCount = {} # we count the HGIDs to warn the user of duplicates
# feedback-only content
    reg = re.compile('\[feedbackOnly(\([^)]+?\))\]([\w\W\s]*?)(\[\/feedbackOnly\])', re.MULTILINE) 
    # \[feedbackOnly(\([^)]+?\))\]- finds the opening tag with HGID, for example [feedbackOnly(myFeedbackContainer)]
    # ([\w\W\s]*?) - finds any content in the middle of the tags, supposed to be the language for highlighting, not greedy
    # (\[\/feedbackOnly\]) - finds closing [/feedbackOnly]
    IDs = []
    feedbackContents = []
    for point in re.finditer(reg, task):
        ID = readID(point, IDCount, "feedbackOnly")
        content = point.groups()[1]
        IDs.append(ID)
        feedbackContents.append(content)
        converters+= """
        HGFeedbackOnlyList.push(HGNextElement({HGID}));
        """.replace("{HGID}", "\"" + ID + "\"")
    task = re.sub(reg, "HGFEEDBACKONLYINPUTPLACE", task)
    taskParts = task.split("HGFEEDBACKONLYINPUTPLACE") # bespoke insertion logic compared to rest, since we can not do the insertions in javascript and we want these to not display when javascript fails
    pos = 0
    task = ""
    while(pos < len(IDs)):
        task += taskParts[pos]
        task += "<div hidden HGID=\"" + str(IDs[pos]) + "\">" + feedbackContents[pos] +"</div>"
        pos = pos + 1
    task += taskParts[-1]
# source-code-editors
    reg = re.compile('\[editor(\([^)]+?\))\]([\w\W]*?)(\[\/editor(\([\w\W\s]*?\))?\])', re.MULTILINE) 
    # \[editor(\([^)]+?\))\] - finds the opening tag with HGID, for example [editor(myEditor)]
    # ([\w\W]*?) - finds any word in the middle of the tags, supposed to be the language for highlighting
    # (\[\/editor(\([\w\W\s]*?\))?\]) - finds closing [/editor(feedback)] or [/editor] with feedback being any string with possible line breaks
    IDs = []
    for point in re.finditer(reg, task):
        ID = readID(point, IDCount, "editor")
        feedback = point.groups()[3]
        lang = point.groups()[1]
        IDs.append(ID)
        converters += """
        HGTempEditor = HGNextElement({HGID});
        HGTempEditor = HGEditor(HGTempEditor, {EditorLang});
        HGRegisterInput(HGTempEditor, {HGID});
        HGTempEditor.HGGetter = (function(useEditor){ var editorCopy=useEditor; var func = function(){return editorCopy.getValue()}; return func;})(HGTempEditor.editor);
        HGTempEditor.HGSetter = (function(useEditor){ var editorCopy=useEditor; var func = function(content){editorCopy.setValue(content)}; return func;})(HGTempEditor.editor);
        """.replace("{HGID}", "\"" + ID + "\"").replace("{EditorLang}", "\"" + lang + "\"") # using 'format' bad idea due to curly braces
        if feedback != None: # feedback is optional, so check is needed (or replace feedback by empty string beforehand)
            feedback = feedback[1:-1] # remove enclosing brackets
            feedback = feedback.replace('"', '\\"') # auto-escape double-quotes
            converters += """
            HGFeedbackMap[{HGID} + "num" + HGInstance] = {feedback};
            if(HGInstance == HGFeedbackInstance && !HGIsExamReviewGlobal){
              HGTempEditor.HGSetter(HGFeedbackMap[{HGID} + "num" + HGInstance]);
            }
            """.replace("{feedback}", "\"" + escapeLineBreaks(feedback) + "\"").replace("{HGID}", "\"" + ID + "\"")
    task = re.sub(reg, "HGEDITORINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGEDITORINPUTPLACE")    
# text-fields
    reg = re.compile('\[textField(\([^)]+?\))\](\d*)(,\d*)?(\[\/textField(\(.*?\))?\])', re.MULTILINE)
    #\[textField(\([^)]+?\))\] - finds the initial tag with HGID, for example [textField(myTextField)]
    #(\d*)(,\d*)? - finds any integer in the middle of the tags, supposed to be the maximum input size of the field or two comma separated integers with the second integer now being the visual size
    #(\[\/textField(\(.*?\))?\]) - finds closing [/textField(feedback)] or [/textField] with feedback being any string (but shouldn't contain line breaks)
    IDs = [];
    for point in re.finditer(reg, task):
        ID = readID(point, IDCount, "textField")
        feedback = point.groups()[4]
        maxSize = point.groups()[1]
        size = point.groups()[2]
        if(size == None):
            size = maxSize
        else:
            size = size[1:]
        IDs.append(ID)
        converters += """
        HGTempField = HGNextElement({HGID});
        HGTempField.innerHTML = '<input class="ilc_qinput_TextInput" type="text" spellcheck="false" autocomplete="off" autocorrect="off" autocapitalize="off" size="{fieldSize}" maxlength="{fieldCap}">'; // copied from ILIAS
	HGRegisterInput(HGTempField, {HGID});
        HGTempField.HGGetter = (function(useField){ var fieldCopy=useField; var func = function(){return fieldCopy.value}; return func;})(HGTempField.childNodes[0]);
        HGTempField.HGSetter = (function(useField){ var fieldCopy=useField; var func = function(content){fieldCopy.value = content}; return func;})(HGTempField.childNodes[0]);
        """.replace("{HGID}", "\"" + ID + "\"").replace("{fieldSize}", size).replace("{fieldCap}", maxSize) # using 'format' bad idea due to curly braces
        if feedback != None: # feedback is optional, so check is needed (or replace feedback by empty string beforehand)
            feedback = feedback[1:-1] # remove enclosing brackets
            feedback = feedback.replace('"', '\\"') # auto-escape double-quotes
            converters += """
            HGFeedbackMap[{HGID} + "num" + HGInstance] = {feedback};
            if(HGInstance == HGFeedbackInstance && !HGIsExamReviewGlobal){
              HGTempField.HGSetter(HGFeedbackMap[{HGID} + "num" + HGInstance]);
            }
            """.replace("{feedback}", "\"" + feedback + "\"").replace("{HGID}", "\"" + ID + "\"")
    task = re.sub(reg, "HGTEXTFIELDINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGTEXTFIELDINPUTPLACE") 
# inline-text-fields
    reg = re.compile('\[inlineTextField(\([^)]+?\))\](\d*)(,\d*)?(\[\/inlineTextField(\(.*?\))?\])', re.MULTILINE)
    #\[inlineTextField(\([^)]+?\))\] - finds the initial tag with HGID, for example [inlineTextField(myTextField)]
    #(\d*)(,\d*)? - finds any integer in the middle of the tags, supposed to be the maximum input size of the field or two comma separated integers with the second integer now being the visual size
    #(\[\/inlineTextField(\(.*?\))?\]) - finds closing [/inlineTextField(feedback)] or [/inlineTextField] with feedback being any string without line breaks
    IDs = [];
    for point in re.finditer(reg, task):
        ID = readID(point, IDCount, "inlineTextField")
        feedback = point.groups()[4]
        maxSize = point.groups()[1]
        size = point.groups()[2]
        if(size == None):
            size = maxSize
        else:
            size = size[1:]
        IDs.append(ID)
        converters += """
        HGTempField = HGNextElement({HGID});
        HGTempField.innerHTML = '<input class="ilc_qinput_TextInput" type="text" spellcheck="false" autocomplete="off" autocorrect="off" autocapitalize="off" size="{fieldSize}" maxlength="{fieldCap}">'; // copied from ILIAS
	HGRegisterInput(HGTempField, {HGID});
        HGTempField.HGGetter = (function(useField){ var fieldCopy=useField; var func = function(){return fieldCopy.value}; return func;})(HGTempField.childNodes[0]);
        HGTempField.HGSetter = (function(useField){ var fieldCopy=useField; var func = function(content){fieldCopy.value = content}; return func;})(HGTempField.childNodes[0]);
        """.replace("{HGID}", "\"" + ID + "\"").replace("{fieldSize}", size).replace("{fieldCap}", maxSize) # using 'format' bad idea due to curly braces
        if feedback != None: # feedback is optional, so check is needed (or replace feedback by empty string beforehand)
            feedback = feedback[1:-1] # remove enclosing brackets
            feedback = feedback.replace('"', '\\"') # auto-escape double-quotes
            converters += """
            HGFeedbackMap[{HGID} + "num" + HGInstance] = {feedback};
            if(HGInstance == HGFeedbackInstance && !HGIsExamReviewGlobal){
              HGTempField.HGSetter(HGFeedbackMap[{HGID} + "num" + HGInstance]);
            }
            """.replace("{feedback}", "\"" + feedback + "\"").replace("{HGID}", "\"" + ID + "\"")
    task = re.sub(reg, "HGINLINETEXTFIELDINPUTPLACE", task)
    task = InterleaveWithTags(task, "span", IDs, "HGINLINETEXTFIELDINPUTPLACE") 
# text-areas
    reg = re.compile('\[textArea(\([^)]+?\))\]((\d)*)(\[\/textArea(\([\w\W\s]*?\))?\])', re.MULTILINE)
    # \[textArea(\([^)]+?\))\] - finds the initial tag with HGID, for example [textArea(myTextArea)]
    # ((\d)*) - finds any integer in the middle of the tags, supposed to be the maximum input length (omittable)
    # (\[\/textArea(\([\w\W\s]*?\))?\]) - finds closing [/textArea(feedback)] or [/textArea] with feedback being any string possibly with line-breaks
    IDs = [];
    for point in re.finditer(reg, task):
        ID = readID(point, IDCount, "textArea")
        feedback = point.groups()[4]
        maxSize = point.groups()[1]
        IDs.append(ID)
        maxSizePart = ""; # will be inserted into attributes, standard is no attribute added
        if(maxSize != ""): # in case maxSize was given, add attribute
            maxSizePart = 'maxlength = ' + maxSize;
        converters += """
        HGTempArea = HGNextElement({HGID});
        HGTempArea.innerHTML = '<textarea cols="80" rows="6" {maxSizePart}></textarea>'; // not from ILIAS, tinyMCE used there (but that requires API-key etc.)
	HGRegisterInput(HGTempArea, {HGID});
        HGTempArea.HGGetter = (function(useArea){ var areaCopy=useArea; var func = function(){return areaCopy.value}; return func;})(HGTempArea.childNodes[0]);
        HGTempArea.HGSetter = (function(useArea){ var areaCopy=useArea; var func = function(content){areaCopy.value = content}; return func;})(HGTempArea.childNodes[0]);
        """.replace("{HGID}", "\"" + ID + "\"").replace("{maxSizePart}", maxSizePart) # using 'format' bad idea due to curly braces
        if feedback != None: # feedback is optional, so check is needed (or replace feedback by empty string beforehand)
            feedback = feedback[1:-1] # remove enclosing brackets
            feedback = feedback.replace('"', '\\"') # auto-escape double-quotes
            converters += """
            HGFeedbackMap[{HGID} + "num" + HGInstance] = {feedback};
            if(HGInstance == HGFeedbackInstance && !HGIsExamReviewGlobal){
              HGTempArea.HGSetter(HGFeedbackMap[{HGID} + "num" + HGInstance]);
            }
            """.replace("{feedback}", "\"" + escapeLineBreaks(feedback) + "\"").replace("{HGID}", "\"" + ID + "\"")
    task = re.sub(reg, "HGTEXTAREAINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGTEXTAREAINPUTPLACE") 
# checkboxes
    reg = re.compile('\[(\\*?)checkBoxes(\([^)]+?\))\]([\w\W]*?)(\[\/checkBoxes(\([^\)]*?\))?\])', re.MULTILINE) # unsure whether to use checkboxes or checkBoxes
    #\[(\\*?)checkBoxes(\([^)]+?\))\] - finds the initial tag with HGID, for example [checkBoxes(myCheckBoxes)] including the possible alias-star
    #([\w\W]*?) - takes everything the middle of the tags, supposed to be the comma-separated selectable values
    #(\[\/checkBoxes(\([^\)]*?\))?\]) - finds closing [/checkBoxes(feedback)] or [/checkBoxes] with feedback being the comma-separated correct answers (written the same as between the tags)
    extraReg = re.compile('([^,]*)([\W]*)', re.MULTILINE) # for the contained comma-separated values
    #([^,]*) - everything up to a comma (should be the checkable options) 
    #([\W]*) - any non-alphanumeric characters afterwards (filters out the commata and spaces etc.)
    IDs = []
    once = True # if true, first checkBox (in this part of the task, copy when reviewing answers will have a new first checkBox)
    for point in re.finditer(reg, task):
        if(once): # if first checkbox add HGCheckBoxSeparator as a global var (could be done multiple times too)
            once = False
            converters += "HGCheckBoxSeparator = '" + CHECK_BOX_SEPARATOR + "';"
        options = []
        values = []
        for option in re.finditer(extraReg, point.groups()[2]): # read the comma-separated options and put them in a list
            options.append(option.groups()[0].replace("\\","\\\\"))
            values.append(option.groups()[0].replace("\\","\\\\"))
        options = options[0:-1] # the loop before adds an empty option in the end
        values = values[0:-1]
        if(point.groups()[0] != None): # alias star contained: change options and values
            aliasReg = re.compile("([\w\W]*):([\w\W]*)", re.MULTILINE)
            for optionNum in range(len(options)):
                for split in re.finditer(aliasReg, options[optionNum]):
                    options[optionNum] = split.groups()[0]
                    values[optionNum] = split.groups()[1]
        ID =  readID(point, IDCount, "radioButtons", pos = 1)
        feedback = point.groups()[4]
        IDs.append(ID)
        inner = ""
        for optionNum in range(len(options)):
            inner += "<p><input type='checkbox' name='" + ID +"checkbox' value='" + values[optionNum] + "'>" + options[optionNum] + "</p>"
        converters += """
        HGTempCheckBoxes = HGNextElement({HGID});
        HGTempCheckBoxes.innerHTML = "{inner}"
	HGRegisterInput(HGTempCheckBoxes, {HGID});
        //note that we will use names for identification to avoid the forced lowercasing from the attributes
        HGTempCheckBoxes.HGGetter = (function(useBoxes){ 
        var boxes=useBoxes.children; 
          var func = function(){
            var output = "";
            for (var boxNum = 0; boxNum < boxes.length; boxNum++){ // go through all checkboxes, concatenate content of checked boxes with the given separator inbetween
              if(boxes[boxNum].childNodes[0].checked){
                output += boxes[boxNum].childNodes[0].value + '{separator}';
              }
            }
            if(output != ""){
              output = output.slice(0, -'{separator}'.length);
            }
            return output;
          };
        return func;})(HGTempCheckBoxes);
        HGTempCheckBoxes.HGSetter = (function(useBoxes){ 
          var boxes=useBoxes.children; 
          var func = function(content){
            var inputs = content.split('{separator}');
            for (var boxNum = 0; boxNum < boxes.length; boxNum++){ // go through the boxes and check everyone contained in the list of the answers after splitting with the given separator
              if(inputs.includes(boxes[boxNum].childNodes[0].value)){
                boxes[boxNum].childNodes[0].checked = true;
              }
            }
          };
          return func;
        })(HGTempCheckBoxes);
        """.replace("{inner}", inner).replace("{HGID}", "\"" + ID + "\"").replace("{separator}", CHECK_BOX_SEPARATOR) # using 'format' bad idea due to curly braces
        if feedback != None: # feedback is optional, so check is needed (or replace feedback by empty string beforehand)
            feedback = feedback[1:-1] # remove enclosing brackets
            converters += """
            HGFeedbackMap[{HGID} + "num" + HGInstance] = {feedback};
            if(HGInstance == HGFeedbackInstance && !HGIsExamReviewGlobal){
              HGTempCheckBoxes.HGSetter(HGFeedbackMap[{HGID} + "num" + HGInstance]);
            }
            """.replace("{feedback}", "\"" + feedback.replace(",", CHECK_BOX_SEPARATOR) + "\"").replace("{HGID}", "\"" + ID + "\"") # also replace the commata inside the feedback with the separator
    task = re.sub(reg, "HGCHECKBOXINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGCHECKBOXINPUTPLACE") 
# radio buttons
    reg = re.compile('\[(\\*?)radioButtons(\([^)]+?\))\]([\w\W]*?)(\[\/radioButtons(\([^\)]*?\))?\])', re.MULTILINE)
    #\[(\\*?)radioButtons(\([^)]+?\))\] - finds the initial tag with HGID, for example [radioButtons(myRadioButtons)] including the possible alias-star
    #([\w\W]*?) - takes everything the middle of the tags, supposed to be the comma-separated selectable values
    #(\[\/radioButtons(\([^\)]*?\))?\]) - finds closing [/radioButtons(feedback)] or [/radioButtons] with feedback being the correct answer (written the same as between the tags)
    extraReg = re.compile('([^,]*)([\W]*)', re.MULTILINE) # for the contained comma-separated values
    #([^,]*) - everything up to a comma (should be the checkable options) 
    #([\W]*) - any non-alphanumeric characters afterwards (filters out the commata and spaces etc.)
    IDs = [];
    for point in re.finditer(reg, task):
        options = []
        values = []
        for option in re.finditer(extraReg, point.groups()[2]): # read the comma-separated options and put them in a list
            options.append(option.groups()[0].replace("\\","\\\\"))
            values.append(option.groups()[0].replace("\\","\\\\"))
        options = options[0:-1] # the loop before adds an empty option in the end
        values = values[0:-1]
        if(point.groups()[0] != None): # alias star contained: change options and values
            aliasReg = re.compile("([\w\W]*):([\w\W]*)", re.MULTILINE)
            for optionNum in range(len(options)):
                for split in re.finditer(aliasReg, options[optionNum]):
                    options[optionNum] = split.groups()[0]
                    values[optionNum] = split.groups()[1]
        ID =  readID(point, IDCount, "radioButtons", pos = 1)
        feedback = point.groups()[4]
        IDs.append(ID)
        inner = ""
        for optionNum in range(len(options)):
            inner += "<p><input type='radio' name='" + ID +"radio' value='" + values[optionNum] + "'>" + options[optionNum] + "</p>"
        converters += """
        HGTempRadios = HGNextElement({HGID});
        HGTempRadios.innerHTML = "{inner}";
	HGRegisterInput(HGTempRadios, {HGID});
        //note that we will use names for identification to avoid the forced lowercasing from the attributes
        HGTempRadios.HGGetter = (function(useRadios){ var radios=useRadios.children; 
        var func = function(){
                for (var radioNum = 0; radioNum < radios.length; radioNum++){ // go through all associated radio buttons and return the content of the first checked one
                    if(radios[radioNum].childNodes[0].checked){
                        return radios[radioNum].childNodes[0].value;
                    }
                }
                return "";
            };
        return func;})(HGTempRadios);
        HGTempRadios.HGSetter = (function(useRadios){
          var radios=useRadios.children; 
            var func = function(content){
              for (var radioNum = 0; radioNum < radios.length; radioNum++){ // go through all radio buttons and check the first one which corresponds to the given content
                  if(radios[radioNum].childNodes[0].value == content){
                      radios[radioNum].childNodes[0].checked = true;
                      return;
                  }
              }
            };
          return func;
        })(HGTempRadios);
        """.replace("{inner}", inner).replace("{HGID}", "\"" + ID + "\"") # using 'format' bad idea due to curly braces
        if feedback != None: # feedback is optional, so check is needed (or replace feedback by empty string beforehand)
            feedback = feedback[1:-1] # remove enclosing brackets
            converters += """
            HGFeedbackMap[{HGID} + "num" + HGInstance] = {feedback};
            if(HGInstance == HGFeedbackInstance && !HGIsExamReviewGlobal){
              HGTempRadios.HGSetter(HGFeedbackMap[{HGID} + "num" + HGInstance]);
            }
            """.replace("{feedback}", "\"" + feedback + "\"").replace("{HGID}", "\"" + ID + "\"")
    task = re.sub(reg, "HGRADIOSINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGRADIOSINPUTPLACE") 
# selections
    reg = re.compile('\[(\\*?)selection(\([^)]+?\))\]([\w\W]*?)(\[\/selection(\([^\)]*?\))?\])', re.MULTILINE)
    #\[(\\*?)selection(\([^)]+?\))\] - finds the initial tag with HGID, for example [selection(mySelection)] including the possible alias-star
    #([\w\W]*?) - takes everything the middle of the tags, supposed to be the comma-separated selectable values
    #(\[\/selection(\([^\)]*?\))?\]) - finds closing [/selection(feedback)] or [/selection] with feedback being the correct answer (written the same as between the tags)
    extraReg = re.compile('([^,]*)([\W]*)', re.MULTILINE) # for the contained comma-separated values
    #([^,]*) - everything up to a comma (should be the checkable options) 
    #([\W]*) - any non-alphanumeric characters afterwards (filters out the commata and spaces etc.)
    IDs = [];
    for point in re.finditer(reg, task):
        options = []
        values = []
        for option in re.finditer(extraReg, point.groups()[2]): # read the comma-separated options and put them in a list
            options.append(option.groups()[0].replace("\\","\\\\"))
            values.append(option.groups()[0].replace("\\","\\\\"))
        options = options[0:-1] # the loop before adds an empty option in the end
        values = values[0:-1]
        if(point.groups()[0] != None): # alias star contained: change options and values
            aliasReg = re.compile("([\w\W]*):([\w\W]*)", re.MULTILINE)
            for optionNum in range(len(options)):
                for split in re.finditer(aliasReg, options[optionNum]):
                    options[optionNum] = split.groups()[0]
                    values[optionNum] = split.groups()[1]
        ID = readID(point, IDCount, "selection", pos = 1)
        feedback = point.groups()[4]
        IDs.append(ID)
        inner = "<select name='" + ID +"radio'>"
        for optionNum in range(len(options)):
            inner += "<option value='" + values[optionNum] + "'>" + options[optionNum] + "</option>"
        inner += "</select>"
        converters += """
        HGTempSelection = HGNextElement({HGID});
        HGTempSelection.innerHTML = "{inner}"
	HGRegisterInput(HGTempSelection, {HGID});
        HGTempSelection.HGGetter = (function(useSelection){ var selection = useSelection.children[0];
            var func = function(){
                return selection.value;
            }
            return func;
        })(HGTempSelection);
        HGTempSelection.HGSetter = (function(useSelection){ var selection = useSelection.children[0];
            var func = function(val){
                selection.value = val;
            }
            return func;
        })(HGTempSelection);
        """.replace("{inner}", inner).replace("{HGID}", "\"" + ID + "\"") # using 'format' bad idea due to curly braces
        if feedback != None: # feedback is optional, so check is needed (or replace feedback by empty string beforehand)
            feedback = feedback[1:-1] # remove enclosing brackets
            converters += """
            HGFeedbackMap[{HGID} + "num" + HGInstance] = {feedback};
            if(HGInstance == HGFeedbackInstance && !HGIsExamReviewGlobal){
              HGTempSelection.HGSetter(HGFeedbackMap[{HGID} + "num" + HGInstance]);
            }
            """.replace("{feedback}", "\"" + feedback + "\"").replace("{HGID}", "\"" + ID + "\"")
    task = re.sub(reg, "HGSELECTIONINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGSELECTIONINPUTPLACE") 
# drawing surfaces (canvas with mouse-drawing)
    reg = re.compile('\[drawingCanvas(\([^)]+?\))\]((\d*),(\d*))?(,)?(\d*)?(\[\/drawingCanvas(\(.*?\))?\])', re.MULTILINE)
    #\[drawingCanvas(\([^)]+?\))\] - finds the initial tag with HGID, for example [drawingCanvas(myDrawingCanvas)]
    #((\d*),(\d*))?(;)?(\d*) - finds the width, height and maximum stack depth
        #((\d*),(\d*))? finds the width and height - only together
        #(,)? this allows the width and height to be separated from the stack depth with a comma, but it is not required if width and height are not there
        #(\d*)? finds the maximum stack depth
        # note that this only works, because width and height can only be given together, so for any number of arguments from 0 to 3 there is only one possibility for the selected parameters to include
    #(\[\/drawingCanvas(\(.*?\))?\]) - finds closing [/drawingCanvas(feedback)] or [/drawingCanvas] with feedback being a (local) path to a correct picture
    IDs = [];
    for point in re.finditer(reg, task):
        ID = readID(point, IDCount, "drawingCanvas")
        width = point.groups()[2]
        height = point.groups()[3]
        stackDepth = point.groups()[5]
        feedbackPath = point.groups()[7]
        if(width == None): # therefore height == None
            width = "400" # default 400x400
            height = "400"
        if(stackDepth == None):
            stackDepth = "-1" # default infinite stack
        IDs.append(ID)
        converters += """
        HGTempCanvas = HGNextElement({HGID});
        HGTempCanvas = HGDrawingCanvas(HGTempCanvas, {width}, {height}, {stackDepth});
	HGRegisterInput(HGTempCanvas, {HGID});
        """.replace("{HGID}", "\"" + ID + "\"").replace("{width}", width).replace("{height}", height).replace("{stackDepth}", stackDepth) # using 'format' bad idea due to curly braces
        if feedbackPath != None: # feedback is optional, so check is needed
            feedbackPath = feedbackPath[1:-1]
            imageType = os.path.splitext(feedbackPath)[1][1:]
            converters += """
            HGFeedbackMap[{HGID} + "num" + HGInstance] = {feedback};
            if(HGInstance == HGFeedbackInstance && !HGIsExamReviewGlobal){
              HGTempCanvas.HGSetter(HGFeedbackMap[{HGID} + "num" + HGInstance]);
            }
            """.replace("{feedback}", "\"" + picPathToDataURL(feedbackPath) + "\"").replace("{HGID}", "\"" + ID + "\"")
    task = re.sub(reg, "HGDRAWINGCANVASINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGDRAWINGCANVASINPUTPLACE") 
# graph editors
    reg = re.compile('\[graphEditor(\([^)]+?\))\]([\w\W]*?)(\[\/graphEditor\])', re.MULTILINE)
    #\[graphEditor(\([^)]+?\))\] - finds the initial tag with HGID, for example [graphEditor(myGraphEditor)]
    #([\w\W]*?) - grabs all the options inside, separated later
    #(\[\/graphEditor\]) - finds closing [/graphEditor]
    IDs = [];
    for point in re.finditer(reg, task):
        ID = readID(point, IDCount, "graphEditor")
        IDs.append(ID)
        args = point.groups()[1]
        args = re.sub("\s", "", args).split(",")
        directedness = args[0]
        args = args[1:]
        basep = os.path.dirname(os.path.abspath(__file__));
        pics = "[";
        for arg in args:
            if(arg in graphNodeTypes):
                nType, nPath = graphNodeTypes[arg];
                pics += "[\"" + nType + "\",\"" + picPathToDataURL(basep + "/GraphNodePics/" + nPath) + "\"],"
            else:
                info("Unknown type of graph node requested:" + arg);
        pics = pics[0:-1] + "]"; 
        converters += """
        HGTempGraphEditor = HGNextElement({HGID});
        HGTempGraphEditor = HGGraphEditor(HGTempGraphEditor, {directedness} , {pics});
	HGRegisterInput(HGTempGraphEditor, {HGID});
        """.replace("{HGID}", "\"" + ID + "\"").replace("{pics}", pics).replace("{directedness}", "\"" + directedness + "\"") # using 'format' bad idea due to curly braces
    task = re.sub(reg, "HGGRAPHEDITORINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGGRAPHEDITORINPUTPLACE")   
# variable Tables
    reg = re.compile('\[variableTable(\([^)]+?\))\]([\d]+),([\d]+)(,(.+?))?(\[\/variableTable(\([^\)]*?\))?\])', re.MULTILINE)
    #\[variableTable(\([^)]+?\))\] - finds the initial tag with HGID, for example [variableTable(myVTable)]
    #([\d]+),([\d]+)(,(.+?))? - grabs two numbers, the initial dimensions, and optionally whatever comes after another comma before the ending tag, the default entry
    #(\[\/variableTable(\([^\)]*?\))?\]) - finds closing [/variableTable(feedback)] with feedback being the rows separated by semicolons and the cells being separated by colons
    IDs = [];
    once = True # if true, first checkBox (in this part of the task, copy when reviewing answers will have a new first checkBox)
    for point in re.finditer(reg, task):
        if(once): # if first checkbox add HGCheckBoxSeparator as a global var (could be done multiple times too)
            once = False
            converters += "HGVTableRowSeparator = '" + VARIABLE_TABLE_ROW_SEPARATOR + "';"
            converters += "HGVTableColumnSeparator = '" + VARIABLE_TABLE_COLUMN_SEPARATOR + "';"
        ID = readID(point, IDCount, "variableTable")
        IDs.append(ID)
        defX = point.groups()[1]
        defY = point.groups()[2]
        defEntry = point.groups()[4];
        feedback = point.groups()[6];
        if(defEntry == None):
            defEntry = "-"
        defEntry = defEntry.replace('"', "&#34").replace("'", "&#39") # escape quotation marks in html style to prevent HGVariableTable() from breaking
        converters += """
        HGTempVariableTable = HGNextElement({HGID});
        HGTempVariableTable = HGVariableTable(HGTempVariableTable, {defX} , {defY}, {defEntry});
	HGRegisterInput(HGTempVariableTable, {HGID});
        """.replace("{HGID}", "\"" + ID + "\"").replace("{defX}", defX).replace("{defY}", defY).replace("{defEntry}", "\"" + defEntry + "\"") # using 'format' bad idea due to curly braces
        if feedback != None: # feedback is optional, so check is needed (or replace feedback by empty string beforehand)
            feedback = feedback[1:-1] # remove enclosing brackets
            feedback = feedback.replace(";", VARIABLE_TABLE_COLUMN_SEPARATOR).replace(",", VARIABLE_TABLE_ROW_SEPARATOR).replace('"', "&#34").replace("'", "&#39")
            converters += """
            HGFeedbackMap[{HGID} + "num" + HGInstance] = {feedback};
            if(HGInstance == HGFeedbackInstance && !HGIsExamReviewGlobal){
              HGTempVariableTable.HGSetter(HGFeedbackMap[{HGID} + "num" + HGInstance]);
            }
            """.replace("{HGID}", "\"" + ID + "\"").replace("{feedback}", "\"" + feedback + "\"") # also replace the commata inside the feedback with the separator
    task = re.sub(reg, "HGVARIABLETABLEINPUTPLACE", task)
    task = InterleaveWithTags(task, "p", IDs, "HGVARIABLETABLEINPUTPLACE")   
# buttons
    reg = re.compile('\[button(\([^)]+?\))\]([\w\W]+?),([^,]*?)(\[\/button\])', re.MULTILINE) # note that the inscription of buttons can not contain commas...
    #\[button(\([^)]+?\))\] - finds the initial tag with HGID, for example [button(myButton)]
    #([\w\W]+?) - takes everything the middle of the tags, except for everything after the last comma (see next part), supposed to be the javaScript to execute on button-press
    #([^,]*?) - takes everything in the middle of the tags after the last comma, supposed to be the title of the button
    #(\[\/button\]) - finds closing [/button]
    IDs = [];
    once = True # if true, first button (in this part of the task, copy when reviewing answers will have a new first button)
    for point in re.finditer(reg, task):
        if(once): # if first button add initialization of button function list and access(could be done multiple times too)
            once = False
            converters += """
            if(typeof HGButtonFunctionList == 'undefined'){
              HGButtonFunctionList=[];
              HGGlobalize(HGButtonFunctionList, "HGButtonFunctionList");
              HGExecuteButtonFunc = function(number, instance){HGButtonFunctionList[instance][number]()};
              HGGlobalize(HGExecuteButtonFunc, "HGExecuteButtonFunc");
            } 
            while(HGButtonFunctionList.length <= HGInstance){ // the instance numbers won't be high enough for the empty entries to become a problem
              HGButtonFunctionList.push([])
            }"""
        ID = readID(point, IDCount, "button")
        toExecute = point.groups()[1]
        #toExecute = toExecute.replace('"',"&quot;").replace("'","&apos;") # automatic html escaping for both types of quotation marks so they can be used here # not needed anymore
        title = point.groups()[2]
        IDs.append(ID)
        converters += """
        HGCurrentButtonFuncCloser = function(){return function(){{toExecute}}};
        HGButtonFunctionList[HGInstance].push(HGCurrentButtonFuncCloser());
        HGTempButton = HGNextElement({HGID});
        HGTempButton.innerHTML = '<button type="button" onclick="HGExecuteButtonFunc(' + (HGButtonFunctionList[HGInstance].length - 1) + ',' + HGInstance + ')">{title}</button>'; // assign function from last button of current instance
	HGRegisterUtility(HGTempButton, {HGID});
        """.replace("{HGID}", "\"" + ID + "\"").replace("{toExecute}", toExecute).replace("{title}", title) # using 'format' bad idea due to curly braces
    task = re.sub(reg, "HGBUTTONINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGBUTTONINPUTPLACE")  
# feedback-buttons
    reg = re.compile('\[feedbackButton(\([^)]+?\))\](\[\/feedbackButton\])', re.MULTILINE) # note that the inscription of buttons can not contain commas...
    #\[feedbackButton(\([^)]+?\))\] - finds the initial tag with HGID, for example [feedbackButton(myFButton)]
    #(\[\/feedbackButton\]) - finds closing [/feedbackButton]
    IDs = [];
    once = True # if true, first button (in this part of the task, copy when reviewing answers will have a new first button)
    for point in re.finditer(reg, task):
        if(once): # if first feedback-button add globalized function for revealing all feedback and blocking the answer
            once = False
            converters += """
            if(typeof HGFeedbackBlocker == 'undefined'){
              var blockEval = HGBlockingEvaluator;
              var HGFButtonFunc = function(){
                HGMetaData["viewedSolution"]="yes"; // marker to block further input on upcoming viewings of the task
                HGSaveAll(); // immediately save the changed metadata and send it to the server to minimize abusability
                if(HGSaveToServer()){ 
                  HGRegisterEvaluator(blockEval); // block further input
                  var inputs = document.querySelectorAll("[HGInput]") // get all inputs
                  for (var InpNum = 0; InpNum < inputs.length; InpNum++){
                    if(typeof HGFeedbackMap[inputs[InpNum].getAttribute("HGInput")] != "undefined"){ // if feedback exists, set content to feedback
                      inputs[InpNum].HGSetter(HGFeedbackMap[inputs[InpNum].getAttribute("HGInput")] );
                    }
                  }
                  for (var FBONum = 0; FBONum < HGFeedbackOnlyList.length; FBONum++){ // go through feedback-only-parts and display them
                    HGFeedbackOnlyList[FBONum].removeAttribute("hidden");
                  }
                }
                else{
                  HGMetaData["viewedSolution"]="no";
                  alert("Fehler beim Serverkontakt. Aufdecken der Musterlösungen abgebrochen.");
                }
              };
              HGGlobalize(HGFButtonFunc, "HGFeedbackBlocker");
            } """
        ID = readID(point, IDCount, "feedbackButton")
        IDs.append(ID)
        converters += """
        HGTempFButton = HGNextElement({HGID});
        HGTempFButton.innerHTML = '<button type="button" onclick="if(confirm(\\'Hierdurch verzichten Sie auf eine Korrektur aller Eingaben, welche Sie in dieser Aufgabe tätigen!\\')){HGFeedbackBlocker()}">Musterlösung anzeigen</button>';
	HGRegisterUtility(HGTempFButton, {HGID});
        """.replace("{HGID}", "\"" + ID + "\"")# using 'format' bad idea due to curly braces
    task = re.sub(reg, "HGFBUTTONINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGFBUTTONINPUTPLACE")  
# text-display (wrapping for pre-tag)
    reg = re.compile('\[text(\([^)]+?\))\]([\w\W]*?)(\[\/text\])', re.MULTILINE)
    #\[text(\([^)]+?\))\] - finds the initial tag with HGID, for example [text(myText)]
    #([\w\W]*?) - takes everything the middle of the tags, supposed to be the standard content of the text-display
    #(\[\/text\]) - finds closing [/text]
    IDs = [];
    for point in re.finditer(reg, task):
        ID = readID(point, IDCount, "text")
        standardContent = point.groups()[1]
        IDs.append(ID)
        converters += """
        HGTempText = HGNextElement({HGID});
        HGTempText.innerHTML = '<pre>{standardContent}</pre>';
        HGTempText.setAttribute("HGUtility", {HGID});
        HGTempText.setAttribute("HGNumber", HGInstance);
        HGTempText.HGGetter = (function(useText){ var textCopy=useText; var func = function(){return textCopy.textContent}; return func;})(HGTempText.childNodes[0]);
        HGTempText.HGSetter = (function(useText){ var textCopy=useText; var func = function(content){textCopy.textContent = content}; return func;})(HGTempText.childNodes[0]);
        """.replace("{HGID}", "\"" + ID + "\"").replace("{standardContent}", standardContent) # using 'format' bad idea due to curly braces
    task = re.sub(reg, "HGTEXTINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGTEXTINPUTPLACE")  
# images
    reg = re.compile('\[image(\([^)]+?\))\]([\w\W]*?)(\[\/image\])', re.MULTILINE)
    #\[image(\([^)]+?\))\] - finds the initial tag with HGID, for example [image(myImage)]
    #([\w\W]*?) - takes everything the middle of the tags, supposed to be the (relative) path to the image
    #(\[\/image\]) - finds closing [/image]
    IDs = [];
    for point in re.finditer(reg, task):
        ID = readID(point, IDCount, "image")
        picPath = point.groups()[1]
        IDs.append(ID)
        converters += """
        HGTempImage = HGNextElement({HGID});
        HGTempImage.innerHTML = '<img src={dataURL}>';
	HGRegisterUtility(HGTempImage, {HGID});
        """.replace("{HGID}", "\"" + ID + "\"").replace("{dataURL}", "\"" +  picPathToDataURL(picPath) + "\"") # using 'format' bad idea due to curly braces
    task = re.sub(reg, "HGTEXTINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGTEXTINPUTPLACE")  
# VMs
    reg = re.compile('\[virtualMachine(\([^)]+?\))\]([\w\W]+?),([\w\W]+?),([\w\W]+?),([\d]+?),([\d]+?)(\[\/virtualMachine\])', re.MULTILINE)
    #\[virtualMachine(\([^)]+?\))\] - finds the initial tag with HGID, for example [virtualMachine(myVirtualMachine)]
    #([\w\W]+?), ... - to find the fixed amount of comma-separated values:
    # 1. bios
    # 2. vgabios
    # 3. iso
    # 4. memory
    # 5. vmemory
    #(\[\/virtualMachine\]) - finds closing [/virtualMachine]
    IDs = [];
    for point in re.finditer(reg, task):
        ID = readID(point, IDCount, "virtualMachine")
        data = list(point.groups()[1:6])
        IDs.append(ID)
        for fNum in range(3):
            with open(data[fNum].strip(),"rb") as emu_file:
                data[fNum] = str(base64.b64encode(emu_file.read()))[2:-1]
        converters += """
        HGTempVM = HGNextElement({HGID});
        HGTempVM = HGMakeVM(HGTempVM, {bios}, {vgaBios}, {iso}, {memory}, {vmemory});
	HGRegisterUtility(HGTempVM, {HGID});
        """.replace("{HGID}", "\"" + ID + "\"").replace("{memory}", data[3]).replace("{vmemory}", data[4]).replace("{bios}", "'data:;base64," + data[0] + "'").replace("{vgaBios}", "'data:;base64," + data[1] + "'").replace("{iso}", "'data:;base64," + data[2] + "'")# using 'format' bad idea due to curly braces
    task = re.sub(reg, "HGVIRTUALMACHINEINPUTPLACE", task)
    task = InterleaveWithTags(task, "div", IDs, "HGVIRTUALMACHINEINPUTPLACE")




# error detection
    for(key, val) in IDCount.items():
        if(val>1):
            error("Duplicate ID " + key + " detected. Output will probably have defects.")

    reg = re.compile('\[[^\[]+?\([\w\W]+?\)\]', re.MULTILINE)
    for point in re.finditer(reg, task):
        info("Unprocessed tag-like structure detected (check for correct use, spelling and end-tag):" + point.group())
  
    return (task, converters)
