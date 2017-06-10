from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as box


fileptr = [False, 0]

class MainWIndow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background='#4fc3f7')
        self.parent = parent
        self.initUI()
        self.initQuitButton()
        self.initFileButton()
        self.initInputText()
        self.initOutputText()
        self.initBinaryText()
        self.initClearButton()
        self.initLabels()
        self.initAssembleButton()
        self.initInfoLabel()
        self.initExecutionLabel()
        self.initFirstPassOutput()
        self.initExecResult()
        self.filename=""
        
        
    def initUI(self):
        self.parent.title('Two-Pass Assembler')
        self.pack(fill=BOTH, expand=1)
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        self.parent.geometry('500x500+%d+%d' % ((sw - 500)/2, (sh - 500)/2))

    def initBinaryText(self, textParam=''):
        self.BinaryText = Text(self)
        self.BinaryText.place(relx = 0.5, rely = 0.5, relwidth = 0.44, relheight = 0.35)
        self.BinaryText.insert(index = INSERT, chars = textParam)

    def initFirstPassOutput(self, textParam=''):
        self.FirstPassOutput = Text(self)
        self.FirstPassOutput.place(relx = 0.62, rely = 0.069, relwidth = 0.32, relheight = 0.15)
        self.FirstPassOutput.insert(index = INSERT, chars = textParam)

    def initExecResult(self, textParam=''):
        self.ExecResult = Text(self)
        self.ExecResult.place(relx = 0.62, rely = 0.27, relwidth = 0.32, relheight = 0.15)
        self.ExecResult.insert(index = INSERT, chars = textParam)

    def initExecutionLabel(self, textParam = "Execution Result:"):
        l5 = Label(self, text = textParam, background='#2ed') 
        l5.place(relx = 0.62, rely = 0.23, relwidth = 0.32)

    def initQuitButton(self):
        quitButton = Button(self, text = "Quit", command = self.quit,background='red')
        quitButton.place(relx = 0.8, rely = 0.9, relwidth = 0.1)

    def initAssembleButton(self):
        genButton = Button(self, text = "Assemble", command = self.invokeAssemble,background='#bbdefb')
        genButton.place(relx = 0.48, rely = 0.9, relwidth = 0.2)

    def initFileButton(self):
        fileButton = Button(self, text = "Select Input", command = self.onOpen,background='#bbdefb')
        fileButton.place(relx = 0.25, rely = 0.9, relwidth = 0.2)

    def initClearButton(self):
        ClearButton = Button(self, text = "Clear", command = self.onClear,background='#ffee58')
        ClearButton.place(relx = 0.69, rely = 0.9, relwidth = 0.1)
    
    def initInputText(self, textParam=''):
        self.inputText = Text(self,wrap=WORD)
        self.inputText.place(relx = 0.07, rely = 0.07, relwidth = 0.5, relheight = 0.35)
        self.inputText.insert(index = INSERT, chars = textParam)
    
    def initLabels(self):
        l1 = Label(self, text = "Input Assembly Source", background='#fff')
        l2 = Label(self, text = "Output Hex Code", background='#fff')
        l3 = Label(self, text = "Output Binary Code", background='#fff')
        l1.place(relx = 0.07, rely = 0.02, relwidth = 0.5)
        l2.place(relx = 0.07, rely = 0.45, relwidth = 0.43)
        l3.place(relx = 0.51, rely = 0.45, relwidth = 0.43)

    def initInfoLabel(self, textParam = "First Pass Output:"):
        l3 = Label(self, text = textParam, background='#2ed') 
        l3.place(relx = 0.62, rely = 0.02, relwidth = 0.32)

    def initOutputText(self, textParam=''):
        self.outputText = Text(self)
        self.outputText.place(relx = 0.07, rely = 0.5, relwidth = 0.44, relheight = 0.35)
        self.outputText.insert(index = INSERT, chars = textParam)

    def onClear(self):
        self.outputText.delete("1.0", END)
        self.BinaryText.delete("1.0", END)
        self.FirstPassOutput.delete("1.0",END)
        self.ExecResult.delete("1.0",END)


    def onOpen(self):
        self.filename = filedialog.askopenfilename()
        if self.filename is '':
            box.showinfo("Info", "You did not select a file.")
        else:
            global fileptr
            fileptr[0] = True
            fileptr[1] = self.filename
            f = open(fileptr[1], 'r')
            self.text = f.read()
            self.text = self.text.split('\n')
            displayText = ''
            for i in range(len(self.text)):
                displayText += (str(i+1) + ' ' + self.text[i] + '\n')
            self.initInputText(displayText)
    def AddOperation(self):
            n3=0
            n2=0
            n1=0
            outP=0
            dataReg=0
            memReg=0
            outAco=0
           
            get = self.outputText.get('1.0', END + '-1c')
            hexad=get.split()
            tem=0
            dic={}
            while (tem<len(hexad)):

                dic[tem]=hexad[tem]
                dic[tem+1]=" "
                tem=tem+1
            tem2=1
            while(tem2<len(dic)):
              number=""
              number+=str(dic[tem2])
              if(tem2==9):
                dataReg=int(str(dic[9]),16)
                memReg=dataReg
                outAco=dataReg
                memReg=0
                dataReg=0
                n1=int(str(dic[9]),16)
              elif(tem2==11):
                memReg=int(str(dic[11]),16)
                dataReg=memReg
              outp=dataReg+outAco
              outp=bin(outp).split("b")[1].zfill(16)
              tem2+=2
            self.ExecResult.insert(END, "RESULT : \n" + str(outp))
             
     
    def invokeAssemble(self):
        #call to assembly code module
        get = self.inputText.get('1.0', END + '-1c')
        two_pass_Assembler = Two_Pass_Assembler()
        self.result = two_pass_Assembler.assemble(self.filename)
        
        
        try:
            self.result["Error"]
            self.outputText.insert(END, self.result["Error"] + "\n")
            self.outputText["fg"] = "red"
        except:
            self.outputText["fg"] = "black"
            fil = open("output.txt", "w")
            self.FirstPassOutput.insert(END,two_pass_Assembler.labels)#print First Pass Output
            for i in range(len(self.result)):
                fil.write(self.result[i].split()[0] + " "+ bin(int(self.result[i].split()[1], 16)).split("b")[1].zfill(16) + "\n")
                self.outputText.insert(END, self.result[i] + "\n")
            fil.close()
            sample = open("output.txt", "r")
            fil2 = sample.readline()
            while(fil2 != ''):
                #print(fil2)
                self.BinaryText.insert(END,fil2)
                fil2 = sample.readline()
            self.AddOperation() 

