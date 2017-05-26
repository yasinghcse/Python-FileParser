#!/usr/bin/python

import glob, os #import lib for file parsing
import sys #import lib for reading command line argument
import zipfile #import lib for archiving the files
import re #import for regular exp

#check for input arguments
if len(sys.argv) <3:
    print("Please provide source and destination directory. Output file name is optional")
    print("Example: fileParser.py sourcePath destinationPath [outputfilename]")
    exit()
print 'Source Directory:', str(sys.argv[1])
print 'Destination Directory:', str(sys.argv[2])

#check if the output filename is provided
try:
    outputfilename=str(sys.argv[3])
    ext=os.path.splitext(outputfilename)[1]
    #check for the output file extension. If not ".zip" stop the program
    if ext != ".zip":
        print("invalid outputfilename format.")
        print("Valid Format :- .zip")
        exit()
    print("Setting the outputfilename to {}".format(outputfilename))
except SystemExit:
    exit() #handling of above exit() call for failure scenario
except:
    #If no name is provided set the dafault value
    print("No outputfilename provided. Setting the outputfilename to processed.zip")
    outputfilename="processed.zip"

#checking for the presence of input directory
try:
    os.stat(sys.argv[1])
except:
    print("Invalid input Directory")
    exit()

#checking for files in the directory, if no file to process STOP
os.chdir(str(sys.argv[1])) #change current directory to input directory
if len(glob.glob("*.js"))==0:
    print("No files to process")
    exit()

print("Starting File processing ......")
#changing the extensions, contents of matched file
for file in glob.glob("*.js"):
    #opening the file and read the contents
    with open(file,'r') as f:
        content=f.read()
    #find all the occurences of comments and replace it
    for x in re.findall(r'("[^\n]*"(?!\\))|(//[^\n]*$|/(?!\\)\*[\s\S]*?\*(?!\\)/)',content,8):
        content=content.replace(x[1],'')
    #open the main file again and overwrite the contents to it.
    fout=open(file,'w')
    fout.write("/** iDream Interactive **/\n");
    fout.writelines(content)
    #extract the file name and rename it by appending the .ts as the file format to the file
    name=os.path.splitext(file)[0]
    os.rename(file, name+".ts")
print("File processing done!!")


#check for the presence of output directory, if not found create new one
try:
    os.stat(sys.argv[2])
except:
    os.mkdir(sys.argv[2])

#archiving the impacted files
print("Starting Archiving ......")
zf = zipfile.ZipFile(sys.argv[2]+"/"+outputfilename, "w")
for file in glob.glob("*.ts"):
    zf.write(file)
zf.close()
print("Archiving Done!!!")
