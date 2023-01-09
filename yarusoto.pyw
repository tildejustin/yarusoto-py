import ctypes
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import List, Optional


@dataclass
class TodoItem:
    name: str
    checked: Optional[tk.BooleanVar] = None


def add_todo(add_todo_text: ttk.Entry, todos_frame: ttk.Frame) -> None:
    """
    Add a new TodoItem to todo_list from the add_todo_text widget and re-renders the list.

    :param add_todo_text: ttk.Entry widget that hold the text that should be the new TodoItem
    :param todos_frame: The ttk.Frame that needs to be passed to update_todos to re-render the list
    """
    global todo_list

    todo_to_add: str = add_todo_text.get().strip()
    if len(todo_to_add) > 0:
        todo_list.append(TodoItem(todo_to_add))
        add_todo_text.delete(0, "end")
        update_todos(todos_frame, show_checked_var.get())


def update_todos(todos_frame: ttk.Frame, show_checked: bool) -> None:
    """
    Updates the todos_frame with the TodoItems in todo_list. This allows for hidden checkboxes to not be rendered.

    :param todos_frame: The ttk.Frame that should display the TodoItems
    """
    for old_todo in todos_frame.winfo_children():
        old_todo.destroy()
    for todo in todo_list:
        # check if [TodoItem].checked is None, so it can be initialized
        if todo.checked is None:
            # need to instantiate tk var here because if it is done outside the class or
            # before tk is initialized the script crashes
            todo.checked = tk.BooleanVar()
        if not show_checked and todo.checked.get():
            continue
        else:
            ttk.Checkbutton(
                todos_frame,
                text=todo.name,
                variable=todo.checked,
                onvalue=True,
                offvalue=False,
                command=lambda: update_todos(todos_frame, show_checked_var.get())
            ).pack(anchor="w")


# global vars
todo_list: List[TodoItem] = []
show_checked_var: Optional[tk.BooleanVar] = None


def main() -> None:
    """
    Manages tk initialization and adds the non-dynamic widgets.
    """
    global todo_list, show_checked_var

    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    root.title("Yarusoto")
    root.geometry("400x600")

    # vars
    show_checked_var = tk.BooleanVar()

    # frames
    todos_frame: ttk.Frame = ttk.Frame(root)
    add_todo_frame: ttk.Frame = ttk.Frame(root)

    # widgets
    title_label: ttk.Label = ttk.Label(root, text="Welcome to Yarusoto!")
    show_checked: ttk.Checkbutton = ttk.Checkbutton(
        root,
        text="Show completed to-dos",
        variable=show_checked_var,
        onvalue=True,
        offvalue=False,
        command=lambda: update_todos(todos_frame, show_checked_var.get())
    )
    seperator: ttk.Separator = ttk.Separator(root, orient="horizontal")
    todos_label = ttk.Label(text="To-dos:")

    # add_todos_frame widgets
    add_todo_text: ttk.Entry = ttk.Entry(add_todo_frame, width=30)
    add_todo_button: ttk.Button = ttk.Button(
        add_todo_frame,
        text="Add",
        command=lambda: add_todo(add_todo_text, todos_frame)
    )
    root.bind("<Return>", lambda _: add_todo(add_todo_text, todos_frame))

    # pack
    title_label.pack()
    show_checked.pack()
    seperator.pack(fill="x", padx=5)
    todos_label.pack(anchor="w")

    todos_frame.pack(anchor="w")

    add_todo_text.pack(side="left")
    add_todo_button.pack(side="left")
    add_todo_frame.pack(side="bottom")

    # loop
    root.mainloop()


if __name__ == '__main__':
    main()
