from yapf.yapflib.yapf_api import FormatCode


def pyBeautify(code):

    res = (FormatCode(code))[0]
    return res
