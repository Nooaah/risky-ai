import json

def jsonValue(nameFile):
    fileObject = open(nameFile, "r")
    jsonContent = fileObject.read()
    if jsonContent != "":
      obj_python = json.loads(jsonContent)
      fileObject.close()
      if (obj_python):
        return obj_python
      
def learnFromTraining(file):
    jsonString = json.dumps(file)
    jsonFile = open("file1.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def concatJson(file, file1):
   for key in file1.keys():
      if key not in file.keys():
         file[key] = file1[key]
      else:
         for keyMove in file1[key].keys():
            if keyMove not in file[key].keys():
               file[key][keyMove] = file1[key][keyMove]
   return file

file = jsonValue("file1.json")
file1 = jsonValue("file2.json")
res = concatJson(file,file1)
learnFromTraining(res)
