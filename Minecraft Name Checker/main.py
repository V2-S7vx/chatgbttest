"""
Minecraft Name Checker
----------------------
A GUI application to check Minecraft username availability using namemc.
Features:
- Checks 3-letter/number combinations
- Checks 3, 4, 5 letter real words
- Checks 4-letter/number combinations
- Activity log with timestamps
- Sound notification when available name found
- Copy button for available names
- Real-time activity log
"""

import sys
import asyncio
import aiohttp
import threading
import time
import json
import random
import string
import logging
import subprocess
import os
from datetime import datetime
from pathlib import Path
from typing import List, Set, Optional, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import queue

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QComboBox,
    QSpinBox, QDoubleSpinBox, QProgressBar, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QFormLayout, QCheckBox, QMessageBox,
    QFileDialog, QStyle, QSystemTrayIcon, QMenu, QFrame, QSplitter
)
from PySide6.QtCore import (
    Qt, QTimer, QThread, Signal, QObject, QUrl, QMutex, QWaitCondition
)
from PySide6.QtGui import (
    QFont, QColor, QIcon, QPixmap, QDesktopServices, QAction
)
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mc_name_checker")


@dataclass
class CheckResult:
    """Result of a name availability check."""
    name: str
    available: bool
    checked_at: datetime
    source: str  # "namemc" or "api"


