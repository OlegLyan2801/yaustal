def hold_book(conn, pr, title, author, date):
    db_cursor = conn.cursor()
    db_cursor.execute("SELECT id, free FROM books WHERE title=? AND author=?", (title, author))
    book = db_cursor.fetchone()
    if not book or book[1] <= 0:
        print("Нет свободных экземпляров.")
        return
    book_id = book[0]

    db_cursor.execute("SELECT COUNT(*) FROM holds WHERE pr=?", (pr,))
    if db_cursor.fetchone()[0] >= 5:
        print("У читателя уже 5 броней.")
        return

    db_cursor.execute("INSERT INTO holds (pr, book_id, date) VALUES (?, ?, ?)", (pr, book_id, date))
    db_cursor.execute("UPDATE books SET free=free-1 WHERE id=?", (book_id,))
    conn.commit()
    print("Книга забронирована.")

def unhold_book(conn, pr, title, author):
    db_cursor = conn.cursor()
    db_cursor.execute("SELECT id FROM books WHERE title=? AND author=?", (title, author))
    book = db_cursor.fetchone()
    if not book:
        print("Книга не найдена.")
        return
    book_id = book[0]
    db_cursor.execute("DELETE FROM holds WHERE pr=? AND book_id=?", (pr, book_id))
    db_cursor.execute("UPDATE books SET free=free+1 WHERE id=?", (book_id,))
    conn.commit()
    print("Бронь снята.")

def loan_book(conn, pr, title, author, date):
    db_cursor = conn.cursor()
    db_cursor.execute("SELECT id, free FROM books WHERE title=? AND author=?", (title, author))
    book = db_cursor.fetchone()
    if not book or book[1] <= 0:
        print("Нет свободных экземпляров.")
        return
    book_id = book[0]

    db_cursor.execute("SELECT COUNT(*) FROM loans WHERE pr=?", (pr,))
    if db_cursor.fetchone()[0] >= 5:
        print("У читателя уже 5 книг.")
        return

    db_cursor.execute("DELETE FROM holds WHERE pr=? AND book_id=?", (pr, book_id))
    db_cursor.execute("INSERT INTO loans (pr, book_id, date) VALUES (?, ?, ?)", (pr, book_id, date))
    db_cursor.execute("UPDATE books SET free=free-1 WHERE id=?", (book_id,))
    conn.commit()
    print("Книга выдана.")

def return_book(conn, pr, title, author):
    db_cursor = conn.cursor()
    db_cursor.execute("SELECT id FROM books WHERE title=? AND author=?", (title, author))
    book = db_cursor.fetchone()
    if not book:
        print("Книга не найдена.")
        return
    book_id = book[0]
    db_cursor.execute("DELETE FROM loans WHERE pr=? AND book_id=?", (pr, book_id))
    db_cursor.execute("UPDATE books SET free=free+1 WHERE id=?", (book_id,))
    conn.commit()
    print("Книга возвращена.")

def get_loans_by_reader(conn, pr):
    db_cursor = conn.cursor()
    db_cursor.execute("""
    SELECT b.title, b.author, l.date
    FROM loans l JOIN books b ON l.book_id=b.id
    WHERE l.pr=?
    """, (pr,))
    return db_cursor.fetchall()

def get_holds_by_reader(conn, pr):
    db_cursor = conn.cursor()
    db_cursor.execute("""
    SELECT b.title, b.author, h.date
    FROM holds h JOIN books b ON h.book_id=b.id
    WHERE h.pr=?
    """, (pr,))
    return db_cursor.fetchall()

def search(conn, title=None, author=None, genre=None):
    db_cursor = conn.cursor()
    query = "SELECT title, author, genre, total, free FROM books WHERE 1=1"
    params = []
    if title:
        query += " AND LOWER(title) LIKE ?"
        params.append(f"%{title.lower()}%")
    if author:
        query += " AND LOWER(author) LIKE ?"
        params.append(f"%{author.lower()}%")
    if genre:
        query += " AND LOWER(genre) LIKE ?"
        params.append(f"%{genre.lower()}%")
    db_cursor.execute(query, params)
    return db_cursor.fetchall()
