import sys
import os
import json
import csv
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                            QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, 
                            QComboBox, QLineEdit, QDialog, QFormLayout, QSpinBox, QDoubleSpinBox, 
                            QMessageBox, QFileDialog, QTabWidget, QTextEdit, QFrame, QScrollArea)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QSize, QTranslator, QLocale, QLibraryInfo, pyqtSignal, QTimer
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Default language
DEFAULT_LANGUAGE = "en"  # "en" for English, "ar" for Arabic

# Translations dictionary
translations = {
    "en": {
        "app_title": "Café POS System",
        "menu": "Menu",
        "inventory": "Inventory",
        "sales": "Sales",
        "settings": "Settings",
        "add_item": "Add Item",
        "edit_item": "Edit Item",
        "remove_item": "Remove Item",
        "checkout": "Checkout",
        "print_receipt": "Print Receipt",
        "export_sales": "Export Sales",
        "total": "Total",
        "quantity": "Quantity",
        "price": "Price",
        "name": "Name",
        "description": "Description",
        "category": "Category",
        "item_added": "Item added successfully!",
        "item_updated": "Item updated successfully!",
        "item_removed": "Item removed successfully!",
        "inventory_level": "Inventory Level",
        "top_selling": "Top Selling Items",
        "language": "Language",
        "receipt": "Receipt",
        "date": "Date",
        "time": "Time",
        "thank_you": "Thank you for your visit!",
        "save": "Save",
        "cancel": "Cancel",
        "confirm_remove": "Are you sure you want to remove this item?",
        "yes": "Yes",
        "no": "No",
        "subtotal": "Subtotal",
        "tax": "Tax",
        "search": "Search",
        "item_id": "Item ID",
        "sold": "Sold",
        "revenue": "Revenue",
        "analytics": "Analytics",
        "daily_sales": "Daily Sales",
        "monthly_sales": "Monthly Sales",
        "add_to_cart": "Add to Cart",
        "clear_cart": "Clear Cart",
        "cart": "Cart"
    },
    "ar": {
        "app_title": "نظام نقاط البيع للمقهى",
        "menu": "القائمة",
        "inventory": "المخزون",
        "sales": "المبيعات",
        "settings": "الإعدادات",
        "add_item": "إضافة عنصر",
        "edit_item": "تعديل العنصر",
        "remove_item": "إزالة العنصر",
        "checkout": "الدفع",
        "print_receipt": "طباعة الإيصال",
        "export_sales": "تصدير المبيعات",
        "total": "المجموع",
        "quantity": "الكمية",
        "price": "السعر",
        "name": "الاسم",
        "description": "الوصف",
        "category": "الفئة",
        "item_added": "تمت إضافة العنصر بنجاح!",
        "item_updated": "تم تحديث العنصر بنجاح!",
        "item_removed": "تمت إزالة العنصر بنجاح!",
        "inventory_level": "مستوى المخزون",
        "top_selling": "العناصر الأكثر مبيعًا",
        "language": "اللغة",
        "receipt": "إيصال",
        "date": "التاريخ",
        "time": "الوقت",
        "thank_you": "شكرا لزيارتك!",
        "save": "حفظ",
        "cancel": "إلغاء",
        "confirm_remove": "هل أنت متأكد أنك تريد إزالة هذا العنصر؟",
        "yes": "نعم",
        "no": "لا",
        "subtotal": "المجموع الفرعي",
        "tax": "الضريبة",
        "search": "بحث",
        "item_id": "معرف العنصر",
        "sold": "تم البيع",
        "revenue": "الإيرادات",
        "analytics": "التحليلات",
        "daily_sales": "المبيعات اليومية",
        "monthly_sales": "المبيعات الشهرية",
        "add_to_cart": "أضف إلى السلة",
        "clear_cart": "مسح السلة",
        "cart": "عربة التسوق"
    }
}

# File paths
DATA_DIR = "data"
MENU_FILE = os.path.join(DATA_DIR, "menu.json")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")
SALES_FILE = os.path.join(DATA_DIR, "sales.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Default menu items
default_menu = [
    {
        "id": 1,
        "name_en": "Espresso",
        "name_ar": "إسبريسو",
        "description_en": "Strong black coffee",
        "description_ar": "قهوة سوداء قوية",
        "price": 3.50,
        "category": "Coffee",
        "image": "espresso.png"
    },
    {
        "id": 2,
        "name_en": "Cappuccino",
        "name_ar": "كابتشينو",
        "description_en": "Espresso with steamed milk and foam",
        "description_ar": "إسبريسو مع حليب مبخر ورغوة",
        "price": 4.50,
        "category": "Coffee",
        "image": "cappuccino.png"
    },
    {
        "id": 3,
        "name_en": "Latte",
        "name_ar": "لاتيه",
        "description_en": "Espresso with lots of steamed milk",
        "description_ar": "إسبريسو مع الكثير من الحليب المبخر",
        "price": 4.00,
        "category": "Coffee",
        "image": "latte.png"
    },
    {
        "id": 4,
        "name_en": "Mocha",
        "name_ar": "موكا",
        "description_en": "Espresso with chocolate and steamed milk",
        "description_ar": "إسبريسو مع الشوكولاتة والحليب المبخر",
        "price": 5.00,
        "category": "Coffee",
        "image": "mocha.png"
    },
    {
        "id": 5,
        "name_en": "Americano",
        "name_ar": "أمريكانو",
        "description_en": "Espresso with hot water",
        "description_ar": "إسبريسو مع ماء ساخن",
        "price": 3.75,
        "category": "Coffee",
        "image": "americano.png"
    },
    {
        "id": 6,
        "name_en": "Croissant",
        "name_ar": "كرواسان",
        "description_en": "Buttery flaky pastry",
        "description_ar": "معجنات هشة بالزبدة",
        "price": 2.50,
        "category": "Pastry",
        "image": "croissant.png"
    },
    {
        "id": 7,
        "name_en": "Chocolate Muffin",
        "name_ar": "مافن الشوكولاتة",
        "description_en": "Rich chocolate muffin",
        "description_ar": "مافن شوكولاتة غني",
        "price": 3.00,
        "category": "Pastry",
        "image": "muffin.png"
    },
    {
        "id": 8,
        "name_en": "Orange Juice",
        "name_ar": "عصير البرتقال",
        "description_en": "Freshly squeezed orange juice",
        "description_ar": "عصير برتقال طازج",
        "price": 4.25,
        "category": "Beverage",
        "image": "juice.png"
    },
    {
        "id": 9,
        "name_en": "Iced Tea",
        "name_ar": "شاي مثلج",
        "description_en": "Sweet iced tea",
        "description_ar": "شاي مثلج حلو",
        "price": 3.25,
        "category": "Beverage",
        "image": "icedtea.png"
    },
    {
        "id": 10,
        "name_en": "Cheesecake",
        "name_ar": "كعكة الجبن",
        "description_en": "Creamy New York style cheesecake",
        "description_ar": "كعكة الجبن الكريمية على طريقة نيويورك",
        "price": 5.50,
        "category": "Dessert",
        "image": "cheesecake.png"
    }
]

# Initialize default data files if they don't exist
def initialize_data_files():
    # Menu
    if not os.path.exists(MENU_FILE):
        with open(MENU_FILE, 'w') as f:
            json.dump(default_menu, f, indent=4)
            
    # Inventory (Initial stock of 50 for each item)
    if not os.path.exists(INVENTORY_FILE):
        inventory = {str(item["id"]): 50 for item in default_menu}
        with open(INVENTORY_FILE, 'w') as f:
            json.dump(inventory, f, indent=4)
            
    # Sales
    if not os.path.exists(SALES_FILE):
        with open(SALES_FILE, 'w') as f:
            json.dump([], f, indent=4)
            
    # Settings
    if not os.path.exists(SETTINGS_FILE):
        settings = {
            "language": DEFAULT_LANGUAGE,
            "tax_rate": 0.08,
            "shop_name_en": "Café Coffee",
            "shop_name_ar": "مقهى القهوة",
            "address_en": "123 Coffee Street, City",
            "address_ar": "١٢٣ شارع القهوة، المدينة",
            "phone": "+1 555-123-4567"
        }
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)