class Symbol_Tables:
    def __init__(self):
        self._reg_ref = self.extract_reg_ref("Symbole_Tables/register_reference_table.txt")
        self._io_ref = self.extract_io_ref("Symbole_Tables/input_output_table.txt")

    def extract_reg_ref(self, file):
        try:
            return open(file)
        except IOError:
            print("Error: File " + file + " doesn't Exist!")

    def extract_io_ref(self, file):
        try:
            return open(file)
        except IOError:
            print("Error: File " + file + " doesn't Exist!")

    def get_reg_ref_table(self):
        table = {}
        read = self._reg_ref.readline().split()
        while len(read) > 0: 
            table[read[0]] = read[1] #['cla':'7800']
            read = self._reg_ref.readline().split()
        return table

    def get_io_ref_table(self):
        table = {}
        read = self._io_ref.readline().split()
        while len(read) > 0:
            table[read[0]] = read[1]
            read = self._io_ref.readline().split()
        return table
    
class Two_Pass_Assembler:
    def complement_to_binary(num):
        binary = bin(int(num)).split("b")[1].zfill(16)
        binary = binary.replace("0", "x")
        binary = binary.replace("1", "0")
        binary = binary.replace("x", "1")
        return bin(int(binary, 2) + 1).split("b")[1]

    def complement_to_hex(num):
        binary = bin(int(num)).split("b")[1].zfill(16)
        binary = binary.replace("0", "x")
        binary = binary.replace("1", "0")
        binary = binary.replace("x", "1")
        return hex(int(binary, 2) + 1).split("x")[1]

    def __init__(self):
        self.dict = {}
        t = Symbol_Tables()
        self.reg_ref_table = t.get_reg_ref_table()
        self.io_ref_table = t.get_io_ref_table()
        self.mri_table = "and add lda sta bun bsa isz".split()
        self.labels = {}
        self.output = []
        self.output_dict = {}
    def first_pass(self):
        Loc_counter = 0
        line_Number = 1
        read = self.file.readline()
        while read != "":
            r = read.split(",")
            if len(r) > 1:#label Exist
                if ("org" in r[1].lower()):
                    try:
                        Loc_counter = int(r[1].split()[1],16) - 1 #hex to int
                        if (Loc_counter+1 >= 4096):
                            self.output_dict["Error"]= "Error at line " + str(line_Number) + " Location can't be > FFF"
                    except IndexError:
                        self.output_dict["Error"] = "Error at line " + str(line_Number)
                else:
                    self.labels[r[0]] = hex(Loc_counter).split("x")[1].zfill(3)#save labels in hex address value{'min':106}
                    
            else:
                if ("org" in r[0].lower()):#no lable
                    try:
                        Loc_counter = int(r[0].split()[1],16) - 1 #hex to int
                        if (Loc_counter+1 >= 4096):
                            self.output_dict["Error"] = "Error at line " + str(line_Number) + " Location can't be > FFF"
                    except:
                        self.output_dict["Error"] = "Error at line " + str(line_Number)      
            Loc_counter += 1
            line_Number += 1
            read = self.file.readline()
            if ("END" in read or read == ""):
                self.file.seek(0)
                break
    def second_pass(self):
        self.Loc_counter = 0
        line_Number = 1
        read = self.file.readline()
        while read != "":
            r = read.split(",")
            if len(r) > 1:
                if r[1].split()[0].lower() in {"org","dec","hex","end"}:
                    self.pseudo_helper(r[1].split(), line_Number)
                else:
                    self.output.append(str(hex(self.Loc_counter)) + " " + str(self.parse(r[1].split(), line)))
            else:
                re = read.split()
                instruction = ""
                if len(re) == 0 or "end" in re[0].lower():
                    break
                elif re[0].lower() in ["org", "dec", "hex", "end"]:
                    self.pseudo_helper(re, line_Number)
                else:
                    self.output.append(str(hex(self.Loc_counter)) + " " + str(self.parse(re, line_Number)))
            self.Loc_counter += 1
            line_Number += 1
            read = self.file.readline()
        
    def pseudo_helper(self, ins_list, line):
        if "org" in ins_list[0].lower():
            try:
                self.Loc_counter = int(ins_list[1], 16) - 1
            except:
                self.output_dict["Error"] = "Error at line " + str(line)
        elif "end" in ins_list[0].lower():
            sys.exit()
        elif "dec" in ins_list[0].lower():
            st = hex(int(ins_list[1])).split("x")
            if ("-" in ins_list[1]):
                st[1] = utils.complement_to_hex(ins_list[1])
            else:
                st[1] = st[1].zfill(4)
            self.output.append(str(hex(self.Loc_counter)) + " " + str(st[1]))
        elif "hex" in ins_list[0].lower():
            self.output.append(str(hex(self.Loc_counter)) + " " + str(ins_list[1].zfill(4)))
            
    def parse(self, ins_list, line):
        instruction = ""
        if ins_list[0].lower() in self.mri_table:
            instruction += self.mri_helper(ins_list)
            try:
                if ins_list[1].isdigit():
                    instruction += ins_list[1]
                else:
                    instruction += str(self.labels[ins_list[1]])
            except:
                print("Error: '" + str(ins_list[0]) + "' instruction missing an operand at line", line)
                self.output_dict["Error"] = "Error: unable to resolve address '" + str(ins_list[1]) + "' at line " + str(line)

        elif ins_list[0].lower() in self.reg_ref_table:
            if len(ins_list) > 1 and "/" not in ins_list[1]:
                print("Error at line", line)
                self.output_dict["Error"] = "Error at line " + str(line)
                return
            instruction = self.reg_ref_table[ins_list[0].lower()]

        elif ins_list[0].lower() in self.io_ref_table:
            instruction = self.io_ref_table[ins_list[0].lower()]
        else:
            print("Instruction '" + str(ins_list[0]) +"' not recognized at line", line)
            self.output_dict["Error"] = "Instruction '" + str(ins_list[0]) +"' not recognized at line " + str(line)


        return instruction
    
    def mri_helper(self, ins_list):
        if ins_list[0].lower() == "and":
            return "8" if len(ins_list) > 2 and ins_list[2].lower() == "i" else "0"
        elif ins_list[0].lower() == "add":
            return "9" if len(ins_list) > 2 and ins_list[2].lower() == "i" else "1"
        elif ins_list[0].lower() == "lda":
            return "A" if len(ins_list) > 2 and ins_list[2].lower() == "i" else "2"
        elif ins_list[0].lower() == "sta":
            return "B" if len(ins_list) > 2 and ins_list[2].lower() == "i" else "3"
        elif ins_list[0].lower() == "bun":
            return "C" if len(ins_list) > 2 and ins_list[2].lower() == "i" else "4"
        elif ins_list[0].lower() == "bsa":
            return "D" if len(ins_list) > 2 and ins_list[2].lower() == "i" else "5"
        elif ins_list[0].lower() == "isz":
            return "E" if len(ins_list) > 2 and ins_list[2].lower() == "i" else "6"


        
    def assemble(self, file):
        try:
            self.file = open(file, "r")
            self.first_pass()
            self.second_pass()
            try:
                self.output_dict["Error"]
            except KeyError:
                self.output_dict = self.output
            return self.output_dict
        except IOError:
            print("Error: File " + file + " not opened!")
            self.output.append("Helo")
            sys.exit()
    
                
        
        
def main():
    root = Tk()
    app = MainWIndow(root)
    root.mainloop()
    

main() #success #called  __init__.py

