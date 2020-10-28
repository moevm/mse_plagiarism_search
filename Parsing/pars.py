from bs4 import BeautifulStoneSoup
from bs4 import BeautifulSoup
import html


pathToParse = ''
print("Enter file path")
pathToParse = input()

f = open(pathToParse, 'r')
o = open('aft.txt', 'w')
java = open('java.txt', 'w')
c = open('c.txt', 'w')
python = open('python.txt', 'w')



count = 0
syblolsClanguage = 0
syblolsJavalanguage = 0
syblolsPythonlanguage = 0

try: 
    for line in f:
        count +=1
        xml = html.unescape(line)
        soup = BeautifulSoup(xml, features="xml")
        #print(soup.prettify)
        if soup.pre:
            o.write(str(soup.pre) + '\n')
            for link in soup.find_all('pre'):
                if (link.get('class') != None and link.get('class') != 'lang-none prettyprint-override'):
                    print("Language - ", link.get('class'))
                    #print(soup.pre) 
                    #print("\n")
                    o.write(str(soup.pre) + '\n')
                    if(link.get('class') == 'lang-c prettyprint-override' or link.get('class') == 'lang-objective-c prettyprint-override' or link.get('class') == 'lang-cpp prettyprint-override'):
                        syblolsClanguage += len(str(soup.pre))
                        c.write(str(soup.pre) + '\n')
                    elif(link.get('class') == 'lang-java prettyprint-override' or link.get('class') == 'lang-js prettyprint-override'):
                        syblolsJavalanguage += len(str(soup.pre))
                        java.write(str(soup.pre) + '\n')
                    elif(link.get('class') == 'lang-py prettyprint-override'):
                        syblolsPythonlanguage += len(str(soup.pre))
                        python.write(str(soup.pre) + '\n')
                    
except Exception:
    print(' ')

print("Parse ", int(syblolsClanguage/65), " lines on C language")
print("Parse ", int(syblolsJavalanguage/65), " lines on Java language")
print("Parse ", int(syblolsPythonlanguage/65), " lines on Python language")
print("Posts with <pre> ",count)
f.close()
o.close()
java.close()
c.close()
python.close()
