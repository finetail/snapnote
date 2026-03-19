"""Desktop GUI for snapnote using tkinter."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from snapnote.models import Note
from snapnote.store import NoteStore


class SnapnoteApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.store = NoteStore()
        self.title("snapnote")
        self.geometry("800x560")
        self.minsize(600, 400)
        self.configure(bg="#1e1e2e")
        self._build_ui()
        self._refresh_list()

    # ------------------------------------------------------------------ layout

    def _build_ui(self) -> None:
        self._build_input_panel()
        self._build_search_bar()
        self._build_list()
        self._build_status_bar()

    def _build_input_panel(self) -> None:
        frame = tk.Frame(self, bg="#1e1e2e", pady=10, padx=12)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="メモ", bg="#1e1e2e", fg="#cdd6f4",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky=tk.W)
        self._note_var = tk.StringVar()
        self._note_entry = tk.Entry(
            frame, textvariable=self._note_var,
            font=("Segoe UI", 11), bg="#313244", fg="#cdd6f4",
            insertbackground="#cdd6f4", relief=tk.FLAT, bd=4,
        )
        self._note_entry.grid(row=1, column=0, sticky=tk.EW, ipady=4)
        self._note_entry.bind("<Return>", lambda _: self._add_note())

        tk.Label(frame, text="タグ (カンマ区切り)", bg="#1e1e2e", fg="#cdd6f4",
                 font=("Segoe UI", 9), padx=8).grid(row=0, column=1, sticky=tk.W)
        self._tag_var = tk.StringVar()
        self._tag_entry = tk.Entry(
            frame, textvariable=self._tag_var, width=22,
            font=("Segoe UI", 11), bg="#313244", fg="#cdd6f4",
            insertbackground="#cdd6f4", relief=tk.FLAT, bd=4,
        )
        self._tag_entry.grid(row=1, column=1, sticky=tk.EW, ipady=4, padx=8)
        self._tag_entry.bind("<Return>", lambda _: self._add_note())

        add_btn = tk.Button(
            frame, text="追加", command=self._add_note,
            bg="#89b4fa", fg="#1e1e2e", font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT, padx=14, cursor="hand2",
        )
        add_btn.grid(row=1, column=2, ipady=4)

        frame.columnconfigure(0, weight=1)

    def _build_search_bar(self) -> None:
        frame = tk.Frame(self, bg="#181825", padx=12, pady=6)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="🔍", bg="#181825", fg="#6c7086",
                 font=("Segoe UI", 11)).pack(side=tk.LEFT)

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._refresh_list())
        search_entry = tk.Entry(
            frame, textvariable=self._search_var,
            font=("Segoe UI", 10), bg="#181825", fg="#cdd6f4",
            insertbackground="#cdd6f4", relief=tk.FLAT, bd=0,
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2, padx=4)

        tk.Button(
            frame, text="クリア", command=self._clear_search,
            bg="#181825", fg="#6c7086", font=("Segoe UI", 9),
            relief=tk.FLAT, cursor="hand2",
        ).pack(side=tk.RIGHT)

    def _build_list(self) -> None:
        frame = tk.Frame(self, bg="#1e1e2e")
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 4))

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Notes.Treeview",
                        background="#181825", foreground="#cdd6f4",
                        fieldbackground="#181825", rowheight=28,
                        font=("Segoe UI", 10))
        style.configure("Notes.Treeview.Heading",
                        background="#313244", foreground="#89b4fa",
                        font=("Segoe UI", 9, "bold"), relief=tk.FLAT)
        style.map("Notes.Treeview",
                  background=[("selected", "#45475a")],
                  foreground=[("selected", "#cdd6f4")])

        self._tree = ttk.Treeview(
            frame,
            columns=("id", "date", "tags", "body"),
            show="headings",
            style="Notes.Treeview",
            selectmode="browse",
        )
        self._tree.heading("id",   text="ID",       anchor=tk.W)
        self._tree.heading("date", text="日付",     anchor=tk.W)
        self._tree.heading("tags", text="タグ",     anchor=tk.W)
        self._tree.heading("body", text="メモ",     anchor=tk.W)
        self._tree.column("id",   width=75,  stretch=False)
        self._tree.column("date", width=90,  stretch=False)
        self._tree.column("tags", width=130, stretch=False)
        self._tree.column("body", width=400)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL,
                                  command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        btn_frame = tk.Frame(self, bg="#1e1e2e", padx=12, pady=4)
        btn_frame.pack(fill=tk.X)
        tk.Button(
            btn_frame, text="削除", command=self._delete_selected,
            bg="#f38ba8", fg="#1e1e2e", font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT, padx=10, cursor="hand2",
        ).pack(side=tk.RIGHT)

    def _build_status_bar(self) -> None:
        self._status_var = tk.StringVar()
        bar = tk.Label(
            self, textvariable=self._status_var,
            bg="#181825", fg="#6c7086", font=("Segoe UI", 8),
            anchor=tk.W, padx=12, pady=3,
        )
        bar.pack(fill=tk.X, side=tk.BOTTOM)

    # ------------------------------------------------------------------ actions

    def _add_note(self) -> None:
        body = self._note_var.get().strip()
        if not body:
            self._note_entry.focus_set()
            return
        raw_tags = self._tag_var.get().strip()
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
        note = Note.new(body, tags=tags)
        self.store.save(note)
        self._note_var.set("")
        self._tag_var.set("")
        self._note_entry.focus_set()
        self._refresh_list()
        self._set_status(f"メモを保存しました: {note.id[:8]}")

    def _delete_selected(self) -> None:
        selected = self._tree.selection()
        if not selected:
            return
        note_id = self._tree.item(selected[0], "values")[0]
        if not messagebox.askyesno("確認", f"メモ {note_id} を削除しますか？"):
            return
        self.store.delete(note_id)
        self._refresh_list()
        self._set_status(f"削除しました: {note_id}")

    def _clear_search(self) -> None:
        self._search_var.set("")

    # ------------------------------------------------------------------ helpers

    def _refresh_list(self) -> None:
        query = self._search_var.get().strip()
        if query:
            notes = self.store.search(query)
        else:
            notes = self.store.list_notes(limit=200)

        for row in self._tree.get_children():
            self._tree.delete(row)

        for note in notes:
            self._tree.insert("", tk.END, values=(
                note.id[:8],
                note.created_at.strftime("%Y-%m-%d"),
                ", ".join(note.tags) if note.tags else "—",
                note.body,
            ))

        count = len(notes)
        label = f"検索結果: {count} 件" if query else f"{count} 件のメモ"
        self._set_status(label)

    def _set_status(self, msg: str) -> None:
        self._status_var.set(msg)


def main() -> None:
    import sys
    import traceback
    from pathlib import Path

    # exe と同じフォルダの logs/ ディレクトリにログを出力
    if getattr(sys, "frozen", False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).parent
    log_dir = base_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / "snapnote-error.log"

    # Windows DPI awareness (高解像度ディスプレイ対応)
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    try:
        app = SnapnoteApp()
        app.mainloop()
    except Exception:
        err = traceback.format_exc()
        log_path.write_text(err, encoding="utf-8")
        try:
            messagebox.showerror("エラー", err)
        except Exception:
            pass
        sys.exit(1)
