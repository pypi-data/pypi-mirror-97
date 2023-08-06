################################################################################
#
# This script contains the main part of hallgrimJS and is the only script that
# needs to be invoked. The steps it takes to generate a task are as follows:
#
# * parse the commandline arguments with argparse
# * for each script determine the type and validate correct syntax
# * delegate the script to a handler for the specific type
# * the handler parses the script into the intermediate representation (mostly
#   arrays)
# * the handler passes the needed information to the script generator, which
#   will print the final xml file.
# * a finisher compresses data if needed (needs to be implemented, maybe as
#   separate subparser).
#
################################################################################

import os
import argparse
import importlib.util
import re
import sys
from configparser import ConfigParser
from typing import List, Iterator, Tuple, Any, Dict
from shutil import copyfile

# import messaging system
from .messages import info, error, abort, exit

# local import
from . import parser
from . import tablemaker
from . import uploader
from . import IliasXMLCreator
from . import templates
from . import custom_markdown

from .taskPreProcessing import pre_process_text
from .javaScriptUtils import pre_process_js

# set markdown
markdown = custom_markdown.get_markdown()

def get_config() -> ConfigParser:
    config = ConfigParser()
    config.read('config.ini')
    if not 'META' in config.sections():
        config['META'] = {}
    if not 'author' in config['META']:
        config['META']['author'] = '<your name>'
    if not 'output' in config['META']:
        config['META']['output'] = '.'
    return config


def file_exists(path: str) -> str:
    if not os.path.exists(path):
        msg = 'The script "{}" does not exist.'.format(path)
        raise argparse.ArgumentTypeError(msg)
    return path


def valid_scripts(script_list: List[str]) -> Iterator[Tuple[Any, Any]]:
    """ Loads a script and tests if it is valid.

    This method does the following:
        1. Loads the script
        2. Tests if it is a python file
        3. Tests it is executable and gives an error description if not
        4. Tests if mandatory fields are present
        5. yields the loaded script and spec back if everything worked fine

    Arguments:
        script_list (list): a list of script names.

    Yields:
        (module): the loaded and executed object
        (spec object): an object that contains info about the surroundings
    """
    for script_name in script_list:
        try:
            module_name = os.path.basename(script_name)
            sys.path.append(os.path.split(os.path.abspath(script_name))[0]) # add the path of the executed module to search path for modules to allow for local imports in executed modules
            spec = importlib.util.spec_from_file_location(module_name, script_name, submodule_search_locations="test")
            assert spec is not None, \
                "%s is not a python file." % script_name
            script = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(script)
            assert all(hasattr(script, field) for field in ['meta', 'feedback', 'task']), \
                "%s is not a valid script. A field is missing." % script_name
            assert all(key in script.meta for key in ('author', 'title', 'type')), \
                "'meta' field of %s is incomplete." % script_name
            if 'order' in script.meta['type']:
                assert hasattr(script, "order"), "%s needs an 'order' field." % script_name
            if 'multi' in script.meta['type'] or 'single' in script.meta['type']:
                assert hasattr(script, "choices"), "%s needs a 'choices' field." % script_name
        except AssertionError as e:
            error(str(e) + " Skipping.")
        except Exception as e:
            error("%s failed due to %s. Not good, check again. Skipping." \
                % (script_name, e))
        else:
            yield script, spec


