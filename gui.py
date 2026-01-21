import tkinter as tk
from tkinter import ttk,filedialog,colorchooser,messagebox,font
from PIL import Image,ImageTk
import htmltools


'''
- Changed case method:
    - camelCase for variables
    - snake_case for functions
    - PascalCase for classes/objects (including buttons/objects created by tkinter)
'''

def find_file():
    filePath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a filtered file to convert",
                                          filetypes=(("Filtered HTML File","*.htm*"),
                                                     ("All Files","*.*")))
    currentPath = FileEntry.get()
    FileEntry.delete(0,len(currentPath))
    FileEntry.insert(0,filePath)

def validate_file():
    try:
        filePath = FileEntry.get()
        filePath.index("htm")
        FileEntry.config(highlightthickness = 0)
        return True
    except:
        FileEntry.config(highlightbackground = "red",highlightthickness = 1)
        return False

def find_logo():
    path = FileEntry.get()
    try:
        initdir = path[:path.rindex("/")]
    except:
        initdir = 'C:/'
    logoPath = filedialog.askopenfilename(initialdir = initdir,
                                    title = "Select an image",
                                    filetypes=(("ImageFile",("*.jpg","*.bmp","*.png")),
                                    ("All Files","*.*")))
    currentPath = LogoPath.get()
    LogoPath.delete(0,len(currentPath))
    LogoPath.insert(0,logoPath)
    return True

def load_logo():
    logoPath = LogoPath.get()
    try:
        logo = Image.open(logoPath)
    except:
        Demo.itemconfig(DemoLogoRect,outline = "")
        return False
    width, height = logo.size
    ratio = height/width
    width = int(SidenavSlider.get())
    height = int(width*ratio)
    Demo.coords(DemoLogoRect,2,2,width,height)
    Demo.itemconfig(DemoLogoRect,outline = "black")
    return True

def choose_colour():
    colourCode = colorchooser.askcolor(title = "Choose Colour for accenting and higlighting")
    try:
        ColourButton.config(background = str(colourCode[1]))
        currentColour = ColourEntry.get()
        ColourEntry.delete(0,len(currentColour))
        ColourEntry.insert(0,str(colourCode[1]))
        Demo.itemconfig(DemoWindow,outline = colourCode[1])
        return True
    except:
        return False

def type_colour():
    try:
        ColourButton.config(background=ColourEntry.get())
        Demo.itemconfig(DemoWindow,outline = ColourEntry.get())
        ColourEntry.config(highlightthickness = 0)
        return True
    except:
        currentColour = ColourEntry.get()
        ColourEntry.delete(0,len(currentColour))
        ColourEntry.insert(0,"")
        ColourEntry.config(highlightbackground = "red",highlightthickness = 1)
        return False

def update_canvas(pos=0):
    VerticalLinePos = float(SidenavSlider.get())
    HorizLinePos = float(TopnavSlider.get())
    
    Entry = str(TopnavEntry.get())
    TopnavEntry.delete(0,len(Entry))
    TopnavEntry.insert(0,int(HorizLinePos*4))

    Entry = SidenavEntry.get()
    SidenavEntry.delete(0,len(Entry))
    SidenavEntry.insert(0,int(VerticalLinePos*4))


    ColourHex = ColourEntry.get()
    Demo.itemconfig(DemoWindow,outline = ColourHex)
    Demo.coords(DemoWindow,490,280,VerticalLinePos+5,HorizLinePos+5)
    Demo.coords(DemoSearch,475,HorizLinePos/4,425,HorizLinePos/4 + 10)
    load_logo()

