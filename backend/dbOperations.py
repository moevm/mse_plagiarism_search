import os
import hashlib
import configparser
from pypika import Query, Table, Field, Schema, CustomFunction, Order, functions
import psycopg2
import traceback
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from app import con, db, app, config, ALLOWED_EXTENSIONS, ALLOWED_ARCHIVES
import zipfile
import tempfile
import sqlQueries
import contextlib
import shutil


@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield d
    finally:
        shutil.rmtree(d, ignore_errors=True)


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_archive(filename):
    return '.' in filename and \
                filename.rsplit('.', 1)[1] in ALLOWED_ARCHIVES


def allowed_file_custom(filename, allowedExtensions):
    return '.' in filename and \
                filename.rsplit('.', 1)[1] in allowedExtensions


#Загрузка файлов в БД. Работает!
@app.route('/upload', methods=['POST'])  #methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and (
            allowed_file(file.filename) or allowed_archive(file.filename)
        ):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if ".zip" in filename:
                #with tempfile.TemporaryDirectory() as tmp: #какого-то хера темпфайл не может почистить директорию за собой, хотя раньше все чистилось нормально. Винда говорит, что папка используется. Ошибки.
                with temporary_directory() as tmp:  #игнорируем ошибки.
                    tmp_dir_name = tmp
                    path = os.path.join(os.getcwd(), tmp_dir_name)
                    with zipfile.ZipFile(
                        os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    ) as zf:
                        zf.extractall(path)
                        addManyFiles(path, filename)
                        return jsonify({"ok": "ok"})
            else:
                addOneFile(
                    app.config['UPLOAD_FOLDER'], filename
                )  #TODO: Удалить файл после всех операций?
                return jsonify(
                    {"ok": "ok"}
                )  #redirect(url_for('uploaded_file', filename=filename))
        else:
            return jsonify({"error": "failed"})


# return '''
# <!doctype html>
# <title>Upload new File</title>
# <h1>Upload newsss File</h1>
# <form action="" method=post enctype=multipart/form-data>
# <p><input type=file name=file>
# <input type=submit value=Upload>
# </form>
# '''


