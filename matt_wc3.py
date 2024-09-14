

import sys
import docx
import sqlite3
import re

letters = [chr(ord("a")+i) for i in range(26)]

def prepare_database(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE t0(i INTEGER, s TEXT, v TEXT);''');
    cur.execute('''CREATE TABLE t1(i INTEGER, s TEXT, v TEXT);''');
    cur.close()

def convert_sentence(sentence):
    buf = re.sub(r'[^a-zA-Z]', '', sentence.lower())
    counter = [0] * 26
    for j, letter in enumerate(letters):
        counter[j] = buf.count(letter)
    return ','.join([str(n) for n in counter])

def convert_word(word):
    total = 0
    for j, letter in enumerate(letters):
        total += word.lower().count(letter) * (j+1)
    return total

def load_document(filename):
    text = ""
    doc = docx.Document(filename)
    for paragraph in doc.paragraphs:
        text += paragraph.text + " "
    return text

def analyze(conn, tablename, text):
    cur = conn.cursor()
    ary = re.split('\.\s+', text)
    for i, sentence in enumerate(ary):
        value = convert_sentence(sentence)
        if value != '':
            cur.execute('''INSERT INTO %s VALUES(?, ?, ?);''' % tablename,
                (i, sentence, value))
    cur.close()

def main(filename0, filename1):
    conn = sqlite3.connect(':memory:')
    prepare_database(conn)
    text = load_document(filename0)
    analyze(conn, 't0', text)
    text = load_document(filename1)
    analyze(conn, 't1', text)
    cur = conn.cursor()
    cur.execute('''
        SELECT t0.s, t1.s, t0.v
        FROM t0
        LEFT OUTER JOIN t1 ON t0.v = t1.v
        ORDER BY t0.i''')
    values = cur.fetchall()
    print('"%s", "%s", %s' % (filename0, filename1, ', '.join(letters)))
    for v in values:
        print('"%s", "%s", %s' % (v[0], v[1], v[2]))
    cur.close()
    conn.close()

def test():
    print(convert_sentence('The building was owned by a zealous attorney.'))
    print(convert_sentence('True goal you want body size with banal needs.'))
    print(convert_word('zealous'))

if __name__ == '__main__':
    #test()
    main(sys.argv[1], sys.argv[2])