# Load data functions
def load_menu():
    try:
        with open(MENU_FILE, 'r') as f:
            return json.load(f)
    except:
        return default_menu

def load_inventory():
    try:
        with open(INVENTORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def load_sales():
    try:
        with open(SALES_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"language": DEFAULT_LANGUAGE, "tax_rate": 0.08}

# Save data functions
def save_menu(menu):
    with open(MENU_FILE, 'w') as f:
        json.dump(menu, f, indent=4)

def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f, indent=4)

def save_sales(sales):
    with open(SALES_FILE, 'w') as f:
        json.dump(sales, f, indent=4)

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# Utility function to get text based on current language
def get_text(key, language):
    if key in translations[language]:
        return translations[language][key]
    else:
        return key  # Return the key itself if translation not found

# Theme and style settings
DARK_THEME = {
    "background": "#1E1E1E",
    "foreground": "#FFFFFF",
    "primary": "#28B463",
    "secondary": "#3498DB",
    "accent": "#E74C3C",
    "button_bg": "#34495E",
    "button_fg": "#FFFFFF",
    "button_hover": "#2C3E50",
    "card_bg": "#2D2D2D",
    "border": "#555555",
    "success": "#2ECC71",
    "warning": "#F39C12",
    "error": "#E74C3C",
    "highlight": "#F1C40F"
}

# Custom QWidget for rounded cards
class Card(QFrame):
    def __init__(self, parent=None, background_color=None, border_radius=10):
        super().__init__(parent)
        self.background_color = background_color or DARK_THEME["card_bg"]
        self.border_radius = border_radius
        self.setStyleSheet(f"""
            background-color: {self.background_color};
            border-radius: {self.border_radius}px;
            padding: 15px;
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(self.layout)

# Custom QPushButton with modern styling
class StyledButton(QPushButton):
    def __init__(self, text="", parent=None, color=None, icon_path=None, size=(None, None)):
        super().__init__(text, parent)
        self.color = color or DARK_THEME["button_bg"]
        
        width, height = size
        if width and height:
            self.setFixedSize(width, height)
        
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                color: {DARK_THEME["button_fg"]};
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {DARK_THEME["button_hover"]};
            }}
            QPushButton:pressed {{
                background-color: {self.color};
            }}
        """)

