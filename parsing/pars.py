from bs4 import BeautifulStoneSoup
from bs4 import BeautifulSoup
import html


pathToParse = '123.txt'
print("Enter file path")
pathToParse = input()

f = open(pathToParse, 'r')
o = open('aft.txt', 'w')
java = open('java.txt', 'w')
js = open('js.txt', 'w')
c = open('c.txt', 'w')
cpp = open('cpp.txt', 'w')
python = open('python.txt', 'w')



count = 0
symbolsClanguage = 0
symbolsJavalanguage = 0
symbolsPythonlanguage = 0
symbolsJSlanguage = 0
symbolsCpplanguage = 0


try: 
    for line in f:
        count +=1
        xml = html.unescape(line)
        soup = BeautifulSoup(xml, features="xml")
        #print(soup.prettify)
        for link in soup.find_all('pre'):
            if (link.get('class') != None and link.get('class') != 'lang-none prettyprint-override'):
                #print("Language - ", link.get('class'))
                print(soup.code.contents[0])
                #print("\n")
                o.write(str(soup.code.contents[0]) + '\n')
                if(link.get('class') == 'lang-c prettyprint-override'):
                    symbolsClanguage += len(str(soup.pre))
                    c.write(str(soup.code.contents[0]) + '\n')
                elif(link.get('class') == 'lang-java prettyprint-override'):
                    symbolsJavalanguage += len(str(soup.pre))
                    java.write(str(soup.code.contents[0]) + '\n')
                elif(link.get('class') == 'lang-py prettyprint-override'):
                    symbolsPythonlanguage += len(str(soup.pre))
                    python.write(str(soup.code.contents[0]) + '\n')
                elif(link.get('class') == 'lang-js prettyprint-override'):
                    symbolsJSlanguage += len(str(soup.pre))
                    js.write(str(soup.code.contents[0]) + '\n')
                elif(link.get('class') == 'lang-cpp prettyprint-override' or link.get('class') == 'lang-objective-c prettyprint-override'):
                    symbolsCpplanguage += len(str(soup.pre))
                    cpp.write(str(soup.code.contents[0]) + '\n')                    
                    
except Exception:
    print(' ')

print("Parse ", int(symbolsClanguage/65), " lines on C language")
print("Parse ", int(symbolsJavalanguage/65), " lines on Java language")
print("Parse ", int(symbolsPythonlanguage/65), " lines on Python language")
print("Parse ", int(symbolsJSlanguage/65), " lines on JS language")
print("Parse ", int(symbolsCpplanguage/65), " lines on C++s language")
print("Posts with <pre> ",count)
f.close()
o.close()
java.close()
c.close()
python.close()
