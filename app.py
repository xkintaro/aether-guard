"""
╔═════════════════════════════════════════════════════════════════════╗
║                           AETHER GUARD                              ║
╚═════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import ctypes
import tkinter as tk
from typing import Optional, Tuple, List
import win32gui
import win32con
import win32com.client
from PIL import Image, ImageTk, ImageDraw

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class Config:
    DEFAULT_PASSWORD = "1234"         # Your master access key
    MAX_ATTEMPTS = 5                  # Attempts allowed before lockout
    LOCKOUT_TIME = 60                 # Initial lockout duration in seconds
    GRACE_PERIOD = 300                # Authorized session duration in seconds

# ═══════════════════════════════════════════════════════════════════════════════
# RATE LIMITER
# ═══════════════════════════════════════════════════════════════════════════════

class RateLimiter:
    def __init__(self):
        self.max_attempts = Config.MAX_ATTEMPTS
        self.base_lockout = Config.LOCKOUT_TIME
        self.attempts = 0
        self.lockout_until = 0
        self.total_lockouts = 0
    
    def record_attempt(self, success: bool) -> Tuple[bool, int]:
        if success:
            self.attempts = 0
            self.total_lockouts = 0
            return False, 0
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            duration = min(self.base_lockout * (2 ** self.total_lockouts), 3600)
            self.lockout_until = time.time() + duration
            self.total_lockouts += 1
            self.attempts = 0
            return True, duration
        return False, 0
    
    def is_locked(self) -> Tuple[bool, int]:
        if time.time() < self.lockout_until:
            return True, int(self.lockout_until - time.time())
        return False, 0
    
    def remaining(self) -> int:
        return self.max_attempts - self.attempts

# ═══════════════════════════════════════════════════════════════════════════════
# FOLDER WATCHER
# ═══════════════════════════════════════════════════════════════════════════════

class FolderWatcher:
    def __init__(self):
        self.shell = None
    
    def init_shell(self):
        if self.shell is None:
            try:
                self.shell = win32com.client.Dispatch("Shell.Application")
            except:
                pass
    
    def find_target(self) -> Optional[int]:
        self.init_shell()
        if not self.shell:
            return None
        try:
            for i in range(self.shell.Windows().Count):
                try:
                    w = self.shell.Windows().Item(i)
                    if w and getattr(w, "FullName", None):
                        if "explorer" in str(w.FullName).lower():
                            return w.HWND
                except:
                    continue
        except:
            self.shell = None
        return None
    
    def hide_and_close(self, hwnd: int):
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        except:
            pass
    
    def close_all_targets(self):
        self.init_shell()
        if not self.shell:
            return
        try:
            for i in range(self.shell.Windows().Count):
                try:
                    w = self.shell.Windows().Item(i)
                    if w and getattr(w, "FullName", None):
                        if "explorer" in str(w.FullName).lower():
                            win32gui.ShowWindow(w.HWND, win32con.SW_HIDE)
                            win32gui.PostMessage(w.HWND, win32con.WM_CLOSE, 0, 0)
                except:
                    continue
        except:
            self.shell = None

# ═══════════════════════════════════════════════════════════════════════════════
# AUTH MODAL
# ═══════════════════════════════════════════════════════════════════════════════

class AuthModal:
    BG = '#0d0d0d'
    CARD = '#161616'
    INPUT_BG = '#1a1a1a'
    ACCENT = '#00e676'
    ACCENT_DIM = '#00c853'
    DANGER = '#ff1744'
    TEXT = '#fafafa'
    TEXT_DIM = '#757575'
    BORDER = '#2a2a2a'
    LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
    
    def __init__(self, limiter: RateLimiter, password: str, watcher: FolderWatcher):
        self.limiter = limiter
        self.password = password
        self.watcher = watcher
        self.result = False
        self.root = None
        self.closed = False
        self.password_visible = False
        self._after_ids = []
    
    def _cancel_timers(self):
        if self.root:
            for aid in self._after_ids:
                try:
                    self.root.after_cancel(aid)
                except:
                    pass
            self._after_ids.clear()
    
    def _schedule(self, ms, func, *args):
        if not self.closed and self.root:
            aid = self.root.after(ms, func, *args)
            self._after_ids.append(aid)
            return aid
        return None
    
    def _protect(self):
        if self.closed:
            return
        self.watcher.close_all_targets()
        if self.root and not self.closed:
            self._schedule(50, self._protect)
    
    def show(self) -> bool:
        locked, secs = self.limiter.is_locked()
        
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("Aether Guard")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=self.BG)
        self.root.resizable(False, False)
        
        W, H = 380, 300
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - W) // 2
        y = (sh - H) // 2
        self.root.geometry(f"{W}x{H}+{x}+{y}")
        
        outer = tk.Frame(self.root, bg=self.ACCENT, padx=1, pady=1)
        outer.pack(fill="both", expand=True)
        
        card = tk.Frame(outer, bg=self.CARD)
        card.pack(fill="both", expand=True)
        
        self._drag_x = 0
        self._drag_y = 0
        
        def start_drag(e):
            self._drag_x = e.x
            self._drag_y = e.y
        
        def do_drag(e):
            nx = self.root.winfo_x() + e.x - self._drag_x
            ny = self.root.winfo_y() + e.y - self._drag_y
            self.root.geometry(f"+{nx}+{ny}")
        
        card.bind("<Button-1>", start_drag)
        card.bind("<B1-Motion>", do_drag)
        
        header = tk.Frame(card, bg=self.CARD, height=40)
        header.pack(fill="x")
        header.pack_propagate(False)
        header.bind("<Button-1>", start_drag)
        header.bind("<B1-Motion>", do_drag)
        
        close_btn = tk.Label(
            header, text="✕", font=("Segoe UI", 12),
            bg=self.CARD, fg=self.TEXT_DIM, cursor="hand2"
        )
        close_btn.pack(side="right", padx=15, pady=8)
        close_btn.bind("<Button-1>", lambda e: self._close(False))
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg=self.DANGER))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg=self.TEXT_DIM))
        
        content = tk.Frame(card, bg=self.CARD)
        content.pack(fill="both", expand=True, padx=40, pady=10)
        
        try:
            img = Image.open(self.LOGO_PATH).convert("RGBA")
            
            w, h = img.size
            size = min(w, h)
            left = (w - size) // 2
            top = (h - size) // 2
            img = img.crop((left, top, left + size, top + size))
            
            target_size = 80
            img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
            
            mask = Image.new('L', (target_size, target_size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, target_size, target_size), fill=255)
            
            output = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
            output.paste(img, (0, 0), mask=mask)
            
            self.tk_logo = ImageTk.PhotoImage(output)
            logo_label = tk.Label(content, image=self.tk_logo, bg=self.CARD)
            logo_label.pack(pady=(10, 5))
        except Exception as e:
            shield = tk.Label(
                content, text="🛡", font=("Segoe UI Emoji", 42),
                bg=self.CARD, fg=self.ACCENT
            )
            shield.pack(pady=(10, 5))
        
        title = tk.Label(
            content, text="AETHER GUARD",
            font=("Segoe UI", 16, "bold"), bg=self.CARD, fg=self.TEXT
        )
        title.pack(pady=(0, 5))
        
        self.status_lbl = tk.Label(
            content, text="Enter access key",
            font=("Segoe UI", 9), bg=self.CARD, fg=self.TEXT_DIM
        )
        self.status_lbl.pack(pady=(0, 15))
        
        input_frame = tk.Frame(content, bg=self.BORDER)
        input_frame.pack(fill="x", pady=(0, 5))
        
        input_inner = tk.Frame(input_frame, bg=self.INPUT_BG, padx=12, pady=10)
        input_inner.pack(fill="x", padx=1, pady=1)
        
        self.entry = tk.Entry(
            input_inner, show="●", font=("Consolas", 13),
            bg=self.INPUT_BG, fg=self.TEXT, insertbackground=self.ACCENT,
            relief="flat", bd=0
        )
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.focus_set()
        
        self.vis_btn = tk.Label(
            input_inner, text="👁", font=("Segoe UI Emoji", 11),
            bg=self.INPUT_BG, fg=self.TEXT_DIM, cursor="hand2"
        )
        self.vis_btn.pack(side="right", padx=(10, 0))
        self.vis_btn.bind("<Button-1>", lambda e: self._toggle_visibility())
        
        self.attempts_lbl = tk.Label(
            content, text="", font=("Segoe UI", 8),
            bg=self.CARD, fg=self.TEXT_DIM
        )
        self.attempts_lbl.pack(pady=(5, 10))
        
        self.auth_btn = tk.Frame(content, bg=self.ACCENT, cursor="hand2")
        self.auth_btn.pack(fill="x", pady=(5, 0))
        
        btn_inner = tk.Frame(self.auth_btn, bg=self.ACCENT, pady=12)
        btn_inner.pack(fill="x", padx=1, pady=1)
        
        self.btn_text = tk.Label(
            btn_inner, text="AUTHORIZE", font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT, fg=self.BG
        )
        self.btn_text.pack()
        
        def btn_enter(e):
            self.auth_btn.config(bg=self.ACCENT_DIM)
            btn_inner.config(bg=self.ACCENT_DIM)
            self.btn_text.config(bg=self.ACCENT_DIM)
        
        def btn_leave(e):
            self.auth_btn.config(bg=self.ACCENT)
            btn_inner.config(bg=self.ACCENT)
            self.btn_text.config(bg=self.ACCENT)
        
        self.auth_btn.bind("<Enter>", btn_enter)
        self.auth_btn.bind("<Leave>", btn_leave)
        self.auth_btn.bind("<Button-1>", lambda e: self._check_password())
        btn_inner.bind("<Button-1>", lambda e: self._check_password())
        self.btn_text.bind("<Button-1>", lambda e: self._check_password())
        
        self.root.bind('<Return>', lambda e: self._check_password())
        self.root.bind('<Escape>', lambda e: self._close(False))
        
        if locked:
            self._schedule(100, lambda: self._show_lockout(secs))
        
        self._schedule(50, self._protect)
        
        self.root.deiconify()
        self.root.mainloop()
        return self.result
    
    def _toggle_visibility(self):
        self.password_visible = not self.password_visible
        self.entry.config(show="" if self.password_visible else "●")
        self.vis_btn.config(text="🙈" if self.password_visible else "👁")
    
    def _check_password(self):
        locked, secs = self.limiter.is_locked()
        if locked:
            self._show_lockout(secs)
            return
        
        entered = self.entry.get()
        
        if entered == self.password:
            self.limiter.record_attempt(True)
            self.status_lbl.config(text="✓ Access granted", fg=self.ACCENT)
            self._schedule(400, lambda: self._close(True))
        else:
            locked, lockout_time = self.limiter.record_attempt(False)
            if locked:
                self._show_lockout(lockout_time)
            else:
                self._show_error()
    
    def _show_error(self):
        self.entry.delete(0, tk.END)
        self.status_lbl.config(text="✗ Invalid key", fg=self.DANGER)
        self._update_attempts()
        
        ox = self.root.winfo_x()
        oy = self.root.winfo_y()
        offsets = [8, -8, 6, -6, 4, -4, 2, -2, 0]
        
        def shake(i=0):
            if i >= len(offsets) or not self.root or self.closed:
                return
            try:
                self.root.geometry(f"+{ox + offsets[i]}+{oy}")
                self._schedule(25, lambda: shake(i + 1))
            except:
                pass
        
        shake()
        self._schedule(1500, lambda: self.status_lbl.config(text="Enter access key", fg=self.TEXT_DIM) if not self.closed else None)
    
    def _show_lockout(self, seconds: int):
        self.entry.delete(0, tk.END)
        self.entry.config(state='disabled')
        self.btn_text.config(text="LOCKED", fg=self.BG)
        self.auth_btn.config(bg=self.TEXT_DIM)
        
        def countdown(r):
            if r <= 0 or self.closed:
                if not self.closed:
                    self.entry.config(state='normal')
                    self.btn_text.config(text="AUTHORIZE")
                    self.auth_btn.config(bg=self.ACCENT)
                    self.status_lbl.config(text="Enter access key", fg=self.TEXT_DIM)
                    self._update_attempts()
                return
            try:
                m, s = divmod(r, 60)
                self.status_lbl.config(text=f"⏳ Locked for {m:02d}:{s:02d}", fg=self.DANGER)
                self._schedule(1000, lambda: countdown(r - 1))
            except:
                pass
        
        countdown(seconds)
    
    def _update_attempts(self):
        rem = self.limiter.remaining()
        if rem < self.limiter.max_attempts:
            color = self.DANGER if rem <= 2 else self.TEXT_DIM
            self.attempts_lbl.config(text=f"{rem} attempts remaining", fg=color)
        else:
            self.attempts_lbl.config(text="")
    
    def _close(self, authorized: bool):
        self.closed = True
        self.result = authorized
        self._cancel_timers()
        if self.root:
            try:
                self.root.destroy()
            except:
                pass
            self.root = None

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

class AetherGuard:
    def __init__(self):
        self.limiter = RateLimiter()
        self.watcher = FolderWatcher()
        self.password = Config.DEFAULT_PASSWORD
        self.authenticated = False
        self.auth_time = 0
        self.showing_modal = False
    
    def run(self):
        print("╔════════════════════════════════════════════╗")
        print("║             AETHER GUARD ACTIVE            ║")
        print("╠════════════════════════════════════════════╣")
        print("║  ALL FOLDERS PROTECTED                     ║")
        print("║  Press Ctrl+C to exit                      ║")
        print("╚════════════════════════════════════════════╝")
        
        while True:
            try:
                if self.showing_modal:
                    time.sleep(0.05)
                    continue
                
                hwnd = self.watcher.find_target()
                
                if hwnd:
                    if not self.authenticated:
                        self.watcher.hide_and_close(hwnd)
                        time.sleep(0.05)
                        
                        self.showing_modal = True
                        modal = AuthModal(self.limiter, self.password, self.watcher)
                        ok = modal.show()
                        self.showing_modal = False
                        
                        if ok:
                            self.authenticated = True
                            self.auth_time = time.time()
                            print("🔓 Access granted")
                        else:
                            print("🔒 Access denied")
                    else:
                        self.auth_time = time.time()
                else:
                    if self.authenticated:
                        if time.time() - self.auth_time > Config.GRACE_PERIOD:
                            self.authenticated = False
                            print("🔒 Protection re-armed")
                
                time.sleep(0.05)
                
            except KeyboardInterrupt:
                print("\n👋 Stopped")
                break
            except Exception as e:
                print(f"⚠ {e}")
                time.sleep(0.3)

def main():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 47391))
    except:
        print("⚠ Already running!")
        return
    
    AetherGuard().run()

if __name__ == "__main__":
    main()