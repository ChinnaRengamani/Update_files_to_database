list_files_from_db = [(1, 'file1', 'txt')]
new_l=[]
for i in list_files_from_db:

    i=list(i)
    i.pop(0)
    print(i)
    i=".".join(i)
    new_l.append(i)
print(new_l)

# adk  