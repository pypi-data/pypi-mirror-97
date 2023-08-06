# This module contains pre_process_js which is called by hallgrimJS.py to pre-process all javaScript-relevant parts, including adding imports and
# replacing the tags. It furthermore contains base-functionality which is vital to the operation of the produced javaScript and its use.

import re
import base64
import os
from . import javaScriptTagProcessing
from . import javaScriptMiscTools
from .JSComponents import JSDrawingCanvas, JSEditor, JSGraphEditor, JSVariableTable, JSVirtualMachine
MARKDOWN_CONVERTER_SOURCE = "https://cdn.jsdelivr.net/npm/showdown@1.9.0"
CODE_EDITOR_SOURCE = "https://pagecdn.io/lib/ace/1.4.6/ace.js"
DOM_PURIFIER_SOURCE = "https://cdnjs.cloudflare.com/ajax/libs/dompurify/2.1.1/purify.min.js"

# initializes container for initial error messages
ERROR_PREPARATION= """
HGErrorMessages = [];
"""

# pushes given message into container on error
# this concerns errors on startup and is only applied where sensible (i.e. in places where website parts are replaced - code which is purely internal should not need this)
def addErrorReporting(code, message):
    return "try{" + code + "} catch(e){HGErrorMessages.push('" + message + " :' + e.message);}"

UTILITY = """
function HGElement(inp){
    return document.getElementById(inp);
}

function HGElements(inp){
    return document.querySelectorAll("[HGID = '" + inp + "']");
}

if(typeof HGUsedElements == 'undefined'){ // the HGIDs will be replaced in order, so we can count through them for duplicates
  HGUsedElements = {};
}

function HGNextElement(inp){
  if(!HGUsedElements[inp]){
    HGUsedElements[inp] = 0;
  }
  HGUsedElements[inp] += 1;
  return document.querySelectorAll("[HGID = '" + inp + "']")[HGUsedElements[inp] - 1];
}

function HGToB64(inp) {
 return btoa(unescape(encodeURIComponent(inp)));
}

function HGFromB64(inp) {
 return decodeURIComponent(escape(atob(inp)));
}

function HGRand(){
  HGRandomSeed = (((2 ** 31) - 1) & (Math.imul(13466917, HGRandomSeed))); // 32-bit linear congruence generator, do not use for any cryptographic purposes
  return HGRandomSeed;
}

function HGSRand(seed){
  HGMetaData["RandomSeed"] = seed;
  HGRandomSeed = seed;
}

function HGGlobalize(toGlobalize, name){ // push variable out into global context under the given name
  // should you ever want to try and make a version which maintains the same name it cant be a normal javaScript function, as the passing changes the name
  var closer = function(glob){var inside = glob; return inside;}
  window[name] = closer(toGlobalize);
}

function HGPeephole(){ // get a way to eval something inside the context of the task, used for debugging
  console.log(function(){return function(code){eval(code)}}());
}

function HGPeepHole(){ // alias
  HGPeephole();
}
"""


