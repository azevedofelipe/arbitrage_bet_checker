import customtkinter as ctk

def change_entry_text(entry: ctk.CTkEntry, text: str) -> None:
    if entry.cget('state') == 'readonly':
        entry.configure(state='normal')
        entry.delete(0,'end')
        entry.insert(-1,text)
        entry.configure(state='readonly')
    else:
        entry.delete(0,'end')
        entry.insert(-1,text)
