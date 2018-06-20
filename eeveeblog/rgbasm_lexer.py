from pygments.lexer import RegexLexer, include
from pygments.token import Comment, Generic, Keyword, Name, Number, Operator, Punctuation, Text


_preproc = '''
    db dw ds equ equs import export global xref xdef div mul
    sin cos tan asin acos atan atan2 fail warn if else endc
    incbin include macro endm bank def opt popo pusho pushs
    printt printv printf purge rept endr rsset rsreset rb rw
    section shift
'''.split()
_opcodes = '''
    adc add and bit call ccf cp cpl daa dec di ei ex halt
    halt inc jp jr ld ldd ldi ldh ldio nop or pop push
    res ret reti rl rla rlc rlca rr rra rrc rrca rst sbc
    scf sla sra srl stop sub swap xor
'''.split()


class RGBASMLexer(RegexLexer):
    name = 'RGBASM'
    aliases = ['rgbasm']
    filenames = ['*.rgbasm']

    _identifier = r'\w+'

    tokens = {
        'root': [
            # Labels, which must be at the start of the line
            (rf"^[.]?{_identifier}[:]{{0,2}}", Name.Label),
            # Ignore all whitespace
            include('whitespace'),
            (rf"(?:(?i){'|'.join(_preproc)})\b.*\n", Comment.Preproc),
            (rf"(?:(?i){'|'.join(_opcodes)})\b", Keyword, 'opcode-args'),
            (r'.*\n', Text),
        ],
        'opcode-args': [
            # Line continuation, ignore
            (r'\\\n', Text),
            # End of line, instruction over
            (r'[\r\n]+', Text, '#pop'),
            # Otherwise, ignore whitespace
            include('whitespace'),

            (r'[,]', Punctuation),
            # Various forms of numbers
            (r'[$][0-9a-fA-F]+', Number.Hex),
            (r'[%][01]+', Number.Bin),
            (r'[&][0-7]+', Number.Oct),
            (r'[0-9]+[.][0-9]+', Number.Float),
            (r'[0-9]+', Number.Integer),
            # XXX you can change the characters used here, including on the
            # command line, eugh
            (r'`[0-3]+', Number.Bin),
            # Registers
            (r'(?:a|f|b|c|d|e|h|l|af|bc|de|hl)\b', Name.Builtin),
            # Other kinds of names
            (_identifier, Name),
        ],
        'whitespace': [
            (r'\n', Text),
            (r'\s+', Text),
            (r'[;#].*?$', Comment.Single)
        ],
    }


__all__ = ['RGBASMLexer']
