import tkinter as tk
from tkinter import ttk,filedialog,colorchooser,messagebox
from PIL import Image,ImageTk

import htmltools

def Find_File():
    FilePath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a filtered file to convert",
                                          filetypes=(("Filtered HTML File","*.htm*"),
                                                     ("All Files","*.*")))
    #print(FilePath)
    CurrentPath = FileEntry.get()
    FileEntry.delete(0,len(CurrentPath))
    FileEntry.insert(0,FilePath)

def Validate_File():
    try:
        FilePath = FileEntry.get()
        FilePath.index("htm")
        RelativeLogoPath.config(state = "normal")
        RelativeLogoButton.config(state = "normal")
        FileEntry.config(highlightthickness = 0)
        return True
    except:
        FileEntry.config(highlightbackground = "red",highlightthickness = 1)
        RelativeLogoPath.config(state = "disabled")
        RelativeLogoButton.config(state = "disabled")
        return False

def Find_Logo():
    try:
        Path = FileEntry.get()
        initdir = Path[:Path.rindex("/")]
    except:
        FileEntry.config(highlightbackground = "red",highlightthickness = 1)
        return False
    LogoPath = filedialog.askopenfilename(initialdir = initdir,
                                    title = "Select an image",
                                    filetypes=(("ImageFile",("*.jpg","*.bmp","*.png")),
                                    ("All Files","*.*")))
    RelativeLogoPath.delete(0,len(RelativeLogoPath.get()))
    RelativeLogoPath.insert(0,LogoPath[len(initdir)+1:])
    return True

def Load_Logo():
    Path = FileEntry.get()
    try:
        LogoPath = Path[:Path.rindex("/")] + "/" + RelativeLogoPath.get()
    except:
        return False
    #print(LogoPath)
    try:
        Logo = Image.open(LogoPath)
        RelativeLogoPath.config(highlightthickness = 0)
        #print("image opened")
    except:
        #print("failed")
        RelativeLogoPath.config(highlightbackground = "red",highlightthickness = 1)
        Demo.itemconfig(DemoLogoRect,outline = "")
        return False
    width, height = Logo.size
    ratio = height/width
    width = int(SidenavSlider.get())
    height = int(width*ratio)
    Demo.coords(DemoLogoRect,2,2,width,height)
    Demo.itemconfig(DemoLogoRect,outline = "black")
    return True

def Choose_Colour():
    ColourCode = colorchooser.askcolor(title = "Choose Colour for accenting and higlighting")
    try:
        ColourButton.config(background = str(ColourCode[1]))
        CurrentColour = ColourEntry.get()
        ColourEntry.delete(0,len(CurrentColour))
        ColourEntry.insert(0,str(ColourCode[1]))
        Demo.itemconfig(DemoWindow,outline = ColourCode[1])
        return True
    except:
        return False

def Type_Colour():
    try:
        ColourButton.config(background=ColourEntry.get())
        Demo.itemconfig(DemoWindow,outline = ColourEntry.get())
        ColourEntry.config(highlightthickness = 0)
        return True
    except:
        CurrentColour = ColourEntry.get()
        ColourEntry.delete(0,len(CurrentColour))
        ColourEntry.insert(0,"")
        ColourEntry.config(highlightbackground = "red",highlightthickness = 1)
        return False

def Update_Canvas(Pos=0):
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
    Load_Logo()

def Update_Canvas_From_Textbox():
    try:
        TopnavHeight = int(TopnavEntry.get())
        TopnavEntry.config(highlightthickness=0)
    except:
        TopnavEntry.config(highlightthickness=1,highlightbackground="red")
        return False
    try:
        SidenavWidth =int(SidenavEntry.get())
        SidenavEntry.config(highlightthickness=0)
    except:
        SidenavEntry.config(highlightbackground="red",highlightthickness=1)
        return False
    HorizLinePos = TopnavHeight/4
    TopnavSlider.set(HorizLinePos)
    VerticalLinePos = SidenavWidth/4
    SidenavSlider.set(VerticalLinePos)
    Demo.coords(DemoWindow,490,280,VerticalLinePos+5,HorizLinePos+5)
    Demo.coords(DemoSearch,475,HorizLinePos/4,425,HorizLinePos/4 + 10)
    Load_Logo()
    return True

