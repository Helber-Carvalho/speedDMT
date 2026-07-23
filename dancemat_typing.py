import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import ctypes
import os
import sys
import threading
import json
import urllib.request
import subprocess
import datetime


def resource_path(relative_path):
    """Retorna o caminho absoluto do recurso (funciona em script e .exe PyInstaller)."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Timestamp de build (usado para detectar atualizações)
BUILD_TIMESTAMP = "2026-07-23T16:40:58Z"

GITHUB_REPO = "Helber-Carvalho/speedDMT"
GITHUB_API_COMMITS = f"https://api.github.com/repos/{GITHUB_REPO}/commits/main"
GITHUB_EXE_URL = f"https://github.com/{GITHUB_REPO}/raw/main/Speed%20DMT%202.exe"


def _get_exe_path():
    if getattr(sys, 'frozen', False):
        return sys.executable
    return os.path.abspath(__file__)


def _check_update(root):
    def _task():
        try:
            req = urllib.request.Request(
                GITHUB_API_COMMITS,
                headers={"User-Agent": "SpeedDMT/3.1", "Accept": "application/vnd.github.v3+json"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
            remote_date = data["commit"]["committer"]["date"]
            if remote_date > BUILD_TIMESTAMP:
                root.after(0, lambda: _apply_update(root))
        except:
            pass

    t = threading.Thread(target=_task, daemon=True)
    t.start()


def _apply_update(root):
    if not messagebox.askyesno(
        "Atualização Disponível",
        "Nova versão encontrada no repositório!\n\n"
        "Deseja baixar e instalar automaticamente?\n"
        "O aplicativo será fechado para aplicar a atualização.",
        parent=root
    ):
        return

    try:
        with urllib.request.urlopen(GITHUB_EXE_URL, timeout=30) as resp:
            new_data = resp.read()

        temp = os.path.join(os.environ["TEMP"], "Speed DMT 2.new.exe")
        with open(temp, "wb") as f:
            f.write(new_data)

        current = _get_exe_path()
        bat = os.path.join(os.environ["TEMP"], "update_speeddmt.bat")
        with open(bat, "w", newline="\r\n") as f:
            f.write(f"""@echo off
