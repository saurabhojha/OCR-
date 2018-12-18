'''
    This is the ninth process in ocr!!

        Use before this: output_text_generation

        Use after this:  This is the final module!!


'''
import subprocess as sp
def open_file(fileName):
    programName = "notepad.exe"
    sp.Popen([programName, fileName])
