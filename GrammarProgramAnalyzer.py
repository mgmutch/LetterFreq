import re
import sqlite3


def get_word_length(conn, filename):
    with open(filename, mode='w') as fp:
        cur = conn.cursor()
        cur.execute('SELECT word_length, word FROM Words GROUP BY word ORDER BY word_length ASC, word ASC')
        rows = cur.fetchall()
        for row in rows:
            length, word = row[0], row[1]
            fp.write('%d, %s\n' % (length, word))
        cur.close()

def get_count_of_letters(conn, filename):
    with open(filename, mode='w') as fp:
        cur = conn.cursor()
        cur.execute('SELECT bank FROM Docs')
        rows = cur.fetchall()
        for row in rows:
            fp.write(row[0])

def get_vocabulary_list(conn, filename):
    with open(filename, mode='w') as fp:
        cur = conn.cursor()
        cur.execute('SELECT word, count FROM Vocabularies ORDER BY count DESC, word ASC')
        rows = cur.fetchall()
        for row in rows:
            word, length = row[0], row[1]
            fp.write('%d, %s\n' % (length, word))
        cur.close()

def get_phrase_list(conn, filename):
    with open(filename, mode='w') as fp:
        cur = conn.cursor()
        cur.execute('SELECT phrase FROM Phrases WHERE num_of_words > 1 ORDER BY phrase ASC')
        rows = cur.fetchall()
        for row in rows:
            fp.write('%s\n' % (row[0],))
    cur.close()

def get_sentences_with_conjunctions(conn, filename):
    with open(filename, mode='w') as fp:
        cur = conn.cursor()
        cur.execute('''
            SELECT sentence FROM Sentences WHERE sentence_no IN (
                SELECT sentence_no FROM Words WHERE word IN (
                    SELECT word FROM Vocabularies WHERE lc_word IN ('and', 'either', 'since', 'but')))
            ''')
        rows = cur.fetchall()
        for row in rows:
            fp.write('%s\n' % (row[0],))
    cur.close()

def get_sentences_in_alphabetical_order(conn, filename):
    with open(filename, mode='w') as fp:
        cur = conn.cursor()
        cur.execute('SELECT sentence FROM Sentences ORDER BY sentence')
        rows = cur.fetchall()
        for row in rows:
            fp.write('%s\n' % (row[0],))
    cur.close()

def main(dbname):
    conn = sqlite3.connect(dbname)
    get_word_length(conn, './WordLength.csv')
    get_count_of_letters(conn, './CountOfLetters.csv')
    get_vocabulary_list(conn, './VocabularyList.csv')
    get_phrase_list(conn, './PhraseList.csv')
    get_sentences_with_conjunctions(conn, './SentencesWithConjunctions.csv')
    get_sentences_in_alphabetical_order(conn, './SentencesInAlphabeticalOrder.csv')

if __name__ == '__main__':
    main('./tmp.db')