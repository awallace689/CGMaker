"""
====================================================================================================
@Author: Adam Wallace
@Date: 1/30/2019
@About: Stack-based Menu class and templates provided by Frame classes provide a clean,
        multi-purpose console interface for user-interaction.
@Note: Menu.display() automatically checks for valid input on provided templates.
====================================================================================================
"""
from os import system
from os import name as os_name


class Frame:
    """Formatted HEADER, PROMPT, and CONTENT field, meant for Menu class.

    :attributes:
        header: None
                str, Displayed at top of frame as |FORMAT|
        prompt: None
                str, Displayed below header
        content: None
                 str, Displayed below prompt
    """
    header = None
    prompt = None
    content = None

    def __init__(self, header=None, prompt=None, content=None):
        """Create Frame with optional HEADER, PROMPT, and CONTENT fields.

        :kwargs:
            :param header: default: None
                           str    : short |TITLE| for frame
            :param prompt: default: None
                           str    : Question/Description
            :param content: default: None
                            str   : List of options/text-image, etc.
        """
        self.header = header
        self.prompt = prompt
        self.content = content

    def build(self):
        """Generate and return 'print_string' by formatting HEADER, PROMPT, CONTENT fields.

        :return: str, consisting of |HEADER| followed by
                                    PROMPT   followed by
                                    CONTENT
        """
        print_string = ''
        if self.header is not None:
            print_string += "|" + self.header.upper() + "|" + '\n' * 2

        if self.prompt is not None:
            print_string += self.prompt + '\n' * 2

        if self.content is not None:
            print_string += self.content + '\n'

        return print_string


class EnumFrame(Frame):
    """Extends Frame by formatting CONTENT field to be a str of an enumeration of a list of strings.

    (*)<- Inherited
    :attributes:
        *header: None or
                 str, Displayed at top of frame as |FORMAT|
        *prompt: None or
                 str, Displayed below header
        *content: None or
                  List of Strings, Displayed below prompt
        format_options(option_list)
            format list of strings into a str containing a formatted, enumerated list
    """
    def __init__(self, header=None, prompt=None, content=list()):
        """Create Frame with optional HEADER, PROMPT, and enumerated CONTENT fields.

        :kwargs:
            :param header: default: None
                           str    : short |TITLE| for frame
            :param prompt: default: None
                           str    : Question/Description
            :param content: list of strings to be enumerated
        """
        super().__init__(header=header, prompt=prompt)
        self.content = self.format_options(content)

    @staticmethod
    def format_options(option_list: list()):
        """Format list of strings into str consisting of a formatted enumerated list.

        :param option_list: list, list of strings to be enumerated
        :return: str, formatted enumerated list
        """
        content_string = ''
        for p in range(len(option_list)):
            content_string += f"{p + 1}) {option_list[p]}"

            if p is not (len(option_list) - 1):
                content_string += '\n'
        return content_string


class BoolFrame(Frame):
    """Frame takes input of 'y'/'Y' or 'n'/'N' and returns corresponding Bool value when displayed
       (inputs suggested to user automatically)

    (*)<- Inherited
    :attributes:
        *header : str, Displayed at top of frame as |FORMAT|
        *prompt : str, Displayed below header
        *content: str, Displayed below prompt
    """
    def __init__(self, header=None, prompt=None, content=""):
        if content:
            content += "\n*Input [y/n]...*"

        else:
            content += "*Input [y/n]...*"

        super().__init__(header=header, prompt=prompt, content=content)


class ExitFrame(BoolFrame):
    """Frame displaying game exit menu prompting user input.

    (*)<- Inherited
    :attributes:
        *header : str, Displayed at top of frame as |FORMAT|
        *prompt : str, Displayed below header
        *content: str, Displayed below prompt
    """
    def __init__(self, header="EXIT", prompt="Are you sure you want to exit?", content=""):
        super().__init__(header=header, prompt=prompt, content=content)


class EndFrame(BoolFrame):
    """Frame displaying turn-end menu prompting user input.

    (*)<- Inherited
    :attributes:
        *header : str, Displayed at top of frame as |FORMAT|
        *prompt : str, Displayed below header
        *content: str, Displayed below prompt
    """
    def __init__(self, header="END TURN", prompt="Are you sure you want to end your turn?", content=""):
        super().__init__(header=header, prompt=prompt, content=content)


