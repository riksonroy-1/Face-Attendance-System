# ============================================
#  SNGCE College — Face Attendance System
#  Professional Dashboard  (CustomTkinter)
# ============================================

import customtkinter as ctk
import subprocess
import os
import sys
import threading
from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.ticker as mticker

# ── project imports ────────────────────────
from theme import *
from student_utils import (
    get_all_students, get_student_count, add_student,
    delete_student, search_students, get_classes,
)
from attendance_utils import (
    get_today_attendance, get_today_present_count,
    get_today_absent_count, get_attendance_rate,
    get_weekly_summary, get_all_attendance,
    search_attendance, get_unique_dates,
    get_attendance_by_date, get_today_absent_students,
)

# ── working directory → script location ────
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ── CustomTkinter defaults ─────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ════════════════════════════════════════════
#  Reusable Widget Helpers
# ════════════════════════════════════════════

def make_stat_card(parent, title, value, accent_color, icon_text):
    """Create a stat card with accent left strip."""
    card = ctk.CTkFrame(
        parent, fg_color=BG_CARD, corner_radius=CARD_CORNER,
        border_width=0, height=120,
    )
    card.pack_propagate(False)

    # Accent strip (left border simulation)
    strip = ctk.CTkFrame(
        card, fg_color=accent_color, width=4,
        corner_radius=0,
    )
    strip.pack(side="left", fill="y")

    body = ctk.CTkFrame(card, fg_color="transparent")
    body.pack(side="left", fill="both", expand=True, padx=18, pady=14)

    # Icon + label row
    top_row = ctk.CTkFrame(body, fg_color="transparent")
    top_row.pack(anchor="w")

    ctk.CTkLabel(
        top_row, text=icon_text, font=(FONT_FAMILY, 16),
        text_color=accent_color,
    ).pack(side="left")
    ctk.CTkLabel(
        top_row, text=f"  {title}", font=FONT_STAT_LABEL,
        text_color=TEXT_SECONDARY,
    ).pack(side="left")

    # Value
    val_label = ctk.CTkLabel(
        body, text=str(value), font=FONT_STAT_VALUE,
        text_color=TEXT_PRIMARY, anchor="w",
    )
    val_label.pack(anchor="w", pady=(6, 0))

    return card, val_label          # return card + value label for updates


