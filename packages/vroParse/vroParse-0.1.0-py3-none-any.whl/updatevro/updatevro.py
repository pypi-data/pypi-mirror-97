# 
# Example file for parsing and processing XML
#
import xml.dom.minidom
import sys
import os.path

def updateXML(xmlfile):
  #if not os.path.isdir('./js'):
  #  os.makedirs('./js')

  dirName = os.path.dirname(xmlfile)
  print("dirName: %s"%dirName)
  print("xmlfile: %s"%xmlfile)
  wfName = os.path.splitext(os.path.basename(xmlfile))[0]
  print("wfName:%s"%wfName)

  if not os.path.isdir("%s/.parsevro"%dirName):
        print("%s/.parsevro does not exist.  Please run parsevro."%dirName)
        return

  # use the parse() function to load and parse an XML file
  doc = xml.dom.minidom.parse(xmlfile)

  #doc.writexml(sys.stdout)

  
  # print out the document node and the name of the first child tag
  #print(doc.nodeName)
  #print(doc.firstChild.tagName)
  
  # get a list of XML tags from the document and print each one
  wfItems = doc.getElementsByTagName("workflow-item")
  print("%d workflow-item: " % wfItems.length)

  for wfItem in wfItems:
    typeAttr = wfItem.getAttribute("type")
    #print("type: %s" % typeAttr)
    if typeAttr == "task":
      taskName = wfItem.getAttribute("name")
      print("\ntaskName: %s" % taskName)

      displayNameItem = wfItem.getElementsByTagName("display-name")[0]
      for node in displayNameItem.childNodes:
        displayName = node.data
        print("display-name: %s" % displayName)

      scriptItem = wfItem.getElementsByTagName("script")[0]
      for node in scriptItem.childNodes:
        script = node.data
        #print("\nscript: \n%s" % script)

      fileName = "%s/.parsevro/%s_%s_%s.js" % (dirName, wfName, taskName, displayName)
      print("\Reading contents of fileName: \n%s" % fileName)

      if not os.path.isfile(fileName):
        print("%s does not exist.  Please run parsevro again."%fileName)
        continue
        
      f = open(fileName,"r")
      script = f.read()
      f.close()
      #print("file contents:")
      #print(script)


      scriptItem.childNodes[0].data = script

  f = open("%s"%xmlfile,"w+")
  print("writing %s"%f.name)
  doc.writexml(f)
  f.close()

  # create a new XML tag and add it into the document
#   newSkill = doc.createElement("skill")
#   newSkill.setAttribute("name","jQuery")
#   doc.firstChild.appendChild(newSkill)

def main():
  rootDir = './workflows/src/main/resources/Workflow'
  
  if not os.path.isdir(rootDir):
    print("Looking for XML files in %s"%rootDir)
    print("Are you in the right location?  CD to the top leve of a 'mixed' project that contains the %s sub folder structure."%rootDir)
    exit

  print("Updating XML ...")
  
  for dirName, subdirList, fileList in os.walk(rootDir):
    #print("%s" % dirName)

    if len(fileList) > 0:
      for filename in fileList:
        if filename.endswith(".xml"):
          print("\n***%s"%filename)  
          updateXML(dirName+"/"+filename)
