from PyQt5.QtGui import QColor, QTextCharFormat
from PyQt5.QtCore import Qt

class ThoughtsManager:
    def __init__(self, thoughts_display):
        self.thoughts_display = thoughts_display
        self.creature_colors = {}
        self.creature_thoughts = {}  # To track active thoughts for each creature

    def add_thought(self, creature_id, thought_text):
        # Initialize creature's color if not already assigned
        if creature_id not in self.creature_colors:
            color = QColor.fromHsv((creature_id * 100) % 360, 255, 200)
            self.creature_colors[creature_id] = color

        # Track and avoid repeating thoughts
        if thought_text == "feels hungry" and self.creature_thoughts.get(creature_id) == "feels hungry":
            return  # Avoid adding duplicate "feels hungry" thoughts until resolved

        self.creature_thoughts[creature_id] = thought_text

        # Display thought with unique formatting
        color = self.creature_colors[creature_id]
        formatted_text = f"Creature {creature_id + 1}: {thought_text}\n"
        self.prepend_text(formatted_text, color)  # Prepend instead of appending

    def resolve_thought(self, creature_id, thought_text):
        """Remove resolved thoughts for a creature."""
        if self.creature_thoughts.get(creature_id) == thought_text:
            del self.creature_thoughts[creature_id]  # Allow for re-adding later

    def get_current_thought(self, creature_id):
        """Retrieve the current thought for a creature, if available."""
        return self.creature_thoughts.get(creature_id, "No thoughts")

    def update_thoughts_display(self):
        """Update the thoughts display panel with all creatures' current thoughts."""
        thoughts_text = ""
        for creature_id, thought in self.creature_thoughts.items():
            thoughts_text = f"Creature {creature_id + 1}: {thought}\n" + thoughts_text
        self.thoughts_display.setPlainText(thoughts_text)

    def prepend_text(self, text, color):
        cursor = self.thoughts_display.textCursor()
        cursor.movePosition(cursor.Start)  # Move the cursor to the start
        format = QTextCharFormat()
        format.setForeground(color)
        cursor.setCharFormat(format)
        cursor.insertText(text)
        self.thoughts_display.setTextCursor(cursor)  # Keep the cursor at the beginning
