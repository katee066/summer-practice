import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CosmeticsAnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ косметики")
        self.root.geometry("1000x700")

        self.df = None
        self.filtered_df = None

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, pady=5)

        self.load_button = ttk.Button(self.top_frame, text="Загрузить CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.info_button = ttk.Button(self.top_frame, text="Информация о данных", command=self.show_data_info)
        self.info_button.pack(side=tk.LEFT, padx=5)

        self.recommend_button = ttk.Button(self.top_frame, text="Рекомендации", command=self.show_recommendations)
        self.recommend_button.pack(side=tk.LEFT, padx=5)

        self.filter_frame = ttk.LabelFrame(self.main_frame, text="Фильтры")
        self.filter_frame.pack(fill=tk.X, pady=5)

        ttk.Label(self.filter_frame, text="Категория:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self.filter_frame, textvariable=self.category_var, state="readonly")
        self.category_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self.filter_frame, text="Цена до:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(self.filter_frame, textvariable=self.price_var)
        self.price_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self.filter_frame, text="Бренд:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.brand_var = tk.StringVar()
        self.brand_combobox = ttk.Combobox(self.filter_frame, textvariable=self.brand_var, state="readonly")
        self.brand_combobox.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)

        self.apply_button = ttk.Button(self.filter_frame, text="Применить фильтры", command=self.apply_filters)
        self.apply_button.grid(row=1, column=0, columnspan=6, padx=5, pady=5)

        self.display_frame = ttk.Frame(self.main_frame)
        self.display_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_frame = ttk.Frame(self.display_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.graph_frame = ttk.Frame(self.display_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def load_csv(self):
        try:
            self.df = pd.read_csv('cosmetics_clear.csv')

            categories = sorted(self.df['label'].dropna().unique())
            brands = sorted(self.df['brand'].dropna().unique())

            self.category_combobox['values'] = categories
            self.brand_combobox['values'] = brands

            self.status_var.set(f"Данные загружены. Записей: {len(self.df)}")
            self.show_data_in_table(self.df)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")

    def show_data_info(self):
        if self.df is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите данные")
            return

        info_window = tk.Toplevel(self.root)
        info_window.title("Информация о данных")
        info_window.geometry("600x400")

        info_text = tk.Text(info_window, wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        info = []
        info.append(f"Всего записей: {len(self.df)}")
        info.append(f"Колонки: {', '.join(self.df.columns)}")
        info.append("\nОписательная статистика для числовых колонок:")

        numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            info.append(f"\n{col}:")
            info.append(f"  Среднее: {self.df[col].mean():.2f}")
            info.append(f"  Медиана: {self.df[col].median():.2f}")
            info.append(f"  Минимум: {self.df[col].min()}")
            info.append(f"  Максимум: {self.df[col].max()}")
            info.append(f"  Стандартное отклонение: {self.df[col].std():.2f}")

        info_text.insert(tk.END, "\n".join(info))
        info_text.config(state=tk.DISABLED)

    def apply_filters(self):
        if self.df is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите данные")
            return

        self.filtered_df = self.df.copy()

        try:
            category = self.category_var.get()
            if category:
                self.filtered_df = self.filtered_df[self.filtered_df['label'] == category]

            price = self.price_var.get()
            if price:
                self.filtered_df = self.filtered_df[self.filtered_df['price'] <= float(price)]

            brand = self.brand_var.get()
            if brand:
                self.filtered_df = self.filtered_df[self.filtered_df['brand'] == brand]

            self.status_var.set(f"Найдено записей: {len(self.filtered_df)}")
            self.show_data_in_table(self.filtered_df)
            self.show_graphs(self.filtered_df)

        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте правильность введенных значений фильтров")

    def show_data_in_table(self, df):
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"

        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.W)

        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def show_graphs(self, df):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        if len(df) == 0:
            return

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        soft_pink = '#f8c8dc'

        axes[0, 0].hist(df['price'], bins=20, color=soft_pink, edgecolor='black')
        axes[0, 0].set_title('Распределение цен')
        axes[0, 0].set_xlabel('Цена')
        axes[0, 0].set_ylabel('Количество продуктов')
        axes[0, 0].grid(axis='y', alpha=0.5)

        if 'rank' in df.columns:
            axes[0, 1].scatter(df['price'], df['rank'], color=soft_pink, edgecolor='black', alpha=0.8, s=60)
            axes[0, 1].set_title('Цена vs Рейтинг')
            axes[0, 1].set_xlabel('Цена')
            axes[0, 1].set_ylabel('Рейтинг')
            axes[0, 1].grid(alpha=0.3)

        if 'label' in df.columns:
            df.boxplot(column='price', by='label', ax=axes[1, 0], patch_artist=True, boxprops=dict(facecolor=soft_pink))
            axes[1, 0].set_title('Цена по категориям')
            axes[1, 0].set_xlabel('Категория')
            axes[1, 0].set_ylabel('Цена')
            axes[1, 0].tick_params(axis='x', rotation=45)

        if 'ingredients' in df.columns:
            from collections import Counter

            all_ingredients = df['ingredients'].dropna().str.split(',').sum()
            all_ingredients = [i.strip().capitalize() for i in all_ingredients if i.strip()]
            top_ingredients = Counter(all_ingredients).most_common(10)

            if top_ingredients:
                labels, values = zip(*top_ingredients)
                axes[1, 1].bar(labels, values, color=soft_pink, edgecolor='black')
                axes[1, 1].set_title('Топ-10 ингредиентов')
                axes[1, 1].set_ylabel('Частота')
                axes[1, 1].tick_params(axis='x', rotation=45)

        fig.suptitle("Графики по косметике", fontsize=14)
        fig.tight_layout()
        fig.subplots_adjust(top=0.9)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_recommendations(self):
        if self.df is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите данные")
            return

        rec_window = tk.Toplevel(self.root)
        rec_window.title("Рекомендации")
        rec_window.geometry("800x600")

        text = tk.Text(rec_window, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        top_products = self.df.sort_values(by='rank', ascending=False).head(5)
        recommendation = "Рекомендуемые продукты:\n"
        for _, row in top_products.iterrows():
            recommendation += f"- {row['brand']} - {row['name']} (Рейтинг: {row['rank']})\n"

        text.insert('1.0', recommendation)
        text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CosmeticsAnalyticsApp(root)
    root.mainloop()