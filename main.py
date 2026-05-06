import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []
        self.load_data()

        # --- Создание виджетов ---
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(self.root, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(self.root, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Рейтинг (0-10):").grid(row=3, column=0, padx=5, pady=5)
        self.rating_entry = tk.Entry(self.root, width=30)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.add_btn = tk.Button(self.root, text="Добавить фильм", command=self.add_movie)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_genre = tk.Entry(self.root, width=30)
        self.filter_genre.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по году:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_year = tk.Entry(self.root, width=30)
        self.filter_year.grid(row=6, column=1, padx=5, pady=5)

        self.filter_btn = tk.Button(self.root, text="Применить фильтры", command=self.apply_filters)
        self.filter_btn.grid(row=7, column=0, columnspan=2, pady=10)

        # Таблица фильмов
        self.columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(self.root, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120)
        self.tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        if not title or not genre or not year or not rating:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        if not year.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return

        if not (rating.replace('.', '', 1).isdigit() and 0 <= float(rating) <= 10):
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
            return

        self.movies.append({
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": float(rating)
        })
        self.save_data()
        self.update_table()

    def apply_filters(self):
        genre_filter = self.filter_genre.get().strip().lower()
        year_filter = self.filter_year.get().strip()
        
        filtered = self.movies

        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["genre"].lower()]
        
        if year_filter and year_filter.isdigit():
            filtered = [m for m in filtered if m["year"] == int(year_filter)]
        
        self.display_movies(filtered)

    def update_table(self):
        self.display_movies(self.movies)

    def display_movies(self, movies_list):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for movie in movies_list:
            self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def save_data(self):
        os.makedirs("data", exist_ok=True)
        with open("data/movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists("data/movies.json"):
            with open("data/movies.json", "r", encoding="utf-8") as f:
                self.movies = json.load(f)