IO_MANAGEMENT = """

function HGInput(inputID){
  var result = document.querySelectorAll("[HGInput = " + inputID + "][HGNumber = '" + HGInstance + "']")[0];
  if(typeof result == 'undefined'){ // for compatibility with old tasks
    result = document.querySelectorAll("[HGInput = " + inputID + "]")[0];
  }
  return result;
}

function HGRegisterInput(element, HGID){
  element.setAttribute("HGInput", HGID);
  element.setAttribute("HGNumber", HGInstance);
}

function HGOutput(outputID){
  if(outputID == "answer"){
      outputID = "answer0";
  }
  return document.querySelectorAll("[HGOutput = " + outputID + "][HGNumber = '" + HGInstance + "']")[0];
}

function HGUtility(utilityID){ // this is for anything that isn't input or output
  return document.querySelectorAll("[HGUtility = " + utilityID + "][HGNumber = '" + HGInstance + "']")[0];
}

function HGRegisterUtility(element, HGID){
  element.setAttribute("HGUtility", HGID);
  element.setAttribute("HGNumber", HGInstance);
}

function HGInputs(inputID){
  return document.querySelectorAll("[HGInput = " + inputID + "]");
}

function HGUtilities(utilityID){ // this is for anything that isn't input or output
  return document.querySelectorAll("[HGUtility = " + utilityID + "]");
}

function HGSaveInputs(){
  var aggregate = {};
  var inputs = document.querySelectorAll("[HGInput]") // get all inputs
  for (var InpNum = 0; InpNum < inputs.length; InpNum++){
    if((typeof inputs[InpNum].HGNumber == 'undefined') || (inputs[inpNum].HGNumber == HGInstance)){ // backwards compatibility for cases with no HGNumber
      var ID = inputs[InpNum].getAttribute("HGInput");
      aggregate[ID] = inputs[InpNum].HGGetter();
    }
  }
  HGOutput("raw").HGSetter(JSON.stringify(aggregate)); // save results to output for raw inputs
}

function HGLoadInputs(){
  if(HGOutput("raw").HGGetter() != "raw"){
    try{
      var aggregate = JSON.parse(HGOutput("raw").HGGetter());
      for (const [id, content] of Object.entries(aggregate)){
        HGInput(id).HGSetter(content); // redirect content to appropriate input
      }
    }
    catch(err){
      console.log("HallgrimJS: loading inputs failed - " + err.message)
    }
  }
}

function HGSaveMeta(){
  HGOutput("meta").HGSetter(JSON.stringify(HGMetaData));
}

function HGLoadMeta(){
  if(HGOutput("meta").HGGetter() != "meta"){
    try{
      HGMetaData = JSON.parse(HGOutput("meta").HGGetter());
      HGRandomSeed = HGMetaData["RandomSeed"]; // be sure to set loaded random seed
    }
    catch(err){
      console.log("HallgrimJS: loading metadata failed - " + err.message)
    }
  }
}

function HGSaveAll(){
  HGSaveInputs();
  HGSaveMeta();
}

function HGLoadAll(){
  HGLoadInputs();
  HGLoadMeta();
}

HGAutoEvaluate = false;

function HGEnableAutoEvaluation(){
  HGAutoEvaluate = true;
}

function HGSaveToServer(){
  if(HGAutoEvaluate){
    HGEvaluate();
  }
  try{
    var getQParFromURL = function(par, url){
      var reg = new RegExp('(&|\\\\?)' + par + '=[^&]*');
      return (reg.exec(url)[0]).slice(par.length+2)
    }
    var data = $('#taForm').serialize();
    var url = window.location.href;
    var refId = getQParFromURL('ref_id', url);
    var qId = getQParFromURL('q_id', url);
    var actId = getQParFromURL('active_id', url);
    var cmdNode = getQParFromURL('cmdNode', url);
    url = "ilias.php?ref_id=" + refId + "&test_express_mode=1&q_id=" + qId + "&sequence=1&active_id=" + actId + "&pmode=edit&cmd=autosave&cmdClass=iltestplayerfixedquestionsetgui&cmdNode=" + cmdNode + "&baseClass=ilrepositorygui&cmdMode=asynch&test_answer_changed=1"
    var ef = function(a,b,c){console.log("HallgrimJS: saving to server failed - " + a + "/" + b + "/" + c);}
    $.ajax({
      type: 'POST',
      url: url,
      data: data,
      dataType: 'text',
      timeout: 10000,
    })
    .fail(ef);
    return true;
  }
  catch(err){
    console.log("HallgrimJS: saving to server failed - " + err.msg);
    return false;
  }
}

HGAutoSaveDisabled = false;

function HGDisableAutoSave(){
  HGAutoSaveDisabled = true;
}

async function HGAutoSave(period){ // automatically saves every 'period' seconds
  while(true){
    await (new Promise(resolve => setTimeout(resolve, period)));
    if(HGAutoSaveDisabled){
      break;
    }
    HGSaveAll();
    HGSaveToServer();
  }
}

function HGFinish(){ // saves values and calls evaluator, should be called when finishing tasks (navigate elsewhere, time runs out etc.)
  HGSaveAll();
  HGEvaluate();
}

if(typeof HGFinishersGlobal == 'undefined'){ // check for global finisher container
  HGFinishersGlobal = []; // first instance, set to empty list
}

HGFinishersGlobal.push(function(finisher){return function(){finisher();};}(HGFinish));

function HGFinishAll(){
  for(var a = 0; a < HGFinishersGlobal.length; a++){
    HGFinishersGlobal[a]();
  }
}

async function HGTimeEnder(){ // inserted before the script which closes the task after the time runs out, saves and evaluates before closing
  HGFinishAll();
  await (new Promise(resolve => setTimeout(resolve, 200))); // else value sometimes not saved
  il.TestPlayerQuestionEditControl.saveOnTimeReached();
}

function HGTimeEndReplacer(){ // replaces the ending function for when time runs out by HGTimeEnder
  """ + addErrorReporting("""if(typeof setWorkingTime != 'undefined'){ // check if there is a time limit
    setWorkingTimeRenewer = new Function(setWorkingTime.toString().replace(/il.TestPlayerQuestionEditControl.saveOnTimeReached\(\)/g,"HGTimeEnder()") + "return setWorkingTime;") // new function
    setWorkingTime = setWorkingTimeRenewer(); // replace old one
  }""", "Error in replacement of time restriction management") + """
}

async function HGSaveAndClick(toClick){ // to be put on a replacement button for an old navigation button, saves and evaluates answers before clicking old button
  HGFinishAll();
  HGRealButtons[toClick].click();
}

function HGNavButtonReplacer(){ // hides all navigation buttons and replaces them with new buttons which save and evaluate answers before doing the same thing
  """ + addErrorReporting("""
  HGRealButtons = [];
  var links = Array.prototype.slice.call(document.links); // links, converted to array to prevent replacing the replacements etc. for infinite looping
  links = links.concat(Array.from(document.querySelectorAll("[class*='btn-default']"))); // other relevant navigation buttons
  links = Array.from(new Set(links)); // make sure entries are unique
  var fakedNum = 0;
  for (var linkNum = 0; linkNum < links.length; linkNum++){
    var linkClass = links[linkNum].getAttribute("class");
    var fakeInner = "";
    if(linkClass == null){ // plain link
      fakeInner='<a onclick="HGSaveAndClick(' + fakedNum + ');" href="#">' + links[linkNum].innerHTML + '</a>';
      if(links[linkNum].parentElement.getAttribute("role") == "tab"){ // these only exist within the administration-context (riders for preview, editing page etc.)
        fakeInner = "";
      }
    }
    else if((linkClass.search("btn-default") != -1) && (links[linkNum].innerHTML != "Frage entfernen")){ // regular navigation button, we sort out question removal buttons because they are in edit mode, and so don't need saving of answers, and we don't wan't these to be blocked by a faulty evaluator under any circumstances, so the test the question is in does not have to be deleted to remove it
      var shownText = "";
      if(links[linkNum].getAttribute("value") != null){ // buttons which look the same may be built in different ways
        shownText = links[linkNum].getAttribute("value");
      }
      else{
        shownText = links[linkNum].innerHTML;
      }
      fakeInner='<button  type="button" onclick="HGSaveAndClick(' + fakedNum + ');"  class="' + links[linkNum].getAttribute("class") + '">' + shownText + '</button>';
    }
    if(fakeInner != ""){
      links[linkNum].style.display = "none"; // hide old button
      HGRealButtons[fakedNum] = links[linkNum]; // put old button into HGRealButtons list
      var fakeButton = document.createElement("NewLinkButton" + fakedNum); // make new fake button
      fakeButton.innerHTML = fakeInner;
      links[linkNum].parentNode.appendChild(fakeButton); // put fake button into same position as old button
      fakedNum += 1;
    }
  }""", "Error in navigation button replacement") + """
}

function HGEvaluate(){
  return HGEvaluator();
}

function HGRegisterEvaluator(evaluator){
  HGEvaluator = function(evaluatorCl){return function(){evaluator();}}(evaluator);
}

var BestSolutionSeenString = "HallgrimJS: Die Musterlösung wurde angesehen."

function HGBlockingEvaluator(){
  var ansNum = 0;
  while(HGOutput('answer' + ansNum) != undefined){
    HGOutput('answer' + ansNum).HGSetter(BestSolutionSeenString);
    ansNum += 1;
  }
}
"""

