import sys
import requests
import json
from urllib.parse import urlencode
import os
import xmltodict


class te_services:
    def __init__(self, confJSON=None):
        this_dir, this_filename = os.path.split(__file__)
        te_constant_path = os.path.join(this_dir, "te_constant.json")
        te_config_path = os.path.join(this_dir, "te_config.json")
        with open(te_constant_path, "r") as cons:
            self.te_constant = json.load(cons)
        if confJSON:
            self.te_config_json = confJSON
        elif os.path.exists("tetest/te_config.json"):
            with open("tetest/te_config.json", "r") as con:
                self.te_config_json = json.load(con)
        else:
            # load default config file in current folder: te_config.json
            with open(te_config_path, "r") as con:
                self.te_config_json = json.load(con)
        # replace the parameter from argument
        # --TaskID, --Token, --BuildID, --TimeSpan
        for arg in sys.argv:
            if "--TaskID=" in arg:
                self.te_config_json["TaskID"] = arg.split("=")[1]
            if "--Token=" in arg:
                self.te_config_json["Token"] = arg.split("=")[1]
            if "--BuildID=" in arg:
                self.te_config_json["BuildID"] = arg.split("=")[1]
            if "--TimeSpan=" in arg:
                self.te_config_json["TimeSpan"] = arg.split("=")[1]
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.te_config_json["Token"]
        }

    def getTask(self):
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["TASK_DATA"] + \
            "/"+self.te_config_json["TaskID"]
        if self.te_config_json["BuildID"]:
            requestUR += "/"+self.te_config_json["BuildID"]
        if self.te_config_json["TimeSpan"]:
            requestUR += "?timespan="+self.te_config_json["TimeSpan"]
        task = requests.get(requestUR, headers=self.headers)
        result = json.loads(task.text)
        self.te_config_json["JobInfo"] = result["body"]

    def addProjectData(self, tableName, bodyJSON, projectName=None):
        _projectName = projectName if projectName is not None else self.te_config_json[
            "Project"]
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["PROJECT_DATA"] + \
            "/"+_projectName + \
            "/"+tableName
        if self.te_config_json.get("JobInfo") is not None and \
                self.te_config_json.get("JobInfo").get("e2einfo") is not None and \
                self.te_config_json.get("JobInfo").get("e2einfo").get("sourcesproject") is not None:
            bodyJSON["_buildid"] = self.te_config_json["BuildID"]
        result = requests.post(requestUR, json=bodyJSON,  headers=self.headers)
        projectData = json.loads(result.text)
        self.addE2EData({
            "name": self.te_constant["E2EDataType"].get("OUTPUT"),
            "type": self.te_constant["E2ETableType"].get("PROJECT"),
            "description": projectData
        })
        return projectData

    def addMasterData(self, tableName, bodyJSON, projectName=None):
        _projectName = projectName if projectName is not None else self.te_config_json[
            "Project"]
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["MASTER_DATA"] + \
            "/"+_projectName + \
            "/"+tableName
        if self.te_config_json.get("JobInfo") is not None and \
                self.te_config_json.get("JobInfo").get("e2einfo") is not None and \
                self.te_config_json.get("JobInfo").get("e2einfo").get("sourcesproject") is not None:
            bodyJSON["_buildid"] = self.te_config_json["BuildID"]
        result = requests.post(requestUR, json=bodyJSON,  headers=self.headers)
        masterData = json.loads(result.text)
        self.addE2EData({
            "name": self.te_constant["E2EDataType"].get("OUTPUT"),
            "type": self.te_constant["E2ETableType"].get("MASTER"),
            "description": masterData
        })
        return masterData

    def getProjectData(self, tableName, queryJSON=None, projectName=None, isE2E=False):
        _projectName = projectName if projectName is not None else self.te_config_json[
            "Project"]
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["PROJECT_DATA"] + \
            "/"+_projectName + \
            "/"+tableName
        if isE2E:
            if queryJSON is None:
                queryJSON = {}
            queryJSON["_buildid"] = self.te_config_json["BuildID"]
        if queryJSON is not None:
            qString = urlencode(queryJSON)
            requestUR += "?"+qString
        result = requests.get(requestUR, headers=self.headers)
        projectData = json.loads(result.text)
        self.addE2EData({
            "name": self.te_constant["E2EDataType"].get("INTPUT"),
            "type": self.te_constant["E2ETableType"].get("PROJECT"),
            "description": projectData
        })
        return projectData

    def getMasterData(self, tableName, queryJSON=None, projectName=None, isE2E=False):
        _projectName = projectName if projectName is not None else self.te_config_json[
            "Project"]
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["MASTER_DATA"] + \
            "/"+_projectName + \
            "/"+tableName
        if isE2E:
            if queryJSON is None:
                queryJSON = {}
            queryJSON["_buildid"] = self.te_config_json["BuildID"]
        if queryJSON is not None:
            qString = urlencode(queryJSON)
            requestUR += "?"+qString
        result = requests.get(requestUR, headers=self.headers)
        masterData = json.loads(result.text)
        self.addE2EData({
            "name": self.te_constant["E2EDataType"].get("INTPUT"),
            "type": self.te_constant["E2ETableType"].get("MASTER"),
            "description": masterData
        })
        return masterData

    def getCaseData(self, caseName, projectName=None):
        _projectName = projectName if projectName is not None else self.te_config_json[
            "Project"]
        caseInfo = {
            "name": caseName
        }
        qString = urlencode(caseInfo)
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["CASE_DATA"] + \
            "/"+_projectName + "?"+qString
        result = requests.get(requestUR, headers=self.headers)
        caseData = json.loads(result.text)
        return caseData

    def getGlobalCaseData(self, projectName=None):
        _projectName = projectName if projectName is not None else self.te_config_json[
            "Project"]
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["CASE_DATA"] + \
            "/"+_projectName + "/global"
        result = requests.get(requestUR, headers=self.headers)
        caseData = json.loads(result.text)
        return caseData

    def updateProjectData(self, tableName, id, bodyJSON, projectName=None):
        _projectName = projectName if projectName is not None else self.te_config_json[
            "Project"]
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["PROJECT_DATA"] + \
            "/"+_projectName + \
            "/"+tableName + \
            "/" + id
        if self.te_config_json.get("JobInfo") is not None and \
                self.te_config_json.get("JobInfo").get("e2einfo") is not None and \
                self.te_config_json.get("JobInfo").get("e2einfo").get("sourcesproject") is not None:
            bodyJSON["_buildid"] = self.te_config_json["BuildID"]
        result = requests.put(requestUR, json=bodyJSON,  headers=self.headers)
        projectData = json.loads(result.text)
        self.addE2EData({
            "name": self.te_constant["E2EDataType"].get("OUTPUT"),
            "type": self.te_constant["E2ETableType"].get("PROJECT"),
            "description": projectData
        })
        return projectData

    def updateMasterData(self, tableName, id, bodyJSON, projectName=None):
        _projectName = projectName if projectName is not None else self.te_config_json[
            "Project"]
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["MASTER_DATA"] + \
            "/"+_projectName + \
            "/"+tableName + \
            "/" + id
        if self.te_config_json.get("JobInfo") is not None and \
                self.te_config_json.get("JobInfo").get("e2einfo") is not None and \
                self.te_config_json.get("JobInfo").get("e2einfo").get("sourcesproject") is not None:
            bodyJSON["_buildid"] = self.te_config_json["BuildID"]
        result = requests.put(requestUR, json=bodyJSON,  headers=self.headers)
        masterData = json.loads(result.text)
        self.addE2EData({
            "name": self.te_constant["E2EDataType"].get("OUTPUT"),
            "type": self.te_constant["E2ETableType"].get("MASTER"),
            "description": masterData
        })
        return masterData

    def updateCaseData(self, caseName, bodyJSON, projectName=None):
        _projectName = projectName if projectName is not None else self.te_config_json[
            "Project"]
        caseInfo = {
            "name": caseName
        }
        qString = urlencode(caseInfo)
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["CASE_DATA"] + \
            "/"+_projectName + "?"+qString
        result = requests.put(requestUR, json=bodyJSON, headers=self.headers)
        caseData = json.loads(result.text)
        return caseData

    def updateGlobalCaseData(self, bodyJSON, projectName=None):
        _projectName = projectName if projectName is not None else self.te_config_json[
            "Project"]
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["CASE_DATA"] + \
            "/"+_projectName + \
            "/global"
        result = requests.put(requestUR, json=bodyJSON, headers=self.headers)
        caseData = json.loads(result.text)
        return caseData

    def uploadJSONReport(self, projectName=None):
        # get report
        reportPath = os.path.join(self.te_config_json.get("Report").get(
            "Path"), self.te_config_json.get("Report").get("File"))
        if os.path.exists(reportPath):
            reportJSON = self.converXMLReportToJSON(reportPath)
        else:
            print("[TE-Info]: NO report file found")
        _projectName = projectName if projectName is not None else self.te_config_json[
            "Project"]
        # if e2e, should use the E2E sources project name
        if self.te_config_json.get("JobInfo") and \
                self.te_config_json.get("JobInfo").get("e2einfo") and \
                self.te_config_json.get("JobInfo").get("e2einfo").get("sourcesproject"):
            _projectName = self.te_config_json.get(
                "JobInfo").get("e2einfo").get("sourcesproject")
        _groupName = self.te_config_json.get("Report").get("ReportGroupName")
        # if has timespan from task, add timespan for grouping
        if self.te_config_json["TimeSpan"] != "":
            _groupName += "_" + self.te_config_json["TimeSpan"]
        # if has build info
        if self.te_config_json.get("JobInfo") and \
                self.te_config_json.get("JobInfo").get("name") is not None:
            _groupName = self.te_config_json.get("JobInfo").get("name")
        # json type
        jsonType = self.te_config_json["Agent"]
        requestUR = self.te_config_json["Server"]+"/" + \
            self.te_constant["ServerAPI"]["REPORT"] + \
            "/"+_projectName + \
            "/" + _groupName +\
            "/"+jsonType
        # get job id
        jobid = ""
        if self.te_config_json.get("JobInfo") and self.te_config_json.get("JobInfo").get("_id"):
            jobid = self.te_config_json.get("JobInfo").get("_id")
        bodyJSON = {
            "jobid": jobid,
            "report": reportJSON,
            "data": []
        }
        # get the e2e data json list
        dataFilePath = "tetest/teE2EData_" + \
            self.te_config_json["BuildID"]+".json"
        jString = ''
        if os.path.exists(dataFilePath):
            with open(dataFilePath, "r") as js:
                jString = js.read()
        if jString != '':
            dataList = json.loads(jString)
            bodyJSON["data"] = dataList.get("data")
            # ==todo: clean data, before the script stateble
        # upload report
        result = requests.post(requestUR, json=bodyJSON, headers=self.headers)
        reportData = json.loads(result.text)
        return reportData

    def converXMLReportToJSON(self, path):
        with open(path) as xmlString:
            doc = xmltodict.parse(xmlString.read())
        if doc is None:
            doc = {}
            print("[TE-Info]: Failed to conver XML to JSON body")
        return doc

    def addE2EData(self, data):
        if os.environ.get('PYTEST_CURRENT_TEST') != "":
            fileInfo = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            fileName = fileInfo[0]
            className = fileInfo[1]
            methodName = fileInfo[2].split(' ')[0]
            # this naming is following the TE backend DB schema
            data["classname"] = className
            data["methoname"] = methodName
            data["filename"] = fileName
        # check if json file in tetest
        dataFilePath = "tetest/teE2EData_" + \
            self.te_config_json["BuildID"]+".json"
        jString = ''
        if os.path.exists(dataFilePath):
            with open(dataFilePath, "r") as js:
                jString = js.read()
        with open(dataFilePath,  "w+") as con:
            if jString == "":
                dataList = {"data": []}
            else:
                dataList = json.loads(jString)
            dataList.get("data").append(data)
            con.write(json.dumps(dataList))

    def isE2E(self):
        isFlag = False
        if self.te_config_json.get("JobInfo") is not None and \
                self.te_config_json.get("JobInfo").get("e2elist") is not None and \
                len(self.te_config_json.get("JobInfo").get("e2elist")) > 0:
            isFlag = True
        return isFlag