def update_canvas_from_textbox():
    try:
        topnavHeight = int(TopnavEntry.get())
        TopnavEntry.config(highlightthickness=0)
    except:
        TopnavEntry.config(highlightthickness=1,highlightbackground="red")
        return False
    try:
        sidenavWidth =int(SidenavEntry.get())
        SidenavEntry.config(highlightthickness=0)
    except:
        SidenavEntry.config(highlightbackground="red",highlightthickness=1)
        return False
    horizLinePos = topnavHeight/4
    TopnavSlider.set(horizLinePos)
    verticalLinePos = sidenavWidth/4
    SidenavSlider.set(verticalLinePos)
    Demo.coords(DemoWindow,490,280,verticalLinePos+5,horizLinePos+5)
    Demo.coords(DemoSearch,475,horizLinePos/4,425,horizLinePos/4 + 10)
    load_logo()
    return True

def name_check():
    label = NewNameEntry.get()
    invalidChars = ['"','*','?','<','>',':','|','/','\\']
    for x in invalidChars:
        index = label.find(x)
        if index > 0:
            NewNameEntry.config(highlightbackground = "red",highlightthickness = 1)
            return False
        else:
            NewNameEntry.config(highlightthickness = 0)
            continue
    return True

def font_check():
    try:
        fontSize = int(FontSizeEntry.get())
        FontSizeEntry.config(highlightthickness=0)
        return True
    except:
        FontSizeEntry.config(highlightthickness=1,highlightbackground="red")
        return False

def create_file():
    if validate_file():
        path = FileEntry.get()
    else:
        return False    
    if update_canvas_from_textbox: 
        topNav = int(TopnavEntry.get())
        sideNav = int(SidenavEntry.get())
    else:
        print("Failed size check")
        return False
    if type_colour:
        colour = ColourEntry.get()
    else:
        print("Failed colour check")
        return False
    if load_logo():
        logoPath = LogoPath.get()
        print("Logo valid")
    else:
        logoPath = ""
    if name_check():
        destination = NewNameEntry.get()
    else:
        print("Failed name check")
        return False
    
    name = destination
    output = htmltools.Manual(original=path,newName=name)
    output.logoPath = logoPath
    output.sideNavWidth = sideNav
    output.topNavHeight = topNav
    output.highlight = colour
    try:
        output.navFontSize = FontSizeEntry.get()
    except:
        pass
    try:
        output.nameBlacklist = NameBlacklistEntry.get().split(',')
        output.nameCutoff = NameCutoffEntry.get().split(',')
    except:
        pass
    try:
        output.prettify_html()
        dir = output.newDir
        messagebox.showinfo(message=f"File successfully created and saved to {dir}")
    except:
        return False
    
# ~~~~~~~~~~~ Variables + Defaults ~~~~~~~~~~~

filePath = ""
topnavHeight = 80
horizLinePos = topnavHeight/4
sidenavWidth = 340
verticalLinePos = sidenavWidth/4
colourHex = "#604D81"
fontSize = 16
defBg = '#e1e1e1'

root = tk.Tk()
root.title("HTML Doc to HTML Help File")
minWidth = 750
minHeight = 950
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.minsize(minWidth, minHeight)
root.geometry(f"{minWidth}x{minHeight}+{round(screenWidth/2 - minWidth/2)}+{round(screenHeight/2 - minHeight/2)}") 
root.configure(bg=defBg)

# ~~~~~~~~~~~ Control Grids ~~~~~~~~~~~

FileControl = tk.Frame(root,width = 200, height = 10, background = defBg)
FileControl.grid(row = 0, column = 0,pady=10,padx=30,sticky = "w")

HTMLControls = tk.Frame(root,width = 800, height = 200,background = defBg)
HTMLControls.grid(row = 1, column = 0,pady=10,padx=30,sticky = "n")

SubmitControls = tk.Frame(root,width=400,height = 30,background = defBg)
SubmitControls.grid(row = 4,column = 0,pady=10,padx=30,sticky = "n")

# ~~~~~~~~~~~ Control Definitions ~~~~~~~~~~~