# Main POS System Window
class POSSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize data
        initialize_data_files()
        
        # Load settings
        self.settings = load_settings()
        self.language = self.settings.get("language", DEFAULT_LANGUAGE)
        
        # Set up the main window
        self.setWindowTitle(get_text("app_title", self.language))
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(f"background-color: {DARK_THEME['background']}; color: {DARK_THEME['foreground']};")
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {DARK_THEME['border']};
                background-color: {DARK_THEME['background']};
            }}
            QTabBar::tab {{
                background-color: {DARK_THEME['button_bg']};
                color: {DARK_THEME['foreground']};
                border: none;
                border-radius: 5px 5px 0 0;
                padding: 10px 15px;
                margin-right: 5px;
            }}
            QTabBar::tab:selected {{
                background-color: {DARK_THEME['primary']};
            }}
            QTabBar::tab:hover {{
                background-color: {DARK_THEME['button_hover']};
            }}
        """)
        
        # Create tabs
        self.pos_tab = QWidget()
        self.inventory_tab = QWidget()
        self.sales_tab = QWidget()
        self.analytics_tab = QWidget()
        self.settings_tab = QWidget()
        
        # Add tabs to the tab widget
        self.tab_widget.addTab(self.pos_tab, get_text("menu", self.language))
        self.tab_widget.addTab(self.inventory_tab, get_text("inventory", self.language))
        self.tab_widget.addTab(self.sales_tab, get_text("sales", self.language))
        self.tab_widget.addTab(self.analytics_tab, get_text("analytics", self.language))
        self.tab_widget.addTab(self.settings_tab, get_text("settings", self.language))
        
        # Main layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addWidget(self.tab_widget)
        
        # Set up individual tabs
        self.setup_pos_tab()
        self.setup_inventory_tab()
        self.setup_sales_tab()
        self.setup_analytics_tab()
        self.setup_settings_tab()
        
        # Load menu items
        self.load_menu_items()
        
        # Cart items
        self.cart_items = []
        
        # Show the window
        self.show()
    
    def setup_pos_tab(self):
        layout = QHBoxLayout(self.pos_tab)
        
        # Left side - Menu items
        menu_panel = QWidget()
        menu_layout = QVBoxLayout(menu_panel)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(get_text("search", self.language))
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 8px;
            }}
        """)
        self.search_input.textChanged.connect(self.filter_menu_items)
        search_layout.addWidget(self.search_input)
        menu_layout.addLayout(search_layout)
        
        # Category filter
        category_layout = QHBoxLayout()
        category_label = QLabel(get_text("category", self.language))
        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
            QComboBox::drop-down {{
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                selection-background-color: {DARK_THEME['primary']};
            }}
        """)
        self.category_combo.currentTextChanged.connect(self.filter_menu_items)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        menu_layout.addLayout(category_layout)
        
        # Menu items container
        self.menu_items_container = QScrollArea()
        self.menu_items_container.setWidgetResizable(True)
        self.menu_items_container.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {DARK_THEME['background']};
            }}
            QScrollBar:vertical {{
                background-color: {DARK_THEME['card_bg']};
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {DARK_THEME['primary']};
                min-height: 20px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        self.menu_items_widget = QWidget()
        self.menu_items_layout = QVBoxLayout(self.menu_items_widget)
        self.menu_items_layout.setAlignment(Qt.AlignTop)
        self.menu_items_container.setWidget(self.menu_items_widget)
        
        menu_layout.addWidget(self.menu_items_container)
        
        # Right side - Cart and checkout
        cart_panel = QWidget()
        cart_layout = QVBoxLayout(cart_panel)
        
        # Cart title
        cart_title = QLabel(get_text("cart", self.language))
        cart_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        cart_layout.addWidget(cart_title)
        
        # Cart table
        self.cart_table = QTableWidget(0, 4)
        self.cart_table.setHorizontalHeaderLabels([
            get_text("name", self.language),
            get_text("price", self.language),
            get_text("quantity", self.language),
            get_text("total", self.language)
        ])
        self.cart_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.cart_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.cart_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.cart_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.cart_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                gridline-color: {DARK_THEME['border']};
                border: none;
                border-radius: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_THEME['button_bg']};
                color: {DARK_THEME['foreground']};
                padding: 5px;
                border: none;
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QTableWidget::item:selected {{
                background-color: {DARK_THEME['primary']};
            }}
        """)
        cart_layout.addWidget(self.cart_table)
        
        # Total amount
        total_layout = QHBoxLayout()
        subtotal_label = QLabel(get_text("subtotal", self.language) + ":")
        self.subtotal_value = QLabel("$0.00")
        tax_label = QLabel(get_text("tax", self.language) + ":")
        self.tax_value = QLabel("$0.00")
        total_label = QLabel(get_text("total", self.language) + ":")
        self.total_value = QLabel("$0.00")
        self.total_value.setStyleSheet("font-size: 18px; font-weight: bold; color: " + DARK_THEME["success"])
        
        total_layout.addWidget(subtotal_label)
        total_layout.addWidget(self.subtotal_value)
        total_layout.addStretch()
        total_layout.addWidget(tax_label)
        total_layout.addWidget(self.tax_value)
        total_layout.addStretch()
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_value)
        
        cart_layout.addLayout(total_layout)
        
        # Checkout buttons
        buttons_layout = QHBoxLayout()
        
        clear_cart_btn = StyledButton(get_text("clear_cart", self.language), color=DARK_THEME["warning"])
        clear_cart_btn.clicked.connect(self.clear_cart)
        
        checkout_btn = StyledButton(get_text("checkout", self.language), color=DARK_THEME["success"])
        checkout_btn.clicked.connect(self.checkout)
        
        print_receipt_btn = StyledButton(get_text("print_receipt", self.language), color=DARK_THEME["primary"])
        print_receipt_btn.clicked.connect(self.print_receipt)
        
        buttons_layout.addWidget(clear_cart_btn)
        buttons_layout.addWidget(checkout_btn)
        buttons_layout.addWidget(print_receipt_btn)
        
        cart_layout.addLayout(buttons_layout)
        
        # Add panels to main layout
        splitter = QHBoxLayout()
        splitter.addWidget(menu_panel, 3)  # 3:2 ratio (60%/40%)
        splitter.addWidget(cart_panel, 2)
        layout.addLayout(splitter)
    
    def setup_inventory_tab(self):
        layout = QVBoxLayout(self.inventory_tab)
        
        # Title
        title = QLabel(get_text("inventory", self.language))
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Inventory table
        self.inventory_table = QTableWidget(0, 4)
        self.inventory_table.setHorizontalHeaderLabels([
            get_text("item_id", self.language),
            get_text("name", self.language),
            get_text("quantity", self.language),
            get_text("price", self.language)
        ])
        self.inventory_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.inventory_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.inventory_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.inventory_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.inventory_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                gridline-color: {DARK_THEME['border']};
                border: none;
                border-radius: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_THEME['button_bg']};
                color: {DARK_THEME['foreground']};
                padding: 5px;
                border: none;
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QTableWidget::item:selected {{
                background-color: {DARK_THEME['primary']};
            }}
        """)
        layout.addWidget(self.inventory_table)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        add_item_btn = StyledButton(get_text("add_item", self.language), color=DARK_THEME["success"])
        add_item_btn.clicked.connect(self.add_item_dialog)
        
        edit_item_btn = StyledButton(get_text("edit_item", self.language), color=DARK_THEME["primary"])
        edit_item_btn.clicked.connect(self.edit_item_dialog)
        
        remove_item_btn = StyledButton(get_text("remove_item", self.language), color=DARK_THEME["error"])
        remove_item_btn.clicked.connect(self.remove_item)
        
        buttons_layout.addWidget(add_item_btn)
        buttons_layout.addWidget(edit_item_btn)
        buttons_layout.addWidget(remove_item_btn)
        
        layout.addLayout(buttons_layout)
        
        # Update inventory table
        self.update_inventory_table()
    
    def setup_sales_tab(self):
        layout = QVBoxLayout(self.sales_tab)
        
        # Title
        title = QLabel(get_text("sales", self.language))
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Sales table
        self.sales_table = QTableWidget(0, 5)
        self.sales_table.setHorizontalHeaderLabels([
            get_text("date", self.language),
            get_text("time", self.language),
            get_text("item_id", self.language),
            get_text("quantity", self.language),
            get_text("total", self.language)
        ])
        self.sales_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.sales_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.sales_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.sales_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.sales_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.sales_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                gridline-color: {DARK_THEME['border']};
                border: none;
                border-radius: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_THEME['button_bg']};
                color: {DARK_THEME['foreground']};
                padding: 5px;
                border: none;
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QTableWidget::item:selected {{
                background-color: {DARK_THEME['primary']};
            }}
        """)
        layout.addWidget(self.sales_table)
        
        # Export button
        export_layout = QHBoxLayout()
        export_btn = StyledButton(get_text("export_sales", self.language), color=DARK_THEME["primary"])
        export_btn.clicked.connect(self.export_sales)
        export_layout.addStretch()
        export_layout.addWidget(export_btn)
        
        layout.addLayout(export_layout)
        
        # Update sales table
        self.update_sales_table()
    
    def setup_analytics_tab(self):
        layout = QVBoxLayout(self.analytics_tab)
        
        # Title
        title = QLabel(get_text("analytics", self.language))
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Analytics contents - Top row
        top_row = QHBoxLayout()
        
        # Top selling items card
        top_selling_card = Card()
        top_selling_layout = QVBoxLayout()
        top_selling_title = QLabel(get_text("top_selling", self.language))
        top_selling_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.top_selling_table = QTableWidget(0, 3)
        self.top_selling_table.setHorizontalHeaderLabels([
            get_text("name", self.language),
            get_text("sold", self.language),
            get_text("revenue", self.language)
        ])
        self.top_selling_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.top_selling_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.top_selling_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.top_selling_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                gridline-color: {DARK_THEME['border']};
                border: none;
            }}
            QHeaderView::section {{
                background-color: {DARK_THEME['button_bg']};
                color: {DARK_THEME['foreground']};
                padding: 5px;
                border: none;
            }}
        """)
        
        top_selling_layout.addWidget(top_selling_title)
        top_selling_layout.addWidget(self.top_selling_table)
        top_selling_card.layout.addLayout(top_selling_layout)
        
        # Sales chart card
        sales_chart_card = Card()
        sales_chart_layout = QVBoxLayout()
        sales_chart_title = QLabel(get_text("daily_sales", self.language))
        sales_chart_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        # Create matplotlib figure
        self.figure = plt.figure(figsize=(5, 4))
        self.figure.patch.set_facecolor(DARK_THEME['card_bg'])
        self.canvas = FigureCanvas(self.figure)
        
        sales_chart_layout.addWidget(sales_chart_title)
        sales_chart_layout.addWidget(self.canvas)
        sales_chart_card.layout.addLayout(sales_chart_layout)
        
        top_row.addWidget(top_selling_card)
        top_row.addWidget(sales_chart_card)
        
        layout.addLayout(top_row)
        
        # Update analytics data
        self.update_analytics()
    
    def setup_settings_tab(self):
        layout = QVBoxLayout(self.settings_tab)
        
        # Title
        title = QLabel(get_text("settings", self.language))
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Settings form
        settings_card = Card()
        form_layout = QFormLayout()
        
        # Language selection
        language_label = QLabel(get_text("language", self.language))
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("العربية (Arabic)", "ar")
        self.language_combo.setCurrentIndex(0 if self.language == "en" else 1)
        self.language_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
            QComboBox::drop-down {{
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                selection-background-color: {DARK_THEME['primary']};
            }}
        """)
        form_layout.addRow(language_label, self.language_combo)
        
        # Tax rate
        tax_label = QLabel(get_text("tax", self.language) + " (%)")
        self.tax_input = QDoubleSpinBox()
        self.tax_input.setRange(0, 30)
        self.tax_input.setValue(self.settings.get("tax_rate", 0.08) * 100)
        self.tax_input.setStyleSheet(f"""
            QDoubleSpinBox {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form_layout.addRow(tax_label, self.tax_input)
        
        # Shop name (English)
        shop_name_en_label = QLabel("Shop Name (English)")
        self.shop_name_en_input = QLineEdit()
        self.shop_name_en_input.setText(self.settings.get("shop_name_en", "Café Coffee"))
        self.shop_name_en_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form_layout.addRow(shop_name_en_label, self.shop_name_en_input)
        
        # Shop name (Arabic)
        shop_name_ar_label = QLabel("Shop Name (Arabic)")
        self.shop_name_ar_input = QLineEdit()
        self.shop_name_ar_input.setText(self.settings.get("shop_name_ar", "مقهى القهوة"))
        self.shop_name_ar_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form_layout.addRow(shop_name_ar_label, self.shop_name_ar_input)
        
        # Address (English)
        address_en_label = QLabel("Address (English)")
        self.address_en_input = QLineEdit()
        self.address_en_input.setText(self.settings.get("address_en", "123 Coffee Street, City"))
        self.address_en_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form_layout.addRow(address_en_label, self.address_en_input)
        
        # Address (Arabic)
        address_ar_label = QLabel("Address (Arabic)")
        self.address_ar_input = QLineEdit()
        self.address_ar_input.setText(self.settings.get("address_ar", "١٢٣ شارع القهوة، المدينة"))
        self.address_ar_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form_layout.addRow(address_ar_label, self.address_ar_input)
        
        # Phone
        phone_label = QLabel(get_text("phone", self.language))
        self.phone_input = QLineEdit()
        self.phone_input.setText(self.settings.get("phone", "+1 555-123-4567"))
        self.phone_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form_layout.addRow(phone_label, self.phone_input)
        
        settings_card.layout.addLayout(form_layout)
        layout.addWidget(settings_card)
        
        # Save button
        save_layout = QHBoxLayout()
        save_btn = StyledButton(get_text("save", self.language), color=DARK_THEME["primary"])
        save_btn.clicked.connect(self.save_settings)
        save_layout.addStretch()
        save_layout.addWidget(save_btn)
        
        layout.addLayout(save_layout)
    
    def load_menu_items(self):
        self.menu = load_menu()
        
        # Clear existing widgets
        for i in reversed(range(self.menu_items_layout.count())):
            widget = self.menu_items_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Clear and populate category filter
        self.category_combo.clear()
        self.category_combo.addItem("All Categories")
        
        categories = set()
        for item in self.menu:
            categories.add(item["category"])
        
        for category in sorted(categories):
            self.category_combo.addItem(category)
        
        # Load items
        self.display_menu_items(self.menu)
        
        # Update inventory table
        self.update_inventory_table()
    
    def display_menu_items(self, items):
        # Clear existing items
        for i in reversed(range(self.menu_items_layout.count())):
            widget = self.menu_items_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Get inventory data
        inventory = load_inventory()
        
        # Add items to menu layout
        for item in items:
            item_card = Card()
            item_layout = QHBoxLayout()
            
            # Item details
            details_layout = QVBoxLayout()
            
            name_key = f"name_{self.language}"
            desc_key = f"description_{self.language}"
            
            name_label = QLabel(item.get(name_key, item["name_en"]))
            name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            
            desc_label = QLabel(item.get(desc_key, item["description_en"]))
            desc_label.setStyleSheet("color: #AAAAAA;")
            
            price_label = QLabel(f"${item['price']:.2f}")
            price_label.setStyleSheet(f"color: {DARK_THEME['highlight']}; font-weight: bold;")
            
            details_layout.addWidget(name_label)
            details_layout.addWidget(desc_label)
            details_layout.addWidget(price_label)
            
            # Stock indicator
            stock_qty = int(inventory.get(str(item["id"]), 0))
            stock_label = QLabel(f"{get_text('quantity', self.language)}: {stock_qty}")
            
            if stock_qty <= 0:
                stock_label.setStyleSheet(f"color: {DARK_THEME['error']};")
            elif stock_qty < 10:
                stock_label.setStyleSheet(f"color: {DARK_THEME['warning']};")
            else:
                stock_label.setStyleSheet(f"color: {DARK_THEME['success']};")
            
            details_layout.addWidget(stock_label)
            
            # Add to cart button
            add_btn = StyledButton(get_text("add_to_cart", self.language), color=DARK_THEME["primary"])
            add_btn.setProperty("item_id", item["id"])
            add_btn.clicked.connect(self.add_to_cart)
            
            # Disable button if out of stock
            if stock_qty <= 0:
                add_btn.setEnabled(False)
                add_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {DARK_THEME['button_bg']};
                        color: #888888;
                        border: none;
                        border-radius: 5px;
                        padding: 10px 15px;
                        font-weight: bold;
                    }}
                """)
            
            # Item layout
            item_layout.addLayout(details_layout)
            item_layout.addStretch()
            item_layout.addWidget(add_btn)
            
            item_card.layout.addLayout(item_layout)
            self.menu_items_layout.addWidget(item_card)
            
        # Add stretch to push items to the top
        self.menu_items_layout.addStretch()
    
    def filter_menu_items(self):
        search_text = self.search_input.text().lower()
        selected_category = self.category_combo.currentText()
        
        filtered_items = []
        
        for item in self.menu:
            # Check if item matches the search text
            name_en = item["name_en"].lower()
            name_ar = item["name_ar"].lower()
            desc_en = item["description_en"].lower()
            desc_ar = item["description_ar"].lower()
            
            text_match = (search_text in name_en or search_text in name_ar or 
                         search_text in desc_en or search_text in desc_ar)
            
            # Check if item matches the selected category
            category_match = (selected_category == "All Categories" or 
                             item["category"] == selected_category)
            
            if text_match and category_match:
                filtered_items.append(item)
        
        self.display_menu_items(filtered_items)
    
    def add_to_cart(self):
        # Get item ID from the sender
        item_id = self.sender().property("item_id")
        
        # Find item in menu
        item = None
        for menu_item in self.menu:
            if menu_item["id"] == item_id:
                item = menu_item
                break
        
        if not item:
            return
        
        # Check if item already in cart
        for i, cart_item in enumerate(self.cart_items):
            if cart_item["id"] == item_id:
                # Update quantity
                inventory = load_inventory()
                available_stock = int(inventory.get(str(item_id), 0))
                
                if cart_item["quantity"] < available_stock:
                    self.cart_items[i]["quantity"] += 1
                    self.update_cart_table()
                    return
                else:
                    QMessageBox.warning(self, "Out of Stock", f"No more {item['name_en']} available in stock.")
                    return
        
        # Add new item to cart
        name_key = f"name_{self.language}"
        cart_item = {
            "id": item_id,
            "name": item.get(name_key, item["name_en"]),
            "price": item["price"],
            "quantity": 1
        }
        
        self.cart_items.append(cart_item)
        self.update_cart_table()
    
    def update_cart_table(self):
        # Clear table
        self.cart_table.setRowCount(0)
        
        # Calculate totals
        subtotal = 0
        tax_rate = self.settings.get("tax_rate", 0.08)
        
        # Add items to table
        for i, item in enumerate(self.cart_items):
            self.cart_table.insertRow(i)
            
            name_item = QTableWidgetItem(item["name"])
            price_item = QTableWidgetItem(f"${item['price']:.2f}")
            quantity_item = QTableWidgetItem(str(item["quantity"]))
            total_item = QTableWidgetItem(f"${item['price'] * item['quantity']:.2f}")
            
            self.cart_table.setItem(i, 0, name_item)
            self.cart_table.setItem(i, 1, price_item)
            self.cart_table.setItem(i, 2, quantity_item)
            self.cart_table.setItem(i, 3, total_item)
            
            subtotal += item["price"] * item["quantity"]
        
        # Update total labels
        tax = subtotal * tax_rate
        total = subtotal + tax
        
        self.subtotal_value.setText(f"${subtotal:.2f}")
        self.tax_value.setText(f"${tax:.2f}")
        self.total_value.setText(f"${total:.2f}")
    
    def clear_cart(self):
        self.cart_items = []
        self.update_cart_table()
    
    def checkout(self):
        if not self.cart_items:
            QMessageBox.warning(self, "Empty Cart", "Cart is empty. Please add items before checkout.")
            return
        
        # Calculate totals
        subtotal = 0
        for item in self.cart_items:
            subtotal += item["price"] * item["quantity"]
        
        tax_rate = self.settings.get("tax_rate", 0.08)
        tax = subtotal * tax_rate
        total = subtotal + tax
        
        # Create new sale receipt
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        receipt = {
            "id": f"REC-{now.strftime('%Y%m%d%H%M%S')}",
            "date": date_str,
            "time": time_str,
            "items": self.cart_items.copy(),
            "subtotal": subtotal,
            "tax": tax,
            "total": total
        }
        
        # Update inventory
        inventory = load_inventory()
        for item in self.cart_items:
            item_id = str(item["id"])
            if item_id in inventory:
                inventory[item_id] = max(0, int(inventory[item_id]) - item["quantity"])
        
        save_inventory(inventory)
        
        # Update sales data
        sales = load_sales()
        sales.append(receipt)
        save_sales(sales)
        
        # Print receipt
        self.print_receipt(receipt)
        
        # Clear cart
        self.clear_cart()
        
        # Update all relevant tables
        self.update_inventory_table()
        self.update_sales_table()
        self.update_analytics()
        self.load_menu_items()
        
        # Show success message
        QMessageBox.information(self, "Checkout", "Checkout successful! Receipt has been printed.")
    
    def print_receipt(self, receipt=None):
        if not receipt:
            if not self.cart_items:
                QMessageBox.warning(self, "Empty Cart", "Cart is empty. Please add items before printing receipt.")
                return
            
            # Calculate totals for current cart
            subtotal = 0
            for item in self.cart_items:
                subtotal += item["price"] * item["quantity"]
            
            tax_rate = self.settings.get("tax_rate", 0.08)
            tax = subtotal * tax_rate
            total = subtotal + tax
            
            # Create receipt object
            now = datetime.datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            
            receipt = {
                "id": f"REC-{now.strftime('%Y%m%d%H%M%S')}",
                "date": date_str,
                "time": time_str,
                "items": self.cart_items.copy(),
                "subtotal": subtotal,
                "tax": tax,
                "total": total
            }
        
        # Create receipt text
        receipt_text = self.generate_receipt_text(receipt)
        
        # Preview receipt
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle(get_text("receipt", self.language))
        preview_dialog.setMinimumSize(400, 600)
        preview_layout = QVBoxLayout(preview_dialog)
        
        receipt_display = QTextEdit()
        receipt_display.setReadOnly(True)
        receipt_display.setStyleSheet(f"""
            QTextEdit {{
                background-color: white;
                color: black;
                font-family: monospace;
                padding: 20px;
            }}
        """)
        receipt_display.setText(receipt_text)
        
        preview_layout.addWidget(receipt_display)
        
        buttons_layout = QHBoxLayout()
        print_btn = StyledButton(get_text("print_receipt", self.language), color=DARK_THEME["primary"])
        close_btn = StyledButton(get_text("cancel", self.language), color=DARK_THEME["button_bg"])
        
        # Print functionality
        def print_to_printer():
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                receipt_display.print_(printer)
                preview_dialog.accept()
        
        print_btn.clicked.connect(print_to_printer)
        close_btn.clicked.connect(preview_dialog.reject)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(print_btn)
        buttons_layout.addWidget(close_btn)
        
        preview_layout.addLayout(buttons_layout)
        
        preview_dialog.exec_()
    
    def generate_receipt_text(self, receipt):
        is_arabic = self.language == "ar"
        shop_name = self.settings.get(f"shop_name_{self.language}", 
                                    "مقهى القهوة" if is_arabic else "Café Coffee")
        address = self.settings.get(f"address_{self.language}", 
                                   "١٢٣ شارع القهوة، المدينة" if is_arabic else "123 Coffee Street, City")
        phone = self.settings.get("phone", "+1 555-123-4567")
        
        # Generate receipt content
        lines = []
        
        # Header
        lines.append(f"{shop_name}")
        lines.append(f"{address}")
        lines.append(f"{phone}")
        lines.append("=" * 40)
        lines.append(f"{get_text('receipt', self.language)}: {receipt['id']}")
        lines.append(f"{get_text('date', self.language)}: {receipt['date']}")
        lines.append(f"{get_text('time', self.language)}: {receipt['time']}")
        lines.append("-" * 40)
        
        # Items
        lines.append(f"{'Item':<25}{'Qty':>5}{'Price':>10}")
        lines.append("-" * 40)
        
        for item in receipt["items"]:
            lines.append(f"{item['name']:<25}{item['quantity']:>5}${(item['quantity'] * item['price']):.2f}:>10")
        
        lines.append("-" * 40)
        lines.append(f"{get_text('subtotal', self.language)}:{receipt['subtotal']:>33.2f}")
        lines.append(f"{get_text('tax', self.language)}:{receipt['tax']:>38.2f}")
        lines.append(f"{get_text('total', self.language)}:{receipt['total']:>36.2f}")
        lines.append("=" * 40)
        lines.append(f"{get_text('thank_you', self.language)}")
        
        return "\n".join(lines)
    
    def update_inventory_table(self):
        # Clear table
        self.inventory_table.setRowCount(0)
        
        # Get data
        menu = load_menu()
        inventory = load_inventory()
        
        # Populate table
        for i, item in enumerate(menu):
            self.inventory_table.insertRow(i)
            
            item_id = str(item["id"])
            name_key = f"name_{self.language}"
            name = item.get(name_key, item["name_en"])
            quantity = inventory.get(item_id, 0)
            price = item["price"]
            
            id_item = QTableWidgetItem(item_id)
            name_item = QTableWidgetItem(name)
            quantity_item = QTableWidgetItem(str(quantity))
            price_item = QTableWidgetItem(f"${price:.2f}")
            
            # Color code inventory levels
            if int(quantity) <= 0:
                quantity_item.setBackground(QColor(DARK_THEME["error"]))
            elif int(quantity) < 10:
                quantity_item.setBackground(QColor(DARK_THEME["warning"]))
            else:
                quantity_item.setBackground(QColor(DARK_THEME["success"]))
            
            self.inventory_table.setItem(i, 0, id_item)
            self.inventory_table.setItem(i, 1, name_item)
            self.inventory_table.setItem(i, 2, quantity_item)
            self.inventory_table.setItem(i, 3, price_item)
    
    def update_sales_table(self):
        # Clear table
        self.sales_table.setRowCount(0)
        
        # Get sales data
        sales = load_sales()
        
        # Populate table with flattened view
        row = 0
        for receipt in reversed(sales):  # Newest first
            for item in receipt["items"]:
                self.sales_table.insertRow(row)
                
                date_item = QTableWidgetItem(receipt["date"])
                time_item = QTableWidgetItem(receipt["time"])
                id_item = QTableWidgetItem(str(item["id"]))
                quantity_item = QTableWidgetItem(str(item["quantity"]))
                total_item = QTableWidgetItem(f"${item['price'] * item['quantity']:.2f}")
                
                self.sales_table.setItem(row, 0, date_item)
                self.sales_table.setItem(row, 1, time_item)
                self.sales_table.setItem(row, 2, id_item)
                self.sales_table.setItem(row, 3, quantity_item)
                self.sales_table.setItem(row, 4, total_item)
                
                row += 1
    
    def update_analytics(self):
        # Get data
        sales = load_sales()
        menu = load_menu()
        
        if not sales:
            return
        
        # Create item ID to name mapping
        item_names = {}
        for item in menu:
            name_key = f"name_{self.language}"
            item_names[str(item["id"])] = item.get(name_key, item["name_en"])
        
        # Calculate top selling items
        item_sales = {}
        for receipt in sales:
            for item in receipt["items"]:
                item_id = str(item["id"])
                if item_id not in item_sales:
                    item_sales[item_id] = {"quantity": 0, "revenue": 0}
                
                item_sales[item_id]["quantity"] += item["quantity"]
                item_sales[item_id]["revenue"] += item["quantity"] * item["price"]
        
        # Sort by quantity
        top_items = sorted(item_sales.items(), key=lambda x: x[1]["quantity"], reverse=True)
        
        # Update top selling table
        self.top_selling_table.setRowCount(0)
        
        for i, (item_id, data) in enumerate(top_items[:5]):  # Top 5
            self.top_selling_table.insertRow(i)
            
            name = item_names.get(item_id, f"Item {item_id}")
            quantity = data["quantity"]
            revenue = data["revenue"]
            
            name_item = QTableWidgetItem(name)
            quantity_item = QTableWidgetItem(str(quantity))
            revenue_item = QTableWidgetItem(f"${revenue:.2f}")
            
            self.top_selling_table.setItem(i, 0, name_item)
            self.top_selling_table.setItem(i, 1, quantity_item)
            self.top_selling_table.setItem(i, 2, revenue_item)
        
        # Create daily sales chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Get daily totals
        daily_totals = {}
        for receipt in sales:
            date = receipt["date"]
            if date not in daily_totals:
                daily_totals[date] = 0
            
            daily_totals[date] += receipt["total"]
        
        # Sort by date and take last 7 days
        dates = sorted(daily_totals.keys())[-7:]
        values = [daily_totals[date] for date in dates]
        
        # Plot
        ax.bar(dates, values, color=DARK_THEME["primary"])
        ax.set_xlabel("Date", color=DARK_THEME["foreground"])
        ax.set_ylabel(get_text("revenue", self.language), color=DARK_THEME["foreground"])
        ax.set_title(get_text("daily_sales", self.language), color=DARK_THEME["foreground"])
        ax.tick_params(axis='x', colors=DARK_THEME["foreground"], rotation=45)
        ax.tick_params(axis='y', colors=DARK_THEME["foreground"])
        
        for spine in ax.spines.values():
            spine.set_color(DARK_THEME["border"])
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def export_sales(self):
        # Get sales data
        sales = load_sales()
        
        if not sales:
            QMessageBox.warning(self, "No Sales Data", "There are no sales to export.")
            return
        
        # Ask for file path
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Export Sales Data", "", "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )
        
        if not file_path:
            return
        
        # Prepare data for export
        flat_data = []
        for receipt in sales:
            for item in receipt["items"]:
                flat_data.append({
                    "Receipt ID": receipt["id"],
                    "Date": receipt["date"],
                    "Time": receipt["time"],
                    "Item ID": item["id"],
                    "Item Name": item["name"],
                    "Unit Price": item["price"],
                    "Quantity": item["quantity"],
                    "Item Total": item["price"] * item["quantity"],
                    "Receipt Subtotal": receipt["subtotal"],
                    "Receipt Tax": receipt["tax"],
                    "Receipt Total": receipt["total"]
                })
        
        # Export based on file extension
        if file_path.endswith(".csv"):
            with open(file_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=flat_data[0].keys())
                writer.writeheader()
                writer.writerows(flat_data)
        elif file_path.endswith(".xlsx"):
            df = pd.DataFrame(flat_data)
            df.to_excel(file_path, index=False)
        
        QMessageBox.information(self, "Export Successful", f"Sales data exported to {file_path}")
    
    def add_item_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(get_text("add_item", self.language))
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        form = QFormLayout()
        
        # English name
        name_en_input = QLineEdit()
        name_en_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow("Name (English)", name_en_input)
        
        # Arabic name
        name_ar_input = QLineEdit()
        name_ar_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow("Name (Arabic)", name_ar_input)
        
        # English description
        desc_en_input = QLineEdit()
        desc_en_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow("Description (English)", desc_en_input)
        
        # Arabic description
        desc_ar_input = QLineEdit()
        desc_ar_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow("Description (Arabic)", desc_ar_input)
        
        # Price
        price_input = QDoubleSpinBox()
        price_input.setRange(0.1, 1000)
        price_input.setValue(3.50)
        price_input.setPrefix("$")
        price_input.setStyleSheet(f"""
            QDoubleSpinBox {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow(get_text("price", self.language), price_input)
        
        # Category
        category_input = QComboBox()
        category_input.setStyleSheet(f"""
            QComboBox {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
            QComboBox::drop-down {{
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                selection-background-color: {DARK_THEME['primary']};
            }}
        """)
        
        # Add existing categories
        categories = set()
        for item in self.menu:
            categories.add(item["category"])
        
        for category in sorted(categories):
            category_input.addItem(category)
        
        # Add "New Category" option
        category_input.addItem("New Category...")
        
        # New category input (hidden initially)
        new_category_input = QLineEdit()
        new_category_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        new_category_input.setVisible(False)
        
        # Show/hide new category input based on selection
        def category_changed(text):
            if text == "New Category...":
                new_category_input.setVisible(True)
            else:
                new_category_input.setVisible(False)
        
        category_input.currentTextChanged.connect(category_changed)
        
        form.addRow(get_text("category", self.language), category_input)
        form.addRow("New Category", new_category_input)
        
        # Initial stock
        stock_input = QSpinBox()
        stock_input.setRange(0, 1000)
        stock_input.setValue(50)
        stock_input.setStyleSheet(f"""
            QSpinBox {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow(get_text("inventory_level", self.language), stock_input)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QHBoxLayout()
        cancel_btn = StyledButton(get_text("cancel", self.language), color=DARK_THEME["button_bg"])
        save_btn = StyledButton(get_text("save", self.language), color=DARK_THEME["primary"])
        
        cancel_btn.clicked.connect(dialog.reject)
        
        buttons.addStretch()
        buttons.addWidget(cancel_btn)
        buttons.addWidget(save_btn)
        
        layout.addLayout(buttons)
        
        # Save function
        def save_item():
            # Validate inputs
            name_en = name_en_input.text().strip()
            name_ar = name_ar_input.text().strip()
            desc_en = desc_en_input.text().strip()
            desc_ar = desc_ar_input.text().strip()
            price = price_input.value()
            
            selected_category = category_input.currentText()
            if selected_category == "New Category...":
                selected_category = new_category_input.text().strip()
                if not selected_category:
                    QMessageBox.warning(dialog, "Invalid Input", "Please enter a category name.")
                    return
            
            stock = stock_input.value()
            
            if not name_en or not name_ar:
                QMessageBox.warning(dialog, "Invalid Input", "Name is required in both languages.")
                return
            
            # Generate new item ID
            item_ids = [item["id"] for item in self.menu]
            new_id = max(item_ids) + 1 if item_ids else 1
            
            # Create new item
            new_item = {
                "id": new_id,
                "name_en": name_en,
                "name_ar": name_ar,
                "description_en": desc_en,
                "description_ar": desc_ar,
                "price": price,
                "category": selected_category,
                "image": "default.png"
            }
            
            # Add to menu
            self.menu.append(new_item)
            save_menu(self.menu)
            
            # Update inventory
            inventory = load_inventory()
            inventory[str(new_id)] = stock
            save_inventory(inventory)
            
            # Refresh UI
            self.load_menu_items()
            
            # Show success message
            QMessageBox.information(dialog, "Success", get_text("item_added", self.language))
            
            dialog.accept()
        
        save_btn.clicked.connect(save_item)
        
        dialog.exec_()
    
    def edit_item_dialog(self):
        # Check if an item is selected
        selected_rows = self.inventory_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "No Item Selected", "Please select an item to edit.")
            return
        
        # Get item ID from selection
        row = selected_rows[0].row()
        item_id = int(self.inventory_table.item(row, 0).text())
        
        # Find item in menu
        item = None
        for menu_item in self.menu:
            if menu_item["id"] == item_id:
                item = menu_item
                break
        
        if not item:
            return
        
        # Create edit dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(get_text("edit_item", self.language))
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        form = QFormLayout()
        
        # English name
        name_en_input = QLineEdit()
        name_en_input.setText(item["name_en"])
        name_en_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow("Name (English)", name_en_input)
        
        # Arabic name
        name_ar_input = QLineEdit()
        name_ar_input.setText(item["name_ar"])
        name_ar_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow("Name (Arabic)", name_ar_input)
        
        # English description
        desc_en_input = QLineEdit()
        desc_en_input.setText(item["description_en"])
        desc_en_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow("Description (English)", desc_en_input)
        
        # Arabic description
        desc_ar_input = QLineEdit()
        desc_ar_input.setText(item["description_ar"])
        desc_ar_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow("Description (Arabic)", desc_ar_input)
        
        # Price
        price_input = QDoubleSpinBox()
        price_input.setRange(0.1, 1000)
        price_input.setValue(item["price"])
        price_input.setPrefix("$")
        price_input.setStyleSheet(f"""
            QDoubleSpinBox {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow(get_text("price", self.language), price_input)
        
        # Category
        category_input = QComboBox()
        category_input.setStyleSheet(f"""
            QComboBox {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
            QComboBox::drop-down {{
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                selection-background-color: {DARK_THEME['primary']};
            }}
        """)
        
        # Add existing categories
        categories = set()
        for menu_item in self.menu:
            categories.add(menu_item["category"])
        
        for category in sorted(categories):
            category_input.addItem(category)
        
        # Set current category
        category_input.setCurrentText(item["category"])
        
        # Add "New Category" option
        category_input.addItem("New Category...")
        
        # New category input (hidden initially)
        new_category_input = QLineEdit()
        new_category_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        new_category_input.setVisible(False)
        
        # Show/hide new category input based on selection
        def category_changed(text):
            if text == "New Category...":
                new_category_input.setVisible(True)
            else:
                new_category_input.setVisible(False)
        
        category_input.currentTextChanged.connect(category_changed)
        
        form.addRow(get_text("category", self.language), category_input)
        form.addRow("New Category", new_category_input)
        
        # Stock level
        inventory = load_inventory()
        stock_input = QSpinBox()
        stock_input.setRange(0, 1000)
        stock_input.setValue(int(inventory.get(str(item_id), 0)))
        stock_input.setStyleSheet(f"""
            QSpinBox {{
                background-color: {DARK_THEME['card_bg']};
                color: {DARK_THEME['foreground']};
                border: 1px solid {DARK_THEME['border']};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        form.addRow(get_text("inventory_level", self.language), stock_input)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QHBoxLayout()
        cancel_btn = StyledButton(get_text("cancel", self.language), color=DARK_THEME["button_bg"])
        save_btn = StyledButton(get_text("save", self.language), color=DARK_THEME["primary"])
        
        cancel_btn.clicked.connect(dialog.reject)
        
        buttons.addStretch()
        buttons.addWidget(cancel_btn)
        buttons.addWidget(save_btn)
        
        layout.addLayout(buttons)
        
        # Save function
        def save_item():
            # Validate inputs
            name_en = name_en_input.text().strip()
            name_ar = name_ar_input.text().strip()
            desc_en = desc_en_input.text().strip()
            desc_ar = desc_ar_input.text().strip()
            price = price_input.value()
            
            selected_category = category_input.currentText()
            if selected_category == "New Category...":
                selected_category = new_category_input.text().strip()
                if not selected_category:
                    QMessageBox.warning(dialog, "Invalid Input", "Please enter a category name.")
                    return
            
            stock = stock_input.value()
            
            if not name_en or not name_ar:
                QMessageBox.warning(dialog, "Invalid Input", "Name is required in both languages.")
                return
            
            # Update item
            for i, menu_item in enumerate(self.menu):
                if menu_item["id"] == item_id:
                    self.menu[i]["name_en"] = name_en
                    self.menu[i]["name_ar"] = name_ar
                    self.menu[i]["description_en"] = desc_en
                    self.menu[i]["description_ar"] = desc_ar
                    self.menu[i]["price"] = price
                    self.menu[i]["category"] = selected_category
                    break
            
            save_menu(self.menu)
            
            # Update inventory
            inventory[str(item_id)] = stock
            save_inventory(inventory)
            
            # Refresh UI
            self.load_menu_items()
            
            # Show success message
            QMessageBox.information(dialog, "Success", get_text("item_updated", self.language))
            
            dialog.accept()
        
        save_btn.clicked.connect(save_item)
        
        dialog.exec_()
    
    def remove_item(self):
        # Check if an item is selected
        selected_rows = self.inventory_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "No Item Selected", "Please select an item to remove.")
            return
        
        # Get item ID from selection
        row = selected_rows[0].row()
        item_id = int(self.inventory_table.item(row, 0).text())
        item_name = self.inventory_table.item(row, 1).text()
        
        # Confirm deletion
        confirm = QMessageBox.question(
            self,
            "Confirm Removal",
            f"{get_text('confirm_remove', self.language)}\n\n{item_name}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Remove from menu
            for i, item in enumerate(self.menu):
                if item["id"] == item_id:
                    del self.menu[i]
                    break
            
            save_menu(self.menu)
            
            # Remove from inventory
            inventory = load_inventory()
            if str(item_id) in inventory:
                del inventory[str(item_id)]
                save_inventory(inventory)
            
            # Refresh UI
            self.load_menu_items()
            
            # Show success message
            QMessageBox.information(self, "Success", get_text("item_removed", self.language))
    
    def save_settings(self):
        # Get values
        language = self.language_combo.currentData()
        tax_rate = self.tax_input.value() / 100  # Convert percentage to decimal
        shop_name_en = self.shop_name_en_input.text()
        shop_name_ar = self.shop_name_ar_input.text()
        address_en = self.address_en_input.text()
        address_ar = self.address_ar_input.text()
        phone = self.phone_input.text()
        
        # Update settings
        self.settings = {
            "language": language,
            "tax_rate": tax_rate,
            "shop_name_en": shop_name_en,
            "shop_name_ar": shop_name_ar,
            "address_en": address_en,
            "address_ar": address_ar,
            "phone": phone
        }
        
        save_settings(self.settings)
        
        # Show message
        QMessageBox.information(self, "Settings Saved", "Settings have been saved. Restart the application for language changes to take effect.")
        
        # Update tax calculations
        self.update_cart_table()

# Main application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Set font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    pos_system = POSSystem()
    sys.exit(app.exec_())