class NameGenerator:
    """Generates various types of Minecraft name combinations."""
    
    def __init__(self):
        self.letters = string.ascii_lowercase
        self.digits = string.digits
        self.alphanum = self.letters + self.digits
        self._word_cache = {}
    
    def load_word_list(self, length: int) -> List[str]:
        """Load or generate word list for given length."""
        cache_key = f"words_{length}"
        if cache_key in self._word_cache:
            return self._word_cache[cache_key]
        
        # Built-in common English words by length
        word_lists = {
            3: [
                "cat", "dog", "fox", "bat", "rat", "pig", "cow", "ant", "bee", "fly",
                "sky", "sun", "moon", "star", "sea", "oak", "elm", "ash", "ivy", "fig",
                "red", "blue", "gold", "pink", "gray", "white", "black",
                "one", "two", "six", "ten", "man", "boy", "girl", "kid", "dad", "mom",
                "god", "dev", "pro", "vip", "mod", "admin", "root", "sys", "web", "app",
                "api", "bot", "ai", "ml", "db", "os", "ui", "ux", "ci", "cd",
                "git", "ssh", "ftp", "dns", "vpn", "tor", "ssl", "tcp", "udp", "ip",
                "cpu", "gpu", "ram", "ssd", "hdd", "usb", "hdmi", "wifi", "lte", "5g",
                "win", "mac", "lin", "bsd", "unix", "posix", "bash", "zsh", "vim", "emacs",
                "fun", "win", "lose", "draw", "play", "game", "code", "hack", "crack", "exploit",
                "key", "lock", "safe", "vault", "chest", "box", "bag", "pack", "kit", "set",
                "map", "zone", "area", "spot", "site", "page", "link", "node", "edge", "path",
                "run", "walk", "jump", "fly", "swim", "dive", "climb", "fall", "rise", "drop",
                "hot", "cold", "warm", "cool", "dry", "wet", "soft", "hard", "fast", "slow",
                "big", "small", "huge", "tiny", "long", "short", "high", "low", "deep", "shallow",
                "new", "old", "young", "ancient", "modern", "retro", "fresh", "stale", "raw", "cooked",
                "yes", "no", "maybe", "sure", "ok", "fine", "good", "bad", "best", "worst",
                "top", "bottom", "left", "right", "front", "back", "middle", "center", "side", "corner",
                "in", "out", "on", "off", "up", "down", "over", "under", "above", "below",
                "before", "after", "now", "then", "soon", "late", "early", "always", "never", "sometimes",
                "all", "none", "some", "many", "few", "each", "every", "any", "either", "neither",
                "my", "your", "his", "her", "its", "our", "their", "mine", "yours", "theirs",
                "this", "that", "these", "those", "here", "there", "where", "when", "why", "how",
                "who", "what", "which", "whose", "whom", "am", "is", "are", "was", "were",
                "be", "been", "being", "have", "has", "had", "do", "does", "did", "will",
                "would", "could", "should", "may", "might", "must", "can", "shall", "ought", "need"
            ],
            4: [
                "love", "hate", "like", "need", "want", "know", "think", "feel", "see", "hear",
                "read", "write", "play", "work", "study", "learn", "teach", "help", "give", "take",
                "make", "create", "build", "break", "fix", "fix", "test", "run", "walk", "jump",
                "swim", "fly", "drive", "ride", "cook", "eat", "drink", "sleep", "wake", "dream",
                "hope", "wish", "pray", "believe", "trust", "doubt", "fear", "brave", "strong", "weak",
                "fast", "slow", "quick", "swift", "rapid", "sudden", "instant", "quick", "fast", "speedy",
                "home", "house", "room", "door", "wall", "floor", "roof", "window", "gate", "fence",
                "tree", "flower", "grass", "plant", "seed", "root", "leaf", "branch", "bark", "wood",
                "fire", "water", "earth", "air", "wind", "storm", "rain", "snow", "ice", "cloud",
                "sun", "moon", "star", "sky", "space", "world", "planet", "galaxy", "universe", "cosmos",
                "time", "year", "month", "week", "day", "hour", "minute", "second", "moment", "era",
                "life", "death", "birth", "age", "youth", "child", "adult", "elder", "baby", "teen",
                "man", "woman", "boy", "girl", "kid", "adult", "person", "human", "being", "soul",
                "mind", "heart", "brain", "spirit", "will", "hope", "faith", "love", "peace", "joy",
                "good", "bad", "better", "best", "worst", "worse", "great", "small", "big", "huge",
                "hot", "cold", "warm", "cool", "dry", "wet", "soft", "hard", "smooth", "rough",
                "light", "dark", "bright", "dim", "clear", "blurry", "sharp", "dull", "thin", "thick",
                "long", "short", "tall", "wide", "narrow", "deep", "shallow", "high", "low", "flat",
                "round", "square", "flat", "curved", "straight", "crooked", "bent", "twisted", "twisted", "twisted"
            ],
            5: [
                "happy", "angry", "sad", "proud", "brave", "calm", "wild", "tame", "free", "bound",
                "peace", "chaos", "order", "chaos", "truth", "lie", "fact", "myth", "tale", "story",
                "music", "sound", "noise", "silence", "voice", "speech", "word", "letter", "text", "book",
                "write", "read", "think", "learn", "teach", "know", "wise", "smart", "dumb", "foolish",
                "strong", "weak", "tough", "fragile", "solid", "liquid", "gas", "plasma", "energy", "power",
                "force", "speed", "velocity", "momentum", "acceleration", "gravity", "mass", "weight", "density", "volume",
                "color", "hue", "shade", "tint", "tone", "hue", "bright", "dark", "light", "dark",
                "beauty", "ugly", "pretty", "plain", "simple", "complex", "easy", "hard", "difficult", "easy",
                "begin", "start", "end", "finish", "complete", "incomplete", "partial", "whole", "part", "piece",
                "unit", "group", "team", "crowd", "mass", "individual", "person", "people", "crowd", "mob",
                "friend", "enemy", "ally", "foe", "stranger", "guest", "host", "visitor", "member", "leader",
                "king", "queen", "prince", "princess", "lord", "lady", "knight", "hero", "villain", "monster",
                "dragon", "wizard", "witch", "mage", "sorcerer", "elf", "dwarf", "orc", "goblin", "troll",
                "magic", "spell", "curse", "blessing", "potion", "scroll", "wand", "staff", "ring", "amulet",
                "castle", "tower", "dungeon", "cave", "forest", "mountain", "river", "lake", "ocean", "sea",
                "island", "shore", "beach", "desert", "valley", "hill", "plain", "field", "farm", "village",
                "city", "town", "capital", "metropolis", "suburb", "district", "zone", "area", "region", "land"
            ]
        }
        
        words = word_lists.get(length, [])
        self._word_cache[cache_key] = words
        return words
    
    def generate_three_letter_combos(self) -> List[str]:
        """Generate all 3-letter combinations (letters + numbers)."""
        combos = []
        chars = string.ascii_lowercase + string.digits
        for a in chars:
            for b in chars:
                for c in chars:
                    combos.append(a + b + c)
        return combos
    
    def generate_four_letter_combos(self) -> List[str]:
        """Generate all 4-letter combinations (letters + numbers)."""
        combos = []
        chars = string.ascii_lowercase + string.digits
        for a in chars:
            for b in chars:
                for c in chars:
                    for d in chars:
                        combos.append(a + b + c + d)
        return combos
    
    def get_real_words(self, length: int) -> List[str]:
        """Get real English words of specified length."""
        return self.load_word_list(length)
    
    def generate_all_combinations(self) -> List[str]:
        """Generate all name combinations to check."""
        all_names = []
        
        # 3-letter combinations
        all_names.extend(self.generate_three_letter_combos())
        
        # 3-letter real words
        all_names.extend(self.get_real_words(3))
        
        # 4-letter combinations
        all_names.extend(self.generate_four_letter_combos())
        
        # 4-letter real words
        all_names.extend(self.get_real_words(4))
        
        # 5-letter real words
        all_names.extend(self.get_real_words(5))
        
        # Remove duplicates and filter valid Minecraft names (3-16 chars, alphanumeric + underscore)
        valid_names = []
        for name in all_names:
            if 3 <= len(name) <= 16 and all(c.isalnum() or c == '_' for c in name):
                valid_names.append(name)
        
        # Remove duplicates
        return list(dict.fromkeys(valid_names))