FileEntry = tk.Entry(FileControl,width=100,textvariable=filePath,validate = "focusout",validatecommand=validate_file)
FileButton = tk.Button(FileControl,text = "Search",width = 5, height = 1, command = find_file)
FileLabel = tk.Label(FileControl,text = "File Selected:",background = defBg)
SubmitFile = tk.Button(FileControl, text = "Submit",width = 5, height = 1, command = validate_file)
# Accenting/Highlights
ColourButton = tk.Button(HTMLControls, height = 1, width = 2,background = colourHex,command = choose_colour)
ColourLabel = tk.Label(HTMLControls,text = "Colour (Highlights and Accents):",background = defBg)
ColourEntry = tk.Entry(HTMLControls,width = 12,validate = "focusout",validatecommand = type_colour,textvariable = colourHex)
# Topnav adjustments
TopnavEntry = tk.Entry(HTMLControls,width = 5, textvariable = topnavHeight,validate = "focusout",validatecommand = update_canvas_from_textbox)
TopnavLabel = tk.Label(HTMLControls,text = "Topnav Height (px) \n(Values less than 40px will remove the top bar)",background = defBg)
# Sidenav adjustments 
SidenavEntry = tk.Entry(HTMLControls,width = 5,textvariable = sidenavWidth,validate = "focusout",validatecommand = update_canvas_from_textbox)
SidenavLabel = tk.Label(HTMLControls,text = "Sidenav Width (px)",background = defBg)
# Nav text size adjustments
FontSizeEntry = tk.Entry(HTMLControls,width = 5,textvariable = fontSize,validate = "focusout",validatecommand = font_check)
FontSizeLabel = tk.Label(HTMLControls,text="Font Size (pt) :",background=defBg)
# Logo path changes
LogoPath = tk.Entry(HTMLControls,width = 50)
LogoLabel = tk.Label(HTMLControls,text="Path to logo (optional):",background = defBg)
LogoButton = tk.Button(HTMLControls,text = "Search",width = 5, height = 1 ,command = find_logo)
Submit = tk.Button(HTMLControls,width = 5, text = "Submit",command=load_logo)
# Description of cutoff/blacklist elements
BlacklistAndCutoffLabel = tk.Label(HTMLControls,
                                   text = 
                                   '''Can adjust the bookmark and menu item names with options below\nSeperate items with commas (,)''' ,
                                   background = defBg)
# Name blacklist
NameBlacklistEntry = tk.Entry(HTMLControls,validate = 'focusout')
NameBlacklistLabel = tk.Label(HTMLControls,text = "Characters/Strings to remove",background = defBg)
# Name cutoff
NameCutoffEntry = tk.Entry(HTMLControls,validate = 'focusout')
NameCutoffLabel = tk.Label(HTMLControls,text = "Characters/Strings to use as cutoff\n(Uses everything AFTER cutoff)",background = defBg)
# Create file buttons
NewNameLabel = tk.Label(SubmitControls,text = "New Name:",background = defBg)
NewNameEntry = tk.Entry(SubmitControls,width = 50,validate = 'focusout',validatecommand=name_check)
NewNameConfirm = tk.Button(SubmitControls,width = 12, text = "Create HTML\nFile",command=create_file)

# ~~~~~~~~~~~ Control Positioning ~~~~~~~~~~~

FileLabel.grid(row = 0,column = 0,sticky = "w",padx = 5,pady = 5)
FileEntry.grid(row = 1,column = 0,padx = 5,pady = 0)
FileButton.grid(row = 1,column = 1,padx = 5,pady = 5)
SubmitFile.grid(row = 2,column= 0,padx = 5, pady = 5)

ColourButton.grid(row = 0,column = 0,padx = 5,pady = 5)
ColourLabel.grid(row = 0,column = 1,padx = 5,pady = 5)
ColourEntry.grid(row = 0,column = 2, padx = 5, pady = 5)

TopnavEntry.grid(row = 1,column = 0, padx = 5, pady = 5)
TopnavLabel.grid(row = 1, column = 1, padx = 5, pady = 5)

