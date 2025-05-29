# Qix-Style Area Capture Game - Made mainly with 1 other person

A Python arcade game inspired by **Qix**, developed using **Pygame**. The objective is to fill at least **50% of the playfield** by venturing into the square, drawing lines, and safely reconnecting them to the boundary. The challenge lies in avoiding enemies and ensuring your lines don’t get interrupted mid-draw.

---

## 🎮 Game Objective

Start at the screen’s edge and draw lines into the play area. When a new line successfully reconnects to the boundary, the enclosed area is filled. If you fill at least **50%** of the total area, you **win**. If an enemy touches your line while you're drawing, you **lose**.

---

## 🧠 Key Features

- **Pygame Engine**: Smooth rendering, text display, and input handling
- **Flood Fill Algorithm**: Dynamically calculates and fills enclosed areas when lines reconnect
- **Enemy AI**: Random movement logic with boundary collision constraints
- **Player Mechanics**: Edge-safe zones, drawing state, movement restrictions, and collision detection
- **Game Loop Controls**:
  - Frame rate control (FPS)
  - Win/Lose state management
  - In-game text rendering (score, status, etc.)

---

## 🕹️ Controls

- **Arrow Keys** – Move the player
- **Space** – Start a line
- **Esc** – game Menu

---

## 📦 Requirements

- Python 3.8+
- Pygame (`pip install pygame`)
