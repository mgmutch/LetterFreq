import sys
import docx
import re
import sqlite3

dbfilename = './tmp.db'

def load(filename):
    db = sqlite3.connect(dbfilename)
    db.execute("DROP TABLE IF EXISTS phrases;")
    db.execute("CREATE TABLE phrases(phrase text);")
    text =""
    doc = docx.Document(filename)
    for paragraph in doc.paragraphs:
        text += paragraph.text + " "
    ary = re.sub(r'[^a-z]', ' ', text.lower()).split()
    for w in range(2, 15):
        for i in range(len(ary)-w+1):
            phrase = ' '.join(ary[i:i+w])
            print(phrase)
            db.execute("INSERT INTO phrases VALUES(?)", (phrase,))
        db.commit()
    db.close()

def analyze(filename):
    db = sqlite3.connect(dbfilename)
    cur = db.cursor()
    cur.execute('SELECT phrase, num FROM(SELECT phrase, count(phrase) AS num FROM phrases GROUP BY phrase) WHERE num > 1 ORDER BY num DESC')
    rows = cur.fetchall()
    cur.close()
    db.close()
    with open(filename + '.csv', mode='w') as f:
        for row in rows:
            f.write(row[0] + ',' + str(row[1]) + '\n')

def main(filename):
    load(filename)
    analyze(filename)

if __name__ == '__main__':
    main(sys.argv[1])