def make_section_header(parent, title, subtitle=None):
    """Section title with optional subtitle."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", pady=(0, 10))

    ctk.CTkLabel(
        frame, text=title, font=FONT_HEADING_MD,
        text_color=TEXT_PRIMARY, anchor="w",
    ).pack(side="left")

    if subtitle:
        ctk.CTkLabel(
            frame, text=subtitle, font=FONT_SMALL,
            text_color=TEXT_MUTED, anchor="w",
        ).pack(side="left", padx=(10, 0))

    return frame


# ════════════════════════════════════════════
#  Main Application
# ════════════════════════════════════════════

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ── window ─────────────────────────
        self.title(f"{APP_TITLE} — {APP_SUBTITLE}")
        self.geometry("1200x750")
        self.minsize(1050, 650)
        self.configure(fg_color=BG_DARK)

        # Track navigation state
        self._current_page = None
        self._nav_buttons = {}
        self._auto_refresh_id = None

        # ── layout: sidebar + content ──────
        self._build_sidebar()
        self._content = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        self._content.pack(side="left", fill="both", expand=True)

        # Page container (stacking frames)
        self._pages = {}
        self._build_pages()

        # Start on dashboard
        self._show_page("dashboard")

    # ────────────────────────────────────────
    #  Sidebar
    # ────────────────────────────────────────

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(
            self, fg_color=BG_DARKEST, width=SIDEBAR_WIDTH,
            corner_radius=0,
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # ── Logo / Branding area ───────────
        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=20, pady=(28, 8))

        # Logo circle
        logo_frame = ctk.CTkFrame(
            brand, fg_color=ACCENT_PRIMARY, width=46, height=46,
            corner_radius=23,
        )
        logo_frame.pack(anchor="w")
        logo_frame.pack_propagate(False)
        ctk.CTkLabel(
            logo_frame, text="🎓", font=(FONT_FAMILY, 22),
            text_color="#FFFFFF",
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            brand, text=APP_TITLE, font=FONT_HEADING_MD,
            text_color=TEXT_PRIMARY, anchor="w",
        ).pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(
            brand, text="Attendance System",
            font=FONT_SMALL, text_color=TEXT_MUTED, anchor="w",
        ).pack(anchor="w")

        # Divider
        ctk.CTkFrame(
            sidebar, fg_color=BORDER_SUBTLE, height=1,
        ).pack(fill="x", padx=16, pady=(18, 14))

        # ── Nav menu label ─────────────────
        ctk.CTkLabel(
            sidebar, text="   MENU", font=FONT_TINY,
            text_color=TEXT_MUTED, anchor="w",
        ).pack(fill="x", padx=16, pady=(0, 6))

        # ── Nav items ─────────────────────
        for item in NAV_ITEMS:
            btn = ctk.CTkButton(
                sidebar,
                text=f"  {item['icon']}   {item['label']}",
                font=FONT_NAV,
                fg_color="transparent",
                hover_color=ACCENT_SUBTLE,
                text_color=TEXT_SECONDARY,
                anchor="w",
                height=NAV_ITEM_HEIGHT,
                corner_radius=BUTTON_CORNER,
                command=lambda k=item["key"]: self._show_page(k),
            )
            btn.pack(fill="x", padx=12, pady=2)
            self._nav_buttons[item["key"]] = btn

        # ── Spacer ─────────────────────────
        ctk.CTkFrame(sidebar, fg_color="transparent").pack(fill="both", expand=True)

        # ── Bottom section ─────────────────
        ctk.CTkFrame(
            sidebar, fg_color=BORDER_SUBTLE, height=1,
        ).pack(fill="x", padx=16, pady=(0, 10))

        ctk.CTkLabel(
            sidebar, text=f"  {APP_VERSION}",
            font=FONT_TINY, text_color=TEXT_MUTED,
        ).pack(pady=(0, 6))

        exit_btn = ctk.CTkButton(
            sidebar, text="⏻  Exit", font=FONT_BODY,
            fg_color=BG_CARD, hover_color=STATUS_DANGER,
            text_color=TEXT_SECONDARY, height=36,
            corner_radius=BUTTON_CORNER,
            command=self._on_exit,
        )
        exit_btn.pack(fill="x", padx=16, pady=(0, 20))

    # ────────────────────────────────────────
    #  Page Switching
    # ────────────────────────────────────────

    def _show_page(self, key):
        if self._current_page == key:
            return

        # Cancel any pending auto-refresh
        if self._auto_refresh_id:
            self.after_cancel(self._auto_refresh_id)
            self._auto_refresh_id = None

        # Update nav button styles
        for k, btn in self._nav_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=ACCENT_SUBTLE,
                    text_color=ACCENT_PRIMARY,
                    font=FONT_NAV_ACTIVE,
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=TEXT_SECONDARY,
                    font=FONT_NAV,
                )

        # Hide current, show selected
        for pg in self._pages.values():
            pg.pack_forget()

        self._current_page = key
        page = self._pages[key]
        page.pack(fill="both", expand=True)

        # Refresh data when switching to a page
        refresh_fn = getattr(self, f"_refresh_{key}", None)
        if refresh_fn:
            refresh_fn()

    # ────────────────────────────────────────
    #  Build All Pages
    # ────────────────────────────────────────

    def _build_pages(self):
        self._build_dashboard_page()
        self._build_students_page()
        self._build_attendance_page()
        self._build_register_page()
        self._build_train_page()

    # ════════════════════════════════════════
    #  PAGE: Dashboard
    # ════════════════════════════════════════

    def _build_dashboard_page(self):
        page = ctk.CTkScrollableFrame(
            self._content, fg_color=BG_DARK, corner_radius=0,
        )
        self._pages["dashboard"] = page

        # Header
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(24, 0))

        ctk.CTkLabel(
            header, text="Dashboard",
            font=FONT_HEADING_XL, text_color=TEXT_PRIMARY, anchor="w",
        ).pack(side="left")

        # Live clock
        self._clock_label = ctk.CTkLabel(
            header, text="", font=FONT_BODY,
            text_color=TEXT_MUTED,
        )
        self._clock_label.pack(side="right")
        self._update_clock()

        ctk.CTkLabel(
            page, text=f"Welcome back! Here's today's overview.",
            font=FONT_BODY, text_color=TEXT_SECONDARY, anchor="w",
        ).pack(fill="x", padx=30, pady=(4, 18))

        # ── Stat Cards Row ─────────────────
        cards_row = ctk.CTkFrame(page, fg_color="transparent")
        cards_row.pack(fill="x", padx=30, pady=(0, 20))
        cards_row.columnconfigure((0, 1, 2, 3), weight=1, uniform="card")

        c1, self._stat_total   = make_stat_card(cards_row, "Total Students",   "0", CARD_ACCENT_1, "👥")
        c2, self._stat_present = make_stat_card(cards_row, "Present Today",    "0", CARD_ACCENT_2, "✅")
        c3, self._stat_absent  = make_stat_card(cards_row, "Absent Today",     "0", CARD_ACCENT_3, "❌")
        c4, self._stat_rate    = make_stat_card(cards_row, "Attendance Rate",  "0%", CARD_ACCENT_4, "📈")

        c1.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        c2.grid(row=0, column=1, padx=8,       sticky="nsew")
        c3.grid(row=0, column=2, padx=8,       sticky="nsew")
        c4.grid(row=0, column=3, padx=(8, 0),  sticky="nsew")

        # ── Charts + Recent Log ────────────
        middle = ctk.CTkFrame(page, fg_color="transparent")
        middle.pack(fill="x", padx=30, pady=(0, 20))
        middle.columnconfigure(0, weight=3)
        middle.columnconfigure(1, weight=2)

        # -- Chart Card --
        chart_card = ctk.CTkFrame(middle, fg_color=BG_CARD, corner_radius=CARD_CORNER)
        chart_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        ctk.CTkLabel(
            chart_card, text="  📊  Weekly Attendance",
            font=FONT_HEADING_SM, text_color=TEXT_PRIMARY, anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 0))

        self._chart_frame = ctk.CTkFrame(chart_card, fg_color="transparent")
        self._chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # -- Quick Actions Card --
        actions_card = ctk.CTkFrame(middle, fg_color=BG_CARD, corner_radius=CARD_CORNER)
        actions_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        ctk.CTkLabel(
            actions_card, text="  ⚡  Quick Actions",
            font=FONT_HEADING_SM, text_color=TEXT_PRIMARY, anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 12))

        actions_list = [
            ("📸  Start Attendance",  ACCENT_PRIMARY,   lambda: self._launch_subprocess("attendance_recognize.py")),
            ("👤  Register New Face", STATUS_INFO,       lambda: self._show_page("register")),
            ("🧠  Train Model",       STATUS_SUCCESS,    lambda: self._show_page("train")),
            ("➕  Add Student",       STATUS_WARNING,    lambda: self._show_page("students")),
        ]

        for text, color, cmd in actions_list:
            ctk.CTkButton(
                actions_card, text=text, font=FONT_BODY_BOLD,
                fg_color=color, hover_color=ACCENT_HOVER,
                text_color=TEXT_ON_ACCENT, height=42,
                corner_radius=BUTTON_CORNER, command=cmd,
            ).pack(fill="x", padx=16, pady=4)

        ctk.CTkFrame(actions_card, fg_color="transparent", height=10).pack()

        # ── Recent Attendance Table ────────
        recent_card = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=CARD_CORNER)
        recent_card.pack(fill="x", padx=30, pady=(0, 24))

        rec_header = ctk.CTkFrame(recent_card, fg_color="transparent")
        rec_header.pack(fill="x", padx=16, pady=(14, 8))

        ctk.CTkLabel(
            rec_header, text="  📋  Today's Attendance Log",
            font=FONT_HEADING_SM, text_color=TEXT_PRIMARY, anchor="w",
        ).pack(side="left")

        ctk.CTkButton(
            rec_header, text="🔄 Refresh", width=90, height=30,
            font=FONT_SMALL, fg_color=BG_CARD_HOVER,
            hover_color=ACCENT_SUBTLE, text_color=TEXT_SECONDARY,
            corner_radius=6, command=self._refresh_dashboard,
        ).pack(side="right")

        # Table header
        cols = ("Time", "ID", "Name", "Class", "Status")
        widths = (0.18, 0.14, 0.28, 0.20, 0.20)
        th = ctk.CTkFrame(recent_card, fg_color=BG_DARKEST, height=36, corner_radius=0)
        th.pack(fill="x", padx=16, pady=(0, 0))
        th.pack_propagate(False)
        for i, col in enumerate(cols):
            ctk.CTkLabel(
                th, text=col, font=FONT_BODY_BOLD,
                text_color=TEXT_MUTED, anchor="w",
            ).place(relx=sum(widths[:i]), rely=0.5, anchor="w", x=12)

        self._recent_table = ctk.CTkFrame(recent_card, fg_color="transparent")
        self._recent_table.pack(fill="x", padx=16, pady=(0, 14))

    def _render_chart(self):
        """Draw the weekly attendance bar chart using matplotlib."""
        for w in self._chart_frame.winfo_children():
            w.destroy()

        summary = get_weekly_summary()
        dates = list(summary.keys())
        counts = list(summary.values())

        # Abbreviate dates for labels
        labels = []
        for d in dates:
            try:
                dt = datetime.strptime(d, "%Y-%m-%d")
                labels.append(dt.strftime("%d\n%b"))
            except ValueError:
                labels.append(d[-5:])

        fig = Figure(figsize=(5.5, 2.6), dpi=100)
        fig.patch.set_facecolor(BG_CARD)
        ax = fig.add_subplot(111)

        ax.set_facecolor(BG_CARD)

        bars = ax.bar(
            labels, counts,
            color=ACCENT_PRIMARY, width=0.55,
            edgecolor=ACCENT_GRADIENT, linewidth=0.5,
            zorder=3, alpha=0.9,
        )

        # Style the bars with rounded tops isn't easy in mpl, so add gradient
        for bar, c in zip(bars, counts):
            if c > 0:
                bar.set_alpha(0.85)

        ax.set_ylabel("Students", fontsize=9, color=TEXT_MUTED, labelpad=8)
        ax.tick_params(colors=TEXT_MUTED, labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(BORDER_SUBTLE)
        ax.spines["bottom"].set_color(BORDER_SUBTLE)
        ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        ax.grid(axis="y", color=BORDER_SUBTLE, linewidth=0.4, alpha=0.5)

        fig.tight_layout(pad=1.5)

        canvas = FigureCanvasTkAgg(fig, master=self._chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _render_recent_table(self):
        """Populate today's attendance rows."""
        for w in self._recent_table.winfo_children():
            w.destroy()

        records = get_today_attendance()
        cols_w = (0.18, 0.14, 0.28, 0.20, 0.20)

        if not records:
            ctk.CTkLabel(
                self._recent_table,
                text="No attendance recorded today.",
                font=FONT_BODY, text_color=TEXT_MUTED,
            ).pack(pady=20)
            return

        for idx, rec in enumerate(records):
            bg = BG_DARKEST if idx % 2 == 0 else BG_CARD
            row = ctk.CTkFrame(
                self._recent_table, fg_color=bg,
                height=TABLE_ROW_HEIGHT, corner_radius=0,
            )
            row.pack(fill="x", pady=0)
            row.pack_propagate(False)

            values = (rec["Time"], rec["ID"], rec["Name"], rec["Class"], rec["Status"])
            for i, val in enumerate(values):
                color = STATUS_SUCCESS if val == "Present" else TEXT_PRIMARY
                ctk.CTkLabel(
                    row, text=val, font=FONT_BODY,
                    text_color=color, anchor="w",
                ).place(relx=sum(cols_w[:i]), rely=0.5, anchor="w", x=12)

    def _refresh_dashboard(self):
        """Refresh all dashboard data."""
        self._stat_total.configure(text=str(get_student_count()))
        self._stat_present.configure(text=str(get_today_present_count()))
        self._stat_absent.configure(text=str(get_today_absent_count()))
        rate = get_attendance_rate()
        self._stat_rate.configure(text=f"{rate}%")
        self._render_chart()
        self._render_recent_table()

        # Auto-refresh every 30 seconds while on dashboard
        if self._current_page == "dashboard":
            self._auto_refresh_id = self.after(30000, self._refresh_dashboard)

    def _update_clock(self):
        now = datetime.now().strftime("%A, %d %B %Y  •  %I:%M %p")
        self._clock_label.configure(text=now)
        self.after(30000, self._update_clock)

    # ════════════════════════════════════════
    #  PAGE: Students
    # ════════════════════════════════════════

    def _build_students_page(self):
        page = ctk.CTkFrame(self._content, fg_color=BG_DARK, corner_radius=0)
        self._pages["students"] = page

        # Header row
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(24, 0))

        ctk.CTkLabel(
            header, text="Students", font=FONT_HEADING_XL,
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        ctk.CTkButton(
            header, text="➕ Add Student", font=FONT_BUTTON,
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_HOVER,
            text_color=TEXT_ON_ACCENT, height=38,
            corner_radius=BUTTON_CORNER, width=150,
            command=self._show_add_student_dialog,
        ).pack(side="right")

        ctk.CTkLabel(
            page, text="Manage registered students",
            font=FONT_BODY, text_color=TEXT_SECONDARY, anchor="w",
        ).pack(fill="x", padx=30, pady=(4, 14))

        # Search bar
        search_row = ctk.CTkFrame(page, fg_color="transparent")
        search_row.pack(fill="x", padx=30, pady=(0, 10))

        self._student_search = ctk.CTkEntry(
            search_row, placeholder_text="🔍  Search by name, ID, or class ...",
            font=FONT_BODY, fg_color=BG_INPUT,
            border_color=BORDER_SUBTLE, text_color=TEXT_PRIMARY,
            height=INPUT_HEIGHT, corner_radius=INPUT_CORNER,
        )
        self._student_search.pack(side="left", fill="x", expand=True)
        self._student_search.bind("<KeyRelease>", lambda e: self._refresh_students())

        # Table card
        table_card = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=CARD_CORNER)
        table_card.pack(fill="both", expand=True, padx=30, pady=(0, 24))

        # Table header
        cols = ("ID", "Name", "Class", "Actions")
        widths_s = (0.15, 0.35, 0.25, 0.25)
        th = ctk.CTkFrame(table_card, fg_color=BG_DARKEST, height=40, corner_radius=0)
        th.pack(fill="x", padx=0, pady=0)
        th.pack_propagate(False)
        for i, col in enumerate(cols):
            ctk.CTkLabel(
                th, text=col, font=FONT_BODY_BOLD,
                text_color=TEXT_MUTED, anchor="w",
            ).place(relx=sum(widths_s[:i]), rely=0.5, anchor="w", x=16)

        self._students_table = ctk.CTkScrollableFrame(
            table_card, fg_color="transparent",
        )
        self._students_table.pack(fill="both", expand=True)

    def _refresh_students(self):
        for w in self._students_table.winfo_children():
            w.destroy()

        query = self._student_search.get().strip()
        students = search_students(query) if query else get_all_students()
        widths_s = (0.15, 0.35, 0.25, 0.25)

        if not students:
            ctk.CTkLabel(
                self._students_table,
                text="No students found.", font=FONT_BODY,
                text_color=TEXT_MUTED,
            ).pack(pady=30)
            return

        for idx, s in enumerate(students):
            bg = BG_DARKEST if idx % 2 == 0 else "transparent"
            row = ctk.CTkFrame(
                self._students_table, fg_color=bg,
                height=TABLE_ROW_HEIGHT, corner_radius=0,
            )
            row.pack(fill="x", pady=0)
            row.pack_propagate(False)

            vals = (s["ID"], s["Name"], s["Class"])
            for i, val in enumerate(vals):
                ctk.CTkLabel(
                    row, text=val, font=FONT_BODY,
                    text_color=TEXT_PRIMARY, anchor="w",
                ).place(relx=sum(widths_s[:i]), rely=0.5, anchor="w", x=16)

            # Delete button
            ctk.CTkButton(
                row, text="🗑  Delete", width=80, height=28,
                font=FONT_SMALL, fg_color=BG_CARD_HOVER,
                hover_color=STATUS_DANGER, text_color=TEXT_SECONDARY,
                corner_radius=6,
                command=lambda sid=s["ID"]: self._delete_student(sid),
            ).place(relx=sum(widths_s[:3]), rely=0.5, anchor="w", x=16)

    def _show_add_student_dialog(self):
        """Top-level dialog for adding a student."""
        dlg = ctk.CTkToplevel(self)
        dlg.title("Add New Student")
        dlg.geometry("420x460")
        dlg.configure(fg_color=BG_DARK)
        dlg.resizable(False, False)
        dlg.transient(self)
        dlg.grab_set()

        # Center the dialog
        dlg.after(10, lambda: dlg.focus_force())

        ctk.CTkLabel(
            dlg, text="Add New Student", font=FONT_HEADING_LG,
            text_color=TEXT_PRIMARY,
        ).pack(pady=(24, 4))
        ctk.CTkLabel(
            dlg, text="Fill in the student details below",
            font=FONT_BODY, text_color=TEXT_SECONDARY,
        ).pack(pady=(0, 18))

        form = ctk.CTkFrame(dlg, fg_color="transparent")
        form.pack(fill="x", padx=32)

        # ID
        ctk.CTkLabel(form, text="Student ID", font=FONT_BODY_BOLD, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 4))
        id_entry = ctk.CTkEntry(form, font=FONT_BODY, fg_color=BG_INPUT, border_color=BORDER_SUBTLE, text_color=TEXT_PRIMARY, height=INPUT_HEIGHT, corner_radius=INPUT_CORNER)
        id_entry.pack(fill="x", pady=(0, 10))

        # Name
        ctk.CTkLabel(form, text="Student Name", font=FONT_BODY_BOLD, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 4))
        name_entry = ctk.CTkEntry(form, font=FONT_BODY, fg_color=BG_INPUT, border_color=BORDER_SUBTLE, text_color=TEXT_PRIMARY, height=INPUT_HEIGHT, corner_radius=INPUT_CORNER)
        name_entry.pack(fill="x", pady=(0, 10))

        # Class
        ctk.CTkLabel(form, text="Class", font=FONT_BODY_BOLD, text_color=TEXT_SECONDARY).pack(anchor="w", pady=(0, 4))
        class_entry = ctk.CTkEntry(form, font=FONT_BODY, fg_color=BG_INPUT, border_color=BORDER_SUBTLE, text_color=TEXT_PRIMARY, height=INPUT_HEIGHT, corner_radius=INPUT_CORNER)
        class_entry.pack(fill="x", pady=(0, 18))

        # Status label
        status = ctk.CTkLabel(form, text="", font=FONT_SMALL, text_color=STATUS_DANGER)
        status.pack()

        def on_submit():
            ok, msg = add_student(
                id_entry.get().strip(),
                name_entry.get().strip(),
                class_entry.get().strip(),
            )
            if ok:
                status.configure(text=msg, text_color=STATUS_SUCCESS)
                self._refresh_students()
                dlg.after(800, dlg.destroy)
            else:
                status.configure(text=msg, text_color=STATUS_DANGER)

        ctk.CTkButton(
            form, text="Add Student", font=FONT_BUTTON,
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_HOVER,
            text_color=TEXT_ON_ACCENT, height=42,
            corner_radius=BUTTON_CORNER, command=on_submit,
        ).pack(fill="x", pady=(8, 0))

    def _delete_student(self, student_id):
        """Confirm and delete a student."""
        confirm = ctk.CTkToplevel(self)
        confirm.title("Confirm Delete")
        confirm.geometry("360x180")
        confirm.configure(fg_color=BG_DARK)
        confirm.resizable(False, False)
        confirm.transient(self)
        confirm.grab_set()
        confirm.after(10, lambda: confirm.focus_force())

        ctk.CTkLabel(
            confirm, text="⚠️  Are you sure?", font=FONT_HEADING_MD,
            text_color=STATUS_WARNING,
        ).pack(pady=(24, 8))
        ctk.CTkLabel(
            confirm, text=f"Delete student ID: {student_id}",
            font=FONT_BODY, text_color=TEXT_SECONDARY,
        ).pack(pady=(0, 16))

        btn_row = ctk.CTkFrame(confirm, fg_color="transparent")
        btn_row.pack()

        ctk.CTkButton(
            btn_row, text="Cancel", width=100, height=36,
            font=FONT_BODY, fg_color=BG_CARD_HOVER,
            text_color=TEXT_SECONDARY, corner_radius=BUTTON_CORNER,
            command=confirm.destroy,
        ).pack(side="left", padx=6)

        def do_delete():
            delete_student(student_id)
            self._refresh_students()
            confirm.destroy()

        ctk.CTkButton(
            btn_row, text="Delete", width=100, height=36,
            font=FONT_BUTTON, fg_color=STATUS_DANGER,
            hover_color="#DC2626", text_color=TEXT_ON_ACCENT,
            corner_radius=BUTTON_CORNER, command=do_delete,
        ).pack(side="left", padx=6)

    # ════════════════════════════════════════
    #  PAGE: Attendance
    # ════════════════════════════════════════

    def _build_attendance_page(self):
        page = ctk.CTkFrame(self._content, fg_color=BG_DARK, corner_radius=0)
        self._pages["attendance"] = page

        # Header
        header = ctk.CTkFrame(page, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(24, 0))

        ctk.CTkLabel(
            header, text="Attendance Log", font=FONT_HEADING_XL,
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        # Start Attendance Camera button
        ctk.CTkButton(
            header, text="📸  Start Camera", font=FONT_BUTTON,
            fg_color=STATUS_SUCCESS, hover_color="#059669",
            text_color=TEXT_ON_ACCENT, height=38,
            corner_radius=BUTTON_CORNER, width=160,
            command=lambda: self._launch_subprocess("attendance_recognize.py"),
        ).pack(side="right", padx=(8, 0))

        # Open CSV
        ctk.CTkButton(
            header, text="📂  Open CSV", font=FONT_BUTTON,
            fg_color=BG_CARD, hover_color=BG_CARD_HOVER,
            text_color=TEXT_SECONDARY, height=38,
            corner_radius=BUTTON_CORNER, width=130,
            command=self._open_attendance_csv,
        ).pack(side="right")

        ctk.CTkLabel(
            page, text="View and filter attendance records",
            font=FONT_BODY, text_color=TEXT_SECONDARY, anchor="w",
        ).pack(fill="x", padx=30, pady=(4, 14))

        # Search row
        search_row = ctk.CTkFrame(page, fg_color="transparent")
        search_row.pack(fill="x", padx=30, pady=(0, 10))

        self._att_search = ctk.CTkEntry(
            search_row,
            placeholder_text="🔍  Search by name, ID, class, or date ...",
            font=FONT_BODY, fg_color=BG_INPUT,
            border_color=BORDER_SUBTLE, text_color=TEXT_PRIMARY,
            height=INPUT_HEIGHT, corner_radius=INPUT_CORNER,
        )
        self._att_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self._att_search.bind("<KeyRelease>", lambda e: self._refresh_attendance())

        # Date filter
        self._att_date_var = ctk.StringVar(value="All Dates")
        self._att_date_menu = ctk.CTkOptionMenu(
            search_row, variable=self._att_date_var,
            values=["All Dates"],
            font=FONT_BODY, fg_color=BG_INPUT,
            button_color=ACCENT_SUBTLE,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=ACCENT_SUBTLE,
            text_color=TEXT_PRIMARY, width=160, height=INPUT_HEIGHT,
            corner_radius=INPUT_CORNER,
            command=lambda _: self._refresh_attendance(),
        )
        self._att_date_menu.pack(side="right")

        # Table card
        table_card = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=CARD_CORNER)
        table_card.pack(fill="both", expand=True, padx=30, pady=(0, 24))

        # Table header
        att_cols = ("Date", "Time", "ID", "Name", "Class", "Status")
        self._att_widths = (0.17, 0.14, 0.12, 0.24, 0.16, 0.17)
        th = ctk.CTkFrame(table_card, fg_color=BG_DARKEST, height=40, corner_radius=0)
        th.pack(fill="x")
        th.pack_propagate(False)
        for i, col in enumerate(att_cols):
            ctk.CTkLabel(
                th, text=col, font=FONT_BODY_BOLD,
                text_color=TEXT_MUTED, anchor="w",
            ).place(relx=sum(self._att_widths[:i]), rely=0.5, anchor="w", x=14)

        self._att_table = ctk.CTkScrollableFrame(table_card, fg_color="transparent")
        self._att_table.pack(fill="both", expand=True)

    def _refresh_attendance(self):
        for w in self._att_table.winfo_children():
            w.destroy()

        # Update date filter options
        dates = ["All Dates"] + get_unique_dates()
        self._att_date_menu.configure(values=dates)

        query = self._att_search.get().strip()
        date_filter = self._att_date_var.get()

        if query:
            records = search_attendance(query)
        elif date_filter != "All Dates":
            records = get_attendance_by_date(date_filter)
        else:
            records = get_all_attendance()

        if not records:
            ctk.CTkLabel(
                self._att_table, text="No records found.",
                font=FONT_BODY, text_color=TEXT_MUTED,
            ).pack(pady=30)
            return

        for idx, rec in enumerate(reversed(records)):  # newest first
            bg = BG_DARKEST if idx % 2 == 0 else "transparent"
            row = ctk.CTkFrame(
                self._att_table, fg_color=bg,
                height=TABLE_ROW_HEIGHT, corner_radius=0,
            )
            row.pack(fill="x")
            row.pack_propagate(False)

            vals = (rec["Date"], rec["Time"], rec["ID"], rec["Name"], rec["Class"], rec["Status"])
            for i, val in enumerate(vals):
                color = STATUS_SUCCESS if val == "Present" else TEXT_PRIMARY
                ctk.CTkLabel(
                    row, text=val, font=FONT_BODY,
                    text_color=color, anchor="w",
                ).place(relx=sum(self._att_widths[:i]), rely=0.5, anchor="w", x=14)

    def _open_attendance_csv(self):
        path = os.path.join(os.path.dirname(__file__), "attendance.csv")
        if os.path.exists(path):
            os.startfile(path)

    # ════════════════════════════════════════
    #  PAGE: Register Face
    # ════════════════════════════════════════

    def _build_register_page(self):
        page = ctk.CTkFrame(self._content, fg_color=BG_DARK, corner_radius=0)
        self._pages["register"] = page

        ctk.CTkLabel(
            page, text="Register Face", font=FONT_HEADING_XL,
            text_color=TEXT_PRIMARY, anchor="w",
        ).pack(fill="x", padx=30, pady=(24, 4))
        ctk.CTkLabel(
            page, text="Capture face images for a student to train the recognition model",
            font=FONT_BODY, text_color=TEXT_SECONDARY, anchor="w",
        ).pack(fill="x", padx=30, pady=(0, 24))

        # Card
        card = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=CARD_CORNER)
        card.pack(fill="x", padx=30, pady=(0, 20))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=40, pady=36)

        # Big camera icon
        ctk.CTkLabel(
            inner, text="📸", font=(FONT_FAMILY, 56),
        ).pack(pady=(0, 16))

        ctk.CTkLabel(
            inner, text="Face Registration",
            font=FONT_HEADING_LG, text_color=TEXT_PRIMARY,
        ).pack(pady=(0, 6))
        ctk.CTkLabel(
            inner,
            text="Select a student and click 'Start Capture' to open the camera.\n"
                 "100 face images will be captured automatically.",
            font=FONT_BODY, text_color=TEXT_SECONDARY, justify="center",
        ).pack(pady=(0, 22))

        # Student selector
        self._reg_student_var = ctk.StringVar(value="Select Student")
        self._reg_student_menu = ctk.CTkOptionMenu(
            inner, variable=self._reg_student_var,
            values=["Select Student"],
            font=FONT_BODY, fg_color=BG_INPUT,
            button_color=ACCENT_SUBTLE,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=ACCENT_SUBTLE,
            text_color=TEXT_PRIMARY, width=280, height=INPUT_HEIGHT,
            corner_radius=INPUT_CORNER,
        )
        self._reg_student_menu.pack(pady=(0, 16))

        self._reg_status = ctk.CTkLabel(
            inner, text="", font=FONT_BODY, text_color=TEXT_MUTED,
        )
        self._reg_status.pack(pady=(0, 10))

        ctk.CTkButton(
            inner, text="🎥  Start Capture", font=FONT_BUTTON,
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_HOVER,
            text_color=TEXT_ON_ACCENT, height=46, width=220,
            corner_radius=BUTTON_CORNER,
            command=self._start_face_registration,
        ).pack()

    def _refresh_register(self):
        students = get_all_students()
        names = [s["Name"] for s in students]
        if names:
            self._reg_student_menu.configure(values=names)
        else:
            self._reg_student_menu.configure(values=["No students registered"])

    def _start_face_registration(self):
        name = self._reg_student_var.get()
        if name in ("Select Student", "No students registered"):
            self._reg_status.configure(
                text="⚠️  Please select a student first.",
                text_color=STATUS_WARNING,
            )
            return

        self._reg_status.configure(
            text=f"📸  Camera opened for {name}. Press 'Q' to stop.",
            text_color=STATUS_SUCCESS,
        )

        # Launch register_face.py with piped student name
        def run():
            proc = subprocess.Popen(
                [sys.executable, "register_face.py"],
                stdin=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__)),
            )
            proc.communicate(input=name + "\n")
            self.after(0, lambda: self._reg_status.configure(
                text="✅  Registration complete! Don't forget to train the model.",
                text_color=STATUS_SUCCESS,
            ))

        threading.Thread(target=run, daemon=True).start()

    # ════════════════════════════════════════
    #  PAGE: Train Model
    # ════════════════════════════════════════

    def _build_train_page(self):
        page = ctk.CTkFrame(self._content, fg_color=BG_DARK, corner_radius=0)
        self._pages["train"] = page

        ctk.CTkLabel(
            page, text="Train Model", font=FONT_HEADING_XL,
            text_color=TEXT_PRIMARY, anchor="w",
        ).pack(fill="x", padx=30, pady=(24, 4))
        ctk.CTkLabel(
            page, text="Train the face recognition model with registered faces",
            font=FONT_BODY, text_color=TEXT_SECONDARY, anchor="w",
        ).pack(fill="x", padx=30, pady=(0, 24))

        # Card
        card = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=CARD_CORNER)
        card.pack(fill="x", padx=30, pady=(0, 20))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=40, pady=40)

        ctk.CTkLabel(
            inner, text="🧠", font=(FONT_FAMILY, 56),
        ).pack(pady=(0, 16))

        ctk.CTkLabel(
            inner, text="LBPH Face Recognizer",
            font=FONT_HEADING_LG, text_color=TEXT_PRIMARY,
        ).pack(pady=(0, 6))
        ctk.CTkLabel(
            inner,
            text="This will scan all registered face images in the 'faces/' directory\n"
                 "and train the Local Binary Pattern Histogram model.",
            font=FONT_BODY, text_color=TEXT_SECONDARY, justify="center",
        ).pack(pady=(0, 8))

        # Info about trainer.yml
        trainer_path = os.path.join(os.path.dirname(__file__), "trainer.yml")
        if os.path.exists(trainer_path):
            size_mb = os.path.getsize(trainer_path) / (1024 * 1024)
            mtime = datetime.fromtimestamp(os.path.getmtime(trainer_path))
            info = f"Last trained: {mtime.strftime('%d %b %Y, %I:%M %p')}  •  Model size: {size_mb:.1f} MB"
        else:
            info = "No trained model found yet."

        self._train_info = ctk.CTkLabel(
            inner, text=info, font=FONT_SMALL, text_color=TEXT_MUTED,
        )
        self._train_info.pack(pady=(4, 20))

        self._train_status = ctk.CTkLabel(
            inner, text="", font=FONT_BODY, text_color=TEXT_MUTED,
        )
        self._train_status.pack(pady=(0, 10))

        # Progress bar
        self._train_progress = ctk.CTkProgressBar(
            inner, width=300, height=8,
            progress_color=ACCENT_PRIMARY,
            fg_color=BG_DARKEST,
        )
        self._train_progress.pack(pady=(0, 16))
        self._train_progress.set(0)

        self._train_btn = ctk.CTkButton(
            inner, text="🚀  Start Training", font=FONT_BUTTON,
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_HOVER,
            text_color=TEXT_ON_ACCENT, height=46, width=220,
            corner_radius=BUTTON_CORNER,
            command=self._start_training,
        )
        self._train_btn.pack()

    def _refresh_train(self):
        trainer_path = os.path.join(os.path.dirname(__file__), "trainer.yml")
        if os.path.exists(trainer_path):
            size_mb = os.path.getsize(trainer_path) / (1024 * 1024)
            mtime = datetime.fromtimestamp(os.path.getmtime(trainer_path))
            info = f"Last trained: {mtime.strftime('%d %b %Y, %I:%M %p')}  •  Model size: {size_mb:.1f} MB"
        else:
            info = "No trained model found yet."
        self._train_info.configure(text=info)

    def _start_training(self):
        self._train_btn.configure(state="disabled", text="⏳  Training...")
        self._train_status.configure(text="Training in progress...", text_color=STATUS_WARNING)
        self._train_progress.set(0)

        # Animate progress
        self._train_anim_running = True

        def animate(val=0.0):
            if not self._train_anim_running:
                return
            if val < 0.85:
                val += 0.02
                self._train_progress.set(val)
                self.after(200, lambda: animate(val))

        animate()

        def run():
            proc = subprocess.run(
                [sys.executable, "train_model.py"],
                capture_output=True, text=True,
                cwd=os.path.dirname(os.path.abspath(__file__)),
            )

            def done():
                self._train_anim_running = False
                self._train_progress.set(1.0)
                if proc.returncode == 0:
                    self._train_status.configure(
                        text="✅  Training complete! Model saved to trainer.yml",
                        text_color=STATUS_SUCCESS,
                    )
                else:
                    error_msg = proc.stderr.strip()[:120] if proc.stderr else "Unknown error"
                    self._train_status.configure(
                        text=f"❌  Error: {error_msg}",
                        text_color=STATUS_DANGER,
                    )
                self._train_btn.configure(state="normal", text="🚀  Start Training")
                self._refresh_train()

            self.after(0, done)

        threading.Thread(target=run, daemon=True).start()

    # ════════════════════════════════════════
    #  Subprocess Launcher
    # ════════════════════════════════════════

    def _launch_subprocess(self, script_name):
        """Launch a Python script as a detached subprocess."""
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        subprocess.Popen(
            [sys.executable, script],
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

    def _on_exit(self):
        if self._auto_refresh_id:
            self.after_cancel(self._auto_refresh_id)
        self.destroy()


# ════════════════════════════════════════════
#  Entry Point
# ════════════════════════════════════════════

if __name__ == "__main__":
    app = App()
    app.mainloop()