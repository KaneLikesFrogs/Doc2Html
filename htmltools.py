
import webbrowser
'''
Filepath = '/put/path/here'
File = open(Filepath)
Data = str(File.read())
Data = Data.replace(u'\xa0',u'&#160;')
'''
#can uncomment above code and call the create doc function with appropiate parameters to skip need for using gui

def Get_Header(Data,HeaderStart,HeaderEnd,TitlePrefix="",TitleSuffix=""): #used for finding particular types of headers inside header bracketing

    Found = True
    Index = 0
    EndIndex = 0
    IndexList = []
    EndIndexList = []
    TidyIndexList = []
    IDList = []
    NameList = []
    
    while Found == True:
        Index = Data.find(HeaderStart,Index + 1)
        EndIndex = Data.find(HeaderEnd,Index)
        if Index == -1:
            Found = False
        else:
            IndexList.append(Index)
            EndIndexList.append(EndIndex)

    if TitlePrefix == "" or TitleSuffix == "": 

        for x in range(len(IndexList)):
            IDStart = IndexList[x]
            IDEnd = EndIndexList[x]
            IDList.append(Data[IDStart:IDEnd])
            TidyIndexList.append(IndexList[x])
            Name = Data[IDStart + len(HeaderStart):IDEnd]
            UndesiredChars = ['</a>','<', '>', '"'] 
            for i in UndesiredChars:
                Name = Name.replace(i, '')
            Name = Name.replace('\n',' ')
            NameList.append(Name)
        
        return(IDList,TidyIndexList,NameList)

    for x in range(len(IndexList)): #creates a list of titles found within bounds of header markers
        IDStart = Data.find(TitlePrefix,IndexList[x],EndIndexList[x])
        IDEnd = Data.find(TitleSuffix,IDStart,EndIndexList[x])
        if IDStart == -1 or IDEnd == -1:
            continue
        else:
            IDList.append(Data[IDStart:IDEnd-1])
            TidyIndexList.append(IndexList[x]) #Want to essentially filter to elements were there is something present
            NameEnd = EndIndexList[x]
            NameStart = Data.rindex(r'">',IndexList[x],NameEnd) 
            Name = Data[NameStart:NameEnd] #As name is at end of header but otherwise inconsistent can isolate it with this
            UndesiredChars = ['</a>','<', '>', '"'] 
            for i in UndesiredChars:
                Name = Name.replace(i, '')
            Name = Name.replace('\n',' ')
            NameList.append(Name)
        
    TidyIndexList.append(len(Data))

    return(IDList,TidyIndexList,NameList)

def Add_Tags(Data,Header,Tag="qq"): #This will add tags if a document does not have them so that the nav menus have a reference to go to
    #try and use a tag that is unique for example qq never appears ordinairily so is used by default
    IDs, Indexes, Names = Get_Header(Data,f"<{Header}>",f"</{Header}>")
    TagList = []
    Names = Names[1:] #first eleemnt may be title or something, unsure of doing things this way
    Indexes = Indexes[1:]
    for x in Names:
        Name = f"{Tag}_{x.replace(' ','_')}"
        TagList.append(Name)
    for x in range(len(Indexes)):
        #print(f'<a name="{TagList[x]}"></a>)
        Name = f'<a name="{TagList[x]}"></a>'
        #print(Name)
        NameLen = len(Name)
        Index = Indexes[x]
        #print(Data[Index:Index+len(TagList[x])+1])
        Data = Data[:Index+4] + Name + Data[Index+4:]
        #print(Data[Index:Index + NameLen + len(TagList[x]) + 6])
        Indexes = [y+NameLen for y in Indexes]
        
    return(Data)
    
