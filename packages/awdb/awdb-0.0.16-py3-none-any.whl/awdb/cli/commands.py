

class Command(object):
    def to_json(self):
        raise NotImplementedError()

    @classmethod
    def parse(cls, data):
        raise NotImplementedError()

    def to_command(self):
        return self.to_json()


class DebuggerCommand(Command):
    pass


class TraceCommand(Command):
    def to_command(self):
        action = {
            'action': 'call',
            'params': self.to_json(),
        }
        return action


class SimpleCommand(DebuggerCommand):
    _command = None

    @classmethod
    def parse(cls, data):
        if data.strip() == cls._command:
            return cls()

    def to_json(self):
        return {
            "action": self._command
        }


class SimpleTraceCommand(TraceCommand):
    _command = None

    @classmethod
    def parse(cls, data):
        if data.strip() == cls._command:
            return cls()

    def to_json(self):
        return {
            "action": self._command
        }


class BreakCommand(TraceCommand):
    def __init__(self, event, line, filename, condition):
        self.event = event
        self.line = line
        self.filename = filename
        self.condition = condition

    @classmethod
    def parse(cls, data):
        command = data
        _, rest = command.split(' ', 1)
        event, rest = rest.split(' ', 1)
        line, filename = rest.split(' ', 1)

        if ':' in line:
            line = line.split(':', 1)
            line[0] = int(line[0])
            line[1] = int(line[1])
        else:
            line = int(line) if line != 'any' else line

        return BreakCommand(event=event, line=line, filename=filename)

    def to_json(self):
        return {
            "event": self.event,
            "line": self.line,
            "filename": self.filename,
            "condition": self.condition
        }


debugger_command_names = [
    "list"
]

debugger_commands = [
    type(
        "SimpleDebuggerCommand{}".format(cmd.upper()),
        (Command,),
        {
            "_command": cmd
        }
    )
    for cmd in debugger_command_names
]

trace_command_names = [
    'step',
    's',
    'continue',
    'c',
    'stop',
    'inspect',
    'return',
    'interrupt',
    'breakpoints',
    'w',
    'up',
    'down',
]

trace_commands = [
    type(
        "SimpleTraceCommand{}".format(cmd.upper()),
        (Command,),
        {
            "_command": cmd
        }
    )
    for cmd in trace_command_names
]
