from pygments.lexer import RegexLexer, include
from pygments.token import Comment, Error, Generic, Keyword, Name, Number, Operator, Punctuation, Text


_preproc = '''
    db dw ds equ equs import export global xref xdef div mul
    sin cos tan asin acos atan atan2 fail warn if else endc
    incbin include macro endm bank def opt popo pusho pushs
    printt printv printf purge rept endr rsset rsreset rb rw
    section shift
'''.upper().split()
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
            # This is the start of a line, which must be one of:
            # A keyword, which we have to check before checking for labels
            include('keyword'),
            # A label, which can ONLY appear at the start of the line and may
            # precede an instruction
            # TODO label can also precede EQU, SET, =
            (rf"^[.]?{_identifier}\b[:]{{0,2}}", Name.Function, 'labeled'),
            # Whitespace, which may precede anything but a label
            (rf"[ \t]+", Text),
            # A comment, which consumes the rest of the line
            (rf";.*\n", Comment.Single),
            # An opcode
            (rf"(?i)(?:{'|'.join(_opcodes)})\b", Operator.Word, 'opcode-args'),
            # Otherwise, what the heck is this
            (r'.*\n', Error),
        ],
        # Things that can appear after a label
        'labeled': [
            # Horizontal whitespace
            (r'[ \t]+', Text),
            # One of the assignment keywords
            (r'(?i)(?:equ|set|=)', Keyword, ('#pop', 'line-expression')),
            # A keyword
            include('keyword'),
            # An opcode, which will be followed by args until the end of the line
            (rf"(?i)(?:{'|'.join(_opcodes)})\b", Operator.Word, ('#pop', 'opcode-args')),
            # A comment
            (r';.*?\n', Comment.Single, '#pop'),
            # Nothing
            (r'\n', Text, '#pop'),
        ],
        'keyword': [
            # A keyword, which opaquely consumes the rest of the line (for now)
            (rf"(?i)(?:{'|'.join(_preproc)})\b.*\n", Keyword),
        ],
        'opcode-args': [
            # Line continuation, ignore
            (r'\\\n', Text),
            # End of line, instruction over
            (r'[\r\n]+', Text, '#pop'),
            # Otherwise, ignore whitespace
            include('whitespace'),

            (r'[,]', Punctuation),
            # Registers
            (r'(?:a|f|b|c|d|e|h|l|af|bc|de|hl)\b', Name.Builtin),
            # Brackets around addresses and the +/- notation for hl
            (r'[][+-]', Punctuation),
            # Other kinds of names
            (_identifier, Name.Variable),
            # Arbitrary expressions
            include('expression'),
        ],
        'line-expression': [
            include('expression'),
            (r'\n', Text, '#pop'),
        ],
        'expression': [
            # Ignore whitespace
            (r'[ \t]+', Text),
            # Various forms of numbers
            (r'[$][0-9a-fA-F]+', Number.Hex),
            (r'[%][01]+', Number.Bin),
            (r'[&][0-7]+', Number.Oct),
            (r'[0-9]+[.][0-9]+', Number.Float),
            (r'[0-9]+', Number.Integer),
            # XXX you can change the characters used here, including on the
            # command line, eugh
            (r'`[0-3]+', Number.Bin),
        ],
        'whitespace': [
            (r'\n', Text),
            (r'\s+', Text),
            (r'[;#].*?$', Comment.Single)
        ],
    }


__all__ = ['RGBASMLexer']
