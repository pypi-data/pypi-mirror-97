#taken from https://github.com/oerpub/mathconverter/blob/master/converter.py and then modified
#(under MIT license:)



#MIT License

#Copyright (c) 2016 Marvin Reimer, OERPUB

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#original used for mathml->latex (asciimath->latex was extremely slow)
#other functionality has been removed

import os
import requests
import sys
import asciitomathml.asciitomathml as asciiToMathML
from lxml import etree
from .messages import error

input_formats = ['asciimath', 'latex', 'mathml']
output_formats = ['latex', 'mathml']


def mathml2latex_yarosh(equation):
    """ MathML to LaTeX conversion with XSLT from Vasil Yaroshevich """
    script_base_path = os.path.dirname(os.path.realpath(__file__))
    xslt_file = os.path.join(script_base_path, 'xsl_yarosh', 'mmltex.xsl')
    dom = etree.fromstring(equation)
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return newdom


def convert(equation, iformat, oformat):
    result = ""
    if (iformat == oformat):
        error("Misuse of asciiMathConverter")
    if (oformat == 'mathml'):
        error("Misuse of asciiMathConverter")
    else:   # LaTeX
        if (iformat == 'mathml'):
            error("Misuse of asciiMathConverter")
        else:  # AsciiMath
            AMLconv = asciiToMathML.AsciiMathML()
            AMLconv.parse_string(equation)
            mathml = AMLconv.to_xml_string(encoding='unicode')
            result = mathml2latex_yarosh(mathml)
    result = str(result)
    result = "[[" + result[1:-1] + "]]" #replace $ with [[ and ]]
    return result