# for preparing task (mostly putting answers back in the right place and reloading or setting the random seed), especially when continuing or correcting

PREPPER = """ 
HGLoaded = false; 
HGLoadHandler = function(){}; // may be replaced by user code to be called upon loading

function HGPrepLoad(){ // loads values after user code runs, calls load handler at end
    if(!HGLoaded){
        HGLoaded = true;
        HGLoadAll();
        if(HGMetaData["viewedSolution"] == "yes"){ // caused by using a feedbackButton
            HGRegisterEvaluator(blockEval);
        }
        HGLoadHandler();
        if(HGInstance == HGFeedbackInstance && !HGIsExamReviewGlobal && HGOutput("answer").HGGetter() == BestSolutionSeenString){ // checking for feedback instance already ensures we are correcting
            alert("Die Musterlösung für diese Aufgabe wurden angesehen!");
        }
    }
}

function HGRegisterLoadingHandler(handler){ // sets new load handler (see HGPrepLoad)
    HGLoadHandler = handler;
}

var HGRandomSeed = 0;
var HGMetaData = {};

function HGPrep(){
    HGRegisterEvaluator(function(){HGOutput('answer').HGSetter(HGOutput('raw').HGGetter());});
    if(typeof(HGPrepPass) == "undefined"){HGPrepPass = 0;} //temporary solution for solving the second round of preparations when correcting}
    if(HGMode == "ANSWERING"){
        HGSRand((new Date).getTime());
        HGAutoSave({STANDARDTIME});
        HGTimeEndReplacer();
        HGNavButtonReplacer();
        HGLoaded = true; // no loading needed
    }
    else if(HGMode == "CONTINUING"){
        HGAutoSave({STANDARDTIME});
        HGTimeEndReplacer();
        HGNavButtonReplacer();
    }
    else if(HGMode == "CORRECTING"){
        if(HGPrepPass == 0){
            HGLoaded = false; // load on second pass only (done so the loading handler is only called once)
        }
    }
    HGPrepPass += 1;
}
"""

