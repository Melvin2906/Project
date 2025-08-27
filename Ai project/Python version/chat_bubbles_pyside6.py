# chat_bubbles_pyside6.py
# Requires: pip install PySide6
# Run: python chat_bubbles_pyside6.py

from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QLineEdit, QPushButton, QFrame, QSizePolicy
)
import sys
import textwrap
import random

class MessageBubble(QFrame):
    def __init__(self, text: str, is_user: bool, max_width: int = 420, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.setObjectName("userBubble" if is_user else "botBubble")

        # Core label
        self.label = QLabel(text, self)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Layout for padding
        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 10, 14, 10)  # inner padding
        outer.addWidget(self.label)

        # Constrain width so the label wraps like a real chat app
        self.max_width = max_width
        self.label.setMaximumWidth(self.max_width)

        # Visual style via styleSheet (rounded corners like WhatsApp/Messenger)
        # Different colors for user vs bot
        self.setStyleSheet("""
        QFrame#userBubble {
            background: #dcf8c6;
            border-radius: 16px;
        }
        QFrame#botBubble {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 16px;
        }
        QLabel {
            font-size: 14px;
            color: #000000;
        }
        """)

        # Add a subtle drop shadow feel by using margins in the container layout
        self.setFrameShape(QFrame.NoFrame)

    def sizeHint(self):
        # Provide a decent default size hint to help layouts
        sh = super().sizeHint()
        if sh.width() > self.max_width:
            return QSize(self.max_width, sh.height())
        return sh


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Bubbles (PySide6)")
        self.resize(560, 700)

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        # Scroll area for messages
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.scroll_content = QWidget()
        self.vbox = QVBoxLayout(self.scroll_content)
        self.vbox.setSpacing(8)
        self.vbox.addStretch(1)

        self.scroll.setWidget(self.scroll_content)
        root.addWidget(self.scroll, 1)

        # Input area
        input_row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Écris un message…")
        self.send_btn = QPushButton("Envoyer")
        self.send_btn.setDefault(True)

        input_row.addWidget(self.input, 1)
        input_row.addWidget(self.send_btn)
        root.addLayout(input_row)

        # Signals
        self.send_btn.clicked.connect(self.send_user_message)
        self.input.returnPressed.connect(self.send_user_message)

        # Greeting
        self.add_message("Bonjour 👋 Je suis un bot. Pose-moi une question !", is_user=False)

    def add_message(self, text: str, is_user: bool):
        # Row with left/right alignment using stretch
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)

        bubble = MessageBubble(text, is_user=is_user, max_width=420)

        if is_user:
            row.addStretch(1)
            row.addWidget(bubble, 0, Qt.AlignRight)
        else:
            row.addWidget(bubble, 0, Qt.AlignLeft)
            row.addStretch(1)

        # Insert above the stretch at the bottom
        self.vbox.insertLayout(self.vbox.count() - 1, row)

        # Auto-scroll to bottom
        QTimer.singleShot(0, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        bar = self.scroll.verticalScrollBar()
        bar.setValue(bar.maximum())

    def send_user_message(self):
        txt = self.input.text().strip()
        if not txt:
            return
        self.input.clear()
        self.add_message(txt, is_user=True)

        # Simulated bot: respond after a short delay
        QTimer.singleShot(500, lambda: self.bot_reply(txt))

    def bot_reply(self, user_text: str):
        # Simple echo + a pseudo "typing" feeling: wrap text to demonstrate resizing
        responses = [
            "Tu as dit: " + user_text,
            "Intéressant. Peux-tu préciser ?",
            "Je comprends. Voici une idée: " + (user_text[:80] + "…" if len(user_text) > 80 else user_text),
            "Bonne question ! Je vais développer un peu là-dessus.",
            "D'accord 👍"
        ]
        import random
        reply = random.choice(responses)
        self.add_message(reply, is_user=False)


def main():
    app = QApplication(sys.argv)
    font = QFont()
    font.setPointSize(10)
    app.setFont(font)
    w = ChatWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
