import os
import xml.etree.ElementTree as ET
#import ply.lex as lex
#import ply.yacc as yacc
#lexer = lex.lex
#yaccer = yacc.yacc
#print(lexer)

#from lark import Lark

print(os.getcwd())

# Default Vizzy program location.
#vizzyProgramFileDirectory = os.path.expanduser(
#    '~') + "/KFTRWI/Android/data/com.jundroo.SimpleRockets2/files/UserData/FlightPrograms/"
vizzyProgramFileDirectory = "/storage/emulated/0/Android/data/com.jundroo.SimpleRockets2/files/UserData/FlightPrograms/"
vizzyProgramName = "parsethis"

# Get Vizzy program name
while len(vizzyProgramName) == 0:
    vizzyProgramName = input(
        "Please enter the name of the Vizzy program (do not include .xml). \n")

vizzyFile = vizzyProgramFileDirectory + vizzyProgramName + ".xml"

print("Printing out " + vizzyFile)
#vizzyProgram = open(vizzyProgramDirectory, "r").readlines()
#print(vizzyProgram)

#buf = ""

#for line in vizzyProgram:
#   buf = buf + line
#   line = line.rstrip()
#   print(line)


# Creates output directory
try:
#    outputPath = str(os.path.expanduser(
#       '~')) + "\\AppData\\LocalLow\\Jundroo\\SimpleRockets 2\\Text-Based-Vizzy\\DecimpiledPrograms"
    outputPath = "/storage/emulated/0/Download/vizzy"
    if os.path.exists(outputPath):
        print("output exists")
    else:
        os.makedirs(outputPath)
except OSError:
    print("Creation of the output directory %s failed" % outputPath)
    quit()

# Creates output file
#outputFile = open(outputPath + "/" + vizzyProgramName + ".vizzy", "w")

def parseXML(infile):
   tree = ET.parse(infile)
   root = tree.getroot()
#   print(root)
#   print(root.tag)
#   print(root.attrib)
   deep(root,root,0,"","","")
          
def deep(node, parent, depth, highstyle, highformat, highcall):
    if depth>888: return
#    if node.tag in separate:
#        print("================================")
#        print("   "*depth + "[" + node.tag + "]")
#    else: 
#       if node.tag in blocktypes:
#          print("   "*depth + "[" + node.tag + "]")
    tees[node.tag] = 1
    instyle = ""
    informat = ""
    incall = ""

    if (node.tag in ["Variables","Variable","Items","Instructions","Expressions"]):
          print(node.tag + " >>> " + "".join(f'{k}: {v}, ' for k,v in node.attrib.items()))
        
#    if ( ("pos" in node.attrib.keys()) ):
#            print(node.tag + " >>> " + "".join(f'{k}: {v}, ' for k,v in node.attrib.items()))
    for att in node.attrib:
        if (att == "style"): instyle = node.attrib[att]
        else: 
            if (att == "format"): informat = node.attrib[att]
            else:
                if (att == "call"): incall = node.attrib[att]

    if ( ("style" in node.attrib.keys()) ):
        if (not(node.attrib["style"] in inpstructs["styles"].keys())):
                inpstructs["styles"][node.attrib["style"]] = {"tag": node.tag, "attribs": node.attrib}
        # functions
        if ( ("function" in node.attrib.keys()) ):
            print(node.tag + " " + node.attrib["style"] + " " + "".join(f'{k}: {v}, ' for k,v in node.attrib.items()))
            if (not(node.tag in inpstructs["fns"].keys())):
                inpstructs["fns"][node.tag] = {}
            if (not(node.attrib["style"] in inpstructs["fns"][node.tag].keys())):
                inpstructs["fns"][node.tag][node.attrib["function"] + ":" + node.attrib["style"]] = "".join(f'{k}: {v}, ' for k,v in node.attrib.items())
        # custom instructions
        elif ( ("callFormat" in node.attrib.keys()) ):
            print(node.tag + " " + node.attrib["style"] + " " + "".join(f'{k}: {v}, ' for k,v in node.attrib.items()))
            if (not(node.tag in inpstructs["custinstrs"].keys())):
                inpstructs["custinstrs"][node.tag] = {}
            if (not(node.attrib["style"] in inpstructs["custinstrs"].keys())):
                inpstructs["custinstrs"][node.tag][node.attrib["name"] + ":" + node.attrib["style"]] = "".join(f'{k}: {v}, ' for k,v in node.attrib.items())
        # other
        else:
            if ( (node.attrib["style"].startswith("op-")) or ("-op-" in node.attrib["style"]) ):
                if (not(node.tag in inpstructs["ops"].keys())):
                    inpstructs["ops"][node.tag] = {}
                if (not(node.attrib["style"] in inpstructs["ops"][node.tag].keys())):
                    if ("op" in node.attrib.keys()):
                        inpstructs["ops"][node.tag][node.attrib["op"] + ":" + node.attrib["style"]] = "".join(f'{k}: {v}, ' for k,v in node.attrib.items())
                    else:
                        inpstructs["ops"][node.tag][node.attrib["style"]+ "__:" + node.attrib["style"]] = "".join(f'{k}: {v}, ' for k,v in node.attrib.items())
                
    for ch in node:
        deep(ch,node,depth+1,instyle,informat,incall)   

