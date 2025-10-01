import db
import repo
import service
import sqlite3

def main():
    # Создание или подключение к базе данных
    db.create_tables()
    conn = db.connect("library.db")
    print("База данных успешно настроена!")

    while True:
        print("\nДоступные действия:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Добавить читателя")
        print("4. Удалить читателя")
        print("5. Забронировать книгу")
        print("6. Снять бронь")
        print("7. Взять книгу домой")
        print("8. Вернуть книгу")
        print("9. Показать книги, взятые читателем")
        print("10. Показать забронированные читателем книги")
        print("11. Просмотреть список просроченных книг")
        print("12. Автоматически сбросить бронь")
        print("13. Поиск книг")
        print("0. Выход")

        choice = input("\nВведите номер действия: ").strip()

        try:
            if choice == "1":
                title = input("Введите название книги: ").strip()
                author = input("Введите автора книги: ").strip()
                genre = input("Введите жанр книги: ").strip()
                total = int(input("Введите количество экземпляров: ").strip())
                repo.add_book(conn, title, author, genre, total)
                print("Книга успешно добавлена!")

            elif choice == "2":
                title = input("Введите название книги: ").strip()
                author = input("Введите автора книги: ").strip()
                repo.delete_book(conn, title, author)
                print("Книга успешно удалена!")

            elif choice == "3":
                full_name = input("Введите ФИО читателя: ").strip()
                phone = input("Введите телефон читателя: ").strip()
                age = int(input("Введите возраст читателя: ").strip())
                repo.add_reader(conn, full_name, phone, age)
                print("Читатель успешно добавлен!")

            elif choice == "4":
                pr = input("Введите номер читательского билета: ").strip()
                repo.delete_reader(conn, pr)
                print("Читатель успешно удалён!")

            elif choice == "5":
                pr = input("Введите номер читательского билета: ").strip()
                title = input("Введите название книги: ").strip()
                author = input("Введите автора книги: ").strip()
                service.hold_book(conn, pr, title, author)
                print("Книга успешно забронирована!")

            elif choice == "6":
                pr = input("Введите номер читательского билета: ").strip()
                title = input("Введите название книги: ").strip()
                author = input("Введите автора книги: ").strip()
                service.unhold_book(conn, pr, title, author)
                print("Бронь успешно снята!")

            elif choice == "7":
                pr = input("Введите номер читательского билета: ").strip()
                title = input("Введите название книги: ").strip()
                author = input("Введите автора книги: ").strip()
                service.borrow_book(conn, pr, title, author)
                print("Книга успешно взята на дом!")

            elif choice == "8":
                pr = input("Введите номер читательского билета: ").strip()
                title = input("Введите название книги: ").strip()
                author = input("Введите автора книги: ").strip()
                service.return_book(conn, pr, title, author)
                print("Книга успешно возвращена!")

            elif choice == "9":
                pr = input("Введите номер читательского билета: ").strip()
                books = service.get_loans_by_reader(conn, pr)
                print("\nВзятые книги:")
                for book in books:
                    print(f"Название: {book['title']}, Автор: {book['author']}, Дата: {book['date']}")
                print("Конец списка.")

            elif choice == "10":
                pr = input("Введите номер читательского билета: ").strip()
                books = service.get_holds_by_reader(conn, pr)
                print("\nЗабронированные книги:")
                for book in books:
                    print(f"Название: {book['title']}, Автор: {book['author']}, Дата брони: {book['date']}")
                print("Конец списка.")

            elif choice == "11":
                overdue_books = service.get_overdue_books(conn)
                print("\nПросроченные книги:")
                for book in overdue_books:
                    print(f"Читатель: {book['full_name']}, Книга: {book['title']}, Автор: {book['author']}, Дата сдачи: {book['date_return']}")
                print("Конец списка.")

            elif choice == "12":
                service.auto_reset_holds(conn)
                print("Автосброс всех просроченных броней выполнен!")

            elif choice == "13":
                title = input("Введите название книги (если нужно): ").strip() or None
                author = input("Введите автора книги (если нужно): ").strip() or None
                genre = input("Введите жанр книги (если нужно): ").strip() or None
                results = service.search_books(conn, title, author, genre)
                print("\nНайденные книги:")
                for book in results:
                    print(f"Название: {book['title']}, Автор: {book['author']}, Жанр: {book['genre']}, Всего: {book['total']}, Свободных: {book['free']}")
                print("Конец списка.")

            elif choice == "0":
                print("Завершение работы.")
                break

            else:
                print("Неверный ввод. Попробуйте снова.")

        except Exception as e:
            print(f"Ошибка: {e}")

    conn.close()

if __name__ == "__main__":
    main()