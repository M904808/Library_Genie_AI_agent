
import sqlite3

# 1. Connect to the database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# 2. Create the books table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    available_copies INTEGER NOT NULL,
    times_borrowed INTEGER NOT NULL
)
""")

# 3. Create 32 sample books in 4 categories
books = [
    (1, "Physics Basics", "Ali Khan", "Science", 5, 20),
    (2, "Chemistry for Beginners", "Sara Ahmed", "Science", 0, 35),
    (3, "Biology Today", "Usman Malik", "Science", 3, 28),
    (4, "Space and Stars", "Ayesha Noor", "Science", 2, 42),
    (5, "Modern Science", "Hamza Ali", "Science", 4, 18),
    (6, "The Human Body", "Fatima Shah", "Science", 1, 30),
    (7, "World History", "Ahmed Raza", "History", 3, 25),
    (8, "Ancient Civilizations", "Sana Iqbal", "History", 2, 40),
    (9, "Pakistan History", "Bilal Ahmed", "History", 0, 32),
    (10, "The Roman Empire", "Zara Khan", "History", 4, 15),
    (11, "History of Asia", "Omar Farooq", "History", 2, 22),
    (12, "Great Leaders", "Hina Malik", "History", 1, 38),
    (13, "Python Programming", "Usman Tariq", "Technology", 5, 55),
    (14, "Artificial Intelligence", "Ayesha Ali", "Technology", 2, 48),
    (15, "Computer Networks", "Bilal Khan", "Technology", 0, 26),
    (16, "Web Development", "Sara Noor", "Technology", 3, 33),
    (17, "Data Science Basics", "Hamza Raza", "Technology", 4, 45),
    (18, "Cyber Security", "Fatima Ahmed", "Technology", 1, 29),
    (19, "Pride and Prejudice", "Jane Austen", "Literature", 3, 50),
    (20, "Great Expectations", "Charles Dickens", "Literature", 2, 37),
    (21, "Hamlet", "William Shakespeare", "Literature", 0, 31),
    (22, "The Old Man and the Sea", "Ernest Hemingway", "Literature", 4, 24),
    (23, "Oliver Twist", "Charles Dickens", "Literature", 1, 43),
    (24, "Animal Farm", "George Orwell", "Literature", 2, 46),
    (25, "Basic Mathematics", "Ali Raza", "Science", 3, 17),
    (26, "Earth and Environment", "Sana Ahmed", "Science", 2, 21),
    (27, "Medieval History", "Omar Khan", "History", 5, 19),
    (28, "Digital Technology", "Hina Noor", "Technology", 3, 36),
    (29, "Poetry Collection", "Maya Angelou", "Literature", 2, 27),
    (30, "Introduction to Robotics", "Bilal Raza", "Technology", 1, 41),
    (31, "World Literature", "Fatima Noor", "Literature", 4, 34),
    (32, "Environmental Science", "Ahmed Ali", "Science", 0, 39)
]

# 4. Insert the books into the table
cursor.executemany("""
INSERT OR REPLACE INTO books
(book_id, title, author, category, available_copies, times_borrowed)
VALUES (?, ?, ?, ?, ?, ?)
""", books)

# 5. Save and close the database
conn.commit()
conn.close()

print("Library database created successfully!")
print("Total books inserted: 32")
print("Categories: Science, History, Technology, Literature")
