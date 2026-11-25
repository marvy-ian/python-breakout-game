# Contributing to Breakout (Pygame)

Thank you for your interest in contributing to this project! Whether you are fixing a bug, adding a new power-up, or improving game feel, your contributions are welcome.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to help keep this project welcoming and inclusive for everyone.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/pygame-breakout.git
   cd pygame-breakout
   ```
3. **Set up your environment** and install `pygame`:
   ```bash
   pip install pygame
   ```
4. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

* **Code Style:** Follow [PEP 8](https://peps.python.org/pep-0008/) style conventions for Python code. Keep functions and methods concise and readable.
* **Constants:** Place tunable gameplay values (e.g., speeds, dimensions, colors, probabilities) at the top of `main.py` alongside existing configuration constants.
* **Self-Contained Assets:** If adding audio or visual enhancements, prefer procedural generation or lightweight, openly licensed assets so the game remains easy to run out of the box.
* **Testing:** Before submitting a pull request, playtest your changes across multiple levels to ensure there are no regressions in collision detection, power-up timers, or state transitions (`ready`, `playing`, `paused`, `gameover`).

## Submitting a Pull Request

1. Commit your changes with clear, descriptive commit messages.
2. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
3. Open a **Pull Request** against the `main` branch of the original repository.
4. Provide a clear summary of your changes and link any relevant issues.

## Ideas for Contributions

* Sound effects and background music (using `pygame.mixer`).
* Additional power-ups (e.g., multi-ball, laser paddle, slow ball).
* Persistent high-score tracking.
* Custom level layouts or a level editor.