def Name_Check():
    Label = NewNameEntry.get()
    InvalidChars = ['"','*','?','<','>',':','|','/','\\']
    for x in InvalidChars:
        index = Label.find(x)
        if index > 0:
            NewNameEntry.config(highlightbackground = "red",highlightthickness = 1)
            return False
        else:
            NewNameEntry.config(highlightthickness = 0)
            continue
    return True

def Create_File():
    if Validate_File():
        Path = FileEntry.get()
    else:
        return False    
    if Load_Logo():
        LogoPath = RelativeLogoPath.get()
        print("Logo valid")
    else:
        LogoPath = ""
        print("Logo not valid,skipping")
    if Update_Canvas_From_Textbox: 
        Topnav = int(TopnavEntry.get())
        Sidenav = int(SidenavEntry.get())
    else:
        print("Failed size check")
        return False
    if Type_Colour:
        Colour = ColourEntry.get()
    else:
        print("Failed colour check")
        return False
    if Name_Check():
        Destination = Path[:Path.rindex("/")] + "/" + NewNameEntry.get()
    else:
        print("Failed name check")
        return False
    try:
        Destination.rindex('.htm')
    except:
        Destination = Destination + '.htm'
    if Destination == "":
        Destination = FileEntry.get()
    File = open(Path)
    Name = NewNameEntry.get().rstrip(".htm")
    print(Name)
    print(Destination)
    Data = str(File.read())
    return htmltools.Create_Doc(Data,Name,Destination,"h2","h3",Colour,Sidenav,Topnav,LogoPath)
    

#Everything below this is the layout options 
root = tk.Tk()
root.title("Filtered HTML Doc to HTML Help File")
root.configure(background = "#f1f1f1")
MinWidth = 800
MinHeight = 850
ScreenWidth = root.winfo_screenwidth()
ScreenHeight = root.winfo_screenheight()
root.minsize(MinWidth, MinHeight)
root.geometry(f"{MinWidth}x{MinHeight}+{round(ScreenWidth/2 - MinWidth/2)}+{round(ScreenHeight/2 - MinHeight/2)}") 

FileControl = tk.Frame(root,width = 200, height = 10, background = '#e1e1e1')
FileControl.grid(row = 0, column = 0,pady=10,padx=30,sticky = "w")

FilePath = ""
TopnavHeight = 80
HorizLinePos = TopnavHeight/4
SidenavWidth = 340
VerticalLinePos = SidenavWidth/4

FileEntry = tk.Entry(FileControl,width=100,textvariable=FilePath,validate = "focusout",validatecommand=Validate_File)
FileButton = tk.Button(FileControl,text = "Search",width = 5, height = 1, command = Find_File)
FileLabel = tk.Label(FileControl,text = "File Selected:",background = '#e1e1e1')
SubmitFile = tk.Button(FileControl, text = "Submit",width = 5, height = 1, command = Validate_File)

FileLabel.grid(row = 0,column = 0,sticky = "w",padx = 5,pady = 5)
FileEntry.grid(row = 1,column = 0,padx = 5,pady = 0)
FileButton.grid(row = 1,column = 1,padx = 5,pady = 5)
SubmitFile.grid(row = 2,column= 0,padx = 5, pady = 5)

HTMLControls = tk.Frame(root,width = 800, height = 200,background = '#e1e1e1')
HTMLControls.grid(row = 1, column = 0,pady=10,padx=30,sticky = "n")

SubmitControls = tk.Frame(root,width=400,height = 30,background = '#e1e1e1')
SubmitControls.grid(row = 4,column = 0,pady=10,padx=30,sticky = "n")