PREPPER = PREPPER.replace("{STANDARDTIME}", "30000") # using 'format' bad idea due to curly braces

# for putting some functions outside of the local context in the case of the first instance
# this is done here instead of just writing these functions outside of the function for this instance because some of these are instance dependent and we would prefer to just use the first instance where any version is needed
# this could be split up and put by the original definition if you like, but I chose to collect all these here for a better overview
INSTANCEGLOBALIZER = """
if(HGInstance == 0){
  HGGlobalize(HGToB64, "HGToB64");
  HGGlobalize(HGFromB64, "HGFromB64");
  HGGlobalize(HGSaveAndClick, "HGSaveAndClick");
  HGGlobalize(HGElement, "HGElement");
  HGGlobalize(HGFinishAll, "HGFinishAll");
  HGGlobalize(HGTimeEnder,"HGTimeEnder");
}
"""

def import_string(source):
    return """<script src = {Fsource}></script>""".format(Fsource = source);

# should remove itself if javascript execution successful (at least initially)
ERROR_MESSAGE_WITH_REMOVER = ("""<h1 HGID = 'NOJAVASCRIPTERROR'>FALLS DIESER TEXT NICHT VERSCHWINDET GAB ES EIN PROBLEM MIT DER AUSFÜHRUNG VON JAVASCRIPT. DIES BEEINTRÄCHTIGT MÖGLICHERWEISE DIE FUNKTIONSFÄHIGKEIT DER AUFGABE. STELLEN SIE SICHER, DASS IHR BROWSER NICHT VERALTET IST UND SIE PLUGINS DEAKTIVIEREN, WELCHE JAVASCRIPT AUF ILIAS BLOCKIEREN! KONTAKTIEREN SIE ANDERNFALLS EINEN TUTOR!</h1>""",
"""
if(HGErrorMessages.length == 0){
  for(var copyNum = 0; copyNum < HGElements('NOJAVASCRIPTERROR').length; copyNum++){
    HGElements('NOJAVASCRIPTERROR')[copyNum].style.display = 'none';
  }
}
else{
  message = "Critical errors on task startup:";
  for(var msn = 0; msn < HGErrorMessages.length; msn++){
    message += "\\n" + HGErrorMessages[msn]
  }
  alert(message);
}
"""
)

