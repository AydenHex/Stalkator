def MakeFile(fileName, tab_abon, tab_abon2):
        fp = open(fileName, 'w')
        fp.write('[')
        for i in range(len(tab_abon)):
            if(i < len(tab_abon)-1):
                fp.write(tab_abon[i]+', ')
            else:
                fp.write(tab_abon[i]+']\n\n[')
        for i in range(len(tab_abon2)):
            if(i < len(tab_abon2)-1):
                fp.write(tab_abon2[i]+', ')
            else:
                fp.write(tab_abon2[i]+']')
        fp.close()

def ParseFile(fileName):
        tabTmp = []
        fp = open(fileName, 'r')
        content = fp.read()
        i = 0
        while(i < len(content)):
            while(i < len(content) and content[i] != '['): i += 1
            tabTmp.append([])
            i += 1
            while(i < len(content) and content[i] != ']'):
                name = ''
                while(content[i] != ',' and content[i] != ']'):
                    name += content[i]
                    i += 1
                tabTmp[len(tabTmp)-1].append(name)
                if(content[i] == ','): i += 2
        fp.close()
        return tabTmp