ColourHex = "#1ed3b0"
#CHANGE COLOUR OF ACCENTING/HIGHLIGHTS
ColourButton = tk.Button(HTMLControls, height = 1, width = 2,background = '#1ED3B0',command = Choose_Colour)
ColourLabel = tk.Label(HTMLControls,text = "Colour (Highlights and Accents):",background = '#e1e1e1')
ColourEntry = tk.Entry(HTMLControls,width = 12,validate = "focusout",validatecommand = Type_Colour,textvariable = ColourHex)
#ADJUST SIZE OF TOPBAR/INDEX SEARCH
TopnavEntry = tk.Entry(HTMLControls,width = 5, textvariable = TopnavHeight,validate = "focusout",validatecommand = Update_Canvas_From_Textbox)
TopnavLabel = tk.Label(HTMLControls,text = "Topnav Height (px) \n(Values less than 40px will remove the top bar)",background = '#e1e1e1')
#ADJUST SIZE OF SIDEBAR/CONTENTS
SidenavEntry = tk.Entry(HTMLControls,width = 5,textvariable = SidenavWidth,validate = "focusout",validatecommand = Update_Canvas_From_Textbox)
SidenavLabel = tk.Label(HTMLControls,text = "Sidenav Width (px)",background = '#e1e1e1')
#CHANGE PATH TO LOGO
RelativeLogoPath = tk.Entry(HTMLControls,width = 50,state = "disabled")
RelativeLogoLabel = tk.Label(HTMLControls,text="Relative Path to logo (optional):",background = '#e1e1e1')
RelativeLogoButton = tk.Button(HTMLControls,text = "Search",width = 5, height = 1 ,command = Find_Logo,state = "disabled")
Submit = tk.Button(HTMLControls,width = 5, text = "Submit",command=Load_Logo)
#CREATE FILE
NewNameLabel = tk.Label(SubmitControls,text = "New File Name:",background = '#e1e1e1')
NewNameEntry = tk.Entry(SubmitControls,width = 50,validate = 'focusout',validatecommand=Name_Check)
NewNameConfirm = tk.Button(SubmitControls,width = 12, text = "Create HTML\nFile",command=Create_File)

#POSITIONING OF CONTROL ELEMENTS
ColourButton.grid(row = 0,column = 0,padx = 5,pady = 5)
ColourLabel.grid(row = 0,column = 1,padx = 5,pady = 5)
ColourEntry.grid(row = 0,column = 2, padx = 5, pady = 5)

TopnavEntry.grid(row = 1,column = 0, padx = 5, pady = 5)
TopnavLabel.grid(row = 1, column = 1, padx = 5, pady = 5)

SidenavEntry.grid(row = 2,column = 0, padx = 5, pady = 5)
SidenavLabel.grid(row = 2, column = 1, padx = 5, pady = 5)

RelativeLogoLabel.grid(row = 3, column = 0, padx = 5 ,pady = 0,columnspan = 2,sticky = "w")
RelativeLogoPath.grid(row = 4, column = 0, pady = 5, padx = 5,columnspan = 3,sticky = "w")
RelativeLogoButton.grid(row = 4,column = 2, pady = 5, padx = 5)

Submit.grid(row = 5,column = 1, padx = 5, pady = 5)

NewNameLabel.grid(row = 0,column =0, padx = 5, pady = 5,sticky = "w")
NewNameEntry.grid(row = 1,column =0, padx = 5, pady = 5)
NewNameConfirm.grid(row = 2,column=0, padx = 5, pady = 5)

#DEFAULT VALUES
ColourEntry.insert(0,'#1ED3B0')
TopnavEntry.insert(0,TopnavHeight)
SidenavEntry.insert(0,SidenavWidth)

#EXAMPLE FRAME
ExampleFrame = tk.Frame (root,width = 490, height = 280, background = 'white',highlightbackground = 'black',highlightthickness = 2)
ExampleLabel = tk.Label(root,text = '^This is an example window at 1:4 scale of a 1920x1080 display')

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
                        variable = VerticalLinePos,
                        command = Update_Canvas)
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
                        variable = HorizLinePos,
                        command = Update_Canvas)

TopnavSlider.set(20)
SidenavSlider.set(85)

Demo = tk.Canvas(ExampleFrame,width = 480, height = 270,background='#f1f1f1')

SidenavSlider.grid(row = 0,column = 1,sticky = "w")
TopnavSlider.grid(row = 1,column = 0,sticky ="n")
Demo.grid(row = 1,column = 1,sticky="nw")


DemoWindow = Demo.create_rectangle(490,
                                   280,
                                   VerticalLinePos+5,
                                   HorizLinePos+5,
                                   outline = ColourHex, 
                                   fill = 'white',
                                   width = 5)
DemoSearch = Demo.create_rectangle(480-5,
                                   5,
                                   480-55,
                                   15,
                                   fill = "white"
                                   )
DemoLogoRect = Demo.create_rectangle(2,
                                     2,
                                     90,
                                     20,
                                     fill = '',
                                     outline = '')

root.mainloop()