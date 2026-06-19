import pygame
import random

pygame.init()

#title and icon of the game

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐸 Ribbit Rush")

try:
    font = pygame.font.SysFont("Arial", 24, bold=True)    
    big_font = pygame.font.SysFont("Arial", 56, bold=True)  
except Exception:
    font = pygame.font.Font(None, 28)
    big_font = pygame.font.Font(None, 64)

clock = pygame.time.Clock()

#dictionary of words and their clues for the game

clues = {
    "FROG": "An amphibian that croaks.",
    "APPLE": "A fruit that keeps the doctor away.",
    "POND": "A small body of still water.",
    "PYTHON": "A snake which is also a programming language.",
    "LOOP": "A needed structure for repeating code.",
    "GREEN": "The common color of frogs.",
    "MERGE": "To combine or join together.",
    "MAYBE": "An uncertain answer.",
    "WATER": "A liquid that covers most of the Earth.",
    "CAR": "A common mode of transportation for roads",
    "LEAF": "Part of a plant that is often green.",
    "CAGE": "A structure used to confine animals.",
    "LOTUS": "A beautiful water flower.",
    "BOOK": "A collection of pages with information or stories.",
    "MANGO": "Known as the 'king of fruits'.",
    "CUBE": "A three-dimensional shape. Has 6 square faces.",
    "RAIN": "Falls from clouds.",
    "STREAM": "A small flowing river.",
    "STARS": "Twinkle in the night sky.",
    "BUBBLE": "A thin sphere of liquid enclosing air or gas.",
    "GOLD": "A precious yellow metal.",
    "SNAKE": "A legless reptile.",
    "BRIDGE": "A structure built to span a physical obstacle.",
    "CLOUD": "A visible mass of condensed water vapor in the sky.",
    "MUSIC": "An art form consisting of sound and silence.",
    "BUTTER": "A dairy product made from churning cream.",
    "GARDEN": "A plot of land where plants are cultivated.",
    "CANDLE": "A source of light made of wax.",
    "BREAD": "A staple food made from flour and water.",
    "KEY": "A small piece of metal used to open locks.",
    "UMBRELLA": "Used for protection against rain.",
    "MIRROR": "Reflects your image.",
}

available_words = list(clues.keys())

#each time a word is guessed, it is removed from the available words list to avoid repetition until all words are used, then it resets

def get_next_word():
    global available_words
    if not available_words:
        available_words = list(clues.keys())
    chosen = random.choice(available_words) 
    available_words.remove(chosen)
    return chosen

current_word = get_next_word()
current_clue = clues[current_word]

# Variables to track user input, tries, messages, frog position, and game state

user_text = ""
tries_left = 3
message = "Guess the word from the clue!"

TEXT_DARK = (30, 30, 30)
message_color = TEXT_DARK 

frog_pos = 1
game_won = False
game_lost = False

# Variables for screen shake effect and confetti particles for victory celebration

shake_duration = 0
shake_intensity = 0
confetti_particles = []

# Generate confetti particles with random properties for a vibrant victory celebration

for _ in range(100):
    confetti_particles.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(-HEIGHT, 0),
        'speed': random.uniform(2, 5),
        'angle': random.uniform(0, 360),
        'spin': random.uniform(-5, 5),
        'color': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
        'size': random.randint(8, 15)
    })

def trigger_screen_shake(duration=30, intensity=10):
    global shake_duration, shake_intensity
    shake_duration = duration
    shake_intensity = intensity

# Converts the frog's position (1-50) to x,y coordinates on the screen for smooth animation

def get_frog_coordinates(pos):
    pos -= 1
    row = pos // 10
    col = pos % 10
    x = 100 + col * 80
    y = 220 + (4 - row) * 95
    return x, y

frog_x, frog_y = get_frog_coordinates(frog_pos)
target_x, target_y = frog_x, frog_y
ANIMATION_SPEED = 0.15 

# Allow custom scale for beautiful size variation

def draw_lotus(surface, x, y, scale=1.0):
    petals = [(0, -18), (-14, -6), (14, -6), (-8, -18), (8, -18)]
    for px, py in petals:
        pygame.draw.ellipse(surface, (255, 182, 193),
                            (x + int(px * scale) - int(10 * scale), 
                             y + int(py * scale) - int(15 * scale), 
                             int(20 * scale), int(30 * scale)))
    pygame.draw.circle(surface, (255, 215, 0), (x, y - int(5 * scale)), int(6 * scale))
    pygame.draw.ellipse(surface, (50, 180, 50), 
                        (x - int(22 * scale), y - int(2 * scale), 
                         int(44 * scale), int(20 * scale)))

# Generate background lotuses with random positions and scales for a lively pond atmosphere
# Avoids the top dashboard area (y < 160)
background_lotuses = []
for _ in range(12):
    background_lotuses.append({
        'x': random.randint(40, WIDTH - 40),
        'y': random.randint(180, HEIGHT - 60),
        'scale': random.uniform(0.7, 1.1)  # Gives depth variation
    })