def Create_HTML_Contents(Data,ParentHeader = "h2",ChildHeader = "h3",Prefix="",Suffix="",LogoLocation = "",LogoSize = 340,LogoLink = ""): #Creates sidenav menu in HTML

    ParentIDs , ParentIndexes, ParentNames = Get_Header(Data,f"<{ParentHeader}>",f"</{ParentHeader}>",Prefix,Suffix)
    ChildIDs, ChildIndexes, ChildNames = Get_Header(Data,f"<{ChildHeader}>",f"</{ChildHeader}>",Prefix,Suffix)
    Output= [('<div class="sidenav">')]
    if LogoLocation == "":
        pass
    else:
        Output.append('\t<a href="'+ LogoLink + '" target="_blank">')
        Output.append(f'\t<img src="{LogoLink}" width="'+ str(LogoSize) + '">')
        Output.append('\t</a>')
        Output.append('<p><br></p>')
    for x in range(len(ParentIDs)):
        if ParentIDs[x] != "":
            children = 0
            for y in range(len(ChildIndexes)):
                if ChildIndexes[y] > ParentIndexes[x]:
                    if ChildIndexes[y] < ParentIndexes[x+1]:
                        children += 1
            if children < 2:
                #print(x)
                Output.append("\t" + '<a href="#' + ParentIDs[x] + '">' + ParentNames[x] + '</a>')
                pass
            else:
                Output.append("\t" + '<button class="dropdown-btn">' + str(ParentNames[x]) + '</button>')
                Output.append("\t \t" + '<div class="dropdown-container">')
                Output.append("\t \t" + '<a href="#' + ParentIDs[x] +  '">' + ParentNames[x] + '</a>')
                for y in range(len(ChildIndexes)):
                    if ChildIndexes[y] > ParentIndexes[x]:
                        if ChildIndexes[y] < ParentIndexes[x+1]:
                            Output.append("\t \t" + '<a href="#' + ChildIDs[y] + '">' + ChildNames[y] + '</a>')
                Output.append("\t \t" + '</div>')
    Output.append("\t<p><br></p>")
    Output.append("\t<p><br></p>") # adds 2 page breaks to help avoid bottom element disappearing when too many elements present
    Output.append("</div>")

    return(Output)

def Create_HTML_Index(Data,ParentHeader = "h2",ChildHeader = "h3",Prefix="",Suffix=""): #Creates searchbar items in HTML

    ParentIDs , ParentIndexes, ParentNames = Get_Header(Data,f"<{ParentHeader}>",f"</{ParentHeader}>",Prefix,Suffix)
    ChildIDs, ChildIndexes, ChildNames = Get_Header(Data,f"<{ChildHeader}>",f"</{ChildHeader}>",Prefix,Suffix)
    IDs = ParentIDs + ChildIDs
    Indexes = ParentIndexes + ChildIndexes
    Names = ParentNames + ChildNames
    ListItems = []
    Output = ['<div class = "topnav">']
    Output.append('\t<div class = "SearchField">')
    Output.append('\t\t<input type="text" id = "SearchBox" onkeyup="SearchFunc()" placeholder="Search...">')
    Output.append('\t\t<div class = "SearchResults">')
    Output.append('\t\t\t<ul id = "IndexItems">')
    for x in range(len(IDs)): 
        ListItems.append('\t\t\t\t<li><a href="#' + IDs[x] + '">' + Names[x] + '</a></li>')
    ListItems.sort()
    for x in ListItems:
        Output.append(x)
    Output.append('\t\t\t</ul>')
    Output.append('\t\t</div>')
    Output.append('\t</div>')
    Output.append("</div>")

    return(Output)

def Create_CSS_Contents(HighlightColour = "#1ED3B0",SidenavSize = 340): 
    Output = ['/*CSS for contents, paste into style section of html and change as desired*/']
    Output.append(".sidenav {")
    Output.append("\theight: 100%;")
    Output.append('\twidth: ' + str(SidenavSize) + 'px;')
    Output.append('\tposition: fixed;')
    Output.append("\tz-index: 1;")
    Output.append("\ttop: 0;")
    Output.append("\tleft: 0;")
    Output.append("\tbackground-color: #f1f1f1;")
    Output.append("\toverflow-x: hidden;")
    Output.append("\tpadding: 20px;")
    Output.append("\tfont-family: Arial, sans-serif;")
    Output.append("}")
    Output.append("\n")
    Output.append('.sidenav a, .dropdown-btn {')
    Output.append('\tpadding: 6px 8px 6px;')
    Output.append('\ttext-decoration: none;')
    Output.append('\tfont-size: 18px;')
    Output.append('\tcolor: #424242;')
    Output.append('\tdisplay: block;')
    Output.append('\tborder: none;')
    Output.append('\tbackground: none;')
    Output.append('\twidth: 100%;')
    Output.append('\ttext-align: left;')
    Output.append('\tcursor: pointer;')
    Output.append('\toutline: none;')
    Output.append("\tfont-family: Arial, sans-serif;")
    Output.append('}')
    Output.append("\n")
    Output.append('.sidenav a:hover, .dropdown-btn:hover {')
    Output.append('\tcolor: #f1f1f1;')
    Output.append('\tbackground-color: ' + HighlightColour +";")
    Output.append('}')
    Output.append("\n")
    Output.append(".active {")
    Output.append("\tbackground-color: " + HighlightColour + ";")
    Output.append("\tcolor: white;")
    Output.append("}")
    Output.append("\n")
    Output.append(".dropdown-container {")
    Output.append("\tdisplay: none;")
    Output.append("\tpadding-left: 20px;")
    Output.append("\tpadding-right: 20px;")
    Output.append('\twidth:' + str(SidenavSize - 40) + 'px;')
    Output.append("\tbackground-color: #e1e1e1;")
    Output.append("\tfont-family: Arial, sans-serif;")
    Output.append("}")
    Output.append("\n")
    Output.append("@media screen and (max-height: 450px) {")
    Output.append("\t.sidenav {padding-top: 0px;}")
    Output.append("\t.sidenav a {font-size: 18px;}")
    Output.append("}")
    Output.append("\n")

    return(Output)