class NameMCChecker:
    """Checks name availability using Mojang API (official)"""
    
    def __init__(self):
        self.session = None
        self.base_url = "https://api.mojang.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
    
    async def check_name(self, name: str) -> Tuple[bool, str]:
        """Check if a Minecraft name is available using Mojang API.
        Returns (available, status) where available=True means name is available.
        """
        if not self.session:
            import aiohttp
            self.session = aiohttp.ClientSession()
        
        try:
            # Mojang API returns 200 if taken, 404 if available, 429 if rate limited
            url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
            
            async with self.session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    return False, "taken"
                elif resp.status == 404:
                    return True, "available"
                elif resp.status == 429:
                    return False, "rate_limited"
                else:
                    return False, f"error_{resp.status}"
                    
        except Exception as e:
            logger.error(f"Error checking {name}: {e}")
            return False, f"error: {str(e)}"
    
    async def check_batch(self, names: List[str], delay: float = 0.5) -> List[Tuple[str, bool, str]]:
        """Check multiple names with delay between requests."""
        results = []
        for name in names:
            available, status = await self.check_name(name)
            results.append((name, available, status))
            await asyncio.sleep(delay)  # Rate limiting
        return results
    
    async def close(self):
        if self.session:
            await self.session.close()


class WorkerSignals(QObject):
    """Signals for the worker thread."""
    result_found = Signal(str, bool, str)  # name, available, status
    progress_update = Signal(int, int)  # current, total
    log_message = Signal(str)
    finished = Signal()
    error_occurred = Signal(str)