running = True

# Main game loop that handles events, updates game state, and renders everything on the screen

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_won and not game_lost and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]

            elif event.key == pygame.K_RETURN:
                guess = user_text.upper()

                if guess == current_word:
                    move = len(current_word)
                    frog_pos += move

                    if frog_pos >= 50:
                        frog_pos = 50
                        game_won = True

                    message = f"Correct! Move forward {move} lily pads!"
                    message_color = (0, 120, 0) 
                    target_x, target_y = get_frog_coordinates(frog_pos)

                    if not game_won:
                        current_word = get_next_word()
                        current_clue = clues[current_word]
                        tries_left = 3
                else:
                    tries_left -= 1

                    if tries_left > 0:
                        message = f"Wrong guess! {tries_left} tries left."
                        message_color = (180, 70, 0)
                        trigger_screen_shake(15, 4) 
                    else:
                        move = len(current_word)
                        frog_pos -= move

                        if frog_pos <= 1:
                            frog_pos = 1
                            game_lost = True
                            trigger_screen_shake(45, 15) 

                        message = f"Out of tries! Answer was {current_word}. Move back {move} pads."
                        message_color = (200, 0, 0) 
                        target_x, target_y = get_frog_coordinates(frog_pos)

                        if not game_lost:
                            current_word = get_next_word()
                            current_clue = clues[current_word]
                            tries_left = 3

                user_text = ""
            else:
                if event.unicode.isalpha():
                    user_text += event.unicode.upper()

# Smoothly animate the frog's movement towards the target position for a polished visual effect

    frog_x += (target_x - frog_x) * ANIMATION_SPEED
    frog_y += (target_y - frog_y) * ANIMATION_SPEED

# Apply screen shake effect by randomly offsetting the entire display surface when shake_duration is active

    offset_x = 0
    offset_y = 0
    if shake_duration > 0:
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
        shake_duration -= 1

# Create a separate surface for drawing the game elements, which allows for easy application of screen shake and layering effects
    display_surface = pygame.Surface((WIDTH, HEIGHT))

    bg_color = (40, 20, 30) if game_lost else (60, 145, 220)
    display_surface.fill(bg_color)

    ripple_color = (70, 40, 50) if game_lost else (90, 180, 255)
    for i in range(10):
        pygame.draw.circle(display_surface, ripple_color,
                           (100 + i * 90, 350),
                           20 + (i % 3) * 12, 2)

    # They are drawn BEFORE lily pads and the frog so they blend perfectly into the background
    if not game_lost:
        for lotus in background_lotuses:
            draw_lotus(display_surface, lotus['x'], lotus['y'], lotus['scale'])