def Create_CSS_Index(HighlightColour = "#1ED3B0",TopnavHeight = 80):
    if TopnavHeight<40:
        return(["/*No CSS Included for topnav*/"])
    Output = ['/*CSS for topnav*/']
    Output.append('.topnav {')
    Output.append('\tposition: fixed;')
    Output.append('\ttop: 0;')
    Output.append('\theight: ' + str(TopnavHeight) +'px;')
    Output.append('\twidth: 105%;')
    Output.append('\tbackground-color: #f1f1f1;')
    Output.append('\tborder-bottom: 20px solid '+ HighlightColour +';')
    Output.append('\toverflow: visible')
    Output.append('}')
    Output.append('#SearchBox {')
    Output.append('\tfloat: right;')
    Output.append('\tmargin-top: ' + str(TopnavHeight/4) + 'px;')
    Output.append('\tmargin-right: 150px;')
    Output.append('\theight: 40px;')
    Output.append('\twidth: 200px;')
    Output.append('\tpadding: 11px;')
    Output.append('\tz-index: 2;')
    Output.append('}')
    Output.append('.SearchResults {')
    Output.append('\tdisplay: none;')
    Output.append('\tfloat: right;')
    Output.append('\tmargin-top: ' + str(TopnavHeight/4 + 40) + 'px;')
    Output.append('\tmargin-right: -200px;')
    Output.append('\tmargin-left: 0px;')
    Output.append('\tmax-width: 200px;')
    Output.append('\tmin-width: 200px;')
    Output.append('\tz-index: 1;')
    Output.append('\tbackground-color: #e1e1e1;')
    Output.append('\toverflow-y: scroll;')
    Output.append('\theight: auto;')
    Output.append('\tmax-height: 375px;')
    Output.append('\tscrollbar-gutter: stable;')
    Output.append('\tmargin-left: 0px;')
    Output.append('}')
    Output.append('.SearchResults a {')
    Output.append('\tcolor: black;')
    Output.append('\ttext-decoration: none;')
    Output.append('\tdisplay: block;')
    Output.append('\tborder-top: solid #d1d1d1 2px;')
    Output.append('\tpadding-top: 6px;')
    Output.append('\tpadding-bottom: 6px;')
    Output.append('}')
    Output.append('.SearchResults a:hover {')
    Output.append( '\tbackground-color: ' + HighlightColour + ';')
    Output.append('\tcolor: white')
    Output.append('}')
    Output.append('#SearchBox:focus-visible + .SearchResults{')
    Output.append('display: block; ')
    Output.append('}')
    Output.append('.SearchResults:hover{')
    Output.append('\tdisplay: block;')
    Output.append('}')
    Output.append('#IndexItems {')
    Output.append('\tlist-style-type: none;')
    Output.append('\tpadding: 5px;')
    Output.append('\tjustify-content: center;')
    Output.append('\tfont-size: 16px;')
    Output.append('\tfont-family: Arial, sans-serif ;')
    Output.append('}')
    Output.append('html {')
    Output.append('\tscroll-padding-top:' + str(TopnavHeight + 20) + 'px;')
    Output.append('\tscrollbar-gutter: stable;')
    Output.append('}')

    return(Output)

