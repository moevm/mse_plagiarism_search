from dbOperations import con, db, app, config, ALLOWED_EXTENSIONS, ALLOWED_ARCHIVES, executeQ, allowed_file, allowed_archive, secure_filename, addOneFile, addManyFiles, temporary_directory
from pypika import Query, Table, Field, Schema, CustomFunction, Order, functions
from flask import request, jsonify
import os
import time
import zipfile
import tempfile
import json

def getAllMetaphones():
    metaphones = {}
    texts = {}
    files = {}
    extensions = {}
    q = Query.from_(
        db.tables["CodeFragment"]
    ).select("fileId", "metaphone", "text").orderby('id', order=Order.asc)
    rows = executeQ(q, True)
    for row in rows:
        metaphones.setdefault(row[0], []).append(row[1])
        texts.setdefault(row[0], []).append(row[2])
        if not files.get(row[0]):
            q = Query.from_(db.tables["File"]).select("path").where(db.tables["File"].id == int(row[0]))
            res = executeQ(q, True)
            for row_ in res:
                files[row[0]] = row_[0]
                extensions[row[0]] = row_[0].rsplit('.', 1)[1]
                break
    return (metaphones, texts, files, extensions)

    
@app.route('/checkFile/<fileId>', methods=['GET'])
def trueAlgo(fileId, needList = False):
    allTime = time.time()
    fileId = int(fileId)
    
    metaphones, texts, files, extensions = getAllMetaphones()
    currentExtension = extensions[fileId]
    fileMetaphones = metaphones[fileId]
    
    distances = []
    stringsFile = []
    stringsRelevant = []
    stringsFrom = []
    stringsFromNum = []
    result = []
    combo = []
    counterF = 0
    lastFile = -1
    comboCounter = 1
    start_time = time.time()
    
    allKeys = list(metaphones.keys())
    dropKeys = []
    for k in allKeys:
        if k == fileId:
            dropKeys.append(k)
            continue
        if currentExtension != extensions[k]:
            #print("skip! ", currentExtension, " != ", extensions[k], files[k])
            dropKeys.append(k)
            continue
    for k in dropKeys:
        allKeys.remove(k)
        
        
    for val in fileMetaphones:
        
        stringsFile.append(texts[fileId][counterF])
        if val == "":
            counterF += 1
            stringsRelevant.append("_empty_")
            result.append("skipped")
            distances.append(255)
            stringsFromNum.append(-1)
            stringsFrom.append("")
            combo.append(0)
            continue

        minD = 255
        stringsRelevant.append("_empty_")
        result.append("unique")
        
        curFile = -1
        for k in allKeys:

            counter = 0
            
            for val2 in metaphones[k]:
                if val2 == "":
                    counter += 1
                    continue
                if abs(len(val2) - len(val)) > 3:
                    counter += 1
                    continue
                if len(val) > 1 and len(val2)>1 and ((val2[0] != val[0]) or (val2[1] != val[1])):
                    counter += 1
                    continue
                maxD = min(len(val), len(val2), 7) // 2 + 2
                
                q = Query.select(
                    db.func["levenshtein_less_equal"](
                        str(val), val2, min(len(val), len(val2), 7) // 2 + 1
                    )
                )
                
                rows = executeQ(q, True)
                for row in rows:
                    if row[0] != maxD:
                        if minD > row[0]:
                            curFile = k
                            stringsRelevant[len(stringsRelevant) -
                                            1] = texts[k][counter]
                            if row[0] == 0 or row[0] == 1:
                                result[len(result) - 1] = "plagiarism"
                            else:
                                result[len(result) - 1] = "similar"
                        minD = min(minD, row[0])
                counter += 1
                if minD == 0 or minD == 1:
                    break
                #!!!!!!!!!!!!!!!!!!
                #if (minD == 2 or minD == 3) and lastFile == k:
                #    break
            if minD == 0 or minD == 1:
                break
            #!!!!!!!!!!!!!!!!!!
            #if (minD == 2 or minD == 3) and lastFile == k:
            #    break
        distances.append(minD)
        stringsFromNum.append(curFile)
        stringsFrom.append(files[curFile] if curFile != -1 else "")
        if (minD == 0 or minD == 1):
            allKeys.remove(curFile)
            allKeys.insert(0, curFile)
        if lastFile == -1:
            combo.append(1)
        else:
            if lastFile == curFile:
                comboCounter += 1
            else:
                comboCounter = 1
            combo.append(comboCounter)
            
        lastFile = curFile
       

         
        counterF += 1
     
    coincidences = 0
    empty = 0
    currentCombo = 0
    comboToAdd = 0
    for i in reversed(range(len(stringsFile))):
        #print(
        #    stringsFile[i], " ||| ", stringsRelevant[i], " ||| ", distances[i],
        #    result[i]
        #)
        if result[i] == "plagiarism":
            coincidences += 1
        elif result[i] == "similar":
            coincidences += 0.3
        elif result[i] == "skipped":
            empty += 1
        
        if currentCombo > 0:
            if combo[i] == 0:
                continue
            combo[i] += comboToAdd
            currentCombo -= 1
            comboToAdd += 1
        else:
            if combo[i] > 1:
                currentCombo = combo[i] - 1
                comboToAdd = 1
 

    print("RESULT: ", round(coincidences/(len(stringsFile)-empty)*100, 1))
    fullResult = [stringsFile, stringsRelevant, stringsFrom, combo, distances, result, round(coincidences/(len(stringsFile)-empty)*100, 1), files[fileId]]
    print("--- %s seconds ---" % (time.time() - start_time))     
    if needList:
        return fullResult
    else:
        jsonResult = json.dumps(fullResult)
        q = Query.into(db.tables["SearchResult"]).columns("result", "createdAt").insert(jsonResult, functions.CurTimestamp())
        executeQ(q)
        return jsonify(fullResult)


@app.route('/loadAndCheckFile', methods=['POST'])
def loadAndCheckFile():
    if request.method == 'POST':
        file = request.files['file']
        if file and (
            allowed_file(file.filename)  #or allowed_archive(file.filename)
        ):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileId = addOneFile(app.config['UPLOAD_FOLDER'], filename)[1]
            #TODO: Удалить файл после всех операций?
            return trueAlgo(fileId)
        elif file and (
            allowed_archive(file.filename)
        ):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with temporary_directory() as tmp:  #игнорируем ошибки.
                tmp_dir_name = tmp
                path = os.path.join(os.getcwd(), tmp_dir_name)
                with zipfile.ZipFile(
                    os.path.join(app.config['UPLOAD_FOLDER'], filename)
                ) as zf:
                    zf.extractall(path)
                    info = addManyFiles(path, filename)
                    results = []
                    for val in info:
                        print(val)
                        results.append(trueAlgo(val[1], True))
                    jsonResult = json.dumps(results)
                    q = Query.into(db.tables["SearchResult"]).columns("result", "createdAt").insert(jsonResult, functions.CurTimestamp())
                    executeQ(q)
                    return jsonify(results)
        else:
            return jsonify({"error": "failed"})

@app.route('/checkFilesByEntries', methods=['GET'])
def checkFilesByEntries():
    entries = request.form['entries']
    listEntries = json.loads(entries)
    results = []
    for v in listEntries:
        q = Query.from_(db.tables["File"]).select("id").where(db.tables["File"].entryId == int(v))
        res = executeQ(q, True)
        for val in res:
            results.append(trueAlgo(val[0], True))
    
    return jsonify(results)

#trueAlgo(8)
