import sys
import re
import os
import Tkinter as tk
from gac import GAC
from search import Search


class GUI(tk.Tk):
    def __init__(self, columns, rows):
        tk.Tk.__init__(self)
        self.columns = columns
        self.rows = rows
        self.gac = GAC(columns,rows)
        self.search = Search(self.gac)
        solution = self.search.a_star()
        "ASDASDJKASHDKAJSD"
        self.canvas = tk.Canvas(self, width = 800, height = 800, borderwidth = 0)
        self.canvas.pack(side="top", fill="both", expand="true")



        menubar = tk.Menu(self)

        mapMenu = tk.Menu(menubar)
        mapMenu.add_command(label="Scenario 0", command= lambda: self.changeMap('scenario0.txt'))
        mapMenu.add_command(label="Scenario 1", command= lambda: self.changeMap('scenario1.txt'))
        mapMenu.add_command(label="Scenario 2", command= lambda: self.changeMap('scenario2.txt'))
        mapMenu.add_command(label="Scenario 3", command= lambda: self.changeMap('scenario3.txt'))
        mapMenu.add_command(label="Scenario 4", command= lambda: self.changeMap('scenario4.txt'))
        mapMenu.add_command(label="Scenario 5", command= lambda: self.changeMap('scenario5.txt'))
        mapMenu.add_command(label="Scenario 6", command= lambda: self.changeMap('scenario6.txt'))
        menubar.add_cascade(label="Maps", menu=mapMenu)
        self.config(menu=menubar)



    def changeMap(self,mapFileName):
        print mapFileName
        os.execl(sys.executable, 'python', __file__, mapFileName)

inFile = sys.argv[1]
onlyNumbers = re.compile('\-?\d+(?:\.\d+)?')

def get_instructions_from_file(inFile):

    instructions = [onlyNumbers.findall(line) for line in open(inFile, 'r')]

    columns = int(instructions[0][0])
    rows = int(instructions[0][1])

    row_specs = instructions[1:rows+1]
    for row_spec in range(len(row_specs)):
        for x in range(len(row_specs[row_spec])):
            row_specs[row_spec][x] = int(row_specs[row_spec][x])
    column_specs = instructions[rows+1:]
    for column_spec in range(len(column_specs)):
        for x in range(len(column_specs[column_spec])):
            column_specs[column_spec][x] = int(column_specs[column_spec][x])

    return (columns,column_specs),(rows,row_specs)

columns, rows = get_instructions_from_file(inFile)

gui = GUI(columns, rows)
gui.mainloop()
