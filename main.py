import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.favorites = self.load_favorites()

        # Поле ввода
        self.search_label = ttk.Label(root, text="Введите имя пользователя GitHub:")
        self.search_label.pack(pady=5)
        self.search_entry = ttk.Entry(root, width=30)
        self.search_entry.pack(pady=5)

        # Кнопка поиска
        self.search_button = ttk.Button(root, text="Найти", command=self.search_user)
        self.search_button.pack(pady=5)

        # Список результатов
        self.results_list = tk.Listbox(root, width=50, height=10)
        self.results_list.pack(pady=10)

        # Кнопка добавления в избранное
        self.add_favorite_button = ttk.Button(root, text="Добавить в избранное", command=self.add_to_favorites)
        self.add_favorite_button.pack(pady=5)

        # Список избранных
        self.favorites_label = ttk.Label(root, text="Избранные пользователи:")
        self.favorites_label.pack(pady=5)
        self.favorites_list = tk.Listbox(root, width=50, height=5)
        self.favorites_list.pack(pady=10)
        self.update_favorites_list()

    def search_user(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым!")
            return

        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)

        if response.status_code == 200:
            user_data = response.json()
            self.results_list.delete(0, tk.END)
            self.results_list.insert(tk.END, f"Имя: {user_data.get('name', 'Не указано')}")
            self.results_list.insert(tk.END, f"Логин: {user_data['login']}")
            self.results_list.insert(tk.END, f"Публичные репозитории: {user_data['public_repos']}")
            self.results_list.insert(tk.END, f"Подписчики: {user_data['followers']}")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден!")

    def add_to_favorites(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым!")
            return

        if username not in self.favorites:
            self.favorites.append(username)
            self.save_favorites()
            self.update_favorites_list()
            messagebox.showinfo("Успех", f"{username} добавлен в избранное!")
        else:
            messagebox.showwarning("Предупреждение", f"{username} уже в избранном!")

    def load_favorites(self):
        if os.path.exists("favorites.json"):
            with open("favorites.json", "r") as f:
                return json.load(f)
        return []

    def save_favorites(self):
        with open("favorites.json", "w") as f:
            json.dump(self.favorites, f)

    def update_favorites_list(self):
        self.favorites_list.delete(0, tk.END)
        for user in self.favorites:
            self.favorites_list.insert(tk.END, user)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()

