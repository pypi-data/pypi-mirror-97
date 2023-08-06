# Module for prewritten javaScript functionality not concerning the base structure of hallgrim-produced JS-scripts.
# The contents should be exclusively called by users or by other contained contents.
# BaseCollection() contains all parts which are always imported.

# cleans HTML, intended for XSS-protection
CLEAN_HTML = """function HGCleaner(inp){
    DOMPurify.sanitize(inp);
}
"""

# encodes < and >, used for protection against XSS-attacks
ENCODE_COMPARATORS ="""function HGCompEnc(inp){
    inp = inp.replace(/</g,"&lt;");
    inp = inp.replace(/>/g,"&gt;");
    return inp;
}
"""

# converts markdown with AsciiMath to HTML which can then be correctly displayed with MathJax
MD_AND_AM_TO_HTML = """function HGConvertMarkdown(val){
    HGMarkdownConverter = new showdown.Converter(); // we decided to initialize every time because otherwise we have to initially wait and check if showdown has been loaded already and this doesnt cost much
    return HGMarkdownConverter.makeHtml(val);
}

function HGAsciiMathToTexHelperA(match, p1, p2, p3, offset, string){ // replace the $$ with '\[' and '\]' (see HGAsciiMathToTex)
    p2 = AMTparseAMtoTeX(p2) // convert to latex
    p2 = p2.replace(/&lt/g,"<"); // fix html-encoded < and >
    p2 = p2.replace(/&gt/g,">");
    return ["&#92;[", p2, "&#92;]"].join(''); // escaped characters because conversion from markdown ruins this otherwise
}

function HGAsciiMathToTexHelperB(match, p1, p2, p3, offset, string){ // replace the $$ with '\(' and '\)' (see HGAsciiMathToTex)
    p2 = AMTparseAMtoTeX(p2) // convert to latex
    p2 = p2.replace(/&lt/g,"<"); // fix html-encoded < and >
    p2 = p2.replace(/&gt/g,">");
    return ["&#92;(", p2, "&#92;)"].join(''); // escaped characters because conversion from markdown ruins this otherwise
}

function HGAsciiMathToTex(val){ // for replacing the $$ ... $$ with \( ... \) and \[ ... \] so MathJax detects this 
    val = val.replace(/(\$\$)([^\$]*)(\$\$)/g, HGAsciiMathToTexHelperA);
    val = val.replace(/(\$)([^\$]*)(\$)/g, HGAsciiMathToTexHelperB);
    return val;
}

function HGMDAndAMToHTMLCodeFixer(val){ // the XSS-protection causes wrong displays of '<' and '>' in CODE and PRE tags, which is fixed here by manual replacement
    fixed = document.createElement("HGFixerTemp"); // new element (never added to document) for going through the html structure
    fixed.innerHTML = val;
    var a = 0;
    while (a < fixed.childNodes.length){
        var elm = fixed.childNodes[a];
        if(((typeof elm.tagName) != 'undefined') && (elm.tagName == "CODE" || elm.tagName == "PRE")){ // replace in code and pre tags only
            elm.textContent = elm.textContent.replace(/\&lt;/g,"\<");
            elm.textContent = elm.textContent.replace(/\&gt;/g,"\>");
        }
    a = a + 1;
    }
    return fixed.innerHTML;
}

function HGMDAndAMToHTML(val){
    val = HGCompEnc(val); // to prevent insertion of html tags, against XSS attacks
    val = HGAsciiMathToTex(val);
    val = val.replace(/\\\\/g,"&#92;"); // replaces each backslash with encoding
    val = val.replace(/_/g,'HALLGRIMUNDERSCOREPLACEHOLDER'); // underscores needed for math are destroyed by markdown conversion, replace them for a bit
    val = HGConvertMarkdown(val);
    val = val.replace(/HALLGRIMUNDERSCOREPLACEHOLDER/g,'_'); // replace underscores back
    val = HGMDAndAMToHTMLCodeFixer(val);
    return val;
}"""

SKULPT_PY = """

function HGSkulptBuiltInRead(x) {
  if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
    throw "File not found: '" + x + "'";
  return Sk.builtinFiles["files"][x];
}

function HGSkulptDecrementErrorLines(message, lineNumber) {
  var numberStart = message.lastIndexOf("on line ") + 8;
  var newNumber = parseInt(message.slice(numberStart)) + 1 - lineNumber;
  return message.slice(0, numberStart) + newNumber;
}

async function HGRunPython(code, outputHandler, errorHandler, timeout = 10000) { // note that this function causes a lot of unreachable-statement-after-return-errors, but I think this is caused by Skulpt
  if(code.search(/[^\\w]sys\\./) != -1 || code.search(/import[\\s]*sys/) != -1 || code.search(/[^\\w]sysconfig\\./) != -1 || code.search(/import[\\s]*sysconfig/) != -1){ // no manipulation of the timeout is wanted, also have to prevent "import sys as ..."
    alert("Zugriffe auf die Module sys und sysconfig sind nicht erlaubt.\\n(Hier finden möglicherweise Fehlerkennungen statt. Benennen Sie im Zweifelsfall Funktionen mit 'sys' um)");
    return null;
  }
  if(code.search(/eval[^\\S\\r\\n]*\\(/) != -1 || code.search(/exec[^\\S\\r\\n]*\\(/) != -1 || code.search(/compile[^\\S\\r\\n]*\\(/) != -1){ // with eval, exec or compile someone could assemble a string during execution which manipulates the controlling parts
    alert("Die Nutzung von 'exec', 'eval' und 'compile' ist aus Sicherheitsgründen nicht erlaubt.\\n(Hier finden möglicherweise Fehlerkennungen statt. Benennen Sie im Zweifelsfall Funktionen, welche mit 'exec', 'eval' oder 'compile' enden um)"); 
    return null;
  }
  var prepCode = "";
  if(timeout > 0){
    prepCode = "import sys\\nsys.setExecutionLimit(" + timeout + ")\\n\\n" + prepCode;
  }
  prepCode += "\\n";
  var extraLines = (prepCode.match(/\\n/g) || []).length + 1;
  code = prepCode + code;
  Sk.pre = "output";
  var outputBuffer = [""]; // array used for closure (since strings immutable)
  var outf = (function(buffer){var bufferCopy = buffer; var func = function(text){bufferCopy[0] = bufferCopy[0] + text;}; return func;})(outputBuffer);
  Sk.configure({output:outf, read:HGSkulptBuiltInRead}); 
  var myPromise = Sk.misceval.asyncToPromise(function() {
    Sk.importMainWithBody("<stdin>", false, code, true);
  });
  var endPromise = myPromise.then(function(mod) {
      outputHandler(outputBuffer[0]); // things went well on execution, send output to handler
    },
    function(err) {
      if(errorHandler != undefined){
        var errMes = HGSkulptDecrementErrorLines(err.toString(), extraLines); // decrement line number of error to reflect the position in the user code
        errorHandler(errMes); // send error message from Skulpt to handler
      }
  });
  return endPromise;
} 
"""

#parts to always import
def BaseCollection():
    return ENCODE_COMPARATORS + CLEAN_HTML