class Menu:
    """Menu consisting of a stack of Frame objects, the top of which is displayed.

    :attributes:
        frame_stack: Stack of Frame objects

    :methods:
        display(get_input=False, check=Function(str) -> Bool, error=False)
            : print top-most frame, option to accept/check user input,
                                    automatically checks bounds when frame_type="list"

        add_frame(frame_type="custom")
            : add a frame of 'frame_type' to the top of 'Menu.frame_stack',
                                    add frame content with **kwargs 'header', 'prompt', and 'content'
            **See function definition for more information**

        pop_frame()
            : pop top frame off of frame_stack

        clear()
            : calls system-specific console 'clear' command
    """
    frame_stack = []

    def __init__(self):
        self._os = os_name

    def display(self, get_input=False, check=lambda inp: True, error=False):
        """Clear console, print Frame on top of frame_stack. If get_input is True, user input is gathered,
           returned, and frame_stack is popped.


        :**kwargs:
            :param get_input: Bool, default: display 'frame_stack[-1].build()'
                                    =True  : display 'frame_stack[-1].build()', return input, pop frame_stack

            :param check: default: input always passes 'check'
                          Function(arg: str) -> Bool=True : return input str
                                                    =False: recursively re-display frame until input passes 'check'
                          *Note: Bool, Enum, Exit, and End frames all automatically check for valid input.*

            :param error: Bool, prints invalid input message if True when getting input

        :return: get_input=False: None
                 get_input=True : str, user input
        """
        self.clear()
        print(self.frame_stack[-1].build())

        if get_input:
            if error:
                u_in = input("*Invalid input.*\n>").strip()
            else:
                u_in = input(">").strip()

            if check(u_in):
                # type-specific input checks
                if isinstance(self.frame_stack[-1], EnumFrame):
                    if check_int(u_in) and 0 < int(u_in) <= len(self.frame_stack[-1].content.split('\n')):
                        self.frame_stack.pop()
                        return u_in

                elif isinstance(self.frame_stack[-1], BoolFrame):
                    if u_in.lower() == 'y':
                        self.frame_stack.pop()
                        return True

                    elif u_in.lower() == 'n':
                        self.frame_stack.pop()
                        return False

                else:
                    self.frame_stack.pop()
                    return u_in

            return self.display(get_input=get_input, check=check, error=True)

    def add_frame(self, frame_type="custom", **kwargs):
        """Add a frame of 'frame_type' to the top of 'frame_stack'. Edit frame fields with **kwargs

        :param frame_type:
            "custom" (default) : blank frame template
            "bool"             : Returns True for input 'y'/'Y', False for 'n'/'N'
            "list"             : enumerated list, kwarg 'content' must be list of strings or unassigned
            "exit"             : default exit-menu template
            "end"              : default turn-end template

        :**kwargs:
            header : Default or
                     str, Displayed at top of frame as |FORMAT|
            prompt : Default or
                     str, Displayed below header
            content: Default or
                     str, Displayed below prompt, formatted as enumerated list or
                     if frame_type="list": List, list of strings to be enumerated and formatted

        :return: None
        """
        if frame_type.lower() == "custom":
            self.frame_stack.append(Frame(**kwargs))

        elif frame_type.lower() == "bool":
            self.frame_stack.append(BoolFrame(**kwargs))

        elif frame_type.lower() == "list":
            self.frame_stack.append(EnumFrame(**kwargs))

        elif frame_type.lower() == "exit":
            self.frame_stack.append(ExitFrame(**kwargs))

        elif frame_type.lower() == "end":
            self.frame_stack.append(EndFrame(**kwargs))

        else:
            raise ValueError

    def pop_frame(self):
        self.frame_stack.pop()

    def clear(self):
        """Calls system-specific console 'clear' command.

        :return: None
        """
        if self._os == "posix":
            system('clear')

        elif self._os == "nt":
            system('cls')


def check_int(_input: str):
    """Check whether input is digit (accepts negative ints)

    :param _input: str, reserved for display function
    :return: Bool
    """
    try:
        int(_input)
        return True

    except (TypeError, ValueError):
        return False
