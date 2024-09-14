#
# if python-docx is not installed on your computer, run
# pip install python-docx
#
import docx

filename = "../docs/Typoglycemia.docx"

# initialize variables
letters = [chr(ord("a")+i) for i in range(26)]
result = {}
for letter in letters:
    result[letter] = 0

text = ""
doc = docx.Document(filename)
for paragraph in doc.paragraphs:
    text += paragraph.text + " "
for letter in text.lower():
    if letter in result:
        result[letter] += 1
print(result)
