import os
import shutil
import math

from bs4 import BeautifulSoup
from pathlib import Path
'''
    CHANGES 
    - Changed case method:
        - camelCase for variables
        - snake_case for functions
        - PascalCase for classes/objects
        - This was previously jumbled. This makes code more readable as its easier to discern what something is at a glance
    - Introduced 'Manual' class :
        - Many of the old functions had gotten needlessly complicated and messy due to repeating the same variables in. 
        - This now means they are all stored as part of the class instead and makes it easier to adjust parts of it 
    - Always adds tags as it avoids overhead on having to discern what the tag actually is 
    - Adds paragraph breaks above start of text so that nothing is hidden behind topbar 
    - Changed from create_doc to prettify_html to minimise chance of confusion between .doc files
    - Simplifed finding of headers

    
'''
class Manual: # moved to class as many variables ended up getting repeated throughout
    def __init__(self,original,newName): # default value setting
        # Setup files and folders
        original = original.replace('\\','/')
        self.ogDir = os.path.dirname(original)
        self.ogName = os.path.basename(original).split('.', 1)[0]
        self.ogFiles = self.ogDir + '/' + self.ogName + '_files'
        self.logoPath = 'logo.png' # this is a path relative to program. May be better to state entire path?
        self.logoName = os.path.basename(self.logoPath)
        self.logoLink =  'https://github.com/KaneLikesFrogs' # set this to a website to redirect a user to somewhere else when clicking logo
        self.ogRelPath = (self.ogName + '_files').replace(' ','%20')

        self.newDir = self.ogDir + '/' + newName
        self.newName = newName
        self.newFiles = self.newDir + '/' + newName + '_files'
        self.newRelPath = (self.newName + '_files').replace(' ','%20')
        
        self.nameBlacklist = []
        self.nameCutoff = []
        self.tagBlacklist = ['1','2','3','4','5','6','7','8','9','0',' ','\n'] 
        self.tagCutoff = []
        # these are characters to remove from names on nav menus/bookmarks
        # exists as a class variable so it can be changed/altered externally
        # similarly can use cutoff to remove everything before a marker 
        #   for example chapter 1 - Example 1 would become: Example (with cutoff of ['-'])
        #   as the tag cutsoff numbers the tag would end up being _example

        # order of operations means that any changes to the name will also be applied to the tag

        # Setup default parameters
        # More concise than functions with repeated arguments
        self.parentHeading = 'h2'
        self.childHeading = 'h3'
        self.tag = 'qq_' 
        

        self.parentIds = []
        self.parentIndexes = []
        self.parentNames = []
        self.childIds = []
        self.childIndexes = []
        self.childNames = []

        # add and clean data
        self.data = str(open(original).read()).replace(u'\xa0',u'&#160;')
        
        self.update_paths(newName)

        # set css parameters
        self.sideNavWidth = 340
        self.topNavHeight = 80
        self.highlight = '#604D81' 
        self.navFontSize = 14 
        print("init complete")

    def set_tag(self,newTag): # can be called to change the bookmark tags
        # called at start of prettify_html function
        # can change before prettifying 
        self.tag = newTag
        self.add_tags(False)
        self.add_tags(True)

    def get_header(self,child=False): # used for adding tags and setting up lists inside class
        index = 0
        endIndex = 0
        indexList = []
        endIndexList = []
        tidyIndexList = []
        idList = []
        nameList = []
        undesiredChars = ['</a>','<', '>', '"']

        if child:
            startStr = f"<{self.childHeading}>"
            endStr = f"</{self.childHeading}>"
        else:
            startStr = f"<{self.parentHeading}>"
            endStr = f"</{self.parentHeading}>"
        # isolates headers (defined above depending on if it is a child)
        # can change it manually via the object itself
        # currently uses h2 and h3 to (as h1 would likely be a title)
        while True:
            index = self.data.find(startStr,index + 1)
            endIndex = self.data.find(endStr,index)
            if index == -1:
                break
            else:
                indexList.append(index)
                endIndexList.append(endIndex)

        for x in range(len(indexList)):
            snip = self.data[indexList[x]:endIndexList[x]]
            soup = BeautifulSoup(snip,'html.parser')
            soupName = ''
            for y in soup.strings:
                soupName = soupName + repr(y)
            soupSpoon = ['>','<','/','"',"'","\\xa0","\\xa"] # scoop out any whitespace/invalid chars
            for y in soupSpoon:
                soupName = soupName.replace(y,'')
            soupName = soupName.replace('\\n',' ')
            name = soupName
            undesiredChars = ['</a>','<', '>', '"'] # removes anything that could mess with html tagging
            # note that both soupSpoon and undesiredChars are hardcoded to NOT be changed
            # however as I may have missed some cases they can be changed here if necesseary
            
            for y in undesiredChars:
                    name = name.replace(y, '')
            for y in self.nameBlacklist:
                name = name.replace(y,'')
            for y in self.nameCutoff:
                 if name.find(y) > 0:
                     name = name[name.find(y)+1:]
        
            tidyTag = self.tag + name.lower()
            for y in self.tagBlacklist:
                tidyTag = tidyTag.replace(y.lower(),'')
            for y in self.tagCutoff:
                 if tidyTag.find(y) > 0:
                     tidyTag = tidyTag[tidyTag.find(y)+1:]
            if name != "": # skip items were there is no name
                nameList.append(name)
                tidyIndexList.append(indexList[x])
                idList.append(tidyTag)

        tidyIndexList.append(len(self.data))

        if child:
            self.childIds = idList
            self.childIndexes = tidyIndexList
            self.childNames = nameList
        else:
            self.parentIds = idList
            self.parentIndexes = tidyIndexList
            self.parentNames = nameList
        return(idList,tidyIndexList,nameList) # sets class values but can also be used to grab the headers themselves 
    
    def add_tags(self,child=False): # adds specified tag to all items
        ids, indexes, names = self.get_header(child) # gets indexes + names
        tagList = ids
        # print(ids,indexes,names)
        # names = names[1:]
        for x in range(len(indexes)):
            try:
                name = f'<a name="{tagList[x]}"></a>'
                nameLen = len(name)
                index = indexes[x]
                self.data = self.data[:index+4] + name + self.data[index+4:] # offset by 4 for the for characters in : <h2> (or <h3>)
                # this inserts the reference to the document
                indexes = [y+nameLen for y in indexes] # offset remaining indexes
            except:
                pass
        self.get_header(child) # refreshes indexes and can now send out ids

    def update_paths(self,newName=""): # updates files to be in new folder to remove dependency on old folder
            if newName == "":
                print("no name submitted, adjusting logo position")
                newName = self.newName # if name isnt submitted just uses previous name
            else: # if target is changing then moves files around
                self.newDir = self.ogDir + '/' + newName
                self.newName = newName
                self.newFiles = self.newDir + '/' + newName + '_files'
                self.newRelPath = (self.newName + '_files').replace(' ','%20')
                if Path(self.newFiles).exists() and Path(self.newFiles).is_dir(): # if dir exists then errors
                    return FileExistsError(self.newFiles)            
                try: # error proofing for invalid logo path
                    shutil.copy(self.logoPath,self.newFiles)
                except:
                    print("logo not found")
                os.makedirs(self.newFiles,exist_ok=True)
                shutil.copytree(self.ogFiles,self.newFiles,dirs_exist_ok=True) 
            if self.logoPath == "":
                pass
            else:
                self.logoName = os.path.basename(self.logoPath)
                try:
                    shutil.copy(self.logoPath,self.newFiles) # replaces logo if changed
                except:
                    print("logo not found")

    def create_html_contents(self): # creates html for contents page based on 
        output = [('<div class="sidenav">')]
        if self.logoPath != "":
            if self.logoLink != "":
                output.append('\t<a href="'+ self.logoLink + f'" target="_blank">')
            output.append(f'\t<img src="{self.newRelPath}/{self.logoName}" width="'+ str(self.sideNavWidth) + '">')
            output.append('\t</a>')
            output.append('<p><br></p>')
        for x in range(len(self.parentIds)):
                if self.parentIds[x] != "":
                    children = 0
                    for y in range(len(self.childIndexes)):
                        if self.childIndexes[y] > self.parentIndexes[x]:
                            if self.childIndexes[y] < self.parentIndexes[x+1]:
                                children += 1
                    if children < 1:
                        #print(x)
                        output.append("\t" + '<a href="#' + self.parentIds[x] + '">' + self.parentNames[x] + '</a>')
                        pass
                    else:
                        output.append("\t" + '<button class="dropdown-btn">' + str(self.parentNames[x]) + '</button>')
                        output.append("\t \t" + '<div class="dropdown-container">')
                        output.append("\t \t" + '<a href="#' + self.parentIds[x] +  '">' + self.parentNames[x] + '</a>')
                        for y in range(len(self.childIndexes)):
                            if self.childIndexes[y] > self.parentIndexes[x]:
                                if self.childIndexes[y] < self.parentIndexes[x+1]:
                                    output.append("\t \t" + '<a href="#' + self.childIds[y] + '">' + self.childNames[y] + '</a>')
                        output.append("\t \t" + '</div>')
        output.append("\t<p><br></p>")
        output.append("\t<p><br></p>") # adds 2 page breaks to help avoid bottom element disappearing when too many elements present
        output.append("</div>")
        output = '\n'.join(output)
        self.htmlContents = output

    def create_html_index(self):
        if self.topNavHeight < 40:
            self.htmlIndex = ['<!--no index included-->']
            return
        ids = self.parentIds + self.childIds
        names = self.parentNames + self.childNames
        listItems = []
        output = ['<div class="topnav">']
        output.append('\t<div class="SearchField">')
        output.append('\t\t<input type="text" id = "SearchBox" onkeyup="SearchFunc()" placeholder="Search...">')
        output.append('\t\t<div class="SearchResults">')
        output.append('\t\t\t<ul id = "IndexItems">')
        for x in range(len(ids)): 
            listItems.append('\t\t\t\t<li><a href="#' + ids[x] + '">' + names[x] + '</a></li>')
        listItems.sort()
        for x in listItems:
            output.append(x)
        output.append('\t\t\t</ul>')
        output.append('\t\t</div>')
        output.append('\t</div>')
        output.append("</div>")
        output = '\n'.join(output)
        self.htmlIndex = output
    
    def create_css_index(self):
        if self.topNavHeight<40:
            return(["/*No CSS Included for topnav*/"])
        # dislike this method but where there is variables thrown in it gets more 
        # difficult to handle as a multi line string (due to fact {} brackets exist as part of css)
        output= ['/*CSS for topnav*/']
        output.append('.topnav {')
        output.append('\tposition: fixed;')
        output.append('\ttop: 0;')
        output.append('\theight: ' + str(self.topNavHeight) +'px;')
        output.append('\twidth: 105%;')
        output.append('\tbackground-color: #f1f1f1;')
        output.append('\tborder-bottom: 20px solid '+ self.highlight +';')
        output.append('\toverflow: visible')
        output.append('}')
        output.append('#SearchBox {')
        output.append('\tfloat: right;')
        output.append('\tmargin-top: ' + str(self.topNavHeight/4) + 'px;')
        output.append('\tmargin-right: 150px;')
        output.append('\theight: 40px;')
        output.append('\twidth: 200px;')
        output.append('\tpadding: 11px;')
        output.append('\tz-index: 2;')
        output.append('}')
        output.append('.SearchResults {')
        output.append('\tdisplay: none;')
        output.append('\tfloat: right;')
        output.append('\tmargin-top: ' + str(self.topNavHeight/4 + 40) + 'px;')
        output.append('\tmargin-right: -200px;')
        output.append('\tmargin-left: 0px;')
        output.append('\tmax-width: 200px;')
        output.append('\tmin-width: 200px;')
        output.append('\tz-index: 1;')
        output.append('\tbackground-color: #e1e1e1;')
        output.append('\toverflow-y: scroll;')
        output.append('\theight: auto;')
        output.append('\tmax-height: 375px;')
        output.append('\tscrollbar-gutter: stable;')
        output.append('\tmargin-left: 0px;')
        output.append('}')
        output.append('.SearchResults a {')
        output.append('\tcolor: black;')
        output.append('\ttext-decoration: none;')
        output.append('\tdisplay: block;')
        output.append('\tborder-top: solid #d1d1d1 2px;')
        output.append('\tpadding-top: 6px;')
        output.append('\tpadding-bottom: 6px;')
        output.append('}')
        output.append('.SearchResults a:hover {')
        output.append( '\tbackground-color: ' + self.highlight + ';')
        output.append('\tcolor: white')
        output.append('}')
        output.append('#SearchBox:focus-visible + .SearchResults{')
        output.append('display: block; ')
        output.append('}')
        output.append('.SearchResults:hover{')
        output.append('\tdisplay: block;')
        output.append('}')
        output.append('#IndexItems {')
        output.append('\tlist-style-type: none;')
        output.append('\tpadding: 5px;')
        output.append('\tjustify-content: center;')
        output.append(f'\tfont-size: {self.navFontSize}pt;')
        output.append('\tfont-family: Arial, sans-serif ;')
        output.append('}')
        output.append('html {')
        output.append('\tscroll-padding-top:' + str(self.topNavHeight + 20) + 'px;')
        output.append('\tscrollbar-gutter: stable;')
        output.append('}')
        output.append('</style>\n')
        output = '\n'.join(output)
        # creation of css
        self.cssIndex = output
        # offsets start of text so that it does not disappear below top nav (as it sits on top)
        self.data 

    def create_css_contents(self):
        output = ['<style>']
        output.append('/*CSS for contents*/')
        output.append('.sidenav {')
        output.append('\theight: 100%;')
        output.append('\twidth: ' + str(self.sideNavWidth) + 'px;')
        output.append('\tposition: fixed;')
        output.append('\tz-index: 1;')
        output.append('\ttop: 0;')
        output.append('\tleft: 0;')
        output.append('\tbackground-color: #f1f1f1;')
        output.append('\toverflow-x: hidden;')
        output.append('\tpadding: 20px;')
        output.append('\tfont-family: Arial, sans-serif;')
        output.append('}')
        output.append('\n')
        output.append('.sidenav a, .dropdown-btn {')
        output.append('\tpadding: 6px 8px 6px;')
        output.append('\ttext-decoration: none;')
        output.append(f'\tfont-size: {self.navFontSize}pt;')
        output.append('\tcolor: #424242;')
        output.append('\tdisplay: block;')
        output.append('\tborder: none;')
        output.append('\tbackground: none;')
        output.append('\twidth: 100%;')
        output.append('\ttext-align: left;')
        output.append('\tcursor: pointer;')
        output.append('\toutline: none;')
        output.append('\tfont-family: Arial, sans-serif;')
        output.append('}')
        output.append('\n')
        output.append('.sidenav a:hover, .dropdown-btn:hover {')
        output.append('\tcolor: #f1f1f1;')
        output.append(f'\tbackground-color: {self.highlight};')
        output.append('}')
        output.append('\n')
        output.append('.active {')
        output.append(f'\tbackground-color: {self.highlight};')
        output.append('\tcolor: white;')
        output.append('}')
        output.append('\n')
        output.append('.dropdown-container {')
        output.append('\tdisplay: none;')
        output.append('\tpadding-left: 20px;')
        output.append('\tpadding-right: 20px;')
        output.append('\twidth:' + str(self.sideNavWidth - 40) + 'px;')
        output.append('\tbackground-color: #e1e1e1;')
        output.append('\tfont-family: Arial, sans-serif;')
        output.append('}')
        output.append('\n')
        output.append('@media screen and (max-height: 450px) {')
        output.append('\t.sidenav {padding-top: 0px;}')
        output.append('\t.sidenav a {font-size:'+ f'{self.navFontSize}pt;'+'}')
        output.append('}')
        output.append('\n')
        output = '\n'.join(output)
        self.cssContents = output

    def create_js(self): 
        # this could be a constant as it does not care about other parts of class
        # is a function ato maintain a sort of consistent flow though may revisit this 
        output = ['//dropdown setup start']
        output.append('var dropdown = document.getElementsByClassName("dropdown-btn"); ')
        output.append('var i;')
        output.append('for (i = 0; i < dropdown.length; i++) {')
        output.append('\tdropdown[i].addEventListener("click", function() {')
        output.append('\t\tthis.classList.toggle("active");')
        output.append('\t\tvar dropdownContent = this.nextElementSibling;')
        output.append('\t\tif (dropdownContent.style.display === "block") {')
        output.append('\t\t\tdropdownContent.style.display = "none";')
        output.append('\t\t} else {')
        output.append('\t\t\tdropdownContent.style.display = "block";')
        output.append('\t\t}')
        output.append('\t});')
        output.append('}')
        output.append('//end of dropdown setup')
        output.append('\n \n')
        output.append('//start of index setup')
        output.append('var ul = document.getElementById("IndexItems");')
        output.append('var li = ul.getElementsByTagName("li");')
        output.append('\n')
        output.append('for (i = 0; i < li.length; i++) {')
        output.append('\tli[i].style.display = "none"')
        output.append('\t} //hides all elements on startup')
        output.append('\n')
        output.append('function SearchFunc() {')
        output.append('\t//this function is called by the search box when hte input is changed  ')
        output.append('\tvar input = document.getElementById("SearchBox");')
        output.append('\tvar filter = input.value.toUpperCase(); /*makes it so search is not case sensitive*/')
        output.append('\tvar ul = document.getElementById("IndexItems");')
        output.append('\tvar li = ul.getElementsByTagName("li");')
        output.append('\tvar i;')
        output.append('\t//sets up variables')
        output.append('\tif (filter == "") {')
        output.append('\t\tfor (i = 0; i < li.length; i++) {')
        output.append('\t\t\tli[i].style.display = "none";')
        output.append('\t\t}')
        output.append('\t}')
        output.append('\telse{')
        output.append('\t\tfor (i = 0; i < li.length; i++) {')
        output.append('\t\t\ta = li[i].getElementsByTagName("a")[0];')
        output.append('\t\t\tif (a.innerHTML.toUpperCase().indexOf(filter) > -1) {')
        output.append('\t\t\t\tli[i].style.display = "";')
        output.append('\t\t\t} ')
        output.append('else {')
        output.append('\t\t\t\tli[i].style.display = "none";')
        output.append('\t\t\t}')
        output.append('\t\t}')
        output.append('\t}')
        output.append('\t}')
        output.append('//end of index setup')
        output = '\n'.join(output)
        self.js = output

    def prettify_html(self): # returns directory saved to if successful
        self.set_tag(self.tag)
        self.data = self.data.replace(f'src="{self.ogRelPath}/',f'src="{self.newRelPath}/') 
        # this is a one way process (difficult to undo). More efficient to just do it here instead
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # co-erce image positioning to be consistent here #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        try: 
            self.update_paths("") # updates all paths if logo has changed (for example)
        except:
            print("Target folder already exists")
            return FileExistsError
        

        self.create_css_contents()
        self.create_css_index() 
        # in css functions we open and close a unique style marker due as it is dififcult to tell (when indexing) if it is in a comment or not
        dataCss = self.cssContents + '\n' + self.cssIndex 

        self.create_html_contents()
        self.create_html_index()
        dataHtml = self.htmlContents + '\n' + self.htmlIndex

        self.create_js()
        # need to update each word div to have a margin so that sidenav is not over the text
        divUpdate = f' style="margin-left: {str(self.sideNavWidth+30)}px; border-left: 20px solid  {self.highlight}; padding-left: 20px"' 
        start = 0
        end = 0

        while True: # replaces div classes to all have larger margins, may conflict if there is existing formatting there
            try:
                start = self.data.index('<div class=',end) # page marker in document
                end = self.data.index('>',start)
                self.data = self.data[:end] + divUpdate + self.data[end:]
            except:
                break # errors on index and then stops loop
        try: # insert some paragraphs to offset text (due to topnav)
            textStart = self.data.index('<div class') 
            textStart = self.data.index('>',textStart)
            self.data = self.data[:textStart+1] + ('<br>')*int(math.ceil(self.topNavHeight/15)) + self.data[textStart+1:]
        except:
            print("Warning: Failed to insert paragraphs to pad for topnav")
            pass
        try: # find start of css section
            cssEnd = self.data.find('</head>')
        except: # errors if not found
            print("could not find css section in file")
            return(False)
        
        try: # find start of html section
            htmlStart = self.data.find("<div class")
        except: # errors if not found
            print("could not find html section in file")
            return(False)
        
        try: # find start of javascript section
            jsStart = self.data.index("<script>")
            dataJs = self.data[htmlStart:jsStart] + "\n" + self.js + "\n</script>\n</html>"
        except: # create new if not found
            jsStart = self.data.find("</html>")
            dataJs = self.data[htmlStart:jsStart - 1] + "\n<script>\n" + self.js + "\n</script>" 

        dataCss = self.data[:cssEnd] + '\n' + dataCss + '\n'
        dataHtml = self.data[cssEnd:htmlStart] + '\n' + dataHtml + '\n'

        self.data = dataCss + dataHtml + dataJs
        try: # replace title
            titleStart = self.data.index('<title>')
            titleEnd = self.data.index('</title>')
            self.data = self.data[:titleStart] + f"<title>{self.newName}</title>\n" + self.data[titleEnd+8:]
            # 8 is length of </title> (so that it does not end up doubled up
        except: # add title if not found
            titleStart = self.data.find("</head>")
            self.data = self.data[:titleStart] + f"<title>{self.newName}</title>\n" + self.data[titleStart:] 
        print("document created successfully")
        try:
            with open(f'{self.newDir }/{self.newName}.html','w') as File:
                File.write(self.data)
            #command = "explorer 'file:///" + Destination + "'"
            print(f"File successfully saved to {self.newDir}")
            return(self.newDir)
        except Exception as ex:
            print("Save Failed")
            return(ex)