class NameCheckerWorker(QThread):
    """Worker thread for checking name availability."""
    
    def __init__(self, names: List[str], delay: float = 0.5):
        super().__init__()
        self.names = names
        self.delay = delay
        self.signals = WorkerSignals()
        self._running = True
        self._paused = False
        self.checker = NameMCChecker()
        self._total = len(names)
        self._completed = 0
    
    def pause(self):
        self._paused = True
    
    def resume(self):
        self._paused = False
    
    def stop(self):
        self._running = False
    
    def run(self):
        """Run the name checking process."""
        self._run_checker()
    
    async def _check_loop(self):
        self.checker = NameMCChecker()
        
        for name in self.names:
            if not self._running:
                break
            
            while self._paused:
                await asyncio.sleep(0.1)
            
            if not self._running:
                break
            
            try:
                available, status = await self.checker.check_name(self.names[self._completed])
                self._completed += 1
                
                self.signals.result_found.emit(self.names[self._completed - 1], available, status)
                self.signals.progress_update.emit(self._completed, self._total)
                
                if available:
                    # Play sound notification
                    self.signals.log_message.emit(f"🎉 FOUND: {self.names[self._completed - 1]} is AVAILABLE!")
                else:
                    self.signals.log_message.emit(f"❌ {self.names[self._completed - 1]} - {status}")
                
            except Exception as e:
                logger.error(f"Error checking name: {e}")
                self.signals.error_occurred.emit(str(e))
            
            await asyncio.sleep(self.delay)
        
        self.signals.finished.emit()
    
    def _run_checker(self):
        asyncio.run(self._check_loop())
    
    def pause(self):
        self._paused = True
    
    def resume(self):
        self._paused = False
    
    def stop(self):
        self._running = False