def parseme():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    type_choices = IliasXMLCreator.abstract_question.IliasQuestion.available_types().keys()

    subparsers.add_parser(
        "init", help="Initializes a directory for the use with hallgrimJS")
    parser_new = subparsers.add_parser(
        "new", help="The utility to generate new scripts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='available question types:\n\t' + '\n\t'.join(type_choices))
    parser_gen = subparsers.add_parser(
        "gen", help="Subcommand to convert from script to xml.")
    parser_upload = subparsers.add_parser(
        "upload", help="Subcommand to upload created xml instances.")
    parser_documentation = subparsers.add_parser(
        "doc", help="Subcommand to copy the documentation into the current working directory.")

    # continue with correct config
    config = get_config()
    parser_new.add_argument(
        "type",
        help='The type of the question',
        choices=type_choices,
        default='multiple',
        metavar='TYPE'
    )
    parser_new.add_argument(
        "name",
        help="The name of the new script",
        metavar='NAME'
    )
    parser_new.add_argument(
        "-a",
        "--author",
        help="Name of the scripts author",
        default=config['META']['author'],
        metavar='AUTHOR'
    )
    parser_new.add_argument(
        "-p",
        "--points",
        help='Points given for correct answer (different behavior for different questions)',
        type=float,
        default=0.0,
        metavar='POINTS',
    )

    # generator arguments
    parser_gen.add_argument(
        '-o',
        '--out',
        help='''Specify different output dir.''',
        default=config['META']['output'],
        metavar='FILE')
    parser_gen.add_argument(
        'input',
        help='Script to execute',
        nargs='+',
        type=file_exists,
        metavar='FILE')
    parser_gen.add_argument(
        '-p',
        '--parametrized',
        help='Print the number of parametrized instances specified in question.',
        action='store_true')
    parser_gen.add_argument(
        '-m',
        '--minify',
        help='Minify the code for the task, reducing the size (JavaScript tasks only).',
        action='store_true')

    # uploader arguments
    parser_upload.add_argument(
        'script_list',
        help='The scripts that should be uploaded',
        nargs='+',
        type=file_exists,
        metavar='FILE')

    args = parser.parse_args()
    if args.command == 'init':
        handle_init()
    elif args.command == 'gen':
        delegator(args.out, args.input, args.parametrized, args.minify)
    elif args.command == 'upload':
        handle_upload(args.script_list, config)
    elif args.command == 'new':
        handle_new_script(args.name, args.type, args.author, args.points)
    elif args.command == 'doc':
        write_doc()
    else:
        parser.print_help()



def delegator(output: str, script_list: List[str], parametrized: bool, minify: bool):
    """
    It gets a list of filenames and delegates them to the correct handler.
    Every file that does not end with ``.py`` will be ignored. Each script
    is imported and then passed as module to the handler:

    Args:
        output (str): where to write the finished XML document
        script_list (list): a list of filenames that contain scripts
        parametrized (bool): output all instances (no test mode)
    """
    options = {
      'minify': minify,
    }
    for script, spec in valid_scripts(script_list):
        handler = {
            'gap': handle_gap_questions,
            'single choice': handle_choice_questions,
            'multiple choice': handle_choice_questions,
            'order': handle_order_questions,
            'free': handle_free_questions,
            'javaScript': handle_javaScript_questions,
        }[script.meta['type']]

        if 'instances' in script.meta and parametrized:
            instances = script.meta['instances']
        else:
            instances = 1

        final = IliasXMLCreator.packer.compile(
            handler(script, spec, instances, options),
            script.meta['type']
        )
        script_output = os.path.join(output, script.meta['title'] + '.xml')
        IliasXMLCreator.packer.print_xml(final, script_output)
        info('Processed "{}"'.format(script.__name__))
        data = ""
        with open(script_output,'r') as workfile: # reread the written file
            data = workfile.read()
            andRegex = re.compile(tablemaker.AND_REPLACEMENT, re.MULTILINE)
            data = re.sub(andRegex, "&", data) # replace HALLGRIMTABLEAND with &
        with open(script_output,'w') as workfile: #rewrite file
            workfile.write(data)
        info('Wrote xml "{}"'.format(script_output.lstrip('./')), notag=True)

def ask(question: str, default: str = "") -> str:
    """A Simple interface for asking questions to user

    Three options are given:
        * question and no default -> This is plain input
        * question and a default value -> with no user input dafault is returned
        * question and 'yes'/'no' default -> user can type n, y, yes, no
            type-insensitive and 'yes' or 'no' is returned in any case

    Arguments:
        question (str): the question for the user

    Keyword Arguments:
        default (str): a default value (default: {""})

    Returns:
        str -- the user answer of the default (can be empty string)
    """
    if default == 'yes':
        appendix = " [Y/n] "
    elif default == 'no':
        appendix = " [y/N] "
    elif default:
        appendix = " [{}] ".format(default)
    else:
        appendix = " "

    try:
        answer = input(question + appendix)
    except EOFError as eof:
        exit("Stdin was closed. Exiting...")

    return answer if answer else default

def handle_init():
    author = ask("What is your name?", "John Doe")
    output = ask("Where should I put the converted scripts?", "output")

    if not os.path.exists(output):
        os.makedirs(output)

    if os.path.exists("config.ini"):
        override_config = ask("config.ini exists. Want to override?", "no")

    if not os.path.exists("config.ini") or override_config == 'yes':
        with open('config.ini', 'w') as conf:
            conf.write(templates.config_sample.format(author, output))
    print()
    print("Thanks! HallgrimJS is now ready to parse your scripts.")

def handle_gap_questions(script, spec, instances: int, options) -> Iterator[Dict]:
    """ a generator for all kinds of gap questions

    A script can contain any mixture of gap, numeric gap and choice gap
    questions. The data object that is needed by the XML creating scripts
    is generated and the task itself is handled by the parser. The parser
    returns the intermediate representation of the task.

    Arguments:
        script (module): the loaded module
        spec (object):   the specification of the module
        instances (int): number of instances that should be generated
    """
    firstRun = True # do not execute the script here on the first run - it has already been executed once for validation
    for _ in range(instances):
        if(not firstRun):
            spec.loader.exec_module(script) # reload the script to get new instance
        firstRun = False
        yield {
            'gap_list': parser.gap_parser(pre_process_text(script.task, markdown)),
            'author': script.meta['author'],
            'title': script.meta['title'],
            'shuffle': script.meta['shuffle'] if 'shuffle' in script.meta else True,
            'feedback': pre_process_text(script.feedback, markdown),
            'gap_length': script.meta['gap_length'] if 'gap_length' in script.meta else 20,
        }


def handle_choice_questions(script, spec, instances: int, options) -> Iterator[Dict]:
    """ a generator for choice questions

    Handles multiple and single choice questions. The relevant parts of the
    script are fed into a parser that return the correct intermediate
    representation for the task. In this case a list of answers.

    Arguments:
        script (module): the loaded module
        spec (object):   the specification of the module
        instances (int): number of instances that should be generated

    """
    firstRun = True # do not execute the script here on the first run - it has already been executed once for validation
    for _ in range(instances):
        if(not firstRun):
            spec.loader.exec_module(script) # reload the script to get new instance
        firstRun = False
        yield {
            'question_text': pre_process_text(script.task, markdown),
            'author': script.meta['author'],
            'title': script.meta['title'],
            'shuffle': script.meta['shuffle'] if 'shuffle' in script.meta else True,
            'questions': parser.choice_parser(script.choices, script.meta['points']),
            'feedback': pre_process_text(script.feedback, markdown),
            'single': 'single' in script.meta['type']
        }


def handle_order_questions(script, spec, instances: int, options) -> Iterator[Dict]:
    """ a generator for order questions

    Currently handles only vertical ordering questions. The order field of
    the script is fed to the parser, which just returns a list of
    the string where '--' is split character.

    Arguments:
        script (module): the loaded module
        spec (object): the specification of the module
        instances (int): number of instances that should be generated
    """
    firstRun = True # do not execute the script here on the first run - it has already been executed once for validation
    for _ in range(instances):
        if(not firstRun):
            spec.loader.exec_module(script) # reload the script to get new instance
        firstRun = False
        yield {
            'question_text': pre_process_text(script.task, markdown),
            'author': script.meta['author'],
            'title': script.meta['title'],
            'order': parser.order_parser(script.order),
            'points': script.meta['points'],
            'feedback': pre_process_text(script.feedback, markdown),
        }


def handle_free_questions(script, spec, instances: int, options) -> Iterator[Dict]:
    '''
    Handles all types of free/essay questions, although currently only the
    simplest form (human graded) is available. All it gives you is a question
    text and a html <textarea> where you can put your answer.

    Arguments:
        script (module): the loaded module
        spec (object): the specification of the module
        instances (int): number of instances that should be generated
    '''
    firstRun = True # do not execute the script here on the first run - it has already been executed once for validation
    for _ in range(instances):
        if(not firstRun):
            spec.loader.exec_module(script) # reload the script to get new instance
        firstRun = False
        yield {
            'question_text': pre_process_text(script.task, markdown),
            'author': script.meta['author'],
            'title': script.meta['title'],
            'points': script.meta['points'],
            'feedback': pre_process_text(script.feedback, markdown),
        }

def handle_javaScript_questions(script, spec, instances: int, options) -> Iterator[Dict]:
    """
    Handles questions that implement javaScript code. The data object 
    that is needed by the XML creating scripts is generated and the task 
    itself is handled by the parser. The parser returns the intermediate 
    representation of the task.

    Arguments:
        script (module): the loaded module
        spec (object): the specification of the module
        instances (int): number of instances that should be generated
    """
    firstRun = True # do not execute the script here on the first run - it has already been executed once for validation
    for _ in range(instances):
        if(not firstRun):
            spec.loader.exec_module(script) # reload the script to get new instance
        firstRun = False
        JS, imports, task = pre_process_js(script.javaScriptCode, pre_process_text(script.task, markdown));
        if not hasattr(script, "appendedData"): # allow this to be missing, as it is not only not required but also not recommended
            script.appendedData = ""
        yield {
            'question_text': task,
            'author': script.meta['author'],
            'title': script.meta['title'],
            'correctAnswers': script.correctAnswers,
            'appendedData' : script.appendedData,
            'javaScriptCode': JS,
            'javaScriptImports' : imports,
            'feedback': pre_process_text(script.feedback, markdown),
            'doMinify': options['minify'],
        }

def handle_new_script(name, qtype, author, points):
    """ Creates a new script file.

    Takes in some meta information from the command line of if not present takes
    it from the config.ini or uses default values.

    Arguments:
        name (str):     name of the script, will also become file name
        qtype (str):    question type (choice, gap, alignment)
        author (str):   the author of the script
        points (float): number of points for the task
    """
    # create necessary directories
    head, tail = os.path.split(name)
    if not os.path.exists(head) and head:
        os.makedirs(head)
    if not tail.endswith('.py'):
        base = tail
    else:
        base = tail.rstrip('.py')

    script_filename = os.path.join(head, base + '.py')
    if os.path.exists(script_filename):
        answer = input('Script already exists. Do you want to override? [y/N] ')
        if answer != 'y':
            exit()

    if qtype == 'multiple choice' or qtype == 'single choice':
        scaffolding = templates.choice.format(author, base, qtype, points)
    elif qtype == 'order':
        scaffolding = templates.order.format(author, base, points)
    elif qtype == 'gap':
        scaffolding = templates.gap.format(author, base)
    elif qtype == 'free':
        scaffolding = templates.free.format(author, base, points)
    elif qtype == 'javaScript':
        scaffolding = templates.javaScript # format fails due to additional {} in the script
        scaffolding = scaffolding.replace('{author}', author)
        scaffolding = scaffolding.replace('{title}', base)
    else:
        abort('There is no template for this type')

    with open(script_filename, 'w') as new_script:
        new_script.write(scaffolding)
        info('Wrote new script to "%s."' % new_script.name)


def handle_upload(xml_script_list: List[str], config: ConfigParser):
    """ Passes data to the upload script.

    The status code should be 500, since ILIAS always replies with that error
    code after an upload is confirmed. If anything else the script will say
    the status code was bad.

    Arguments:
        xml_script_list (list): list of paths to the files that should be uploaded
    """
    from requests.exceptions import ConnectionError
    if 'UPLAODER' not in config.sections():
        abort("No server data found in config.ini or the file does not exist.")

    for script in xml_script_list:
        try:
            assert script.endswith('.zip') or script.endswith('.xml'), \
                "Uploaded file is neither .xml nor .zip."
            r = uploader.send_script(
                script,
                config['UPLAODER']['host'],
                config['UPLAODER']['user'],
                config['UPLAODER']['pass'],
                config['UPLAODER']['rtoken'],
            )
        except AssertionError as e:
            error(e)
        except ConnectionError as e:
            abort("Server is not responding. Maybe the image is not running?")
        else:
            info("Uploaded %s. Status code looks %s." %
                (script, "good" if r else "bad"))

def write_doc(): # copies doc from package directory to current working directory
    doc_input = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'HallgrimJS user manual.pdf')
    doc_output = os.path.join(os.getcwd(), 'HallgrimJS user manual.pdf')
    data = ""
    copyfile(doc_input, doc_output)

