import pathlib
import inspect


def is_valid_file(file_path, file_type='input'):
    '''
    Function to check input/output existence.

    prepare test file
    >>> valid_file = pathlib.Path(__file__)
    >>> valid_file = valid_file.resolve()
    >>> invalid_file = valid_file.with_suffix('.invalid')

    test valid input file
    >>> is_valid_file(valid_file, file_type='input')
    True

    test invalid input file
    >>> is_valid_file(invalid_file, file_type='input') #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: Input file [...] not exists.
    >>> is_valid_file(None, file_type='input')
    Traceback (most recent call last):
    ValueError: Input file [None] not exists.

    test invalid output file
    >>> is_valid_file(invalid_file, file_type='output')
    False
    '''
    file_flag = False
    if file_path is None:
        pass
    else:
        file_path = pathlib.Path(file_path)
        if file_path.exists() and file_path.stat().st_size:
            file_flag = True
    if file_type == 'input' and (not file_flag):
        raise ValueError(f'Input file [{file_path}] not exists.')
    else:
        return file_flag


def check_in_out(func, params):
    '''
    Extract inputs/outputs information from function doc
    and check their existence

    a test function
    >>> def test_func1(input1, input2, output1, output2):
    ...     """
    ...     input: input1
    ...     input: input2
    ...     output: output1
    ...     output: output2
    ...     """
    ...     pass

    test file
    >>> valid_file = pathlib.Path(__file__)
    >>> valid_file = valid_file.resolve()
    >>> invalid_file = valid_file.with_suffix('.invalid')

    valid input and output
    >>> valid_io_params = {
    ... 'input1': valid_file,
    ... 'input2': valid_file,
    ... 'output1': valid_file,
    ... 'output2': valid_file,
    ... }
    >>> check_in_out(test_func1, valid_io_params)
    True

    invalid input
    >>> valid_io_params['input1'] = invalid_file
    >>> check_in_out(test_func1, valid_io_params) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: Input file [...] not exists.

    invalid output
    >>> valid_io_params['input1'] = valid_file
    >>> valid_io_params['output1'] = invalid_file
    >>> check_in_out(test_func1, valid_io_params)
    False
    >>> valid_io_params['output1'] = valid_file

    function without input annotation
    >>> def test_func2(input1, input2, output1, output2):
    ...     """
    ...     output: output1
    ...     output: output2
    ...     """
    ...     pass
    >>> check_in_out(test_func2, valid_io_params)
    Traceback (most recent call last):
    ValueError: Must define function input.

    function without output annotation
    >>> def test_func3(input1, input2, output1, output2):
    ...     """
    ...     input: input1
    ...     input: input2
    ...     """
    ...     pass
    >>> check_in_out(test_func3, valid_io_params)
    Traceback (most recent call last):
    ValueError: Must define function output.

    '''
    func_doc = inspect.getdoc(func)
    func_doc_obj = func_doc.split('\n')
    input_files = [params.get(each.split(':')[1].strip()) for each
                   in func_doc_obj if each.startswith('input')]
    if len(input_files) == 0:
        raise ValueError('Must define function input.')
    output_files = [params.get(each.split(':')[1].strip()) for each
                    in func_doc_obj if each.startswith('output')]
    if len(output_files) == 0:
        raise ValueError('Must define function output.')
    input_file_status = [is_valid_file(input_file, file_type='input')
                         for input_file in input_files]
    output_file_status = [is_valid_file(output_file, file_type='output')
                          for output_file in output_files]
    return all(output_file_status)