chcp 65001 >nul
:wait
tasklist /fi "IMAGENAME eq Speed DMT 2.exe" 2>nul | find /i "Speed DMT 2.exe" >nul
if not errorlevel 1 (
    timeout /t 1 /nobreak >nul
    goto wait
)
copy /y "{temp}" "{current}" >nul
del /q "{temp}"
start "" "{current}"
del "%~f0"
""")

        subprocess.Popen(
            ["cmd.exe", "/c", bat],
            creationflags=subprocess.CREATE_NO_WINDOW,
            close_fds=True
        )
        root.quit()
    except:
        messagebox.showerror(
            "Erro",
            "Não foi possível baixar a atualização.\nVerifique sua conexão e tente novamente.",
            parent=root
        )


# Paleta de cores - tema verde escuro
COR_FUNDO     = "#333333"
COR_FRAME     = "#2a2a2a"
COR_TITULO    = "#6cc24a"
COR_SUBTITULO = "#68A063"
COR_TEXTO     = "#FFFFFF"
COR_TEXTO_CLARO = "#AAAAAA"

COR_NIVEL1 = "#6cc24a"
COR_NIVEL2 = "#68A063"
COR_NIVEL3 = "#3C873A"
COR_NIVEL4 = "#215732"

COR_EXTRA       = "#44883e"
COR_BOTAO_TEXTO = "#FFFFFF"

# URLs dos níveis do BBC Dance Mat Typing
URL_LEVEL1 = "https://www.bbc.co.uk/games/interactive/activity-dance-mat-typing?exitGameUrl=http%3A%2F%2Fwww.bbc.co.uk%2Fguides%2Fz3c6tfr"
URL_LEVEL2 = "https://www.bbc.co.uk/games/interactive/activity-dance-mat-typing-level2?exitGameUrl=http%3A%2F%2Fwww.bbc.co.uk%2Fguides%2Fz3c6tfr"
URL_LEVEL3 = "https://www.bbc.co.uk/games/interactive/activity-dance-mat-typing-level3?exitGameUrl=http%3A%2F%2Fwww.bbc.co.uk%2Fguides%2Fz3c6tfr"
URL_LEVEL4 = "https://www.bbc.co.uk/games/interactive/activity-dance-mat-typing-level4?exitGameUrl=http%3A%2F%2Fwww.bbc.co.uk%2Fguides%2Fz3c6tfr"

# Mapeamento: cada nível → (cor, lista de (nome_estágio, url))
stages = {
    "N\u00edvel 1": (
        COR_NIVEL1,
        [
            ("Est\u00e1gio 1 - Home Row", URL_LEVEL1),
            ("Est\u00e1gio 2 - EI",       URL_LEVEL1),
            ("Est\u00e1gio 3 - RU",       URL_LEVEL1),
        ],
    ),
    "N\u00edvel 2": (
        COR_NIVEL2,
        [
            ("Est\u00e1gio 4 - TY", URL_LEVEL2),
            ("Est\u00e1gio 5 - WO", URL_LEVEL2),
            ("Est\u00e1gio 6 - QP", URL_LEVEL2),
        ],
    ),
    "N\u00edvel 3": (
        COR_NIVEL3,
        [
            ("Est\u00e1gio 7 - VM",  URL_LEVEL3),
            ("Est\u00e1gio 8 - BN",  URL_LEVEL3),
            ("Est\u00e1gio 9 - C,",  URL_LEVEL3),
        ],
    ),
    "N\u00edvel 4": (
        COR_NIVEL4,
        [
            ("Est\u00e1gio 10 - XZ",         URL_LEVEL4),
            ("Est\u00e1gio 11 - /.",         URL_LEVEL4),
            ("Est\u00e1gio 12 - Shift keys", URL_LEVEL4),
        ],
    ),
}


def open_url(url):
    webbrowser.open(url)


# Botão com cantos arredondados desenhado via Canvas
def criar_botao_arredondado(parent, texto, cor_fundo, comando, altura=40, raio=14):
    canvas = tk.Canvas(
        parent,
        bg=COR_FUNDO,
        highlightthickness=0,
        cursor="hand2",
        height=altura,
    )

    def _desenhar(event=None):
        w = canvas.winfo_width()
        h = altura
        if w < 10:
            return
        r = min(raio, h // 2, w // 4)
        canvas.delete("all")

        canvas.create_arc(
            0, 0, r * 2, r * 2, start=90, extent=90, fill=cor_fundo, outline=cor_fundo
        )
        canvas.create_arc(
            w - r * 2, 0, w, r * 2, start=0, extent=90, fill=cor_fundo, outline=cor_fundo
        )
        canvas.create_arc(
            0, h - r * 2, r * 2, h, start=180, extent=90, fill=cor_fundo, outline=cor_fundo
        )
        canvas.create_arc(
            w - r * 2,
            h - r * 2,
            w,
            h,
            start=270,
            extent=90,
            fill=cor_fundo,
            outline=cor_fundo,
        )
        canvas.create_rectangle(r, 0, w - r, h, fill=cor_fundo, outline=cor_fundo)
        canvas.create_rectangle(0, r, w, h - r, fill=cor_fundo, outline=cor_fundo)

        wrap_width = max(60, w - 20)
        canvas.create_text(
            w // 2,
            h // 2,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            fill=COR_BOTAO_TEXTO,
            width=wrap_width,
        )

    def _click(event):
        comando()

    canvas.bind("<Configure>", _desenhar)
    canvas.bind("<Button-1>", _click)

    return canvas


# Label com ajuste automático de wraplength
def criar_label_responsivo(parent, text, **kwargs):
    label = tk.Label(parent, text=text, **kwargs)

    def _ajustar(event):
        w = event.width - 16
        if w > 20:
            label.configure(wraplength=w)

    label.bind("<Configure>", _ajustar)
    return label


# Define o ícone na janela e na barra de tarefas (Windows)
def _set_app_icon(window):
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('speeddmt.typing.1')
    except:
        pass
    try:
        icon_path = resource_path('icon.ico')
        if os.path.exists(icon_path):
            window.iconbitmap(icon_path)
            hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
            icon_handle = ctypes.windll.user32.LoadImageW(0, icon_path, 1, 0, 0, 0x00000010)
            if icon_handle:
                ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 0, icon_handle)
                ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 1, icon_handle)
    except:
        pass


# Janela principal
root = tk.Tk()
root.title("Dance Mat Typing - Speed DMT 2")
root.configure(bg=COR_FUNDO)

root.after(100, lambda: _set_app_icon(root))
root.after(1000, lambda: _check_update(root))

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Vertical.TScrollbar",
    background="#444444",
    troughcolor="#2a2a2a",
    bordercolor="#2a2a2a",
    arrowcolor="#FFFFFF",
    gripcount=0,
)

# Tamanho proporcional 19:9 centralizado na tela
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()

ww = int(sw * 0.68)
wh = int(ww * 9 / 19)

if wh > sh * 0.88:
    wh = int(sh * 0.88)
    ww = int(wh * 19 / 9)

x = (sw - ww) // 2
y = (sh - wh) // 2
root.geometry(f"{ww}x{wh}+{x}+{y}")
root.minsize(800, 480)

main = tk.Frame(root, bg=COR_FUNDO, padx=24, pady=20)
main.pack(fill=tk.BOTH, expand=True)

# Título
titulo = criar_label_responsivo(
    main,
    text="Dance Mat Typing",
    font=("Segoe UI", 22, "bold"),
    fg=COR_TITULO,
    bg=COR_FUNDO,
    pady=4,
)
titulo.pack(fill=tk.X)

# Subtítulo
subtitulo = criar_label_responsivo(
    main,
    text="Escolha um est\u00e1gio para praticar digita\u00e7\u00e3o!",
    font=("Segoe UI", 11),
    fg=COR_SUBTITULO,
    bg=COR_FUNDO,
    pady=2,
)
subtitulo.pack(fill=tk.X)

ttk.Separator(main, orient="horizontal").pack(fill=tk.X, pady=12)

# Container rolável (Canvas + Scrollbar)
scroll_canvas = tk.Canvas(main, bg=COR_FUNDO, highlightthickness=0)
scroll_bar = ttk.Scrollbar(main, orient="vertical", command=scroll_canvas.yview)
scroll_canvas.configure(yscrollcommand=scroll_bar.set)

scroll_frame = tk.Frame(scroll_canvas, bg=COR_FUNDO)
scroll_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

scroll_window = scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
scroll_canvas.bind("<Configure>", lambda e: scroll_canvas.itemconfig(scroll_window, width=e.width))

def _scroll_enter(event):
    scroll_canvas.bind_all("<MouseWheel>", _scroll_wheel)

def _scroll_leave(event):
    scroll_canvas.unbind_all("<MouseWheel>")

def _scroll_wheel(event):
    scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

scroll_canvas.bind("<Enter>", _scroll_enter)
scroll_canvas.bind("<Leave>", _scroll_leave)

scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

# Botões dos estágios organizados por nível
for level_name, (cor_nivel, stage_list) in stages.items():
    frame_nivel = tk.Frame(scroll_frame, bg=COR_FUNDO, pady=4)
    frame_nivel.pack(fill=tk.X, pady=3)

    lbl_nivel = tk.Label(
        frame_nivel,
        text=level_name,
        font=("Segoe UI", 13, "bold"),
        fg=cor_nivel,
        bg=COR_FUNDO,
        anchor="w",
    )
    lbl_nivel.pack(fill=tk.X, padx=2, pady=(0, 4))

    for nome, url in stage_list:
        btn = criar_botao_arredondado(
            frame_nivel, nome, cor_nivel, lambda u=url: open_url(u), altura=36, raio=12
        )
        btn.pack(fill=tk.X, pady=2)

ttk.Separator(scroll_frame, orient="horizontal").pack(fill=tk.X, pady=10)

# 10 Fast Fingers
btn_10fast = criar_botao_arredondado(
    scroll_frame,
    "10 Fast Fingers - Text Practice (PT)",
    COR_EXTRA,
    lambda: open_url(
        "https://10fastfingers.com/pt/text-practice?sortBy=rating&sortDirection=DESC&filter=top&languageIso=pt&limit=50"
    ),
    altura=42,
    raio=14,
)
btn_10fast.pack(fill=tk.X, pady=4)

# Rodapé
rodape = criar_label_responsivo(
    scroll_frame,
    text="Desenvolvido para alunos aprenderem digita\u00e7\u00e3o de forma divertida!",
    font=("Segoe UI", 8),
    fg=COR_TEXTO_CLARO,
    bg=COR_FUNDO,
    pady=6,
)
rodape.pack(fill=tk.X)

creditos = criar_label_responsivo(
    scroll_frame,
    text="crie conosco OpenSurceFriends  |  helbercarvalho8@gmail.com",
    font=("Segoe UI", 8),
    fg="#6cc24a",
    bg=COR_FUNDO,
    pady=2,
)
creditos.pack(fill=tk.X, pady=(0, 4))

root.mainloop()
