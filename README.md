# Breakout (Pygame)

A classic arcade-style Breakout clone built in Python using `pygame`. Smash through multi-layered brick formations, catch falling power-ups, and advance through increasingly challenging levels.

## Features

* **Progressive Levels:** Advancing levels increase ball speed, introduce multi-hit armored bricks, and vary brick layouts.
* **Power-Ups:** Destroyed bricks have a chance to drop power-ups:
  * **`W` (Wide Paddle):** Temporarily expands your paddle width by 60% for 10 seconds.
  * **`L` (Extra Life):** Grants an additional life (up to a maximum of 9).
* **Dual Control Support:** Play smoothly using either the keyboard or the mouse.
* **Dynamic Ball Physics:** Ball bounce angles adjust dynamically depending on where the ball strikes the paddle.

## Prerequisites

* Python 3.8 or higher
* `pygame` (or `pygame-ce`)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/pygame-breakout.git
   cd pygame-breakout
   ```

2. **Create a virtual environment (optional, recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install pygame
   ```

## How to Play

Run the game from the root directory:

```bash
python main.py
```

### Controls

| Action | Keyboard | Mouse |
| :--- | :--- | :--- |
| **Move Paddle** | `Left` / `Right` Arrows or `A` / `D` | Move cursor horizontally |
| **Launch Ball / Restart** | `Space` | `Left Click` |
| **Pause / Resume** | `P` | — |
| **Quit Game** | `Esc` | Close window |

## Project Structure

* `main.py`: Contains the complete game loop, entity classes (`Brick`, `PowerUp`, `Game`), collision physics, and rendering logic.

## License