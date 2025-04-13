#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox
from checker import InstaUnfollowChecker
import webbrowser

insta_url = "https://www.instagram.com/"
program_name = "Instagram Unfollow Checker Viewer"


class InstaUnfollowCheckerViewer(tk.Frame):
    """
    InstaUnfollowCheckerViewer is a Tkinter-based GUI application
    that allows users to manage and view their Instagram unfollowers.
    The application provides the following functionalities:

    - Load Instagram data from a ZIP file containing user information.
    - Display a list of unfollowers in a Treeview widget.
    - Remove selected users from the list.
    - Save the list of unfollowers to a file.
    - Open selected user profiles directly in a web browser.
    """

    def __init__(self, master, width=400, height=600):
        self.filepath = ""
        self.unfollowers = []
        self.check_vars = {}
        self.visit_btn = None
        self.created_buttons = False

        super().__init__(master)
        master.title(program_name)
        master.geometry(f"{width}x{height}")
        self.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self) -> None:
        # Top dark bar
        self.top_frame = tk.Frame(self, bg='#3C3C3C', height=40)
        self.top_frame.pack(fill=tk.X)

        # Treeview and Scrollbar

        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_scroll = tk.Scrollbar(
                self.tree_frame, bg='#3C3C3C', troughcolor='#2E2E2E'
            )  # Dark scrollbar
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure Treeview style for dark mode
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme for better customization
        style.configure(
                "Treeview",
                background="#2E2E2E",
                foreground="white",
                fieldbackground="#2E2E2E"
            )
        style.configure(
                "Treeview.Heading",
                background="#3C3C3C",
                foreground="white"
            )

        self.tree = ttk.Treeview(
                self.tree_frame, columns=("Users"), show="headings",
                yscrollcommand=self.tree_scroll.set
            )
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.heading("Users", text="Users")
        self.tree.column("Users", width=200, anchor="center")

        self.tree_scroll.config(command=self.tree.yview)

        self.create_button(
            "Open",
            self.open_zip,
            "Click to open the ZIP file\nwith the Instagram Data",
            "left"
        )

        self.create_button(
            "Load",
            self.load_list_from_file,
            "Click to load list from a file",
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
            # Update the unfollowers list
            username = self.tree.item(item_id, "values")[0]
            self.unfollowers.remove(username)

            # Remove the current item from the Treeview
            self.tree.delete(item_id)

    def get_unfollowers(self) -> None | list[str]:
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
            url = f"{insta_url}{username}/"
            try:
                webbrowser.open(url)
            except Exception as e:
                messagebox.showerror("Error", f"Error opening browser: {e}")

    def open_zip(self) -> None:
        """
        Open the ZIP file containing the Instagram Data
        """
        # Open the ZIP file by selecting it from the file dialog
        self.filepath = filedialog.askopenfilename(
                title="Select a Zip file",
                filetypes=[("Zip files", "*.zip")]
            )
        if not self.filepath:
            return

        self.unfollowers = self.get_unfollowers()
        if not self.unfollowers:
            messagebox.showerror("Error", "Unfollowers list is empty")
            return

        # Add users on the Tree
        self.populate_table()

        # Only create buttons if not created already
        if not self.created_buttons:
            self.create_buttons_to_handle_list()
            self.created_buttons = True

    def load_list_from_file(self) -> None:
        """
        Open a file containing a list of usernames
        """
        # Open the file by selecting it from the file dialog
        filepath = filedialog.askopenfilename(
                title="Select a file",
                filetypes=[("txt files", "*.txt")]
            )
        if not filepath:
            return

        try:
            with open(filepath, 'r') as file:
                self.unfollowers = []  # Reset the array
                file_content = file.read()  # Get the content of the file
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")

        for username in file_content.splitlines():
            self.unfollowers.append(username.strip())

        self.populate_table()  # Add the unfollowers to the Tree
        # Only create buttons if not created already
        if not self.created_buttons:
            self.create_buttons_to_handle_list()

    def save_list_to_file(self):
        # Open a file dialog to ask for the save location and filename
        filepath = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",  # Default file extension
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        # Check if the user canceled the dialog
        if not filepath:
            return  # Exit the function if no file was selected

        try:
            with open(filepath, 'w') as file:
                # Loop through all items in the Treeview
                for username in self.unfollowers:
                    file.write(f"{username}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error while saving data: {e}")
            return  # Exit the function if an error occurred

        messagebox.showinfo(
            "Information", f"Saved list to {filepath}."
        )

    def create_buttons_to_handle_list(self) -> None:
        self.create_button(
            "Save",
            self.save_list_to_file,
            "Click to save the list to a file",
            "right"
            )

        self.create_button(
            "Remove",
            self.remove_selected_entry,
            "Click to remove the selected\naccount from the list",
            "right"
            )

        self.create_button(
            "Visit",
            self.open_profile,
            "Click to visit the account\nin your web browser",
            "right"
            )

    def create_button(
                self, text: str, cmd, description: str, side: str
            ) -> None:
        btn = tk.Button(
                self.top_frame,
                text=text,
                command=cmd,
                bg='#3C3C3C',  # Dark background color for the button
                fg='white',     # Light text color for the button
                activebackground='#4C4C4C',  # Darker background when active
                activeforeground='white',     # Light text color when active
                borderwidth=1,
                relief='flat'   # Flat relief for a modern look
            )
        btn.pack(padx=10, pady=5, side=tk.LEFT)

        self.create_tooltip(
                btn,
                description,
                side
            )

    def create_tooltip(self, widget, text: str, side: str) -> None:
        """
        Create a tooltip for the given widget.
        """
        tooltip = tk.Label(
                self, text=text, background="lightyellow", relief="solid",
                bd=1, padx=5, pady=2
            )
        tooltip.place_forget()  # Hide the tooltip initially

        offsetx = 110 if side == "right" else -10

        def show_tooltip(event):
            tooltip.place(  # Position near the cursor
                    x=event.x_root - offsetx,
                    y=event.y_root - 20
                )

        def hide_tooltip(event):
            tooltip.place_forget()  # Hide the tooltip when mouse leaves

        widget.bind("<Enter>", show_tooltip)  # Show when mouse enters widget
        widget.bind("<Leave>", hide_tooltip)  # Hide when mouse leaves widget

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
