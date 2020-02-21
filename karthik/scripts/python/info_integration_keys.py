import os
import sys
import re
import shutil
import logging
import consul
import json
import git
import fnmatch
import docker
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

from st2actions.runners.pythonrunner import Action

class info_integration_keys (Action):


    def deploymentInfotoDB (self, dbMetaData, tableMetaData, projectInfo, commitSha):
	print dbMetaData
	print tableMetaData 
	print projectInfo
	print commitSha
	#jsonInput={"project_name": "sales", "automatic_trigger": "no"}
	#insertDocumentStatus=r.db(dbMetaData).table(tableMetaData).insert(jsonInput, conflict="update").run(conn)
	


    def checkForJiraProjectdb (self, dbMetaData, tableMetaData, projectInfo):
	conn = r.connect('162.44.146.166', 28015)
        foundStatus="DATA_NOT_FOUND"
        try:
            listofTable=r.db(dbMetaData).table_list().run(conn)
            for tableListVal in listofTable:
                if (tableListVal == tableMetaData):
                    query_getting= r.db(dbMetaData).table(tableMetaData).order_by(index="project_name")
                    for row in query_getting.run(conn):
			print ("Matching", row["project_name"])
			print ("Matching new", projectInfo)
                        jiraProjectKey=row["project_name"].split("/")[-1]
                        if (jiraProjectKey == projectInfo):
                            foundStatus="Data_Found"
			    print ("Daaa", foundStatus)
                            break
                    print foundStatus
		    return foundStatus
                else:
                    errorMessage="Could Not Found"+ " "+ tableMetaData+" "+ "in Database"+ " "+dbMetaData
                    print (errorMessage)
        except RqlRuntimeError as err:
            print(err.message)
        finally:
            conn.close()

    def checkForJenkinsProjectdb (self, dbMetaData, tableMetaData, projectInfo):
	conn = r.connect('162.44.146.166', 28015)
	projectName=projectInfo.split("/")[-1]
        try:
            listofTable=r.db(dbMetaData).table_list().run(conn)
            for tableListVal in listofTable:
                if (tableListVal == tableMetaData):
                    query_getting= r.db(dbMetaData).table(tableMetaData).order_by(index="project_name")
                    for row in query_getting.run(conn):
                        if ((row["project_name"] == projectInfo) or (row["project_name"] == projectName)):
                            foundStatus="Data_Found"
			    if (row["automatic_trigger"] == "yes"):
			        automatic_build="true"
			    else:
				automatic_build="false"
				foundStatus="Data_Found"
                            break
			else:
			    automatic_build="true"
			    foundStatus="Data_Not_Found"
			"""if (row["project_name"] == projectInfo and row["automatic_trigger"] == "no"):
			    automatic_build="false"
			    foundStatus="Data_Found" """
		    print ("Jenkins Found Status", foundStatus)
		    print ("Automatic Build", automatic_build)
		    return foundStatus, automatic_build
                else:
                    errorMessage="Could Not Found"+ " "+ tableMetaData+" "+ "in Database"+ " "+dbMetaData
                    print (errorMessage)
        except RqlRuntimeError as err:
            print(err.message)
        finally:
            conn.close()

    def run(self, inputObject):
	dbName="DevOpsOnborad"
        print("Runnning")
	jiraTableName="Jira_integration"
        jenkinsTableName="Jenkins_integration"
        ownerTableName="Project_owner"
        deployTablename="Deployment_Info"
        #******************* Assiging Default Value ************************************************************************
        #print inputObject["commits"]["message"]
	projectName=inputObject["repository"]["name"]
	projectWithNameSpace=inputObject["project"]["path_with_namespace"]
	commitId=inputObject["commits"][0]["id"]
	resultJiraProjectdb=self.checkForJiraProjectdb(dbName,jiraTableName,projectName)
	resultJenkinsProjectdb, buildTrigger=self.checkForJenkinsProjectdb(dbName,jenkinsTableName,projectWithNameSpace)
	resultDeployinfoDump=self.deploymentInfotoDB(dbName, deployTablename, projectWithNameSpace, commitId)
	#print ("Jira Found Status", resultJiraProjectdb)
	#print ("Jenkins Found Status", resultJenkinsProjectdb)
	#print ("Build trigger Found Status", buildTrigger)
        #resultJiraProjectdb="Data_Found"	
	#resultJenkinsProjectdb="Data_not_found"
	#buildTrigger="yes"
	#jsonarrayLoads=json.loads(inputObject)
	#print ("Commit Message is", inputObject["commits"][0]["message"])
	print ("Project With NameSpace", projectWithNameSpace)
	
	commitMessage=inputObject["commits"][0]["message"]
	patternSearch=re.search("\w+\-\d+", commitMessage)
	jenkinsPatternSearch=re.search("No_Jenkins_Trigger$", commitMessage)

#	print ("Jira Match", patternSearch.group())
#	print ("Jira Match", resultJiraProjectdb)

        if (patternSearch is not None and resultJiraProjectdb == "Data_Found"):
	    print "Under Jira"
	    searchJira=patternSearch.group()
	    jiraKey=searchJira
	else:
	    print "outside jira"
	    jiraKey="NOT_FOUND"
            commitMessage="NOT_APPLICABLE"
	    resultJiraProjectdb="false"

	print ("Build Trigger res", buildTrigger)
	print ("Jenkins Pattern Search", jenkinsPatternSearch)
	if (buildTrigger == "false" or jenkinsPatternSearch is not None):
	    jenkinsJobTrigger="False"
	else:
	    jenkinsJobTrigger="True"
		

        return {"dbIntegration": resultJiraProjectdb, "jiraIssue": jiraKey, "jiraCommentMessage": commitMessage, "jenkinsTriggerStatus": jenkinsJobTrigger, "jenkinsFullProject": projectWithNameSpace}

