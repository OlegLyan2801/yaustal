def generate_pr(full_name, phone):
    first, last = full_name.split()
    return first[0].upper() + last[0].upper() + str(len(first)) + str(len(last)) + phone[-4:]

def add_book(conn, title, author, genre, n=1):
    db_cursor = conn.cursor()
    db_cursor.execute("SELECT id FROM books WHERE title=? AND author=?", (title, author))
    row = db_cursor.fetchone()
    if row:
        db_cursor.execute("UPDATE books SET total=total+?, free=free+? WHERE id=?", (n, n, row[0]))
        print("книга обновлена")
    else:
        db_cursor.execute(
            "INSERT INTO books (title, author, genre, total, free) VALUES (?, ?, ?, ?, ?)",
            (title, author, genre, n, n)
        )
        print("книга добавлена")
    conn.commit()

def delete_book(conn, title, author):
    db_cursor = conn.cursor()
    db_cursor.execute("SELECT id FROM books WHERE title=? AND author=?", (title, author))
    row = db_cursor.fetchone()
    if not row:
        print("нету такой книги")
        return
    book_id = row[0]

    db_cursor.execute("SELECT 1 FROM loans WHERE book_id=?", (book_id,))
    if db_cursor.fetchone():
        print("книга уже взята")
        return

    db_cursor.execute("SELECT 1 FROM holds WHERE book_id=?", (book_id,))
    if db_cursor.fetchone():
        print("книга забронена")
        return

    db_cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    print("книга удалена")

def add_reader(conn, full_name, phone, age):
    pr = generate_pr(full_name, phone)
    db_cursor = conn.cursor()
    db_cursor.execute("INSERT INTO readers (pr, full_name, phone, age) VALUES (?, ?, ?, ?)",
                (pr, full_name, phone, age))
    conn.commit()
    print(f"читатель добавлен: {pr}")
    return pr

def delete_reader(conn, pr):
    db_cursor = conn.cursor()
    db_cursor.execute("SELECT 1 FROM loans WHERE pr=?", (pr,))
    if db_cursor.fetchone():
        print("у читателя есть книги")
        return
    db_cursor.execute("SELECT 1 FROM holds WHERE pr=?", (pr,))
    if db_cursor.fetchone():
        print("у читателя есть брони")
        return
    db_cursor.execute("DELETE FROM readers WHERE pr=?", (pr,))
    conn.commit()
    print("читатель удален")
