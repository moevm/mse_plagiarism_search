import subprocess
import tempfile
from yapf.yapflib.yapf_api import FormatCode
import jsbeautifier


def prettierJavaCppFiles(code):
    fp = tempfile.NamedTemporaryFile(suffix='.txt', prefix='')
    fp.write(bytes(code, encoding='utf-8'))
    fp.seek(0)
    subprocess.run(["astyle", "-n", fp.name])
    prettier_code = fp.read().decode('utf-8')
    fp.close()
    return prettier_code


def prettierPython(code):
    res = (FormatCode(code))[0]
    return res


def prettierJs(code):
    res = jsbeautifier.beautify(code)
    return res

def prettierCode(code, filename):
    try:
        if filename.endswith('.py'):
            return prettierPython(code)
        elif filename.endswith('.js'):
            return prettierJs(code)
        elif filename.endswith('.cpp') or filename.endswith('.h') or filename.endswith('.c') or filename.endswith('.java'):
            return prettierJavaCppFiles(code)
        else:
            return code
    except:
        return code