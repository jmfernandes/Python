from tkinter import *

import tkinter.constants, tkinter.filedialog, tkinter.messagebox

from textwrap import wrap

def wrapAndPrint (msg, width=25):
    """ wrap msg to width, then print """

    message = wrap(msg, width)
    for line in message:
        print (line)

msg = ("1. Decide if this message is to be encrypted or decrypted.\n2. Open a txt file with the message you want to alter. The text should appear in the 'Original Text' box. \n3. Enter a keyword and click the 'code' button\n4. If encypting, the encrypted message will appear in the box on the right. If decrypting, the original message should appear in the box on the right. \n5. If you want, you can save the output of the box on the right with the 'Save As' button")

words = []
finishedcode = []
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
capital = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

class App(Frame):
    def __init__(self, root):
        #establish frames
        Frame.__init__(self,root, pady=65)
        topframe = Frame(root, pady=5)
        topframe.pack(side=TOP,fill=X)
        leftframe = Frame(root)
        leftframe.pack(side=LEFT,padx=10, fill=Y)
        rightframe2 = Frame(root)
        rightframe2.pack(side=RIGHT)
        rightframe = Frame(root)
        rightframe.pack(side=RIGHT)
        radioframe = Frame(leftframe)
        radioframe.pack(pady=100)
        helpframe = Frame(leftframe)
        helpframe.pack(side=BOTTOM)

        #make directory button
        button_opt = {'fill': tkinter.constants.BOTH, 'padx': 5, 'pady': 5}
        Button(self, text='open file', command=self.askopenfile).pack(**button_opt)
        buttonlabel = Label(self, text = "enter keyword")
        buttonlabel.pack()
        self.entryfield = Entry(self)
        self.entryfield.pack()
        Button(self, text='code', command=self.code).pack(**button_opt)
        Button(self, text='Save As', command=self.asksaveasfile).pack(**button_opt)
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt')]
        options['initialdir'] = '/Users'
        options['parent'] = root

        #establish if you want to encrypt or decrypt
        storeval = [1]
        def sel():
            switchvar = self.var.get()
            if switchvar == storage[0]:
                pass
            else:
                storage.pop()
                storage.append(switchvar)
                self.text.delete(1.0, END)
                self.text2.delete(1.0, END)
                if not words:
                    pass
                else:
                    words.pop()
            if switchvar==1:
                selection = "Encrypted Text"
                storeval.pop()
                storeval.append(1)
            else:
                selection = "Plain Text"
                storeval.pop()
                storeval.append(2)
            alteredlabel.config(text = selection)
        self.var = IntVar()
        R1 = Radiobutton(radioframe, text="encrypt", variable=self.var, value=1, command=sel)
        R1.pack(side=TOP)
        R2 = Radiobutton(radioframe, text="decrypt", variable=self.var, value=2,comman=sel)
        R2.pack(side=TOP)
        R1.select()
        storage = [self.var.get()]
        label = Label(leftframe)
        label.pack()

        #create text window to show document.
        originallabel = Label(rightframe, text="Original Text")
        originallabel.pack(side=TOP)
        self.text = Text(rightframe, width=60, height=25)
        self.text.pack()



        alteredlabel = Label(rightframe2)
        alteredlabel.pack(side=TOP)
        self.text2 = Text(rightframe2, width=60, height=25)
        self.text2.pack()

        sel()

        #main title
        maintitle = Label(topframe, text = "Vigenere Cipher Coder", font=("Helvetica", 22),relief=SUNKEN)
        maintitle.pack(fill=X)

        #help button
        Button(helpframe, text='help', command=self.helpinfo).pack(**button_opt)

    def askopenfile(self):
        file = tkinter.filedialog.askopenfile(mode='r', **self.file_opt)
        if file == None and not words:
            txt = ''
        elif file == None and words:
            txt = str(words[0])
        else:
            txt = file.read()
            self.text.delete(1.0, END)
            self.text.insert(INSERT, txt)
            file.close()
        if not words:
            words.append(txt)
        else:
            words.pop()
            words.append(txt)
        return file

    def asksaveasfile(self):
        if not finishedcode:
            tkinter.messagebox.showerror(title="error",message="Code a message to save the result")
        else:
            save = tkinter.filedialog.asksaveasfile(mode='w', **self.file_opt)
            if not save:
                pass
            else:
                savetxt = str(finishedcode[0])
                save.write(savetxt)
                save.close()
                return save

    def helpinfo(self):
        tkinter.messagebox.showinfo(title="help",message=msg)

    def code(self):
        items = list((self.text.get(1.0, END)).replace(" ", "").rstrip())
        data = list((self.text.get(1.0, END)))

        if not items:
            tkinter.messagebox.showerror(title="error",message="Open a file first or type into the box on the left")
        else:
            self.text2.delete(1.0, END)
            self.keyword = self.entryfield.get()
            if not self.keyword:
                tkinter.messagebox.showerror(title="error",message="Enter a keyword")
            else:
                counting = 0
                reset = 0
                #data = list(words[0])
                if self.var.get() == 1:
                    for i in range(len(data)):
                        if counting%(len(self.keyword)) ==0 and i!=0:
                            counting = 0
                        else:
                            pass
                        if self.keyword[counting] in letters or self.keyword[counting] in capital:
                            pass
                        else:
                            print ("\n ERROR: not a valid codeword. No letters or special characters allowed. \n")
                            exit()
                        if data[i] in letters or data[i] in capital:
                            if self.keyword[counting] in letters:
                                index = letters.index(self.keyword[counting])
                            else:
                                index = capital.index(self.keyword[counting])
                        else:
                            index = 30
                        if index == 30:
                            pass
                        else:
                            if data[i] in letters:
                                position = letters.index(data[i])
                                difference = position + index
                                if difference >= len(letters):
                                    data[i] = letters[difference - len(letters)]
                                else:
                                    data[i] = letters[difference]
                            else:
                                pass
                            if data[i] in capital:
                                position = capital.index(data[i])
                                difference = position + index
                                if difference >= len(capital):
                                    data[i] = capital[difference - len(letters)]
                                else:
                                    data[i] = capital[difference]
                            else:
                                pass
                            counting = counting + 1
                else:
                    for i in range(len(data)):
                        if counting%(len(self.keyword)) ==0 and i!=0:
                            counting = 0
                        else:
                            pass
                        if self.keyword[counting] in letters or self.keyword[counting] in capital:
                            pass
                        else:
                            print ("\n ERROR: not a valid codeword. No letters or special characters allowed. \n")
                            exit()
                        if data[i] in letters or data[i] in capital:
                            if self.keyword[counting] in letters:
                                index = letters.index(self.keyword[counting])
                            else:
                                index = capital.index(self.keyword[counting])
                        else:
                            index = 30
                        if index == 30:
                            pass
                        else:
                            if data[i] in letters:
                                position = letters.index(data[i])
                                difference = position - index
                                if difference < 0:
                                    data[i] = letters[len(letters) + difference]
                                else:
                                        data[i] = letters[difference]
                            else:
                                pass
                            if data[i] in capital:
                                position = capital.index(data[i])
                                difference = position - index
                                if difference < 0:
                                    data[i] = capital[len(letters) + difference]
                                else:
                                    data[i] = capital[difference]
                            else:
                                pass
                            counting = counting + 1
                self.text2.insert(INSERT, ''.join(data))
                if not finishedcode:
                    pass
                else:
                    finishedcode.pop()
                finishedcode.append(''.join(data))




if __name__=='__main__':
    root = Tk()
    root.resizable(width=FALSE,height=FALSE)
    root.wm_title("Create a Secret Message!")
    App(root).pack()
    root.mainloop()
