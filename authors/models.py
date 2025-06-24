from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Author(BaseModel):
    id: int
    name: str
    biography: str
    birth_date: Optional[str]
    death_date: Optional[str]
    nationality: str
    genres: List[str]
    website: Optional[str]
    image: str
    awards: List[str]
    books: List[str]  # List of book titles by this author

AUTHORS = [
    Author(
        id=1,
        name="Khaled Hosseini",
        biography="Afghan-American novelist and physician, known for his powerful storytelling about Afghanistan.",
        birth_date="1965-03-04",
        death_date=None,
        nationality="Afghan-American",
        genres=["Literary Fiction", "Historical Fiction"],
        website="https://khaledhosseini.com",
        image="https://example.com/khaled_hosseini.jpg",
        awards=["Goodreads Choice Award", "South African Boeke Prize"],
        books=["The Kite Runner"]
    ),
    Author(
        id=2,
        name="Stephen Hawking",
        biography="Renowned theoretical physicist and cosmologist who made groundbreaking contributions to quantum mechanics and general relativity.",
        birth_date="1942-01-08",
        death_date="2018-03-14",
        nationality="British",
        genres=["Science", "Physics", "Cosmology"],
        website=None,
        image="https://example.com/stephen_hawking.jpg",
        awards=["Presidential Medal of Freedom", "Copley Medal", "Wolf Prize in Physics"],
        books=["A Brief History of Time"]
    ),
    Author(
        id=3,
        name="Yuval Noah Harari",
        biography="Israeli historian and professor, known for his books about human history and evolution.",
        birth_date="1976-02-24",
        death_date=None,
        nationality="Israeli",
        genres=["History", "Philosophy", "Science"],
        website="https://www.ynharari.com",
        image="https://example.com/yuval_harari.jpg",
        awards=["Polonsky Prize", "Deutscher Memorial Prize"],
        books=["Sapiens: A Brief History of Humankind"]
    ),
    Author(
        id=4,
        name="J.R.R. Tolkien",
        biography="English writer, poet, and philologist, creator of Middle-earth and modern fantasy literature.",
        birth_date="1892-01-03",
        death_date="1973-09-02",
        nationality="British",
        genres=["Fantasy", "Poetry", "Academic"],
        website=None,
        image="https://example.com/jrr_tolkien.jpg",
        awards=["Commander of the Order of the British Empire", "Locus Award"],
        books=["The Hobbit", "The Lord of the Rings"]
    ),
    Author(
        id=5,
        name="Harper Lee",
        biography="American novelist widely known for her Pulitzer Prize-winning novel.",
        birth_date="1926-04-28",
        death_date="2016-02-19",
        nationality="American",
        genres=["Southern Gothic", "Literary Fiction"],
        website=None,
        image="https://example.com/harper_lee.jpg",
        awards=["Pulitzer Prize", "Presidential Medal of Freedom"],
        books=["To Kill a Mockingbird"]
    ),
    Author(
        id=6,
        name="Richard Dawkins",
        biography="British evolutionary biologist and author, known for his work in evolutionary biology.",
        birth_date="1941-03-26",
        death_date=None,
        nationality="British",
        genres=["Science", "Biology", "Non-fiction"],
        website="https://richarddawkins.net",
        image="https://example.com/richard_dawkins.jpg",
        awards=["Royal Society of Literature Award", "Galaxy British Book Awards"],
        books=["The Selfish Gene"]
    ),
    Author(
        id=7,
        name="Walter Isaacson",
        biography="American writer and journalist, known for his biographical works.",
        birth_date="1952-05-20",
        death_date=None,
        nationality="American",
        genres=["Biography", "History"],
        website="https://walterisaacson.com",
        image="https://example.com/walter_isaacson.jpg",
        awards=["Benjamin Franklin Medal", "Pulitzer Prize finalist"],
        books=["Steve Jobs"]
    ),
    Author(
        id=8,
        name="George Orwell",
        biography="English novelist and essayist, known for his political satire and social commentary.",
        birth_date="1903-06-25",
        death_date="1950-01-21",
        nationality="British",
        genres=["Political Fiction", "Dystopian Fiction", "Essays"],
        website=None,
        image="https://example.com/george_orwell.jpg",
        awards=["Prometheus Hall of Fame Award"],
        books=["1984"]
    ),
    Author(
        id=9,
        name="Paulo Coelho",
        biography="Brazilian lyricist and novelist, known for his spiritual and philosophical works.",
        birth_date="1947-08-24",
        death_date=None,
        nationality="Brazilian",
        genres=["Fiction", "Philosophy", "Spirituality"],
        website="https://paulocoelhoblog.com",
        image="https://example.com/paulo_coelho.jpg",
        awards=["Crystal Award", "World Economic Forum"],
        books=["The Alchemist"]
    ),
    Author(
        id=10,
        name="F. Scott Fitzgerald",
        biography="American novelist and short story writer, known for his depictions of the Jazz Age.",
        birth_date="1896-09-24",
        death_date="1940-12-21",
        nationality="American",
        genres=["Literary Fiction", "Short Stories"],
        website=None,
        image="https://example.com/scott_fitzgerald.jpg",
        awards=["National Book Award finalist"],
        books=["The Great Gatsby"]
    ),
    Author(
        id=11,
        name="Daniel Kahneman",
        biography="Israeli psychologist and economist, Nobel Prize winner in Economic Sciences.",
        birth_date="1934-03-05",
        death_date=None,
        nationality="Israeli-American",
        genres=["Psychology", "Economics", "Non-fiction"],
        website=None,
        image="https://example.com/daniel_kahneman.jpg",
        awards=["Nobel Prize in Economic Sciences", "Presidential Medal of Freedom"],
        books=["Thinking, Fast and Slow"]
    ),
    Author(
        id=12,
        name="Tara Westover",
        biography="American memoirist and historian, known for her compelling personal story.",
        birth_date="1986-09-27",
        death_date=None,
        nationality="American",
        genres=["Memoir", "Autobiography"],
        website="https://tarawestover.com",
        image="https://example.com/tara_westover.jpg",
        awards=["Alex Award", "Goodreads Choice Award"],
        books=["Educated"]
    ),
    Author(
        id=13,
        name="Aldous Huxley",
        biography="English writer and philosopher, known for his dystopian and philosophical novels.",
        birth_date="1894-07-26",
        death_date="1963-11-22",
        nationality="British",
        genres=["Science Fiction", "Philosophy", "Essays"],
        website=None,
        image="https://example.com/aldous_huxley.jpg",
        awards=["Companion of Literature by the Royal Society of Literature"],
        books=["Brave New World"]
    ),
    Author(
        id=14,
        name="J.D. Salinger",
        biography="American writer known for his influential coming-of-age novel.",
        birth_date="1919-01-01",
        death_date="2010-01-27",
        nationality="American",
        genres=["Literary Fiction", "Short Stories"],
        website=None,
        image="https://example.com/jd_salinger.jpg",
        awards=["National Book Award nomination"],
        books=["The Catcher in the Rye"]
    ),
    Author(
        id=15,
        name="Charles Duhigg",
        biography="American journalist and non-fiction author, known for his work on habits and productivity.",
        birth_date="1974-01-01",
        death_date=None,
        nationality="American",
        genres=["Self-help", "Psychology", "Business"],
        website="https://charlesduhigg.com",
        image="https://example.com/charles_duhigg.jpg",
        awards=["Pulitzer Prize", "National Academies Communication Award"],
        books=["The Power of Habit"]
    ),
    Author(
        id=16,
        name="Anne Frank",
        biography="German-Dutch diarist of Jewish heritage, known for her wartime diary.",
        birth_date="1929-06-12",
        death_date="1945-02-01",
        nationality="German-Dutch",
        genres=["Diary", "Holocaust Literature"],
        website=None,
        image="https://example.com/anne_frank.jpg",
        awards=["Posthumous recognition worldwide"],
        books=["The Diary of a Young Girl"]
    ),
    Author(
        id=17,
        name="Mark Manson",
        biography="American self-help author and blogger, known for his direct writing style.",
        birth_date="1984-03-09",
        death_date=None,
        nationality="American",
        genres=["Self-help", "Personal Development"],
        website="https://markmanson.net",
        image="https://example.com/mark_manson.jpg",
        awards=["#1 New York Times Bestseller"],
        books=["The Subtle Art of Not Giving a F*ck"]
    ),
    Author(
        id=18,
        name="Markus Zusak",
        biography="Australian writer known for his unique narrative style and historical fiction.",
        birth_date="1975-06-23",
        death_date=None,
        nationality="Australian",
        genres=["Young Adult", "Historical Fiction"],
        website="https://www.markuszusak.com",
        image="https://example.com/markus_zusak.jpg",
        awards=["Michael L. Printz Award", "Commonwealth Writers' Prize"],
        books=["The Book Thief"]
    ),
    Author(
        id=19,
        name="Michelle Obama",
        biography="American attorney, author, and former First Lady of the United States.",
        birth_date="1964-01-17",
        death_date=None,
        nationality="American",
        genres=["Memoir", "Autobiography"],
        website="https://www.obama.org",
        image="https://example.com/michelle_obama.jpg",
        awards=["Grammy Award for Best Spoken Word Album"],
        books=["Becoming"]
    )
] 