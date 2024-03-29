import sqlite3

# Creating a sqlite database file called email #
conn = sqlite3.connect('email.sqlite')
# Creating a file handle to perform operations on the database #
cur = conn.cursor()

# Droping the pre-existing table #
cur.execute ('DROP TABLE IF EXISTS Counts')
# Creating a table called Counts #
cur.execute ('CREATE TABLE Counts (org TEXT, count INTEGER)')

# Opening the mbox.txt file #
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'mbox.txt'
fh = open(fname)

# Selecting the correct lines #
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()

# Identifying the emails and domains #
    email = pieces[1]
    org = email.split('@') [1]

# Inserting data into the database #
    cur.execute('SELECT count FROM Counts WHERE org = ?', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count) VALUES (?, 1)''', (org,))
    else:
        cur.execute('''UPDATE Counts SET count = count + 1 WHERE org = ?''', (org,))

# Commiting the updates #
    conn.commit()

# Ordering the counts and printing the results #
sqlstring = 'SELECT * FROM Counts ORDER BY count DESC'
for row in cur.execute(sqlstring):
    print(str(row[0]), row[1])

# Closing the connection #
conn.close()