SidenavEntry.grid(row = 2,column = 0, padx = 5, pady = 5)
SidenavLabel.grid(row = 2, column = 1, padx = 5, pady = 5)

FontSizeEntry.grid(row = 3,column = 0, padx = 5, pady = 5)
FontSizeLabel.grid(row = 3,column = 1, padx = 5, pady = 5)

BlacklistAndCutoffLabel.grid(row=4,column = 0, padx = 5, pady = 5,columnspan = 3,sticky = "n")

NameBlacklistEntry.grid(row = 5,column = 0, padx = 5, pady =5)
NameBlacklistLabel.grid(row = 5,column = 1, padx = 5, pady = 5,columnspan = 2,sticky = "w")

NameCutoffEntry.grid(row = 6,column = 0, padx = 5, pady = 5)
NameCutoffLabel.grid(row = 6,column = 1, padx = 5, pady = 5,columnspan = 2,sticky = "w")

LogoLabel.grid(row = 7, column = 0, padx = 5 ,pady = 0,columnspan = 2,sticky = "w")
LogoPath.grid(row = 8, column = 0, pady = 5, padx = 5,columnspan = 3,sticky = "w")
LogoButton.grid(row = 8,column = 2, pady = 5, padx = 5)
Submit.grid(row = 9,column = 1, padx = 5, pady = 5)

NewNameLabel.grid(row = 0,column =0, padx = 5, pady = 5,sticky = "w")
NewNameEntry.grid(row = 1,column =0, padx = 5, pady = 5)
NewNameConfirm.grid(row = 2,column=0, padx = 5, pady = 5)

# ~~~~~~~~~~~ Setup Demo Frame ~~~~~~~~~~~

# Applying defaults
ColourEntry.insert(0,colourHex)
TopnavEntry.insert(0,topnavHeight)
SidenavEntry.insert(0,sidenavWidth)
FontSizeEntry.insert(0,fontSize)
# Example/Demo Frame
ExampleFrame = tk.Frame (root,width = 490, height = 280, background = 'white',highlightbackground = 'black',highlightthickness = 2)
ExampleLabel = tk.Label(root,text = '^This is an example window at 1:4 scale of a 1920x1080 display',background=defBg)

ExampleFrame.grid(row = 2, column = 0,padx=30,sticky = "n")
ExampleLabel.grid(row = 3, column = 0,padx=30,sticky = "n")

SidenavSlider = tk.Scale(ExampleFrame, 
                        from_ = 0,
                        to_ = 480,
                        orient = "horizontal",
                        cursor = "arrow",
                        width=10,
                        length=490,
                        sliderlength=10,
                        showvalue = 0,
                        resolution=0.25,
                        variable = verticalLinePos,
                        command = update_canvas)
TopnavSlider = tk.Scale(ExampleFrame,
                        from_ = 0, 
                        to_ = 270, 
                        orient = "vertical",
                        cursor = "arrow",
                        width = 10,
                        length = 280,
                        sliderlength = 10,
                        showvalue = 0,
                        resolution=0.25,
                        variable = horizLinePos,
                        command = update_canvas)

TopnavSlider.set(20)
SidenavSlider.set(85)

Demo = tk.Canvas(ExampleFrame,width = 480, height = 270,background='#f1f1f1')

SidenavSlider.grid(row = 0,column = 1,sticky = "w")
TopnavSlider.grid(row = 1,column = 0,sticky ="n")
Demo.grid(row = 1,column = 1,sticky="nw")

DemoWindow = Demo.create_rectangle(490,
                                   280,
                                   verticalLinePos+5,
                                   horizLinePos+5,
                                   outline = colourHex, 
                                   fill = 'white',
                                   width = 5)
DemoSearch = Demo.create_rectangle(480-5,
                                   5,
                                   480-55,
                                   15,
                                   fill = "white")
DemoLogoRect = Demo.create_rectangle(2,
                                     2,
                                     90,
                                     20,
                                     fill = '',
                                     outline = '')
root.mainloop()