# Draw the lily pads in a 5x10 grid, with special styling for the HOME pad and dynamic colors based on game state for a vibrant and engaging visual presentation
    square = 1
    for row in range(5):
        for col in range(10):
            pad_x = 100 + col * 80
            pad_y = 220 + (4 - row) * 95

            pad_color1 = (40, 40, 20) if game_lost else (20, 90, 20)
            pad_color2 = (80, 80, 40) if game_lost else (50, 180, 50)
            pad_color3 = (120, 120, 70) if game_lost else (100, 220, 100)

            pygame.draw.ellipse(display_surface, pad_color1, (pad_x - 32, pad_y - 24, 64, 48))
            pygame.draw.ellipse(display_surface, pad_color2, (pad_x - 30, pad_y - 22, 60, 44))
            pygame.draw.ellipse(display_surface, pad_color3, (pad_x - 18, pad_y - 12, 18, 10))

            pygame.draw.polygon(
                display_surface, bg_color,
                [(pad_x, pad_y), (pad_x + 18, pad_y - 10), (pad_x + 18, pad_y + 10)]
            )

            label = "HOME" if square == 50 else str(square)

            if square == 50:
                pygame.draw.circle(display_surface, (255, 215, 0), (pad_x, pad_y), 40, 5)

            txt = font.render(label, True, (255, 255, 255))
            display_surface.blit(txt, (pad_x - txt.get_width() // 2, pad_y - txt.get_height() // 2))
            square += 1

    fx, fy = int(frog_x), int(frog_y)

# Draw the frog with dynamic colors based on game state for a vibrant and engaging visual presentation, using multiple shapes to create a cute and recognizable character
    
    frog_color_dark = (70, 75, 70) if game_lost else (40, 120, 40)
    frog_color_light = (110, 120, 110) if game_lost else (50, 200, 50)
    
    pygame.draw.ellipse(display_surface, frog_color_dark, (fx - 24, fy + 8, 18, 12))
    pygame.draw.ellipse(display_surface, frog_color_dark, (fx + 6, fy + 8, 18, 12))
    pygame.draw.ellipse(display_surface, frog_color_light, (fx - 25, fy - 15, 50, 30))
    pygame.draw.circle(display_surface, frog_color_light, (fx - 10, fy - 15), 8)
    pygame.draw.circle(display_surface, frog_color_light, (fx + 10, fy - 15), 8)
    pygame.draw.line(display_surface, frog_color_dark, (fx - 10, fy - 15), (fx - 15, fy - 28), 4)
    pygame.draw.line(display_surface, frog_color_dark, (fx + 10, fy - 15), (fx + 15, fy - 28), 4)
    pygame.draw.circle(display_surface, frog_color_light, (fx - 15, fy - 28), 10)
    pygame.draw.circle(display_surface, frog_color_light, (fx + 15, fy - 28), 10)
    pygame.draw.circle(display_surface, (255, 255, 255), (fx - 15, fy - 30), 5)
    pygame.draw.circle(display_surface, (255, 255, 255), (fx + 15, fy - 30), 5)
    pygame.draw.circle(display_surface, (0, 0, 0), (fx - 15, fy - 30), 2)
    pygame.draw.circle(display_surface, (0, 0, 0), (fx + 15, fy - 30), 2)
    pygame.draw.ellipse(display_surface, (220, 255, 180), (fx - 15, fy - 5, 30, 18))

# Draw the clue box, input box, message box, and status indicators with dynamic colors based on game state for a vibrant and engaging visual presentation, ensuring all text is centered within their respective boxes for a polished look

    clue_box_rect = pygame.Rect(20, 20, 700, 55)
    pygame.draw.rect(display_surface, (255, 255, 255), clue_box_rect, border_radius=10)
    clue_surface = font.render(f"Clue: {current_clue}", True, TEXT_DARK)

    clue_x = clue_box_rect.x + (clue_box_rect.width - clue_surface.get_width()) // 2
    clue_y = clue_box_rect.y + (clue_box_rect.height - clue_surface.get_height()) // 2
    display_surface.blit(clue_surface, (clue_x, clue_y))

    input_box_rect = pygame.Rect(740, 20, 240, 55)
    pygame.draw.rect(display_surface, (255, 255, 255), input_box_rect, border_radius=10)

    display_text = user_text if user_text != "" else "TYPE HERE..."
    text_color = (0, 0, 255) if user_text != "" else (160, 160, 160)
    input_surface = font.render(display_text, True, text_color)
    input_x = input_box_rect.x + (input_box_rect.width - input_surface.get_width()) // 2
    input_y = input_box_rect.y + (input_box_rect.height - input_surface.get_height()) // 2
    display_surface.blit(input_surface, (input_x, input_y))

    msg_box_rect = pygame.Rect(20, 90, 960, 55)
    pygame.draw.rect(display_surface, (255, 255, 255), msg_box_rect, border_radius=10)
    msg_surface = font.render(message, True, message_color)
    msg_x = msg_box_rect.x + (msg_box_rect.width - msg_surface.get_width()) // 2
    msg_y = msg_box_rect.y + (msg_box_rect.height - msg_surface.get_height()) // 2
    display_surface.blit(msg_surface, (msg_x, msg_y))

    display_surface.blit(font.render(f"Pad: {frog_pos}/50", True, (255, 255, 255)), (40, 160))
    display_surface.blit(font.render(f"Tries Left: {tries_left}", True, (255, 255, 255)), (830, 160))

# If the game is won, display a victory overlay with confetti animation and a congratulatory message. If lost, show a somber overlay with a game over message. Both overlays use semi-transparency to allow the background to subtly show through, enhancing the visual impact of the endgame states.
    if game_won:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 170))
        display_surface.blit(overlay, (0, 0))
        
        for p in confetti_particles:
            p['y'] += p['speed']
            p['angle'] += p['spin']
            if p['y'] > HEIGHT:
                p['y'] = -20
                p['x'] = random.randint(0, WIDTH)
            
            p_surf = pygame.Surface((p['size'], p['size']), pygame.SRCALPHA)
            p_surf.fill(p['color'])
            rot_surf = pygame.transform.rotate(p_surf, p['angle'])
            display_surface.blit(rot_surf, (p['x'], int(p['y'])))

        win_text = big_font.render("🏆 VICTORY! YOU REACHED HOME!", True, (0, 120, 0))
        display_surface.blit(win_text, ((WIDTH - win_text.get_width()) // 2, 300))

    if game_lost:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        display_surface.blit(overlay, (0, 0))
        
        loss_text = big_font.render("💀 GAME OVER... FROG SANK!", True, (220, 20, 20))
        display_surface.blit(loss_text, ((WIDTH - loss_text.get_width()) // 2, 300))

# Finally, blit the entire display surface onto the main screen with any shake offsets applied, and update the display to show all the rendered elements
    screen.blit(display_surface, (offset_x, offset_y))
    pygame.display.flip()

# Quit Pygame and clean up resources when the game loop ends
pygame.quit()
