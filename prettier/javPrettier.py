import jsbeautifier


def pret(code):

    res = jsbeautifier.beautify(code)
    return res
