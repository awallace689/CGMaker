from os import system
from os import name as os_name



class Frame:
    """Formatted HEADER, PROMPT, and CONTENT field, meant for Menu class.

    :attributes:
        header: None
                String, Displayed at top of frame as |FORMAT|
        prompt: None
                String, Displayed below header
        content: None
                 String, Displayed below prompt
    """

    header = None
    prompt = None
    content = None

    def __init__(self, header=None, prompt=None, content=None):
        """Create Frame with optional HEADER, PROMPT, and CONTENT fields.

        :kwargs:
            :param header: default: None
                           String : short |TITLE| for frame
            :param prompt: default: None
                           String : Question/Description
            :param content: default: None
                            String : List of options/text-image, etc.
        """
        self.header = header
        self.prompt = prompt
        self.content = content

    def build(self):
        """Generate and return 'print_string' by formatting HEADER, PROMPT, CONTENT fields.

        :return: String, consisting of |HEADER| followed by
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
    """Extends Frame by formatting CONTENT field to be a string of an enumeration of a list of strings.

    (*)<- Inherited
    :attributes:
        *header: None or
                 String, Displayed at top of frame as |FORMAT|
        *prompt: None or
                 String, Displayed below header
        *content: None or
                  String, Displayed below prompt, formatted as enumerated list
    :staticmethods:
        format_options(option_list)
            format list of strings into a string containing a formatted enumerated list
    """

    def __init__(self, header=None, prompt=None, content_list=list()):
        """Create Frame with optional HEADER, PROMPT, and enumerated CONTENT fields.

        :kwargs:
            :param header: default: None
                           String : short |TITLE| for frame
            :param prompt: default: None
                           String : Question/Description
            :param content_list: list of strings to be enumerated
        """
        super().__init__(header=header, prompt=prompt)
        self.content = self.format_options(content_list)

    @staticmethod
    def format_options(option_list: list()):
        """Format list of strings into string consisting of a formatted enumerated list.

        :param option_list: list, list of strings to be enumerated
        :return: String, formatted enumerated list
        """
        content_string = ''
        for p in range(len(option_list)):
            content_string += f"{p + 1}) {option_list[p]}"

            if p is not (len(option_list) - 1):
                content_string += '\n'
        return content_string


class ExitFrame(Frame):
    """Frame displaying game exit menu prompting user input.

    (*)<- Inherited
    :attributes:
        *header : String, Displayed at top of frame as |FORMAT|
        *prompt : String, Displayed below header
        *content: String, Displayed below prompt
    """
    def __init__(self, header="EXIT", prompt="Are you sure you want to exit?", content="'Y' or 'N'?"):
        super().__init__(header=header, prompt=prompt, content=content)


class EndFrame(Frame):
    """Frame displaying turn-end menu prompting user input.

    (*)<- Inherited
    :attributes:
        *header : String, Displayed at top of frame as |FORMAT|
        *prompt : String, Displayed below header
        *content: String, Displayed below prompt
    """
    def __init__(self, header="END TURN", prompt="Are you sure you want to end your turn?", content = "'Y' or 'N'?"):
        super().__init__(header=header, prompt=prompt, content=content)


class Menu:
    """Menu consisting of a stack of Frame objects, the top of which is displayed.

    :attributes:
        frame_stack: Stack of Frame objects

    :methods:
        display(get_input=False, check=Function -> Bool, error=False)
            : print top-most frame, option to accept/check user input
        clear()
            : calls system-specific console 'clear' command
    """
    frame_stack = []

    def __init__(self):
        self._os = os_name

    def display(self, get_input=False, check=lambda inp: True, error=False):
        """Print top of 'frame_stack', use 'get_input' to receive user input and 'check' to validate input.

        :kwargs:
            :param get_input: Bool, default: display 'frame_stack[-1].build()'
                                    =True  : display 'frame_stack[-1].build()' and return input string

            :param check: default: input always passes 'check'
                          Function(String) -> Bool=True : return input string
                                                  =False: recursively re-display frame until input passes 'check'

            :param error: Bool, prints invalid input message if True when getting input

        :return: get_input=False: None
                 get_input=True : String, user input
        """
        self.clear()
        print(self.frame_stack[-1].build())

        if get_input:
            if error:
                u_in = input("*Invalid input.*\n>")
            else:
                u_in = input(">")

            if check(u_in):
                return u_in
            else:
                return self.display(get_input=get_input, check=check, error=True)

    def add_frame(self, frame_type="custom", *kwargs):
        """Add a frame of 'frame_type' to the top of 'frame_stack'. Edit frame with *kwargs

        :kwarg frame_type:
            "custom" (default) : blank frame template
            "exit"             : default exit-menu template
            "end"              : default turn-end template

        :*kwargs:
            header : Default or
                     String, Displayed at top of frame as |FORMAT|
            prompt : Default or
                     String, Displayed below header
            content: Default or
                     String, Displayed below prompt, formatted as enumerated list

        :return: None
        """
        if frame_type.lower() == "custom":
            self.frame_stack.append(Frame(*kwargs))

        elif frame_type.lower() == "exit":
            self.frame_stack.append(ExitFrame(*kwargs))

        elif frame_type.lower() == "end":
            self.frame_stack.append(EndFrame(*kwargs))

        else:
            raise ValueError

    def clear(self):
        """Calls system-specific console 'clear' command.

        :return: None
        """
        if self._os == "posix":
            system('clear')

        elif self._os == "nt":
            system('cls')
