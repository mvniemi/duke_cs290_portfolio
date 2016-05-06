#This will take in multiple text files of output from maven and create two markdown
#files that will allow navigation of the libraries that are imported to sakai and the modules that use them

'''
What document will we need:

the raw list of imported jars,
needs some sort of parsing, what is a reliable way to exctract the package name?
the jar files will be put in the dictionary

A spreadsheet or text file containing the broad package name,
link to its documentation, and a short description, should probably
also classify what it is
the package name will be the key

list of modules

the dependency tree:
it needs to be proccesed to make the module name as the dict key,
and assign the jar dependencies to the keys

How it will function:
At top of one markdown document is a list of broad package names,
perhaps with a number of imports
click on it and you are linked down to its head
there will be its description and link to its website,
and a list of the indidual jars imported, and where they are imported to
also # of jars

Another md document will list the modules, with the number of imports of each
click on them and brought to header which lists dependencies


parcing dependencies is a little bit, ignore imports when another sakai module is imported...redudentdent


first step test: parse the broad package names...jar "classes",
make a text file to I can manually look them up and make links +


also do something to detect double imports, maybe make a seperate doc???

need to parse tree first, then build package markdown page

Add if possible:
    -dublicates, seperate section
    -do autorun of bash to grab raw list, need processing
    -lets build markdown report straight from sakai build command line
    -could do a thing for packages that are not yet"wikied" or binned
    -flags for including self imports or just unique
'''
import re
import subprocess
import sys
import os


def main(argv):
    built=False
    for arg in sys.argv[1:]:
        print arg
    if len(sys.argv)>1:
        if sys.argv[1]=='build':
            built=True
            print 'Building List and Tree directly from maven....make sure you have sudo logged in'
            os.system("mkdir report")
            os.system("sudo mvn -o dependency:list -Dmaven.test.skip=true | grep \":.*:.*:.*\" | cut -d] -f2- | sed \'s/:[a-z]*$//g\' | sort -u > report/builtlist.txt")
            os.system("sudo mvn -o dependency:tree -Dmaven.test.skip=true  > report/builttree.txt")

    buildData(built)