separate = {"Event":1,"CustomInstruction":1,"CustomExpression":1}

ownline = {
    "Comment": 1,
    "UserInput": 1,
    "WaitUntil": 1,
    "WaitSeconds": 1,
    "SetTarget": 1,
    "Repeat": 1,
    "If": 1,
    "ElseIf":1,
    "Else":1,
    "While":1,
    "For":1,
    "Not":1,
    "Break":1,
   "SetVariable":1,
   "ChangeVariable":1,
   "DisplayMessage":1,
   "LogMessage":1,
   "LogFlight":1,
   "SetInput":1,
   "SetTargetHeading":1,
   "LockNavSphere":1,
   "SetTimeMode":1,
   "SetCameraProperty":1,
   "SetCraftProperty":1,
   "SwitchCraft":1,
   "ListOp":1,
   "SetList":1,
   "BroadcastMessage":1,
   "CallCustomInstruction":1,
   "SetActivationGroup":1,
}


blocktypes = {
    "Variable": 1,
    "Event": 1, 
    "Comment": 1,
    "UserInput": 1,
    "WaitUntil": 1,
    "WaitSeconds": 1,
    "SetTarget": 1,
    "Repeat": 1,
    "If": 1,
    "ElseIf":1,
    "Else":1,
    "While":1,
    "For":1,
    "Not":1,
    "Break":1,
   "Constant":1,
   "Comparison":1,
   "CallCustomExpression":1,
   "SetVariable":1,
   "BinaryOp":1,
   "ChangeVariable":1,
   "DisplayMessage":1,
   "LogMessage":1,
   "BoolOp":1,
   "StringOp":1,
   "MathFunction":1,
   "LogFlight":1,
   "Conditional":1,
   "CraftProperty":1,
   "Vector":1,
   "VectorOp":1,
   "EvaluateExpression":1,
   "ActivationGroup":1,
   "Planet":1,
   "SetInput":1,
   "SetTargetHeading":1,
   "LockNavSphere":1,
   "SetTimeMode":1,
   "SetCameraProperty":1,
   "SetCraftProperty":1,
   "SwitchCraft":1,
   "ListOp":1,
   "SetList":1,
   "BroadcastMessage":1,
   "CallCustomInstruction":1,
   "SetActivationGroup":1,
   "CustomInstruction":1,
   "CustomExpression":1,
    }

tees = {}

inpstructs = {
    "fns": {},
    "ops": {},
    "vars": {},
    "items": {},
    "custinstrs": {},
    "custexprs": {},
    "exprs": {},
    "styles": {},
}

def main():
    parseXML(vizzyFile)

#    for t in tees.keys():
#        if t not in blocktypes: 
#          print('   "'+t+'":1,')
        
#    print("ops = {")
#    for t in ops.keys():
#        print('   "'+t+'":{')       
#        for u in ops[t].keys():
#            print('      "'+u+'": ' + ops[t][u])
#        print("   }")
#    print("}")
#    print("fns = {")
#    for t in fns.keys():
#        print('   "'+t+'":{')       
#        for u in fns[t].keys():
#            print('      "'+u+'": ' + fns[t][u])
#        print("   }")
#    print("}")
#    print("styles = {")
#    for t in styles.keys():
#        print('   "'+t+'":{')       
#        for u in styles[t].keys():
#            if ( isinstance(styles[t][u], dict) ):
#                print('      "'+u+'": {')
#                for v in styles[t][u].keys():
#                    print('         "'+v+'": ' + styles[t][u][v] + ',')
#                print("         },")
#            else:
#                print('      "'+u+'": ' + styles[t][u] + ',')
#        print("   }")
#    print("}")
    
    prtstructs("styles")
    prtstructs("ops")
    prtstructs("fns")
    prtstructs("custinstrs")
    
    print("unfound:")
    for t in blocktypes.keys():
         found = 0
         for u in inpstructs["styles"].keys():
                if (inpstructs["styles"][u]["tag"] == t): 
                    found = 1
                    break
         if (found == 0):
             print(t)
             
#            print('      "'+u+'": ' + styles[t][u] + ' >> ' + "".join(f'{k}: {v}, ' for k,v in styles[t]["attribs"].items()))

def prtstructs(structname):
    print(structname + " = {")
    struct = inpstructs[structname]
    for t in struct.keys():
        print('   "'+t+'":{')       
        for u in struct[t].keys():
            if ( isinstance(struct[t][u], dict) ):
                print('      "'+u+'": {')
                for v in struct[t][u].keys():
                    print('         "' + v + '": "' + struct[t][u][v] + '",')
                print("         },")
            else:
                print('      "'+u+'": "' + struct[t][u] + '",')
        print("   }")
    print("}")
 
main()
         
# ProgramFlow(Instruction):  # The blue blocks
# CraftInstructions(Instruction):  # The black blocks
# Events(Instruction):  # The yellow blocks
# Lists(Instruction):  # The purple blocks
# MultifunctionDisplay(Instruction):  # The light blue blocks
# Expression:
# Operators(Expression):  # The blue capsules
# CraftInformation(Expression):  # The black capsules
# ListExpressions(Expression):  # The purple capsules

