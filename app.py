import db
import repo
import service

def main():
    conn = db.connect()
    db.create_tables(conn)
    repo.add_book(conn, "Война и мир", "Толстой", "Роман", 2)
    repo.add_book(conn, "Преступление и наказание", "Достоевский", "Роман", 1)
    pr = repo.add_reader(conn, "Иван Иванов", "89991112233", 25)
    service.hold_book(conn, pr, "Война и мир", "Толстой", "01/10/25")
    service.loan_book(conn, pr, "Война и мир", "Толстой", "02/10/25")
    service.return_book(conn, pr, "Война и мир", "Толстой")
    print("Книги на руках:", service.get_loans_by_reader(conn, pr))
    print("Забронированные:", service.get_holds_by_reader(conn, pr))
    print("Поиск по жанру 'Роман':", service.search(conn, genre="Роман"))

if __name__ == "__main__":
    main()