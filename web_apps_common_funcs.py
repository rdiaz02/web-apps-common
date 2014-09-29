## APP_NAME is defined in each app itself

import os

def commonOutput():
    print "Content-type: text/html\n\n"
    print """
    <html>
    <head>
    <title>""" + APP_NAME + """</title>
    </head>
    <body>
    """


## For redirections, from Python Cookbook

def getQualifiedURL(uri = None):
    """ Return a full URL starting with schema, servername and port.

        *uri* -- append this server-rooted uri (must start with a slash)
    """
    schema, stdport = ('http', '80')
    host = os.environ.get('HTTP_HOST')
    if not host:
        host = os.environ.get('SERVER_NAME')
        port = os.environ.get('SERVER_PORT', '80')
        if port != stdport: host = host + ":" + port

    result = "%s://%s" % (schema, host)
    if uri: result = result + uri
    
    return result

def getScriptname():
    """ Return te scriptname part of the URL."""
    return os.environ.get('SCRIPT_NAME', '')

# def getPathinfo():
#     """ Return the remaining part of the URL. """
#     pathinfo = os.environ.get('PATH_INFO', '')
#     return pathinfo

def getBaseURL():
    """ Return a fully qualified URL to this script. """
    return getQualifiedURL(getScriptname())




def fileUpload(fieldName, fs, tmpDir):
    """Upload and get the files and do some checking. We assume there is an existing call
    to fs = cgi.FieldStorage()"""
## we don't deal with OS specific "\n"
## because R does not have a problem (at least with Windows files)
## no problem in R either with empty carriage returns at end of file
    
    if fs.has_key(fieldName):
        fileClient = fs[fieldName].file
        if not fileClient:
            shutil.rmtree(tmpDir)
            commonOutput()
            print "<h1>  " + APP_NAME + "  INPUT ERROR </h1>"    
            print "<p> The ", fieldName, "file you entered is not a file </p>"
            print "<p> Please fill up the required fields and try again</p>"
            print "</body></html>"
            sys.exit()
    else:
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1>  " + APP_NAME + "  INPUT ERROR </h1>"    
        print "<p> ", fieldName, "file required </p>"
        print "<p> Please fill up the required fields and try again</p>"
        print "</body></html>"
        sys.exit()
            
    # transferring files to final destination;

    fileInServer = tmpDir + "/" + fieldName
    srvfile = open(fileInServer, mode = 'w')
    fileString = fs[fieldName].value
    srvfile.write(fileString)
    srvfile.close()

    
    os.chmod(fileInServer, 0666)
        
    if os.path.getsize(fileInServer) == 0:
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1>  " + APP_NAME + "  INPUT ERROR </h1>"
        print "<p>", fieldName, " file has size 0 </p>"
        print "<p> Please enter a file with something in it.</p>"
        if APP_NAME == "adacgh2":
                    print "<p> (Did you enter only a single file, but did not check 'One file'?\
                    If you are using only one file, the 'Two files' button should not be checked.)</p>"
        print "</body></html>"
        sys.exit()



def radioUpload(fieldName, acceptedValues, fs, tmpDir):
    """Upload and get the values and do some checking. For radio selections
    with text data; check those are in acceptedValues.
    We assume there is an existing call to fs = cgi.FieldStorage()"""

    if not fs.has_key(fieldName):
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1>  " + APP_NAME + "  ERROR </h1>"    
        print "<p>", fieldName, "required </p>"
        print "<p> Please fill up the required fields and try again</p>"
        print "</body></html>"
        sys.exit()
    if fs[fieldName].filename:
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1>  " + APP_NAME + "  ERROR </h1>"    
        print "<p> ", fieldName, "should not be a file. </p>"
        print "<p> Please fill up the required fields and try again</p>"
        print "</body></html>"
        sys.exit()
    if type(fs[fieldName]) == type([]):
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1>  " + APP_NAME + "  ERROR </h1>"    
        print "<p>", fieldName, "should be a single value.</p>"
        print "<p> Please fill up the required fields and try again</p>"
        print "</body></html>"
        sys.exit()
    else:
        tmp = fs[fieldName].value
            
    if tmp not in acceptedValues:
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1>  " + APP_NAME + "  ERROR </h1>"    
        print "<p> The", fieldName, "choosen is not valid.</p>"
        print "<p> Please fill up the required fields and try again.</p>"
        print "</body></html>"
        sys.exit()

    fileInServer = tmpDir + "/" + fieldName
    srvfile = open(fileInServer, mode = 'w')
    fileString = tmp
    srvfile.write(fileString)
    srvfile.close()
    os.chmod(fileInServer, 0666)

    return tmp



def dummyUpload(fieldName, value, tmpDir):
    """We no longer read itype or organism, but those are needed in many places
    still."""
    
    fileInServer = tmpDir + "/" + fieldName
    srvfile = open(fileInServer, mode = 'w')
    fileString = value
    srvfile.write(fileString)
    srvfile.close()
    os.chmod(fileInServer, 0666)

    return value
    
