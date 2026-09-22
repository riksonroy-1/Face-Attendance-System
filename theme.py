# ============================================
# SNGCE College — Face Attendance System
# Theme & Style Constants
# ============================================

# ── Color Palette ──────────────────────────

# Backgrounds
BG_DARKEST    = "#0B0F19"       # Sidebar / deepest background
BG_DARK       = "#111827"       # Main content area
BG_CARD       = "#1E293B"       # Card / widget background
BG_CARD_HOVER = "#273548"       # Card hover state
BG_INPUT      = "#1A2332"       # Input fields

# Accents
ACCENT_PRIMARY   = "#06B6D4"    # Cyan-500 (primary buttons, highlights)
ACCENT_SECONDARY = "#0EA5E9"    # Sky-500
ACCENT_GRADIENT  = "#22D3EE"    # Cyan-400 (lighter accent)
ACCENT_HOVER     = "#0891B2"    # Cyan-600 (button hover)
ACCENT_SUBTLE    = "#164E63"    # Cyan-900 (subtle backgrounds)

# Status Colors
STATUS_SUCCESS = "#10B981"      # Emerald-500
STATUS_WARNING = "#F59E0B"      # Amber-500
STATUS_DANGER  = "#EF4444"      # Red-500
STATUS_INFO    = "#6366F1"      # Indigo-500

# Text
TEXT_PRIMARY   = "#F1F5F9"      # Slate-100 (headings)
TEXT_SECONDARY = "#94A3B8"      # Slate-400 (body / labels)
TEXT_MUTED     = "#64748B"      # Slate-500 (placeholders, footnotes)
TEXT_ON_ACCENT = "#FFFFFF"      # White on accent backgrounds

# Borders / Dividers
BORDER_COLOR   = "#1E293B"
BORDER_SUBTLE  = "#334155"

# Stat-card accent strips (left border color per card)
CARD_ACCENT_1 = "#06B6D4"   # Total Students  — Cyan
CARD_ACCENT_2 = "#10B981"   # Present Today   — Emerald
CARD_ACCENT_3 = "#EF4444"   # Absent Today    — Red
CARD_ACCENT_4 = "#8B5CF6"   # Attendance Rate — Violet

# ── Fonts ──────────────────────────────────

FONT_FAMILY      = "Segoe UI"
FONT_HEADING_XL  = (FONT_FAMILY, 26, "bold")
FONT_HEADING_LG  = (FONT_FAMILY, 20, "bold")
FONT_HEADING_MD  = (FONT_FAMILY, 16, "bold")
FONT_HEADING_SM  = (FONT_FAMILY, 14, "bold")
FONT_BODY        = (FONT_FAMILY, 13)
FONT_BODY_BOLD   = (FONT_FAMILY, 13, "bold")
FONT_SMALL       = (FONT_FAMILY, 11)
FONT_TINY        = (FONT_FAMILY, 10)
FONT_STAT_VALUE  = (FONT_FAMILY, 32, "bold")
FONT_STAT_LABEL  = (FONT_FAMILY, 11)
FONT_NAV         = (FONT_FAMILY, 14)
FONT_NAV_ACTIVE  = (FONT_FAMILY, 14, "bold")
FONT_BUTTON      = (FONT_FAMILY, 13, "bold")

# ── Dimensions ─────────────────────────────

SIDEBAR_WIDTH     = 240
CARD_CORNER       = 12
CARD_PADDING      = 20
BUTTON_CORNER     = 8
BUTTON_HEIGHT     = 40
INPUT_CORNER      = 8
INPUT_HEIGHT      = 38
TABLE_ROW_HEIGHT  = 42
NAV_ITEM_HEIGHT   = 44

# ── Branding ───────────────────────────────

APP_TITLE   = "SNGCE College"
APP_SUBTITLE = "Face Attendance Management System"
APP_VERSION  = "v2.0"

# ── Navigation Items ───────────────────────

NAV_ITEMS = [
    {"icon": "📊", "label": "Dashboard",     "key": "dashboard"},
    {"icon": "👥", "label": "Students",       "key": "students"},
    {"icon": "📋", "label": "Attendance",     "key": "attendance"},
    {"icon": "📸", "label": "Register Face",  "key": "register"},
    {"icon": "🧠", "label": "Train Model",   "key": "train"},
]
