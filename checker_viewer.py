#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from checker import InstaUnfollowChecker

class InstaUnfollowCheckerViewer(tk.Frame):
    def __init__(self, master, width=400, height=600):
        self.filepath: str = ""
        self.unfollowers: list[str] = []
        self.check_vars = {}

        super().__init__(master)
        master.title("Insta Unfollow Checker Viewer")
        master.geometry(f"{width}x{height}")
        self.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self) -> None:
        # Top grey bar
        top_frame = tk.Frame(self, bg='grey', height=40)
        top_frame.pack(fill=tk.X)

        open_zip_btn = tk.Button(top_frame, text="Open Zip", command=self.open_zip)
        open_zip_btn.pack(padx=10, pady=5, side=tk.LEFT)

        # Treeview and Scrollbar
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_scroll = tk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Users"), show="headings", yscrollcommand=self.tree_scroll.set)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.heading("Users", text="Users")
        self.tree.column("Users", width=200, anchor="center")

        self.tree_scroll.config(command=self.tree.yview)

        # Del key binding for deleting entries
        self.tree.bind("<Delete>", self.delete_selected_entry)

    def delete_selected_entry(self, event) -> None:
        """
        Deletes the currently selected entries when the Delete key is pressed.
        """

        # Get the selected items
        selected_items = self.tree.selection()

        # Loop through all the selected items
        for item_id in selected_items:
            # Remove the current item from the Treeview
            self.tree.delete(item_id)

    def get_unfollowers(self) -> list[str]:
        checker = InstaUnfollowChecker(
            self.filepath,
            "",
            False,
            False,
            False,
            True
        )
        return checker.run()

    def open_zip(self) -> None:
        self.filepath = filedialog.askopenfilename(title="Select a Zip file", filetypes=[("Zip files", "*.zip")])
        self.unfollowers = self.get_unfollowers()
        self.populate_table()

    def populate_table(self) -> None:
        # Clear previous data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Populate table
        for user in self.unfollowers:
            var = tk.BooleanVar()
            self.check_vars[user] = var
            self.tree.insert("", "end", values=(user, ""), tags=(user,))
            self.tree.item(self.tree.get_children()[-1], open=True)


if __name__ == "__main__":
    # Initialize the main application window
    root = tk.Tk()

    InstaUnfollowCheckerViewer(root).mainloop()