def pre_process_js(code, task):
    """Adds functions and function calls for automatic processing of inputs and outputs, management of submissions and abstraction for additional provided functionality and DOM-JS-Interaction. Also adds the needed imports."""
    imp = ""; # imports
    imp = import_string(DOM_PURIFIER_SOURCE) + imp;
    basedir = os.path.dirname(os.path.abspath(__file__))
    (task , converters) = javaScriptTagProcessing.hg_js_tag_processor(task) # process tags
    code = addErrorReporting(code, "Error in user code")
    code = ERROR_PREPARATION + javaScriptMiscTools.BaseCollection() + IO_MANAGEMENT + UTILITY + converters + PREPPER + "HGPrep();" + code + "HGPrepLoad();" # concatenate needed code parts, except for imports
    (errorM, errorR) = ERROR_MESSAGE_WITH_REMOVER
    task = errorM + task # add error message to task
    code = code + errorR # remove warning after all other code has run
    #following parts add imports if relevant function calls are detected
    if("HGMDAndAMToHTML(" in code):
        imp = import_string(MARKDOWN_CONVERTER_SOURCE) + imp
        with open(os.path.join(basedir,"ASCIIMathTeXImg.js"),"r") as conv_file:
            code = conv_file.read() + code
        code = javaScriptMiscTools.MD_AND_AM_TO_HTML + code 
    reg = re.compile('HGProcessLatex\(', re.MULTILINE)
    code = re.sub(reg, "MathJax.Hub.Typeset(", code)
    if("HGRunPython(" in code):
        code = javaScriptMiscTools.SKULPT_PY + code
        with open(os.path.join(basedir,"skulpt-stdlib.js"),"r") as conv_file:
            code = conv_file.read() + code
        with open(os.path.join(basedir,"skulpt.min.js"),"r") as conv_file:
            code = conv_file.read() + code
    if("HGEditor(" in code):
        imp = import_string(CODE_EDITOR_SOURCE) + imp;
        code = JSEditor.CODE_EDITOR + code
    if("HGVariableTable(" in code):
        code = JSVariableTable.VARIABLE_TABLE + code
    if("HGDrawingCanvas(" in code):
        imp = import_string(CODE_EDITOR_SOURCE) + imp;
        code = JSDrawingCanvas.DRAWING_CANVAS + code
    if("HGGraphEditor(" in code):
        code = JSGraphEditor.GRAPH_EDITOR + code
        with open(os.path.join(basedir,"vis-network.min.js"),"r") as conv_file:
            code = conv_file.read() + code
    if("HGMakeVM(" in code or "HGMakeStateVM(" in code):
        code = JSVirtualMachine.VIRTUAL_MACHINE + code
        with open(os.path.join(basedir,"v86_ext.js"),"r") as emu_file:
            code = emu_file.read() + code
    code = INSTANCEGLOBALIZER + code
    return (code, imp, task)
