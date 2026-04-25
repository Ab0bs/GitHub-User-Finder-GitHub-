import tkinter as tk
from tkinter import ttk, messagebox
from api_client import GitHubAPIClient
from favorites import FavoritesManager

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("800x600")

        self.setup_ui()

    def setup_ui(self):
        # Поле поиска
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=20, fill='x')

        ttk.Label(search_frame, text="Поиск пользователя:").pack(side='left')
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Найти", command=self.search_users).pack(side='left')

        # Список результатов
        results_frame = ttk.LabelFrame(self.root, text="Результаты поиска")
        results_frame.pack(pady=10, padx=20, fill='both', expand=True)

        columns = ('login', 'name', 'company', 'location')
        self.tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150)

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.tree.bind('<Double-1>', self.on_double_click)

        # Кнопки избранного
        fav_frame = ttk.Frame(self.root)
        fav_frame.pack(pady=5, padx=20, fill='x')
        ttk.Button(fav_frame, text="Добавить в избранное", command=self.add_to_favorites).pack(side='left', padx=5)
        ttk.Button(fav_frame, text="Показать избранное", command=self.show_favorites).pack(side='left', padx=5)

        # Область избранного
        self.fav_listbox = tk.Listbox(self.root, height=8)
        self.fav_listbox.pack(pady=10, padx=20, fill='x')

    def search_users(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Поле поиска не может быть пустым!")
            return

        users, error = GitHubAPIClient.search_users(username)
        if error:
            messagebox.showerror("Ошибка API", error)
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        for user in users[:10]:  # Ограничиваем 10 результатами
            self.tree.insert('', 'end', values=(
                user.get('login', ''),
                user.get('name', ''),
                user.get('company', ''),
                user.get('location', '')
            ))

    def on_double_click(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            login = values[0]
            name = values[1]
            messagebox.showinfo("Информация", f"Логин: {login}\nИмя: {name}")

    def add_to_favorites(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите пользователя из списка!")
            return

        item = self.tree.item(selection[0])
        values = item['values']
        user_data = {
            'login': values[0],
            'name': values[1],
            'company': values[2],
            'location': values[3]
        }

        if FavoritesManager.add_favorite(user_data):
            messagebox.showinfo("Успех", f"{values[0]} добавлен в избранное!")
        else:
            messagebox.showwarning("Внимание", "Пользователь уже в избранном!")

    def show_favorites(self):
        favorites = FavoritesManager.load_favorites()
        self.fav_listbox.delete(0, tk.END)
        for user in favorites:
            self.fav_listbox.insert(tk.END, f"{user['login']} ({user.get('name', 'N/A')})")

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