class NameCheckerGUI(QMainWindow):
    """Main GUI for the Minecraft Name Checker."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Name Checker")
        self.setMinimumSize(1200, 800)
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        
        # Initialize components
        self.generator = NameGenerator()
        self.all_names = []
        self.worker = None
        self.found_names = []
        
        # Sound effect for found names
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(":/sounds/found.wav"))
        
        self._setup_ui()
        self._apply_styles()
        self._generate_names()
        
        # System tray
        self._setup_tray()
    
    def _setup_ui(self):
        """Setup the main UI."""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("⛏️ Minecraft Name Checker")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #5865F2; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Check Minecraft username availability using namemc.com")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #B9BBBE; font-size: 14px; margin-bottom: 15px;")
        layout.addWidget(subtitle)
        
        # Control panel
        control_frame = QFrame()
        control_frame.setFrameStyle(QFrame.StyledPanel)
        control_frame.setStyleSheet("""
            QFrame {
                background: #2C2F33;
                border-radius: 8px;
                border: 1px solid #40444B;
            }
        """)
        control_layout = QVBoxLayout(control_frame)
        control_layout.setSpacing(15)
        control_layout.setContentsMargins(15, 15, 15, 15)
        
        # Mode selection
        mode_group = QGroupBox("Check Mode")
        mode_group.setStyleSheet("QGroupBox { font-weight: bold; color: #FFFFFF; }")
        mode_layout = QHBoxLayout(mode_group)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "All Combinations (3-5 chars)",
            "3-Letter Combinations Only",
            "4-Letter Combinations Only", 
            "3-Letter Real Words",
            "4-Letter Real Words",
            "5-Letter Real Words",
            "Custom Word List"
        ])
        self.mode_combo.setStyleSheet("""
            QComboBox {
                background: #2C2F33;
                border: 1px solid #40444B;
                border-radius: 6px;
                padding: 8px;
                color: #FFFFFF;
                min-width: 250px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #2C2F33;
                border: 1px solid #40444B;
                color: #FFFFFF;
                selection-background-color: #5865F2;
            }
        """)
        mode_layout.addWidget(QLabel("Mode:"))
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        
        layout.addWidget(mode_group)
        
        # Settings
        settings_group = QGroupBox("Settings")
        settings_group.setStyleSheet("QGroupBox { font-weight: bold; color: #FFFFFF; }")
        settings_layout = QFormLayout(settings_group)
        
        self.delay_spin = QDoubleSpinBox()
        self.delay_spin.setRange(0.1, 5.0)
        self.delay_spin.setValue(0.5)
        self.delay_spin.setSingleStep(0.1)
        self.delay_spin.setSuffix(" sec")
        self.delay_spin.setStyleSheet("""
            QDoubleSpinBox {
                background: #2C2F33;
                border: 1px solid #40444B;
                border-radius: 4px;
                padding: 5px;
                color: white;
            }
        """)
        settings_layout.addRow("Delay between checks:", self.delay_spin)
        
        self.max_concurrent = QSpinBox()
        self.max_concurrent.setRange(1, 10)
        self.max_concurrent.setValue(3)
        self.max_concurrent.setStyleSheet("""
            QSpinBox {
                background: #2C2F33;
                border: 1px solid #40444B;
                border-radius: 4px;
                padding: 5px;
                color: white;
            }
        """)
        settings_layout.addRow("Concurrent checks:", self.max_concurrent)
        
        self.sound_enabled = QCheckBox("Play sound when name found")
        self.sound_enabled.setChecked(True)
        self.sound_enabled.setStyleSheet("color: #FFFFFF;")
        settings_layout.addRow(self.sound_enabled)
        
        self.auto_copy = QCheckBox("Auto-copy available names to clipboard")
        self.auto_copy.setChecked(False)
        self.auto_copy.setStyleSheet("color: #FFFFFF;")
        settings_layout.addRow(self.auto_copy)
        
        layout.addWidget(settings_group)
        
        # Custom word list
        custom_group = QGroupBox("Custom Word List")
        custom_group.setStyleSheet("QGroupBox { font-weight: bold; color: #FFFFFF; }")
        custom_layout = QVBoxLayout(custom_group)
        
        self.custom_words = QTextEdit()
        self.custom_words.setPlaceholderText("Enter custom names to check (one per line)...")
        self.custom_words.setMaximumHeight(100)
        self.custom_words.setStyleSheet("""
            QTextEdit {
                background: #1E1F22;
                border: 1px solid #40444B;
                border-radius: 6px;
                color: #DCddde;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)
        custom_layout.addWidget(self.custom_words)
        
        btn_layout = QHBoxLayout()
        load_btn = QPushButton("Load from File")
        load_btn.clicked.connect(self._load_word_file)
        load_btn.setStyleSheet("background: #40444B; color: white; border-radius: 4px; padding: 8px;")
        btn_layout.addWidget(load_btn)
        
        save_btn = QPushButton("Save to File")
        save_btn.clicked.connect(self._save_word_file)
        save_btn.setStyleSheet("background: #40444B; color: white; border-radius: 4px; padding: 8px;")
        btn_layout.addWidget(save_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(lambda: self.custom_words.clear())
        clear_btn.setStyleSheet("background: #ED4245; color: white; border-radius: 4px; padding: 8px;")
        btn_layout.addWidget(clear_btn)
        
        btn_layout.addStretch()
        custom_layout.addLayout(btn_layout)
        
        layout.addWidget(custom_group)
        
        layout.addWidget(control_frame)
        
        # Progress
        progress_frame = QFrame()
        progress_frame.setStyleSheet("background: transparent;")
        progress_layout = QHBoxLayout(progress_frame)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 6px;
                background: #2C2F33;
                text-align: center;
                color: white;
                font-weight: bold;
                height: 20px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5865F2, stop:1 #4752C4);
                border-radius: 6px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready to start")
        self.status_label.setStyleSheet("color: #B9BBBE; font-size: 13px;")
        self.status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.status_label.setMinimumWidth(200)
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_frame)
        
        # Main content splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Results
        left_panel = self._create_results_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Activity Log
        right_panel = self._create_log_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([600, 600])
        layout.addWidget(splitter, 1)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ Start Checking")
        self.start_btn.setFixedHeight(45)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: #5865F2;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background: #4752C4; }
            QPushButton:pressed { background: #3C45A5; }
            QPushButton:disabled { background: #4A4D54; color: #72767D; }
        """)
        self.start_btn.clicked.connect(self.start_checking)
        button_layout.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.setFixedHeight(45)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background: #FAA61A;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background: #E09418; }
            QPushButton:disabled { background: #4A4D54; color: #72767D; }
        """)
        self.pause_btn.clicked.connect(self.toggle_pause)
        button_layout.addWidget(self.pause_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setFixedHeight(45)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: #ED4245;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background: #C0392B; }
            QPushButton:disabled { background: #4A4D54; color: #72767D; }
        """)
        self.stop_btn.clicked.connect(self.stop_checking)
        button_layout.addWidget(self.stop_btn)
        
        layout.addLayout(button_layout)
    
    def _create_results_panel(self) -> QWidget:
        """Create the results panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("✅ Available Names Found")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #43B581;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        export_btn = QPushButton("📋 Export Results")
        export_btn.setFixedWidth(140)
        export_btn.clicked.connect(self._export_results)
        export_btn.setStyleSheet("background: #40444B; color: white; border-radius: 4px; padding: 8px;")
        header_layout.addWidget(export_btn)
        
        layout.addLayout(header_layout)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Name", "Status", "Found At", "Actions"])
        self.results_table.setStyleSheet("""
            QTableWidget {
                background: #1E1F22;
                border: 1px solid #40444B;
                border-radius: 6px;
                color: #FFFFFF;
                gridline-color: #40444B;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            QHeaderView::section {
                background: #2C2F33;
                border: none;
                border-right: 1px solid #40444B;
                border-bottom: 1px solid #40444B;
                color: #FFFFFF;
                padding: 8px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background: #5865F2;
            }
        """)
        
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.setSelectionMode(QTableWidget.SingleSelection)
        self.results_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.results_table, 1)
        
        return panel
    
    def _create_log_panel(self) -> QWidget:
        """Create the activity log panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Log output (create first)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background: #1E1F22;
                border: 1px solid #40444B;
                border-radius: 8px;
                color: #DCddde;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)
        
        # Log header
        header = QHBoxLayout()
        log_title = QLabel("📋 Activity Log")
        log_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        log_title.setStyleSheet("color: #FFFFFF;")
        header.addWidget(log_title)
        
        header.addStretch()
        
        clear_btn = QPushButton("Clear Log")
        clear_btn.setFixedWidth(100)
        clear_btn.clicked.connect(self.log_output.clear)
        clear_btn.setStyleSheet("background: #40444B; color: white; border-radius: 4px; padding: 5px;")
        header.addWidget(clear_btn)
        
        layout.addLayout(header)
        
        # Log output
        layout.addWidget(self.log_output, 1)
        
        return panel
    
    def _apply_styles(self):
        """Apply dark theme styling."""
        self.setStyleSheet("""
            QMainWindow { background: #23272A; }
            QWidget { background: #23272A; color: #FFFFFF; }
            QGroupBox {
                border: 1px solid #40444B;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                color: #FFFFFF;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #40444B;
                border-radius: 4px;
                background: #2C2F33;
            }
            QCheckBox::indicator:checked {
                background: #5865F2;
                border-color: #5865F2;
            }
            QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit, QTextEdit {
                background: #2C2F33;
                border: 1px solid #40444B;
                border-radius: 4px;
                padding: 5px;
                color: white;
            }
            QScrollBar:vertical {
                background: #2C2F33;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #40444B;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #4A4F56;
            }
        """)
    
    def _setup_tray(self):
        """Setup system tray icon."""
        self.tray = QSystemTrayIcon(self)
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("#5865F2"))
        self.tray.setIcon(QIcon(pixmap))
        self.tray.setToolTip("Minecraft Name Checker")
        
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(self.close)
        self.tray.setContextMenu(tray_menu)
        self.tray.show()
    
    def _generate_names(self):
        """Generate names based on selected mode."""
        # This will be called when starting
        pass
    
    def _load_word_file(self):
        """Load custom word list from file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Word List", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                self.custom_words.setPlainText(content)
                self._log(f"Loaded word list from {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load file: {e}")
    
    def _save_word_file(self):
        """Save custom word list to file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Word List", "wordlist.txt", "Text Files (*.txt)"
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.custom_words.toPlainText())
                self._log(f"Saved word list to {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save file: {e}")
    
    def _generate_names(self):
        """Generate names based on selected mode."""
        mode = self.mode_combo.currentText()
        custom_text = self.custom_words.toPlainText().strip()
        
        self.all_names = []
        
        if "Custom" in mode and custom_text:
            # Use custom word list
            custom_names = [line.strip() for line in custom_text.split('\n') if line.strip()]
            self.all_names = [n for n in custom_names if 3 <= len(n) <= 16 and all(c.isalnum() or c == '_' for c in n)]
        elif "3-Letter Combinations" in mode:
            self.all_names = self.generator.generate_three_letter_combos()
        elif "4-Letter Combinations" in mode:
            self.all_names = self.generator.generate_four_letter_combos()
        elif "3-Letter Real Words" in mode:
            self.all_names = self.generator.get_real_words(3)
        elif "4-Letter Real Words" in mode:
            self.all_names = self.generator.get_real_words(4)
        elif "5-Letter Real Words" in mode:
            self.all_names = self.generator.get_real_words(5)
        else:  # All Combinations
            self.all_names = self.generator.generate_all_combinations()
        
        # Filter valid Minecraft names
        self.all_names = [n for n in self.all_names if 3 <= len(n) <= 16 and all(c.isalnum() or c == '_' for c in n)]
        self.all_names = list(dict.fromkeys(self.all_names))  # Remove duplicates
        
        self._log(f"Generated {len(self.all_names)} names to check")
    
    def start_checking(self):
        """Start the name checking process."""
        if not self.all_names:
            self._generate_names()
        
        if not self.all_names:
            QMessageBox.warning(self, "No Names", "No names generated to check!")
            return
        
        # Update UI
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setRange(0, len(self.all_names))
        self.progress_bar.setValue(0)
        
        # Disable config inputs
        self.mode_combo.setEnabled(False)
        self.delay_spin.setEnabled(False)
        self.custom_words.setEnabled(False)
        
        # Start worker
        delay = self.delay_spin.value()
        self.worker = NameCheckerWorker(self.all_names, self.delay_spin.value())
        self.worker.signals.result_found.connect(self._on_result_found)
        self.worker.signals.progress_update.connect(self._on_progress)
        self.worker.signals.log_message.connect(self._on_log)
        self.worker.signals.finished.connect(self._on_finished)
        self.worker.signals.error_occurred.connect(self._on_error)
        self.worker.start()
        
        self._log("Started checking usernames...")
        self.status_label.setText(f"Status: Checking... (0/{len(self.all_names)})")
    
    def toggle_pause(self):
        """Pause/resume checking."""
        if self.worker:
            if self.worker._paused:
                self.worker.resume()
                self.pause_btn.setText("⏸ Pause")
                self._log("Resumed checking")
            else:
                self.worker.pause()
                self.pause_btn.setText("▶ Resume")
                self._log("Paused checking")
    
    def stop_checking(self):
        """Stop the checking process."""
        if self.worker:
            self.worker.stop()
            self.worker.wait(3000)
            self._on_finished()
    
    def _on_result_found(self, name: str, available: bool, status: str):
        """Handle found result."""
        if available:
            self.found_names.append(name)
            
            # Add to results table
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            
            # Name
            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("Consolas", 11, QFont.Bold))
            name_item.setForeground(QColor("#43B581"))
            self.results_table.setItem(0, 0, name_item)
            
            # Status
            status_item = QTableWidgetItem("AVAILABLE ✅")
            status_item.setForeground(QColor("#43B581"))
            status_item.setFont(QFont("Consolas", 10, QFont.Bold))
            self.results_table.setItem(0, 1, status_item)
            
            # Time
            time_item = QTableWidgetItem(datetime.now().strftime("%H:%M:%S"))
            time_item.setForeground(QColor("#B9BBBE"))
            self.results_table.setItem(0, 2, time_item)
            
            # Copy button
            copy_btn = QPushButton("📋 Copy")
            copy_btn.setStyleSheet("""
                QPushButton {
                    background: #5865F2;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 11px;
                }
                QPushButton:hover { background: #4752C4; }
            """)
            copy_btn.clicked.connect(lambda _, n=name: self._copy_to_clipboard(n))
            self.results_table.setCellWidget(0, 3, copy_btn)
            
            # Scroll to top
            self.results_table.scrollToTop()
            
            # Play sound
            if self.sound_enabled.isChecked():
                try:
                    import winsound
                    winsound.Beep(880, 200)
                except:
                    pass
            
            # Auto-copy
            if self.auto_copy.isChecked():
                self._copy_to_clipboard(name)
        
        # Update found count
        self._log(f"Found {len(self.found_names)} available names so far")
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard."""
        QApplication.clipboard().setText(text)
        self._log(f"Copied to clipboard: {text}")
    
    def _export_results(self):
        """Export found names to file."""
        if not self.found_names:
            QMessageBox.information(self, "No Results", "No available names found yet!")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Results", f"available_names_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt);;CSV Files (*.csv);;JSON Files (*.json)"
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    import csv
                    with open(file_path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Name', 'Found At'])
                        for row in range(self.results_table.rowCount()):
                            name = self.results_table.item(row, 0).text()
                            time_str = self.results_table.item(row, 2).text()
                            writer.writerow([name, time_str])
                elif file_path.endswith('.json'):
                    import json
                    data = []
                    for row in range(self.results_table.rowCount()):
                        data.append({
                            'name': self.results_table.item(row, 0).text(),
                            'found_at': self.results_table.item(row, 2).text()
                        })
                    with open(file_path, 'w') as f:
                        json.dump(data, f, indent=2)
                else:
                    with open(file_path, 'w') as f:
                        for row in range(self.results_table.rowCount()):
                            f.write(f"{self.results_table.item(row, 0).text()} - {self.results_table.item(row, 2).text()}\n")
                
                self._log(f"Exported {len(self.found_names)} names to {file_path}")
                QMessageBox.information(self, "Export Complete", f"Exported {len(self.found_names)} names to {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Export Error", f"Failed to export: {e}")
    
    def _on_progress(self, current: int, total: int):
        self.progress_bar.setValue(current)
        self.status_label.setText(f"Status: Checking... ({current}/{total})")
        
        # Calculate rate
        if hasattr(self, '_check_times'):
            self._check_times.append(time.time())
        else:
            self._check_times = [time.time()]
        
        # Keep last 60 seconds
        now = time.time()
        self._check_times = [t for t in self._check_times if now - t < 60]
        if len(self._check_times) > 1:
            rate = len(self._check_times) / (self._check_times[-1] - self._check_times[0]) * 60
            self.status_label.setText(f"Status: Checking... ({current}/{total}) - {rate:.0f}/min")
    
    def _on_log(self, message: str):
        self._log(message)
    
    def _on_finished(self):
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        
        # Re-enable config
        self.mode_combo.setEnabled(True)
        self.delay_spin.setEnabled(True)
        self.custom_words.setEnabled(True)
        
        self.status_label.setText("Status: Finished")
        self._log(f"Checking complete! Found {len(self.found_names)} available names.")
    
    def _on_error(self, error: str):
        self._log(f"Error: {error}", "error")
    
    def _log(self, message: str, level: str = "info"):
        colors = {
            "info": "#DCddde",
            "success": "#43B581",
            "warning": "#FAA61A",
            "error": "#ED4245",
            "found": "#5865F2"
        }
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = {"info": "#DCddde", "success": "#43B581", "warning": "#FAA61A", 
                "error": "#ED4245", "found": "#5865F2"}.get(level, "#DCddde")
        
        self.log_output.append(
            f'<span style="color: #72767D;">[{timestamp}]</span> '
            f'<span style="color: {color};">{message}</span>'
        )
        
        # Auto-scroll
        self.log_output.verticalScrollBar().setValue(
            self.log_output.verticalScrollBar().maximum()
        )
    
    def closeEvent(self, event):
        """Handle window close."""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(3000)
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Minecraft Name Checker")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Nova")
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = NameCheckerGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()