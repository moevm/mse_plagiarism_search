import subprocess
import tempfile

def prettierJavaCppFiles(code):
    fp = tempfile.NamedTemporaryFile(suffix='.txt', prefix='')
    fp.write(bytes(code, encoding='utf-8'))
    fp.seek(0)
    subprocess.run(["astyle", "-n", fp.name])
    prettier_code = fp.read().decode('utf-8')
    fp.close()
    return prettier_code



