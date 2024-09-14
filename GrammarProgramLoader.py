
import docx
import glob
import re
import sqlite3

CASE_SENSITIVE_MODE = False
MAX_NUM_OF_WORDS_IN_A_PHRASE = 100

letters = [chr(ord("a")+i) for i in range(26)]
if CASE_SENSITIVE_MODE:
    letters = letters + [chr(ord("A")+i) for i in range(26)]

letter_dict = {}
for i, letter in enumerate(letters):
    letter_dict[letter] = i

def get_bank(s):
    bank = [0] * len(letters)
    for letter in s:
        if letter in letter_dict:
            bank[letter_dict[letter]] += 1
    return ','.join([str(i) for i in bank])

def split_into_words(s):
    return re.split(r'\s+', re.sub(r'[^a-zA-Z]+', ' ', s))

def load_docs(conn, pathname: str):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Docs')
    cur.execute('''
        CREATE TABLE Docs(
            doc_no INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            text TEXT,
            bank TEXT)''')
    for filename in glob.glob(pathname):
        text = ""
        doc = docx.Document(filename)
        for paragraph in doc.paragraphs:
            text += paragraph.text + ". "
        if not CASE_SENSITIVE_MODE:
            text = text.lower()
        cur.execute(
            'INSERT INTO Docs(filename, text, bank) VALUES($1, $2, $3)',
            (filename, text, get_bank(text)))
    conn.commit()
    cur.close()

def parse_docs(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Sentences')
    cur.execute('''
        CREATE TABLE Sentences(
            doc_no INTEGER,
            sentence_no INTEGER PRIMARY KEY,
            sentence TEXT,
            bank TEXT)''')
    cur.execute('SELECT doc_no, text FROM Docs ORDER BY doc_no;')
    rows = cur.fetchall()
    for row in rows:
        doc_no, text = row[0], row[1]
        for sentence in re.split(r'[\.\?\!]\s+', text):
            cur.execute(
                'INSERT INTO Sentences(doc_no, sentence, bank) VALUES($1, $2, $3)',
                (doc_no, sentence, get_bank(sentence)))
    conn.commit()
    cur.close()

def parse_sentences_for_phrases(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Phrases')
    cur.execute('''
        CREATE TABLE Phrases(
            doc_no INTEGER,
            sentence_no INTEGER,
            phrase_no INTEGER PRIMARY KEY AUTOINCREMENT,
            num_of_words INTEGER,
            phrase TEXT,
            bank TEXT)''')
    cur.execute('SELECT doc_no, sentence_no, sentence FROM Sentences ORDER BY sentence_no')
    rows = cur.fetchall()
    for row in rows:
        doc_no, sentence_no, sentence = row[0], row[1], row[2]
        words = split_into_words(sentence)
        print('processing sentence#', sentence_no, ' the # of words in this sentence is', len(words))
        for i in range(len(words)):
            for j in range(len(words[i:])):
                words_in_phrase = words[i:][:j+1]
                num_of_words = len(words_in_phrase)
                if num_of_words < MAX_NUM_OF_WORDS_IN_A_PHRASE:
                    phrase = ' '.join(words_in_phrase)
                    cur.execute(
                        'INSERT INTO Phrases(doc_no, sentence_no, num_of_words, phrase, bank) VALUES($1, $2, $3, $4, $5)',
                        (doc_no, sentence_no, num_of_words, phrase, get_bank(phrase)))
    conn.commit()
    cur.close()

def parse_sentences_for_words(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Words')
    cur.execute('''
        CREATE TABLE Words(
            doc_no INTEGER,
            sentence_no INTEGER,
            word_no INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT,
            word_length INTEGER)''')
    cur.execute('SELECT doc_no, sentence_no, sentence FROM Sentences ORDER BY sentence_no')
    rows = cur.fetchall()
    for row in rows:
        doc_no, sentence_no, sentence = row[0], row[1], row[2]
        words = split_into_words(sentence)
        for word in words:
            cur.execute(
                'INSERT INTO Words(doc_no, sentence_no, word, word_length) VALUES($1, $2, $3, $4)',
                (doc_no, sentence_no, word, len(word)))
    conn.commit()
    cur.close()

def parse_words_for_vocabularies(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Vocabularies')
    cur.execute('''
        CREATE TABLE Vocabularies(
            word_id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE,
            lc_word TEXT,
            bank TEXT,
            count INTEGER)''')
    cur.execute('SELECT word, count(*) AS count FROM Words GROUP BY word ORDER BY count DESC, word ASC')
    rows = cur.fetchall()
    for row in rows:
        word, count = row[0], row[1]
        cur.execute(
            'INSERT INTO Vocabularies(word, lc_word, bank, count) VALUES($1, $2, $3, $4)',
            (word, word.lower(), get_bank(word), count))
    conn.commit()
    cur.close()

def main():
    conn = sqlite3.connect('./tmp.db')
    load_docs(conn, './docs/*docx')
    parse_docs(conn)
    parse_sentences_for_phrases(conn)
    parse_sentences_for_words(conn)
    parse_words_for_vocabularies(conn)
    conn.close()

if __name__ == '__main__':
    main()