def Create_JS():
    Output = ['//START OF DROPDOWN SETUP']
    Output.append('var dropdown = document.getElementsByClassName("dropdown-btn"); ')
    Output.append('var i;')
    Output.append('for (i = 0; i < dropdown.length; i++) {')
    Output.append('\tdropdown[i].addEventListener("click", function() {')
    Output.append('\t\tthis.classList.toggle("active");')
    Output.append('\t\tvar dropdownContent = this.nextElementSibling;')
    Output.append('\t\tif (dropdownContent.style.display === "block") {')
    Output.append('\t\t\tdropdownContent.style.display = "none";')
    Output.append('\t\t} else {')
    Output.append('\t\t\tdropdownContent.style.display = "block";')
    Output.append('\t\t}')
    Output.append('\t});')
    Output.append('}')
    Output.append('//END OF DROPDOWN SETUP')
    Output.append('\n \n')
    Output.append('//START OF INDEX SEARCH')
    Output.append('var ul = document.getElementById("IndexItems");')
    Output.append('var li = ul.getElementsByTagName("li");')
    Output.append('\n')
    Output.append('for (i = 0; i < li.length; i++) {')
    Output.append('\tli[i].style.display = "none"')
    Output.append('\t} //hides all elements on startup')
    Output.append('\n')
    Output.append('function SearchFunc() {')
    Output.append('\t//this function is called by the search box when hte input is changed  ')
    Output.append('\tvar input = document.getElementById("SearchBox");')
    Output.append('\tvar filter = input.value.toUpperCase(); /*makes it so search is not case sensitive*/')
    Output.append('\tvar ul = document.getElementById("IndexItems");')
    Output.append('\tvar li = ul.getElementsByTagName("li");')
    Output.append('\tvar i;')
    Output.append('\t//sets up variables')
    Output.append('\tif (filter == "") {')
    Output.append('\t\tfor (i = 0; i < li.length; i++) {')
    Output.append('\t\t\tli[i].style.display = "none";')
    Output.append('\t\t}')
    Output.append('\t}')
    Output.append('\telse{')
    Output.append('\t\tfor (i = 0; i < li.length; i++) {')
    Output.append('\t\t\ta = li[i].getElementsByTagName("a")[0];')
    Output.append('\t\t\tif (a.innerHTML.toUpperCase().indexOf(filter) > -1) {')
    Output.append('\t\t\t\tli[i].style.display = "";')
    Output.append('\t\t\t} ')
    Output.append('else {')
    Output.append('\t\t\t\tli[i].style.display = "none";')
    Output.append('\t\t\t}')
    Output.append('\t\t}')
    Output.append('\t}')
    Output.append('\t}')
    Output.append('//END OF INDEX SETUP ')

    return(Output)

def Save_File(HTMLData,Destination):
    try:
        with open(Destination,'w') as File:
            File.write(HTMLData)
        #command = "explorer 'file:///" + Destination + "'"
        print(f"File successfully saved to {Destination}")
        return(True)
    except:
        print("Save Failed")
        return(False)

def Create_Doc(Data,Title,SaveDestination,ParentHeader = "h2",ChildHeader = "h3",HighlightColour="#1ED3B0",SidenavWidth=340,TopnavHeight=80,LogoLocation = ""):
    
    Data = Add_Tags(Data,ParentHeader)
    Data = Add_Tags(Data,ChildHeader)
    ContentsCSS = Create_CSS_Contents(HighlightColour,SidenavWidth)
    IndexCSS = Create_CSS_Index(HighlightColour,TopnavHeight)
    ContentsHTML = Create_HTML_Contents(Data,Prefix="qq",Suffix=">",ParentHeader=ParentHeader,ChildHeader=ChildHeader,LogoLocation = LogoLocation,LogoSize = SidenavWidth)
    IndexHTML = Create_HTML_Index(Data,ParentHeader=ParentHeader,ChildHeader=ChildHeader,Prefix="qq",Suffix=">")

    JS = Create_JS()
    JS = "\n".join(JS)

    CSS = ContentsCSS + IndexCSS
    CSS = "\n".join(CSS)
    HTML = IndexHTML+ ContentsHTML 
    HTML = "\n".join(HTML)
    
    CSSEnd = Data.find("</style>")
    DataCSS = Data[:CSSEnd] + "\n" + CSS +"\n"
    
    Found = True
    Start = 0
    End = 0
    InsertStr = ' style="margin-left:' + str(SidenavWidth+30) + 'px; border-left: 20px solid ' + HighlightColour + '; padding-left: 20px"' 
    while Found:
        try:
            Start = Data.index("<div class=",End) #May be better to replace ALL finds with index and try/except
            End = Data.index(">",Start)
            Data = Data[:End] + InsertStr + Data[End:]
        except:
            Found = False

    HTMLStart = Data.index("<div class")

    DataHTML = Data[CSSEnd:HTMLStart] + "\n" + HTML + "\n"

    try: 
        JSStart = Data.index("<script>")
        DataJS = Data[HTMLStart:JSStart] + "\n" + JS + "\n</script>\n</html>"
    except:
        JSStart = Data.find("</html>")
        DataJS = Data[HTMLStart:JSStart - 1] + "\n<script>\n" + JS + "\n</script>" 

    Data = DataCSS + DataHTML + DataJS 
    try:
        TitleStart = Data.find("</head>")
        Data = Data[:TitleStart] + f"<title>{Title}</title>\n" + Data[TitleStart:] 

    except:
        print("no head tag")
        pass
    
    if Save_File(Data,SaveDestination): #This returns true or false to top level whilst still creating document
        return(True)
    else:
        return(False)


