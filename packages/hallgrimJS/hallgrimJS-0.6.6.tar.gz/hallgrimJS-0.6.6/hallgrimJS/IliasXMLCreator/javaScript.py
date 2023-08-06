import xml.etree.ElementTree as et
import urllib.parse as url
import base64
from rjsmin import jsmin

from .xmlBuildingBlocks import *
from .abstract_question import IliasQuestion
from .. import messages

class JavaScriptQuestion(IliasQuestion):
    """This class contains all functions, needed for creating
    the XML file for ILIAS, that are special to the JavaScript question type."""

    __slots__ = ('question_text', 'points', 'javaScript',)
    external_type = 'CLOZE QUESTION'
    internal_type = 'javaScript'
    usable_data_type = ('png', 'jpg', 'jpeg', 'gif', 'bmp')

    def __init__(self, question_text, author, title, correctAnswers, appendedData, javaScriptCode, javaScriptImports, feedback, doMinify):
        self.question_text     = question_text
        self.author            = author
        self.title             = title
        self.correctAnswers    = correctAnswers
        self.appendedData      = appendedData
        self.javaScriptCode    = javaScriptCode
        self.javaScriptImports = javaScriptImports
        self.feedback          = feedback
        self.doMinify          = doMinify
        if(type(self.correctAnswers) == str): # if single answer gap written just as string, put into array so can be handled the same as multiple answers
            self.correctAnswers = [self.correctAnswers]
        self.answerGapNum = len(self.correctAnswers);
        if(self.answerGapNum == 0):
            messages.abort("At least one gap for answers has to be given.")

    def itemmetadata(self, feedback_setting=1):
        """This function adds all necessary XML tags and their content that
        need to appear inbetween the "itemmetadata" tags of the XML file for
        ILIAS."""

        subroot = et.Element('qtimetadata')
        subroot.append(qtimetadatafield('ILIAS_VERSION', '5.1.11 2016-10-28'))
        subroot.append(qtimetadatafield('QUESTIONTYPE', self.external_type))
        subroot.append(qtimetadatafield('AUTHOR', self.author))
        subroot.append(qtimetadatafield('additional_cont_edit_mode', 'default'))
        subroot.append(qtimetadatafield('externalId', '99.99'))
        subroot.append(qtimetadatafield('textgaprating', 'ci'))
        subroot.append(qtimetadatafield('identicalScoring', '1'))
        subroot.append(qtimetadatafield('combinations', 'W10='))
        root = et.Element('itemmetadata')
        root.append(subroot)
        return root

    ############################################################################
    def presentation(self):
        """This function adds all necessary XML tags and their content that
        need to appear inbetween the "presentation" tags of the XML file for
        ILIAS (question title, question text, gap)."""

        root = et.Element('presentation', attrib={'label': self.title})
        flow = et.Element('flow')

        root.append(flow)
        self.gapIDs = []
        for x in range(len(self.correctAnswers)):
            self.gapIDs.append("answer" + str(x))
        self.gapIDs.extend(["raw", "comments", "meta", "misc"]);
        javaScriptIDs = "gapIDs = [";
        for ID in self.gapIDs:
            javaScriptIDs += "\"" + ID + "\","
        javaScriptIDs += "];"

        render_fib = et.Element('render_fib', attrib={
            'fibtype': 'String', 
            'prompt': 'Box',
            'columns': '9',
            'maxchars': '999999',})


        for (num, ID) in enumerate(self.gapIDs):
            response_str = et.Element('response_str', attrib={
                'ident': 'gap_' + str(num),
                'rcardinality': 'Single',
            })
            flow.append(response_str)
            response_str.append(render_fib)
            flow.append(material(''))
        
        scriptContent = (";(function(){"
        + javaScriptIDs
        + """
            HGRegularInstance = 0; // the HGInstance numbers to be expected in the respective types of instances, for use in scripts to distinguish both
            HGFeedbackInstance = 1;

            // global marker for being in an exam review

            if(typeof HGIsExamReviewGlobal == 'undefined'){
              HGIsExamReviewGlobal = true; // assumed to be true, if false found when scanning the output gaps
            }

            // global counter for instances, used whenever multiple tasks are on one page (feedback, exams)
            if(typeof HGInstanceGlobal == 'undefined'){ // check for global outside instance counter
              HGInstanceGlobal = 0; // first instance, set number to 0
            }
            var HGInstance = HGInstanceGlobal;

            HGInstanceGlobal = HGInstanceGlobal + 1;

            function HGGapStandardSetter(element){ // for answer-gaps
              var elementCopy = element;
              var setter = function(value){
                elementCopy.value = HGToB64(value);
              }
              return setter;
            }


            function HGGapStandardGetter(element){ // for answer-gaps
              var elementCopy = element;
              var getter = function(){
                return HGFromB64(elementCopy.value);
              }
              return getter;
            }

            function HGSBoxStandardGetter(element){ // for solution-boxes
              var elementCopy = element;
              var getter = function(){
                try{
                  var out = HGFromB64(elementCopy.innerText);
                  return out;
                }
                catch(e){ // ILIAS inserts some whitespace when there is no answer, which causes HGFromB64 to fail
                  return "";
                }
              }
              return getter;
            }


            var taskTop = document.querySelectorAll("[HGTopMarker = 'Mark']")[0];
            taskTop.setAttribute('HGTopMarker', 'Used');
            var taskTopIndex = [].slice.call(taskTop.parentNode.children).indexOf(taskTop);
            var gaps = taskTop.parentNode.children[taskTopIndex - 1].children; // the question gaps are right above the HGTopMarker element

            if(document.getElementsByName("gap_0")[0]){ // check if currently answering
              HGMode = "ANSWERING"; // global variable for current question environment
              HGIsExamReviewGlobal = false;
              for (gapNum = 0; gapNum < gaps.length; gapNum++){
                var element = gaps[gapNum];
                element.type = "hidden"; // if so, hide answer and other fields
                element.setAttribute("HGOutput", gapIDs[gapNum]);
                element.setAttribute("HGNumber", HGInstance);
                element.HGGetter = HGGapStandardGetter(element);
                element.HGSetter = HGGapStandardSetter(element);
              }
              if(document.getElementsByName("gap_{rawInputGapNum}")[0].value != ""){ // if there is already some raw input
                HGMode = "CONTINUING"; // global variable for current question environment
              }
            }
            else if(document.getElementsByClassName("ilc_qinput_TextInput solutionbox")[0]){ // check if currently correcting
              HGMode = "CORRECTING"; // global variable for current question environment
              var gapMultiplier = 1;
              if(gaps[1].nodeName == "IMG"){ // with checkmarks/crosses
                gapMultiplier = 2;
                console.log("Gap contents (Troubleshooting information):"); // farther down gap contents are printed to console
                if(HGInstance == 0){
                  HGIsExamReviewGlobal = false; // when viewing exams this has no checksmarks/crosses, else it does, as it will be the upper part when viewing results
                }
              }
              for (gapNum = 0; gapNum < gaps.length; gapNum++){
                gaps[gapNum].setAttribute("hidden", true); // hide all the answer fields (helped troubleshooting, but sometimes caused a bizarre rendering bug in firefox)
              }
              for (gapNum = 0; gapNum * gapMultiplier < gaps.length; gapNum++){
                var element = gaps[gapNum * gapMultiplier];
                element.setAttribute("HGOutput", gapIDs[gapNum]);
                element.setAttribute("HGNumber", HGInstance);
                element.HGGetter = HGSBoxStandardGetter(element);
                element.HGSetter = function(arg){}; // no changing of solutions
                if(gapMultiplier == 2){
                  console.log(gapIDs[gapNum] + ":");
                  console.log(element.HGGetter());
                }
              }
            }""".replace("{rawInputGapNum}", str(len(self.correctAnswers)))
        + self.javaScriptCode
        + "}).call(this)") # wrap it all up inside a function to isolate possible multiple instances (such as during feedback) from each other

        if(self.doMinify):
          scriptContent = jsmin(scriptContent, True)

        # Here the question text, the javaScript code and the appended data
        # get appendend to the xml file.
        flow.append(material(
              "<div HGTopMarker = 'Mark'></div>" + # marks top of task, used to get the parent - the task container
              self.question_text +
              self.javaScriptImports +
              "<script>eval(decodeURIComponent('{0}'));</script>"
              .format(url.quote(scriptContent + self.appendedDataToString()
              ))
        ))

        return root

    ############################################################################
    def resprocessing(self):
        """This function adds all necessary XML tags and their content that
        need to appear inbetween the "resprocessing" tags of the XML file for
        ILIAS. It adds all (answer, points) tuple to the XML file."""

        root = et.Element('resprocessing')
        outcomes = et.Element('outcomes')
        outcomes.append(simple_element('decvar'))
        root.append(outcomes)

        gap_count = 0;
        for correctAnswer in self.correctAnswers: # answer-gaps
            answer_count = 0
            for i in correctAnswer.splitlines():
                if i !='':
                    answer_count += 1 
                    root.append(
                        self.respcondition(i.partition(':')[0].strip().replace('<p>', ''), 
                        float(i.partition(':')[2].replace('P', '').replace('</p>', '')), 
                        answer_count, gap_count))
            gap_count += 1;
            if(answer_count == 0):
                messages.abort("For each gap at least one answer is necessary!")

        for i in range(len(self.correctAnswers), len(self.gapIDs)): # non-answer-gaps
            root.append(
                self.respcondition(self.gapIDs[i], 0, 1, i))

        return root

    ############################################################################
    @staticmethod
    def respcondition(answer, points, answer_count, gap_num):
        """This function adds all necessary XML tags and their content that
        need to appear inbetween the "respcondition" tags of the XML file for
        ILIAS. Gets called by :func:`~javaScript.JavaScriptQuestion.resprocessing`
        and adds a (answer, points) tuple to the XML file.
        
        Arguments:
            answer (string): answer that will receive points (will be processed by applying uri-encoding and afterwards base64-encoding)
            points (int): points given for entering the answer
            answer_count (int): number of previous answers
        """

        root = et.Element('respcondition', attrib={'continue': 'Yes'})
        conditionvar = et.Element('conditionvar')
        useAnswer = base64.encodestring(answer.encode("utf-8")).decode('utf-8')[0:-1] # the encoding causes an extra newline at the end
        varequal = simple_element(
            'varequal',
            text = useAnswer,
            attrib={'respident': 'gap_' + str(gap_num)}
        ) 
        conditionvar.append(varequal)
        setvar = simple_element(
            'setvar',
            text = str(points),
            attrib = {'action': 'Add'}
        )

        displayfeedback = et.Element(
            'displayfeedback',
            attrib = {'feedbacktype': 'Response',
                      'linkrefid': str(gap_num) + '_Response_{}'.format(answer_count)})
        root.append(conditionvar)
        root.append(setvar)
        root.append(displayfeedback)
        return root

    ############################################################################
    def appendedDataToString(self):
        """This function will tanslate all appended image files in the template
        with base64 to a string and returns that string. It also ensures that
        the images can be called in the question via HTML."""

        data_string = ""
        for i in self.appendedData.splitlines():
            if i !='':

                # This will result in the path and the name of the 
                # data to append, because theappendedData in the 
                # Template will always have the following 
                # format: 'name of image' : 'path
                path = i.partition(':')[2].strip()
                image_name = i.partition(':')[0].strip()

                # Aborts if type of appended data is not in  
                # usable_data_type (currently 'png', 'jpg', 'jpeg', 
                # 'gif' and 'bmp') or if there are formate errors
                # else returns the data type as string
                data_type = self.hasSupportedDataType(path, image_name)

                try:
                    image = open(path, 'rb')
                except FileNotFoundError:
                    messages.abort('File: {0} was not found!'.format(path))   
           
                image_encoded = base64.encodestring(image.read())
                data_string += """
                document.getElementsByName("{0}").forEach(function(img){{
                    img.src = 'data:image/{1};base64,{2}';
                }})""".format(image_name, data_type, image_encoded)

        # The base64.encodestring() will add a "b'" at the beginning and a
        # "\n'" at the and of the string. These need to be removed, hence the replace()
        return data_string.replace('b\'','').replace('\\n\'', '')


    ############################################################################
    def hasSupportedDataType(self, path, image_name):
        """Is called by :func:`~javaScript.JavaScriptQuestion.appendedDataToString`
        and checks wheter the appended files have a supported file type.
        
        Arguments:
            path (string): path to the image to append
            image_name (string): name of the image to append
        """

        if(image_name == ''):
            messages.abort('An image in the template has no name!')
        if(path == ''):
            messages.abort('The image \"{0}\" in the template has no path'.format(image_name))
        for i in self.usable_data_type:
            if path.endswith(i):
                return i

        messages.abort('{0} has an unsupported file type'.format(path))

