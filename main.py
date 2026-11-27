from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from pathlib import Path

from cryptographic_app.audit import write_event
from cryptographic_app.crypto_engine import decrypt_file, encrypt_file
from cryptographic_app.key_manager import KeyManager

APP_NAME = "Cryptographic Application 2.1"

# A restrained graphite palette: dark surfaces, soft text and one teal action colour.
C = {
    "root": "#111315",
    "sidebar": "#171a1d",
    "surface": "#1c2024",
    "surface_2": "#22272c",
    "surface_3": "#292f35",
    "border": "#30373e",
    "text": "#edf1f3",
    "muted": "#9aa5ad",
    "subtle": "#6f7b84",
    "accent": "#55c6b1",
    "accent_hover": "#3eaa97",
    "danger": "#e47777",
    "white": "#ffffff",
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1120x760")
        self.minsize(960, 660)
        self.configure(bg=C["root"])
        self.manager = KeyManager()
        self.active_page = "dashboard"
        self._style()
        self._build()
        self.refresh_profiles()
        self.show_page("dashboard")

    def _style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10), background=C["root"], foreground=C["text"])
        style.configure("TFrame", background=C["root"])
        style.configure("Panel.TFrame", background=C["surface"])
        style.configure("Inset.TFrame", background=C["surface_2"])
        style.configure("TLabel", background=C["root"], foreground=C["text"])
        style.configure("Muted.TLabel", background=C["root"], foreground=C["muted"])
        style.configure("Panel.TLabel", background=C["surface"], foreground=C["text"])
        style.configure("PanelMuted.TLabel", background=C["surface"], foreground=C["muted"])
        style.configure("PageTitle.TLabel", font=("Segoe UI", 23, "bold"), background=C["root"], foreground=C["text"])
        style.configure("SectionTitle.TLabel", font=("Segoe UI", 13, "bold"), background=C["surface"], foreground=C["text"])
        style.configure("Metric.TLabel", font=("Segoe UI", 25, "bold"), background=C["surface"], foreground=C["text"])
        style.configure("Small.TLabel", font=("Segoe UI", 9), background=C["surface"], foreground=C["muted"])
        style.configure("TButton", font=("Segoe UI", 10), padding=(13, 9), background=C["surface_3"], foreground=C["text"], borderwidth=0)
        style.map("TButton", background=[("active", "#343c43"), ("disabled", C["surface"])], foreground=[("disabled", C["subtle"])])
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(15, 10), background=C["accent"], foreground="#10201d")
        style.map("Accent.TButton", background=[("active", C["accent_hover"])], foreground=[("active", "#081512")])
        style.configure("Danger.TButton", background="#3a2527", foreground="#f0a0a0", padding=(12, 9))
        style.map("Danger.TButton", background=[("active", "#513033")])
        style.configure("TEntry", fieldbackground=C["surface_2"], foreground=C["text"], insertcolor=C["text"], bordercolor=C["border"], padding=10)
        style.configure("TCombobox", fieldbackground=C["surface_2"], background=C["surface_2"], foreground=C["text"], arrowcolor=C["muted"], padding=9)
        style.map("TCombobox", fieldbackground=[("readonly", C["surface_2"])], foreground=[("readonly", C["text"])])
        style.configure("Treeview", background=C["surface_2"], fieldbackground=C["surface_2"], foreground=C["text"], rowheight=38, borderwidth=0, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background=C["surface_3"], foreground=C["muted"], font=("Segoe UI", 9, "bold"), padding=10, relief="flat")
        style.map("Treeview", background=[("selected", "#28534d")], foreground=[("selected", C["white"])])
        style.configure("TNotebook", background=C["root"], borderwidth=0)
        style.configure("TNotebook.Tab", background=C["surface"], foreground=C["muted"], padding=(14, 9))
        style.map("TNotebook.Tab", background=[("selected", C["surface_2"])], foreground=[("selected", C["text"])])

    def _build(self):
        shell = tk.Frame(self, bg=C["root"])
        shell.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(shell, bg=C["sidebar"], width=224)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=C["sidebar"])
        brand.pack(fill="x", padx=22, pady=(27, 34))
        mark = tk.Label(brand, text="C", font=("Segoe UI", 17, "bold"), fg=C["accent"], bg=C["surface_3"], width=2, height=1)
        mark.pack(side="left", padx=(0, 11))
        brand_text = tk.Frame(brand, bg=C["sidebar"])
        brand_text.pack(side="left")
        tk.Label(brand_text, text="CRYPTOGRAPHIC", font=("Segoe UI", 9, "bold"), fg=C["text"], bg=C["sidebar"]).pack(anchor="w")
        tk.Label(brand_text, text="APPLICATION", font=("Segoe UI", 8), fg=C["muted"], bg=C["sidebar"]).pack(anchor="w", pady=(2, 0))

        tk.Label(self.sidebar, text="WORKSPACE", font=("Segoe UI", 8, "bold"), fg=C["subtle"], bg=C["sidebar"]).pack(anchor="w", padx=23, pady=(0, 10))
        self.nav_buttons = {}
        for key, label, glyph in [
            ("dashboard", "Overview", "◫"),
            ("encrypt", "Encrypt files", "↗"),
            ("decrypt", "Decrypt files", "↙"),
            ("keys", "Key management", "⌘"),
        ]:
            b = tk.Button(
                self.sidebar, text=f"  {glyph}    {label}", anchor="w",
                command=lambda page=key: self.show_page(page),
                font=("Segoe UI", 10), bd=0, relief="flat", padx=15, pady=12,
                bg=C["sidebar"], fg=C["muted"], activebackground=C["surface_3"],
                activeforeground=C["text"], cursor="hand2", highlightthickness=0,
            )
            b.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[key] = b

        spacer = tk.Frame(self.sidebar, bg=C["sidebar"])
        spacer.pack(fill="both", expand=True)
        tk.Frame(self.sidebar, bg=C["border"], height=1).pack(fill="x", padx=18, pady=(0, 14))
        tk.Label(self.sidebar, text="LOCAL ENCRYPTION", font=("Segoe UI", 8, "bold"), fg=C["accent"], bg=C["sidebar"]).pack(anchor="w", padx=22)
        tk.Label(self.sidebar, text="Your keys stay on this device.", font=("Segoe UI", 8), fg=C["subtle"], bg=C["sidebar"]).pack(anchor="w", padx=22, pady=(5, 22))

        content = tk.Frame(shell, bg=C["root"])
        content.pack(side="left", fill="both", expand=True)
        topbar = tk.Frame(content, bg=C["root"], height=66)
        topbar.pack(fill="x", padx=34, pady=(20, 0))
        topbar.pack_propagate(False)
        self.breadcrumb = tk.Label(topbar, text="WORKSPACE  /  OVERVIEW", font=("Segoe UI", 9, "bold"), fg=C["muted"], bg=C["root"])
        self.breadcrumb.pack(side="left", anchor="center")
        tk.Label(topbar, text="v2.1", font=("Segoe UI", 9), fg=C["subtle"], bg=C["root"]).pack(side="right", anchor="center")

        self.page_host = tk.Frame(content, bg=C["root"])
        self.page_host.pack(fill="both", expand=True, padx=34, pady=(10, 24))
        self.pages = {}
        self._build_dashboard()
        self._build_encrypt()
        self._build_decrypt()
        self._build_keys()

    def _page_header(self, parent, title, subtitle):
        tk.Label(parent, text=title, font=("Segoe UI", 23, "bold"), fg=C["text"], bg=C["root"]).pack(anchor="w")
        tk.Label(parent, text=subtitle, font=("Segoe UI", 10), fg=C["muted"], bg=C["root"]).pack(anchor="w", pady=(7, 22))

    def _panel(self, parent, padx=22, pady=20):
        panel = tk.Frame(parent, bg=C["surface"], highlightthickness=1, highlightbackground=C["border"])
        panel.pack(fill="x", pady=(0, 16))
        inner = tk.Frame(panel, bg=C["surface"])
        inner.pack(fill="both", expand=True, padx=padx, pady=pady)
        return inner

    def _build_dashboard(self):
        page = tk.Frame(self.page_host, bg=C["root"])
        self.pages["dashboard"] = page
        self._page_header(page, "Good to see you.", "Manage your keys and protect files from one place.")
        metrics = tk.Frame(page, bg=C["root"])
        metrics.pack(fill="x", pady=(0, 17))
        self.metric_profiles = self._metric(metrics, "KEY PROFILES", "0")
        self.metric_private = self._metric(metrics, "PRIVATE KEYS", "0")
        self.metric_algorithm = self._metric(metrics, "ENCRYPTION", "AES-256")
        quick = self._panel(page)
        tk.Label(quick, text="Quick actions", font=("Segoe UI", 13, "bold"), fg=C["text"], bg=C["surface"]).pack(anchor="w")
        tk.Label(quick, text="Choose what you want to do next.", font=("Segoe UI", 9), fg=C["muted"], bg=C["surface"]).pack(anchor="w", pady=(5, 17))
        actions = tk.Frame(quick, bg=C["surface"])
        actions.pack(fill="x")
        self._action_tile(actions, "Encrypt a file", "Protect a file using a recipient's public key.", "encrypt", 0)
        self._action_tile(actions, "Decrypt a file", "Restore a file using your private key.", "decrypt", 1)
        self._action_tile(actions, "Manage keys", "Create, import or back up key profiles.", "keys", 2)
        note = self._panel(page)
        tk.Label(note, text="SECURITY AT A GLANCE", font=("Segoe UI", 8, "bold"), fg=C["accent"], bg=C["surface"]).pack(anchor="w")
        tk.Label(note, text="Files are encrypted with AES-256-GCM. RSA-OAEP protects the encryption key. Authentication checks help detect tampering before decrypted content is saved.", font=("Segoe UI", 9), fg=C["muted"], bg=C["surface"], wraplength=760, justify="left").pack(anchor="w", pady=(9, 0))

    def _metric(self, parent, label, value):
        card = tk.Frame(parent, bg=C["surface"], highlightthickness=1, highlightbackground=C["border"])
        card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(card, text=label, font=("Segoe UI", 8, "bold"), fg=C["muted"], bg=C["surface"]).pack(anchor="w", padx=17, pady=(15, 4))
        value_label = tk.Label(card, text=value, font=("Segoe UI", 21, "bold"), fg=C["text"], bg=C["surface"])
        value_label.pack(anchor="w", padx=17, pady=(0, 15))
        return value_label

    def _action_tile(self, parent, title, description, page, column):
        tile = tk.Frame(parent, bg=C["surface_2"], highlightthickness=1, highlightbackground=C["border"])
        tile.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 7, 0 if column == 2 else 7))
        parent.grid_columnconfigure(column, weight=1)
        tk.Label(tile, text=title, font=("Segoe UI", 10, "bold"), fg=C["text"], bg=C["surface_2"]).pack(anchor="w", padx=14, pady=(14, 5))
        tk.Label(tile, text=description, font=("Segoe UI", 8), fg=C["muted"], bg=C["surface_2"], wraplength=190, justify="left").pack(anchor="w", padx=14)
        tk.Button(tile, text="Open  →", command=lambda: self.show_page(page), bd=0, relief="flat", cursor="hand2", bg=C["surface_2"], fg=C["accent"], activebackground=C["surface_2"], activeforeground=C["accent"], font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=14, pady=(12, 14))

    def _build_file_page(self, key, title, subtitle, decrypt=False):
        page = tk.Frame(self.page_host, bg=C["root"])
        self.pages[key] = page
        self._page_header(page, title, subtitle)
        panel = self._panel(page, padx=25, pady=24)
        tk.Label(panel, text="FILE", font=("Segoe UI", 8, "bold"), fg=C["muted"], bg=C["surface"]).pack(anchor="w")
        path_var = tk.StringVar()
        row = tk.Frame(panel, bg=C["surface"])
        row.pack(fill="x", pady=(8, 22))
        entry = ttk.Entry(row, textvariable=path_var)
        entry.pack(side="left", fill="x", expand=True, ipady=3)
        browse = ttk.Button(row, text="Browse files", command=(self.pick_decrypt if decrypt else self.pick_encrypt))
        browse.pack(side="left", padx=(9, 0))
        if decrypt:
            self.dec_path = path_var
            self.dec_entry = entry
        else:
            self.enc_path = path_var
            self.enc_entry = entry
        tk.Label(panel, text=("PRIVATE-KEY PROFILE" if decrypt else "RECIPIENT PUBLIC-KEY PROFILE"), font=("Segoe UI", 8, "bold"), fg=C["muted"], bg=C["surface"]).pack(anchor="w")
        profile_var = tk.StringVar()
        combo = ttk.Combobox(panel, textvariable=profile_var, state="readonly", width=45)
        combo.pack(anchor="w", pady=(8, 20), ipady=3)
        if decrypt:
            self.dec_profile = profile_var
            self.dec_combo = combo
        else:
            self.enc_profile = profile_var
            self.enc_combo = combo
        action_text = "Decrypt file" if decrypt else "Encrypt file"
        ttk.Button(panel, text=action_text, style="Accent.TButton", command=(self.do_decrypt if decrypt else self.do_encrypt)).pack(anchor="w")
        info = "Your private key is unlocked for this operation. The encrypted source file remains unchanged." if decrypt else "The encrypted .cap file is saved beside the original. Existing files are never overwritten."
        tk.Label(page, text=info, font=("Segoe UI", 9), fg=C["muted"], bg=C["root"], wraplength=750, justify="left").pack(anchor="w", pady=(2, 0))

    def _build_encrypt(self):
        self._build_file_page("encrypt", "Encrypt a file", "Protect a file for a recipient using their public key.")

    def _build_decrypt(self):
        self._build_file_page("decrypt", "Decrypt a file", "Restore a protected file using the matching private key.", decrypt=True)

    def _build_keys(self):
        page = tk.Frame(self.page_host, bg=C["root"])
        self.pages["keys"] = page
        self._page_header(page, "Key management", "Keep your public and private keys organised and protected.")
        toolbar = tk.Frame(page, bg=C["root"])
        toolbar.pack(fill="x", pady=(0, 14))
        ttk.Button(toolbar, text="＋  Create key profile", style="Accent.TButton", command=self.create_profile).pack(side="left")
        ttk.Button(toolbar, text="Import public key", command=self.import_public).pack(side="left", padx=9)
        panel = self._panel(page, padx=16, pady=16)
        head = tk.Frame(panel, bg=C["surface"])
        head.pack(fill="x", pady=(0, 12))
        tk.Label(head, text="SAVED PROFILES", font=("Segoe UI", 9, "bold"), fg=C["text"], bg=C["surface"]).pack(side="left")
        tk.Label(head, text="Select a profile to manage its keys", font=("Segoe UI", 8), fg=C["muted"], bg=C["surface"]).pack(side="right")
        columns = ("size", "fingerprint", "private")
        self.key_tree = ttk.Treeview(panel, columns=columns, show="headings", height=8)
        self.key_tree.heading("size", text="KEY SIZE")
        self.key_tree.heading("fingerprint", text="PUBLIC KEY FINGERPRINT")
        self.key_tree.heading("private", text="PRIVATE KEY")
        self.key_tree.column("size", width=105, anchor="center")
        self.key_tree.column("fingerprint", width=420, anchor="w")
        self.key_tree.column("private", width=125, anchor="center")
        self.key_tree.pack(fill="both", expand=True)
        actions = tk.Frame(panel, bg=C["surface"])
        actions.pack(fill="x", pady=(14, 0))
        ttk.Button(actions, text="Export public key", command=self.export_public).pack(side="left")
        ttk.Button(actions, text="Private-key backup", command=self.export_private).pack(side="left", padx=8)
        ttk.Button(actions, text="Delete profile", style="Danger.TButton", command=self.delete_profile).pack(side="right")
        note = self._panel(page, padx=18, pady=15)
        tk.Label(note, text="KEEP YOUR PRIVATE KEY SAFE", font=("Segoe UI", 8, "bold"), fg=C["accent"], bg=C["surface"]).pack(anchor="w")
        tk.Label(note, text="Private keys are protected by your passphrase. Export a secure backup and store it separately. If the private key and its backup are lost, files encrypted for that key cannot be recovered.", font=("Segoe UI", 9), fg=C["muted"], bg=C["surface"], wraplength=760, justify="left").pack(anchor="w", pady=(7, 0))

    def show_page(self, key):
        self.active_page = key
        labels = {"dashboard": "OVERVIEW", "encrypt": "ENCRYPT FILES", "decrypt": "DECRYPT FILES", "keys": "KEY MANAGEMENT"}
        self.breadcrumb.configure(text=f"WORKSPACE  /  {labels[key]}")
        for name, button in self.nav_buttons.items():
            active = name == key
            button.configure(bg=C["surface_3"] if active else C["sidebar"], fg=C["text"] if active else C["muted"])
        for page in self.pages.values():
            page.pack_forget()
        self.pages[key].pack(fill="both", expand=True)

    def refresh_profiles(self):
        profiles = self.manager.profiles()
        names = [p["name"] for p in profiles]
        self.enc_combo["values"] = names
        private_names = [p["name"] for p in profiles if p.get("private_key")]
        self.dec_combo["values"] = private_names
        if self.enc_profile.get() not in names:
            self.enc_profile.set(names[0] if names else "")
        if self.dec_profile.get() not in private_names:
            self.dec_profile.set(private_names[0] if private_names else "")
        for item in self.key_tree.get_children():
            self.key_tree.delete(item)
        for p in profiles:
            self.key_tree.insert("", "end", iid=p["name"], values=(f"RSA-{p['key_size']}", p["fingerprint"], "Available" if p.get("private_key") else "Not imported"))
        self.metric_profiles.configure(text=str(len(profiles)))
        self.metric_private.configure(text=str(len(private_names)))

    def selected_profile(self):
        selection = self.key_tree.selection()
        if not selection:
            messagebox.showinfo("Select a profile", "Select a key profile first.")
            return None
        return selection[0]

    def pick_encrypt(self):
        path = filedialog.askopenfilename(title="Choose a file to encrypt")
        if path:
            self.enc_path.set(path)

    def pick_decrypt(self):
        path = filedialog.askopenfilename(title="Choose an encrypted file", filetypes=[("Cryptographic Application", "*.cap"), ("All files", "*.*")])
        if path:
            self.dec_path.set(path)

    def create_profile(self):
        name = simpledialog.askstring("Create key profile", "Give this key profile a name:", parent=self)
        if not name:
            return
        password = simpledialog.askstring("Protect private key", "Create a passphrase (at least 12 characters):", show="*", parent=self)
        if password is None:
            return
        confirm = simpledialog.askstring("Confirm passphrase", "Enter the passphrase again:", show="*", parent=self)
        if password != confirm:
            messagebox.showerror("Passphrase mismatch", "The passphrases do not match.")
            return
        try:
            record = self.manager.create_profile(name, password)
            write_event("key_profile_created", "success")
            self.refresh_profiles()
            messagebox.showinfo("Profile created", f"Profile: {record['name']}\nFingerprint: {record['fingerprint']}\n\nExport a secure backup of your private key.")
        except Exception as exc:
            messagebox.showerror("Could not create profile", str(exc))

    def import_public(self):
        path = filedialog.askopenfilename(title="Choose a public-key PEM file", filetypes=[("PEM files", "*.pem *.pub"), ("All files", "*.*")])
        if not path:
            return
        name = simpledialog.askstring("Import public key", "Name this profile:", parent=self)
        if not name:
            return
        try:
            record = self.manager.import_public(name, Path(path))
            write_event("public_key_imported", "success")
            self.refresh_profiles()
            messagebox.showinfo("Public key imported", f"Fingerprint: {record['fingerprint']}\nThis profile can encrypt files but cannot decrypt them without its matching private key.")
        except Exception as exc:
            messagebox.showerror("Import failed", str(exc))

    def export_public(self):
        name = self.selected_profile()
        if not name:
            return
        path = filedialog.asksaveasfilename(defaultextension=".pem", initialfile=f"{name}_public.pem", filetypes=[("PEM files", "*.pem")])
        if not path:
            return
        try:
            self.manager.export_public(name, Path(path))
            messagebox.showinfo("Export complete", "Public key exported.")
        except Exception as exc:
            messagebox.showerror("Export failed", str(exc))

    def export_private(self):
        name = self.selected_profile()
        if not name:
            return
        password = simpledialog.askstring("Unlock private key", "Enter the profile passphrase:", show="*", parent=self)
        if password is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".pem", initialfile=f"{name}_private_backup.pem", filetypes=[("PEM files", "*.pem")])
        if not path:
            return
        try:
            self.manager.export_private(name, password, Path(path))
            messagebox.showwarning("Protect this backup", "Your private-key backup is passphrase-protected. Store it somewhere secure and separate from this computer.")
        except Exception as exc:
            messagebox.showerror("Export failed", str(exc))

    def delete_profile(self):
        name = self.selected_profile()
        if not name:
            return
        answer = messagebox.askyesno("Delete key profile?", f"Delete '{name}' and its private key?\n\nFiles encrypted for this key may become permanently unrecoverable. Export a secure backup first. This cannot be undone.")
        if answer and messagebox.askyesno("Final confirmation", "Are you absolutely sure you want to permanently delete this profile?"):
            try:
                self.manager.delete_profile(name)
                write_event("profile_deleted", "success")
                self.refresh_profiles()
            except Exception as exc:
                messagebox.showerror("Delete failed", str(exc))

    def do_encrypt(self):
        source = Path(self.enc_path.get()) if self.enc_path.get() else None
        name = self.enc_profile.get()
        if not source or not name:
            messagebox.showwarning("Missing information", "Choose a file and recipient profile.")
            return
        if not source.is_file():
            messagebox.showerror("File not found", "Choose an existing file.")
            return
        destination = source.with_name(source.name + ".cap")
        try:
            encrypt_file(source, destination, self.manager.load_public(name))
            write_event("file_encrypted", "success")
            messagebox.showinfo("Encryption complete", f"Encrypted file saved to:\n{destination}")
        except Exception as exc:
            messagebox.showerror("Encryption failed", str(exc))

    def do_decrypt(self):
        source = Path(self.dec_path.get()) if self.dec_path.get() else None
        name = self.dec_profile.get()
        if not source or not name:
            messagebox.showwarning("Missing information", "Choose an encrypted file and private-key profile.")
            return
        if not source.is_file():
            messagebox.showerror("File not found", "Choose an existing encrypted file.")
            return
        password = simpledialog.askstring("Unlock private key", "Enter the profile passphrase:", show="*", parent=self)
        if password is None:
            return
        destination = source.with_name(source.name[:-4] if source.name.lower().endswith(".cap") else source.name + ".decrypted")
        try:
            private = self.manager.load_private(name, password)
            decrypt_file(source, destination, private)
            write_event("file_decrypted", "success")
            messagebox.showinfo("Decryption complete", f"Integrity verified. File saved to:\n{destination}")
        except Exception as exc:
            messagebox.showerror("Decryption failed", str(exc))


if __name__ == "__main__":
    App().mainloop()