def buildData(built):
    #Building The Package dictionary
    #first import package list, parse out package names and link to jars
    #Needs sanitizing for erros
    excludes=[]
    packDict={}
    if built:
        print 'Built Variable True'
    if built:
        packlist = open('report/builtlist.txt', 'r')
    else:
        packlist= open('report/goodlist.txt','r')
    packArray=[]
    line=packlist.readline()
    line=str.replace(line,'    ','')
    while line != "":
        packArray.append(line)
        line=packlist.readline()
        line = str.replace(line, '    ', '')

    listout=open('report/csvout.csv','w')
    for packJar in packArray:
        if str.__contains__(packJar,'missing') or str.__contains__(packJar,'no dependency') or str.__contains__(packJar,'artifact') or str.__contains__(packJar,'sakai') or packJar=='' or str.__contains__(packJar,'javax') or str.__contains__(packJar,'problems encountered'):
            continue
        else:
            split=str.split(packJar,':')
            first=str.split(split[0],'.')
            packName=first[-1:][0]
            if packName not in packDict:
                packDict[packName]=[packJar]
            else:
                templist=packDict[packName]
                templist.append(packJar)
                packDict[packName]=templist
            #print packName
            #listout.write(packName+'\n')
    #get rid of anything empty
    keys=[]
    for key in packDict.keys():
        if key=='\n':
            packDict.pop(key)
        else:keys.append(key)
    keys=sorted(keys)
    for item in keys:
        listout.write(item+'\n')
    #print packDict['antlr']




    #DEPENCENDY TREE
    if built:
        depTree =open('report/builttree.txt', 'r')
    else:
        depTree=open('report/goodtree.txt','r')
    depTreeString=depTree.read()

    depTreeString=str.split(depTreeString,'\n')
    #print depTreeString[0:150]
    for index, line in enumerate(depTreeString):
        if str.startswith(line,'[WARN'):
            depTreeString = [x for x in depTreeString if x != line]
        if str.__contains__(line,'SUCCESS'):
            depTreeString = [x for x in depTreeString if x != line]
        if str.__contains__(line,'artifact'):
            depTreeString = [x for x in depTreeString if x != line]
        if str.__contains__(line,'-----'):
            depTreeString = [x for x in depTreeString if x != line]

    for index, line in enumerate(depTreeString):
        if built:
            if line == '[INFO] ':
                # depTreeString = [x for x in depTreeString if x != line]
                depTreeString[index] = '[INFO]'
            if str.startswith(line, '[INFO]    '):
                depTreeString[index] = '[INFO]'
                # depTreeString = [x for x in depTreeString if x != line]

    for index,line in enumerate(depTreeString):
        depTreeString[index]=re.sub("\\[INFO\\]", '', line)

    #recombing so we can split of build
    depTreeString='\n'.join(depTreeString)
    #print depTreeString
    #Here is where we remove self imports w/in sakai



    #Get our module list
    moduleListOut=open('report/moduelist.txt','w')
    buildSplitTree=str.split(depTreeString,"Building")
    modList=buildSplitTree[0]
    #pop it
    buildSplitTree.pop(0)
    #sanitize it
    #get rid of blank spa# ce
    #continue sanitizine tree
    #remove the end junk
    temp=buildSplitTree[-1]
    temp=str.split(temp,'Reactor')
    buildSplitTree[-1]=temp[0]
    cleantree=buildSplitTree
    depTreeOut=open('report/outree.txt','w')
    for line in '\n'.join(cleantree):
        depTreeOut.write(line)

    #We now have our sanitized dep tree, ready to be parsed
    #each string is a module and its tep dree
    moduleDict = {}
    for index,module in enumerate(cleantree):
        #split on empty space
        modArray=str.split(module,'\n\n')
        if len(modArray)==3:
            modArray.pop(2)
        temp=str.split(modArray[0],' 12')
        modArray[0]=str.replace(modArray[0],' 12-SNAPSHOT','')
        modArray[0]=modArray[0][1:]
        #print modArray[0]+'\n'
        moduleDict[modArray[0]]=modArray[1]

    #We now have a dict with the modules mapped to their dep tree, still need to parse dep tree
    #i want to remove imports within sakai, as it also pulls in those libraries...want to know
    #just the unique imports....could be worthwile having a seperate page for inter-sakai dependencies

    #to parse this tree: we can just split on '\n +', this breaks down to indivudual imports
    for key in moduleDict:
        temp=str.split(moduleDict[key],'\n +')
    #get rid of anything self importing
        temp=[x for x in temp if "sakai" not in x]
        #temp=str.split(temp,'\n')
        newArray=[]
        for index,item in enumerate(temp):
            item=str.split(item,'\n')
            for subitem in item:
                newArray.append(subitem)
        #clean up the package names....
        newArray2=[]
        for pack in newArray:
            split=str.split(pack,':')
            split.pop(0)
            split.pop(-1)
            combined=':'.join(split)
            #combined=str.replace(combined,'.RELEASE','')
            newArray2.append(combined)

        moduleDict[key]=newArray2


    #print moduleDict['sakai-assignment-tool']

    #deal with mod list
    modList=str.replace(modList,"\n\n","\n")
    modList=str.replace(modList,"\n\n","")
    modList=str.replace(modList,'\n ','\n')
    modList=str.replace(modList,'Scanning for projects...\nReactor Build Order:\n','')
    modList = str.replace(modList, " ", "",1)
    moduleListOut.write(modList)

    # moduleDict={}
    # modList=str.split(modList,'\n')
    # for item in modList:
    #     #empty array for each module, will populate w/packagege
    #     if item != '':moduleDict[item]=[]

    # Now link package dictionary with spreadsheet data:
    packageCsv = open('report/csvin.csv', )
    csvstring = packageCsv.read()
    rows = str.split(csvstring, '\r')


    ###############################
    # Build The Markdown
    mdout = open('report/JavaLibReport.md', 'w')
    mdout.write("## Sakai Java Libraries \n")

    # build initial list
    for row in rows:
        #sanitize commas
        row=str.split(row,'\"')
        #print row
        if len(row)>1:
            row[1]=str.replace(row[1],',','')
            #print row[1]
        row=''.join(row)
        row = str.split(row, ',')
        for index, item in enumerate(row):
            row[index] = str.replace(item, '\n', '', 1)

        packid = row[0]
        name = row[1]
        link = row[2]
        desc = row[3]
        cat = row[4]

        count=0
        jars = []
        if packid in packDict:
            jars = packDict[packid]
        for index, item in enumerate(jars):
            jars[index] = str.replace(item, '\n', '', 1)
        for jar in jars:
            jar = str.split(jar, ':')
            # print jar
            jar.pop(0)
            jar = ':'.join(jar)
            for module in moduleDict.keys():
                if jar in moduleDict[module]:
                    count=count+1
        count=str(count)

        mdout.write('* [' + name + '](#' + str.replace(str.lower(name), ' ', '-') + ')' + ' ('+count+')\n')

    # build body
    for row in rows:
        row=str.split(row,'\"')
        #print row
        if len(row)>1:
            row[1]=str.replace(row[1],',','')
            #print row[1]
        row=''.join(row)
        row = str.split(row, ',')
        for index, item in enumerate(row):
            row[index] = str.replace(item, '\n', '', 1)
        packid = row[0]
        name = row[1]
        link = row[2]
        desc = row[3]
        cat = row[4]
        jars = []
        if packid in packDict:
            jars = packDict[packid]
        for index, item in enumerate(jars):
            jars[index] = str.replace(item, '\n', '', 1)
        mdout.write('\n# ' + name + '\n  * ' + desc + '\n')
        mdout.write('* [Documentation](' + link + ')\n\n #### Jars:')
        for jar in jars:
            jar=str.split(jar,':')
            #print jar
            jar.pop(0)
            jar=':'.join(jar)
            mdout.write('\n\n* ' + jar + ',')

             #find packages that import jar
            #print jar
            for module in moduleDict.keys():
                if jar in moduleDict[module]:
                    #print module
                    mdout.write('\n  *  '+module)
        mdout.write('\n')



    #CREATE SECOND MARKDOWN,INDEXED BY SAKAI MODULES

    mdout = open('report/SakaiModuleReport.md', 'w')
    mdout.write("## Sakai Modules \n")
    mdout.write("####Resolved External Imports\n")
    modArray=[]
    for module in moduleDict.keys():
        modArray.append(module)
    modArray=sorted(modArray)

    # mdout.write('* [' + name + '](#' + str.replace(str.lower(name), ' ', '-') + ')' + ' (' + count + ')\n')

    for module in modArray:
        count=len(moduleDict[module])
        count=str(count)
        mdout.write('* [' + module + '](#' + str.replace(str.lower(module), ' ', '-') + ')' +'(' + count+')\n' )

    # mdout.write('\n# ' + name + '\n  * ' + desc + '\n')
    for module in modArray:
        mdout.write('\n\n # '+module)
        for jar in moduleDict[module]:
            mdout.write('\n * '+jar)

    return




if __name__ == "__main__":
    main(sys.argv[1:])
