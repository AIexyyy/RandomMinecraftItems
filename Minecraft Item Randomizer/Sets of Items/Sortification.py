import re
def SortItemsIn(filepath):
    File,Result=open(f"{filepath}.txt").readline(),""; File=re.split(r'(?<!\\), ', File[:-1]); File.sort(key=str.lower)
    for f in File: Result+=f+(", " if f!=File[-1] else ".")
    file=open(f"{filepath}.txt","w"); file.write(Result); file.close(); return None
SortItemsIn("Minecraft items viable for Guess or Die")
SortItemsIn("Minecraft April Fools items")
SortItemsIn("Minecraft Education Edition items")