@app.route('/uploads/<filename>')  #временная штука для проверок
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def shorterString(string):
    result = []
    if len(string) <= 255:
        result.append(string)
        return result

    for i in range(0, (len(string) // 253) + 1):
        if i > 0:
            result.append(
                str.encode("~~", encoding="utf-8") +
                string[0 + (i * 253):min(253 * (i + 1), len(string))]
            )
        else:
            result.append(
                string[0 + (i * 255):min(255 * (i + 1), len(string))]
            )
    for v in result:
        print(len(v))
    return result


#TODO: Осмысленное entryName
#       Хранить не весь путь для файла, а только от папки загрузок
def addOneFile(dir, fileName, entryName="", id=0):

    cwd = os.getcwd()

    os.chdir(dir)

    if len(entryName) == 0:
        entryName = fileName

    code = ""
    splittedCode = []
    with open(os.path.join(dir, fileName), encoding='utf-8') as f:
        code = f.read()

    #code = code.replace("\n", "")
    code = code.replace("\t", "")

    codeInBytes = str.encode(code, encoding='utf-8')
    hash_object = hashlib.sha256(codeInBytes)

    q = Query.from_(
        db.tables["File"]
    ).select("id").where(db.tables["File"].hash == hash_object.hexdigest())
    checkDuplicate = executeQ(q, True)
    if checkDuplicate:
        print("Дубликат!", checkDuplicate[0][0])
        return (0, checkDuplicate[0][0])

    if id == 0:
        q = Query.into(
            db.tables["Entry"]
        ).columns('name',
                  'createdAt').insert(entryName, functions.CurTimestamp())
        executeQ(q)
        q = Query.from_(db.tables["Entry"]
                       ).select('id').orderby('id', order=Order.desc).limit(1)
        id = getId(executeQ(q, True))

    fileId = 0
    q = Query.into(db.tables["File"]).columns("entryId", "path",
                                              "hash").insert(
                                                  id,
                                                  os.path.join(dir, fileName),
                                                  hash_object.hexdigest()
                                              )
    executeQ(q)
    q = Query.from_(db.tables["File"]
                   ).select('id').orderby('id', order=Order.desc).limit(1)
    fileId = getId(executeQ(q, True))

    code = code.split("\n")
    #shift = 0
    for string in code:
        stringInBytes = str.encode(string, encoding='utf-8')
        strings = shorterString(stringInBytes)
        for val in strings:
            splittedCode.append(bytes.decode(val, encoding='utf-8'))
    i = 0
    for val in splittedCode:
        q = Query.into(db.tables["CodeFragment"]
                      ).columns("fileId", "order", "text", "metaphone").insert(
                          fileId, i, splittedCode[i],
                          db.func["metaphone"](splittedCode[i], 255)
                      )
        executeQ(q)
        i += 1

    #for i in range(0, (len(codeInBytes)//255)+1):
    #    splittedCode.append(bytes.decode(codeInBytes[0+(i*255):min(255*(i+1), len(codeInBytes))], encoding='utf-8'))
    #    q = Query.into(db.tables["CodeFragment"]).columns("fileId", "order", "text", "metaphone").insert(fileId, i, splittedCode[i], db.func["metaphone"](splittedCode[i], 255))
    #    executeQ(q)

    os.chdir(cwd)

    return (id, fileId)


def addManyFiles(dir, entryName, extensions=ALLOWED_EXTENSIONS):

    id = 0
    results = []
    for dirpath, dirnames, filenames in os.walk(dir):
        # перебрать каталоги
        #for dirname in dirnames:
        #print("Каталог:", os.path.join(dirpath, dirname))
        # перебрать файлы
        for filename in filenames:
            if allowed_file_custom(filename, extensions):
                #print("Файл:", os.path.join(dirpath, filename))
                if id == 0:
                    returned = addOneFile(dirpath, filename, entryName)
                    id = returned[0]
                    print(id)
                    results.append(returned)
                else:
                    returned = addOneFile(dirpath, filename, entryName, id)
                    results.append(returned)
    return results

def addManyFilesByList(fileList, entryName, extensions=ALLOWED_EXTENSIONS):
    id = 0
    results = []
    for filename in fileList:
        if allowed_file_custom(filename, extensions):
            splitted = os.path.split(filename)
            if id == 0:
                returned = addOneFile(splitted[0], splitted[1], entryName)
                id = returned[0]
                print(id)
                results.append(returned)
            else:
                returned = addOneFile(splitted[0], splitted[1], entryName, id)
                results.append(returned)


@app.route('/getEntryFiles/<id>', methods=['GET'])
def getEntryFiles(id):
    q = Query.from_(
        db.tables["File"]
    ).select("path").where(db.tables["File"].entryId == int(id))
    return jsonify(executeQ(q, True))


@app.route('/getFile/<id>', methods=['GET'])
def getFile(id):
    q = Query.from_(
        db.tables["CodeFragment"]
    ).select("text").where(db.tables["CodeFragment"].fileId == int(id)
                          ).orderby('order', order=Order.asc)
    rows = executeQ(q, True)
    text = ""
    for row in rows:
        if text == "":
            text += row[0]
        elif row[0][0] == "~" and row[0][1] == "~":
            text += row[0][2:len(row)]
        else:
            text += "\n" + row[0]
    return jsonify({"file": text})


@app.route('/getAllFiles', methods=['GET'])
def getAllFiles():
    q = Query.from_(db.tables["File"]
                   ).select("id", "path", "entryId").orderby('id', order=Order.asc)
    rows = executeQ(q, True)
    result = {}
    for row in rows:
        q = Query.from_(db.tables["Entry"]).select("createdAt")
        dates = executeQ(q, True)
        result[row[0]] = [row[1], dates[0][0]]
    return jsonify(result)


@app.route('/renameEntry/<id>', methods=['PUT'])
def renameEntry(id):
    #print(request.args)
    q = Query.update(
        db.tables["Entry"]
    ).set(db.tables["Entry"].name,
          request.args["name"]).where(db.tables["Entry"].id == int(id))
    executeQ(q)
    return jsonify(request.args)


@app.route('/deleteEntry/<id>', methods=['DELETE'])
def deleteEntry(id):

    q = Query.from_(db.tables["Entry"]
                   ).delete().where(db.tables["Entry"].id == int(id))
    executeQ(q)
    return jsonify({"ok": "ok"})


@app.route('/deleteAll', methods=['DELETE'])
def deleteAll():

    q = Query.from_(db.tables["Entry"]).delete()
    executeQ(q)
    return jsonify({"ok": "ok"})


def getId(rows):
    for row in rows:
        return row[0]


def executeQ(q, isFetchable=False):
    with con:
        with con.cursor() as cur:
            cur.execute(str(q))
            if isFetchable:
                return cur.fetchall()


def dropAllTables():
    with con:
        with con.cursor() as cur:
            cur.execute(sqlQueries.dropTables)
    print("ALL TABLES WERE DELETED")


#dropAllTables()
