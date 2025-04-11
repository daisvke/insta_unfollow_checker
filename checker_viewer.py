#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from checker import InstaUnfollowChecker
import webbrowser

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
        self.top_frame = tk.Frame(self, bg='grey', height=40)
        self.top_frame.pack(fill=tk.X)

        # Button to open ZIP file
        open_zip_btn = tk.Button(self.top_frame, text="Open Zip", command=self.open_zip)
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

        # Bind the hover events to show/hide tooltip
        self.create_tooltip(
            open_zip_btn,
            "Click to open the ZIP file\nwith the Instagram Data",
            "left"
            )

        # Del key binding for deleting entries
        self.tree.bind("<Delete>", self.remove_selected_entry)

    def remove_selected_entry(self, event=None) -> None:
        """
        Removes the currently selected entries when the Delete key is pressed.
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


    def open_profile(self) -> None:
        """
        Opens the user's Instagram profile in the browser.
        """
        # Get the selected items
        selected_items = self.tree.selection()

        # Loop through all the selected items
        for item_id in selected_items:
            username = self.tree.item(item_id, "values")[0] 
            url = f"https://www.instagram.com/{username}/"
            webbrowser.open(url)

    def open_zip(self) -> None:
        self.filepath = filedialog.askopenfilename(title="Select a Zip file", filetypes=[("Zip files", "*.zip")])
        self.unfollowers = self.get_unfollowers()
        self.populate_table()

        # Button to visit the selected user's account
        visit_btn = tk.Button(self.top_frame, text="Visit Account", command=self.open_profile)
        visit_btn.pack(padx=10, pady=5, side=tk.LEFT)

        # Button to delete the selected account from the list
        remove_btn = tk.Button(self.top_frame, text="Remove", command=self.remove_selected_entry)
        remove_btn.pack(padx=10, pady=5, side=tk.LEFT)

        # Bind the hover events to show/hide tooltip
        self.create_tooltip(
                visit_btn,
                "Click to visit the account\nin your web browser",
                "right"
            )
        self.create_tooltip(
                remove_btn,
                "Click to remove the selected\naccount from the list",
                "right"
            )

    def create_tooltip(self, widget, text: str, side: str) -> None:
        """
        Create a tooltip for the given widget.
        """
        tooltip = tk.Label(self, text=text, background="lightyellow", relief="solid", bd=1, padx=5, pady=2)
        tooltip.place_forget()  # Hide the tooltip initially

        offsetx = 110 if side == "right" else -10

        def show_tooltip(event):
            tooltip.place(  # Position near the cursor
                    x=event.x_root - offsetx,
                    y=event.y_root - 20
                )

        def hide_tooltip(event):
            tooltip.place_forget()  # Hide the tooltip when mouse leaves

        widget.bind("<Enter>", show_tooltip)  # Show tooltip when mouse enters the widget
        widget.bind("<Leave>", hide_tooltip)  # Hide tooltip when mouse leaves the widget

    def populate_table(self) -> None:
        # Clear previous data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Populate table
        for idx, user in enumerate(self.unfollowers):
            self.tree.insert("", "end", values=(user, ""), tags=(user,))
            self.tree.item(self.tree.get_children()[-1], open=True)


if __name__ == "__main__":
    # Initialize the main application window
    root = tk.Tk()

    InstaUnfollowCheckerViewer(root).mainloop()
