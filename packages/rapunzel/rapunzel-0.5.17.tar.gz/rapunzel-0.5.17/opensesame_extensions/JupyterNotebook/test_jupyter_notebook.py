from jupyter_notebook_cell_parsers.parse_nbformat import (
    cells_to_notebook,
    notebook_to_code
)
from jupyter_notebook_cell_parsers.parse_python import parse_python

NO_CELLS = '''print(1)
print(2)
'''
NO_CELLS_OUTPUT = []
ONE_SIMPLE_COMMENT = '''
"""
Comment 3
Comment 4
"""

'''
ONE_SIMPLE_COMMENT_OUTPUT = [{
    'cell_type': 'markdown',
    'source': 'Comment 3\nComment 4',
    'start': 1,
    'end': 29
}]
TWO_SIMPLE_CELLS = '''"""
Comment 5
"""
print('Code 6')
"""
Comment 7
"""
print('Code 8')
'''
TWO_SIMPLE_CELLS_OUTPUT = [
    {
        'cell_type': 'markdown',
        'source': 'Comment 5',
        'start': 0,
        'end': 18
    },
    {
        'cell_type': 'code',
        'source': "print('Code 6')",
        'start': 18,
        'end': 34
    },
    {
        'cell_type': 'markdown',
        'source': 'Comment 7',
        'start': 34,
        'end': 52
    },
    {
        'cell_type': 'code',
        'source': "print('Code 8')",
        'start': 52,
        'end': 68
    }
]
SIMPLE_CELL_WITH_OUTPUT = '''"""
Comment 9
"""

print('Code A')

# % output
# Code A
print('Code B')

# % output
# Code B
# ![](figure.png)
'''
SIMPLE_CELL_WITH_OUTPUT_OUTPUT = [
    {
        'cell_type': 'markdown',
        'source': 'Comment 9',
        'start': 0,
        'end': 18
    },
    {
        'cell_type': 'code',
        'source': "print('Code A')",
        'execution_count': 1,
        'start': 18,
        'end': 35,
        'output_type': 'execute_result',
        'outputs': '# Code A'
    },
    {
        'cell_type': 'code',
        'source': "print('Code B')",
        'execution_count': 2,
        'start': 56,
        'end': 72,
        'output_type': 'execute_result',
        'outputs': '# Code B\n# ![](figure.png)'
    }
]
BASIC_SPYDER_CELL = '''# %%
print(1)
print(2)
'''
BASIC_SPYDER_CELL_OUTPUT = [
    {
        'cell_type': 'code',
        'source': "print(1)\nprint(2)",
        'start': 5,
        'end': 22
    }
]

SPYDER_CELL_WITH_OUTPUT = '''# %%
# Comment 10

print('Code C')

# % output
# Code C
print('Code D')

# % output
# Code D
# ![](figure.png)
'''
SPYDER_CELL_WITH_OUTPUT_OUTPUT = [
    {
        'cell_type': 'markdown',
        'source': 'Comment 10',
        'start': 5,
        'end': 17
    },
    {
        'cell_type': 'code',
        'source': "print('Code C')",
        'execution_count': 1,
        'start': 18,
        'end': 35,
        'output_type': 'execute_result',
        'outputs': '# Code C'
    },
    {
        'cell_type': 'code',
        'source': "print('Code D')",
        'execution_count': 2,
        'start': 56,
        'end': 72,
        'output_type': 'execute_result',
        'outputs': '# Code D\n# ![](figure.png)'
    }
]


def _check_parser(fnc, code, result=None):
    
    cells = fnc(code)
    for cell in cells:
        # Check whether the start and end positions are consistent with the
        # text. Code cells are stripped of whitespaces, and comment cells
        # are stripped of triple quotes.
        if cell['cell_type'] == 'code':
            assert(code[cell['start']:cell['end']].strip() == cell['source'])
        elif cell['cell_type'] == 'markdown':
            code_chunk = code[cell['start']:cell['end']]
            if not code_chunk.startswith('#'):
                assert code_chunk == '"""\n{}\n"""\n'.format(cell['source'])
    # Assert that the full code matches the expected output
    if result is not None:
        assert(cells == result)


def test_python_parser():
    
    _check_parser(
        parse_python,
        TWO_SIMPLE_CELLS,
        TWO_SIMPLE_CELLS_OUTPUT
    )
    _check_parser(
        parse_python,
        NO_CELLS,
        NO_CELLS_OUTPUT
    )
    _check_parser(
        parse_python,
        ONE_SIMPLE_COMMENT,
        ONE_SIMPLE_COMMENT_OUTPUT
    )
    _check_parser(
        parse_python,
        SIMPLE_CELL_WITH_OUTPUT,
        SIMPLE_CELL_WITH_OUTPUT_OUTPUT
    )
    _check_parser(
        parse_python,
        BASIC_SPYDER_CELL,
        BASIC_SPYDER_CELL_OUTPUT
    )
    _check_parser(
        parse_python,
        SPYDER_CELL_WITH_OUTPUT,
        SPYDER_CELL_WITH_OUTPUT_OUTPUT
    )


def test_nbformat_parser():

    cells = parse_python(SIMPLE_CELL_WITH_OUTPUT)
    cells_to_notebook(cells, path='tmp.ipynb', language='python')
    language, code = notebook_to_code(
        'tmp.ipynb',
        (lambda fmt, content: 'figure.png')
    )
    assert(code == SIMPLE_CELL_WITH_OUTPUT)


if __name__ == '__main__':
    test_python_parser()
    test_nbformat_parser()
