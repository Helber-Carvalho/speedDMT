# =============================================================================
# Dance Mat Typing - Lançador de Estágios
# Versão: 3.1
# Descrição: Interface para acessar os estágios do Dance Mat Typing (BBC)
#            e o site 10 Fast Fingers. Design responsivo com tema verde.
# =============================================================================

import tkinter as tk
from tkinter import ttk
import webbrowser

# =============================================================================
# PALETA DE CORES - TEMA VERDE
# =============================================================================
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

URL_LEVEL1 = "https://www.bbc.co.uk/games/interactive/activity-dance-mat-typing?exitGameUrl=http%3A%2F%2Fwww.bbc.co.uk%2Fguides%2Fz3c6tfr"
URL_LEVEL2 = "https://www.bbc.co.uk/games/interactive/activity-dance-mat-typing-level2?exitGameUrl=http%3A%2F%2Fwww.bbc.co.uk%2Fguides%2Fz3c6tfr"
URL_LEVEL3 = "https://www.bbc.co.uk/games/interactive/activity-dance-mat-typing-level3?exitGameUrl=http%3A%2F%2Fwww.bbc.co.uk%2Fguides%2Fz3c6tfr"

stages = {
    "Nível 1": (
        COR_NIVEL1,
        [
            ("Estágio 1 - Home Row", URL_LEVEL1),
            ("Estágio 2 - EI",       URL_LEVEL1),
            ("Estágio 3 - RU",       URL_LEVEL1),
        ],
    ),
    "Nível 2": (
        COR_NIVEL2,
        [
            ("Estágio 4 - TY", URL_LEVEL2),
            ("Estágio 5 - WO", URL_LEVEL2),
            ("Estágio 6 - QP", URL_LEVEL2),
        ],
    ),
    "Nível 3": (
        COR_NIVEL3,
        [
            ("Estágio 7 - VM",  URL_LEVEL3),
            ("Estágio 8 - BN",  URL_LEVEL3),
            ("Estágio 9 - C,",  URL_LEVEL3),
        ],
    ),
    "Nível 4": (
        COR_NIVEL4,
        [
            ("Estágio 10 - XZ",         URL_LEVEL3),
            ("Estágio 11 - /.",         URL_LEVEL3),
            ("Estágio 12 - Shift keys", URL_LEVEL3),
        ],
    ),
}


def open_url(url):
    webbrowser.open(url)


# -------------------------------------------------------------------------
# BOTÃO ARREDONDADO (Canvas-based)
# -------------------------------------------------------------------------
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


# -------------------------------------------------------------------------
# LABEL COM WRAP RESPONSIVO
# -------------------------------------------------------------------------
def criar_label_responsivo(parent, text, **kwargs):
    label = tk.Label(parent, text=text, **kwargs)

    def _ajustar(event):
        w = event.width - 16
        if w > 20:
            label.configure(wraplength=w)

    label.bind("<Configure>", _ajustar)
    return label


# =============================================================================
# JANELA PRINCIPAL
# =============================================================================
root = tk.Tk()
root.title("Dance Mat Typing - Speed DMT 2")
root.configure(bg=COR_FUNDO)

# Estilo da scrollbar compatível com o tema escuro
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

# Tamanho 19:9 centralizado
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

# Frame principal
main = tk.Frame(root, bg=COR_FUNDO, padx=24, pady=20)
main.pack(fill=tk.BOTH, expand=True)

# TÍTULO
titulo = criar_label_responsivo(
    main,
    text="Dance Mat Typing",
    font=("Segoe UI", 22, "bold"),
    fg=COR_TITULO,
    bg=COR_FUNDO,
    pady=4,
)
titulo.pack(fill=tk.X)

# SUBTÍTULO
subtitulo = criar_label_responsivo(
    main,
    text="Escolha um estágio para praticar digitação!",
    font=("Segoe UI", 11),
    fg=COR_SUBTITULO,
    bg=COR_FUNDO,
    pady=2,
)
subtitulo.pack(fill=tk.X)

ttk.Separator(main, orient="horizontal").pack(fill=tk.X, pady=12)

# =========================================================================
# CONTAINER ROLÁVEL (SCROLL)
#   Usa Canvas + Scrollbar + Frame interno para suportar scroll do mouse
# =========================================================================
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

# NÍVEIS
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

# 10 FAST FINGERS
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

# RODAPÉ
rodape = criar_label_responsivo(
    scroll_frame,
    text="Desenvolvido para alunos aprenderem digitação de forma divertida!",
    font=("Segoe UI", 8),
    fg=COR_TEXTO_CLARO,
    bg=COR_FUNDO,
    pady=6,
)
rodape.pack(fill=tk.X)

# CRÉDITOS
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
