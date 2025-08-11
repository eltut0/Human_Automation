# A Human-Like Automation Manager

A Python class that simulates human-like mouse movements, keyboard typing (including realistic errors), and interactions for automation tasks.

## Features

- Human-like mouse movement patterns with natural curves and variable speed
- Realistic keyboard typing simulation with common typing errors
- Error correction system (both immediate and delayed)
- Configurable speed and randomness parameters
- Support for common input actions (clicks, scroll, typing)

## Dependencies

- Python 3.7+
- `pyautogui` (for basic input simulation)
- `human_mouse` (custom mouse controller)
- `random` (built-in)
- `math` (built-in)
- `time` (built-in)

## Instalation
```bash
git clone "https://github.com/eltut0/Human_Automation/"
```
Include the Automation_Manager.py in your project files

## Usage
### Callable methods
``` python
from Automatization_Manager import Manager

# Initialize a new instance of Manager
manager = Manager()

manager.move(x, y) # Receives two ints, that represent a point in the screen, and moves the cursor to the point

manager.move_to(x0, y0, x1, y1) # Receives two pair of ints, that represent an area in the screen, it selects a random point and moves to

manager.clic() # Performs a clic

manager.double_clic() # Performs a double clic with random delays between each clic

manager.scroll(x) # Receives an int that represents the size of the scroll in pixels. Negative represents opposite direction

manager.type_text(text) # Receives a string and types it in the screen


```

### Basic example
``` python
from Automatization_Manager import Manager

# Initialize the manager
bot = Manager()

# Move mouse to specific coordinates
bot.move(500, 300)

# Perform a click
bot.clic()

# Type text with human-like errors
bot.type_text("Hello World! This is automated typing with realistic errors.")
```
## Advanced usage
``` python
# Move within an area
bot.move_to(100, 100, 300, 300)  # Random point within rectangle

# Double click
bot.double_clic()

# Scroll
bot.scroll(200)  # Scroll up
bot.scroll(-100)  # Scroll down

# Customize timing parameters
bot.min_time = 0.1  # Minimum delay between actions
bot.max_time = 0.3  # Maximum delay between actions
```
## Keyboard Error Simulation

The manager includes a comprehensive QWERTY keyboard layout with adjacent keys mapping to simulate common typing mistakes. Error probability is automatically calculated based on:

- Natural key adjacency

- Variable timing

- Random error correction patterns

## Mouse Movement Algorithm

The system uses a recursive approach to:
- Calculate direct path to target

- Generate intermediate control points

- Add natural deviations from perfect straight lines

- Adjust speed based on distance

## Configuration

You can adjust these class attributes:

- min_time/max_time: Control action speed variability

- keyboard_adjacent_keys: Modify key adjacency mapping

- Error probability thresholds in __error_prob()

## Safety Features

- Built-in random delays between actions

- Gradual acceleration/deceleration in mouse movements

- Automatic error correction (both immediate and delayed)

## Contributing

### Contributions are welcome! Please open an issue or pull request for:

- Additional keyboard layouts (AZERTY, QWERTZ)

- Improved movement algorithms

- Enhanced error simulation patterns
