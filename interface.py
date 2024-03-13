import math
import shared_variables
import pygame


def generate_tab_interface(notes, song_info, width=1800, height=900, time_resolution=4, string_spacing=25, padding=30):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"{song_info['artist']} - {song_info['title']}")

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)
    white = (255, 255, 255)
    black = (0, 0, 0)
    light_blue = (173, 216, 230)

    width_limit = width - padding
    row_height = string_spacing * 5  # Decreased y size
    empty_row_height = string_spacing  # Height of the empty row
    total_row_height = row_height + empty_row_height
    scroll_y = 0

    line_x = padding
    line_y_start = 0
    y_accumulator = 0
    pixels_per_ms = 1 / time_resolution

    # Create the rows (length based on the last note's time)
    num_surfaces = math.ceil((notes[-1]['time'] / time_resolution) / (width - padding * 2))
    rows = [pygame.Surface((width, total_row_height)) for _ in range(num_surfaces)]
    for row in rows:
        row.fill(white)

    waiting = False
    wait_start_time = None
    wait_duration = 1000

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if rows:
            rows[0].fill(white)

        current_row = 0

        for note in notes:
            time = note['time']
            if time == 0:
                time = 1
            string = note['string']
            fret = note['fret']
            color = note['color']

            std_time = time / time_resolution
            std_time_width = std_time + padding * math.ceil(std_time / (width - padding * 2))

            x_position = std_time_width % width_limit if std_time_width % width_limit != 0 else width_limit

            row_width_limit = width_limit * (current_row + 1)

            if std_time_width > row_width_limit:
                current_row = math.ceil(std_time_width / width_limit) - 1
                rows[current_row].fill(white)

            y_position = (string_spacing * (string - 1)) + 5

            text = font.render(str(fret), True, color)
            rows[current_row].blit(text, (x_position, y_position))

        # Blit each row (and empty row) onto the main screen
        for i, row in enumerate(rows):
            row_y_position = i * total_row_height - scroll_y
            screen.blit(row, (0, row_y_position))

            # Draw a white rectangle to fill the gap between rows
            pygame.draw.rect(screen, white, (0, row_y_position + row_height, width, empty_row_height))

        # Draw lines for each string in all previous rows and the current row
        for row_offset in range(current_row + 1):
            for i in range(1, 5):
                y = i * string_spacing + (current_row - row_offset) * total_row_height
                pygame.draw.line(screen, black, (padding, y), (width - padding, y), 2)

        # Add string labels at the start of each row
        labels = ["G", "D", "A", "E"]
        for i, label in enumerate(labels):
            y = i * string_spacing
            for row_offset in range(current_row + 1):
                row_y_position = row_offset * total_row_height + 5
                screen.blit(font.render(label, True, black), (0, y + row_y_position))

        # Update the x-coordinate of the line based on the speed and time difference
        time_difference = clock.tick(60)
        line_x += pixels_per_ms * time_difference

        # Draw the rounded ends of the vertical line within the width limit
        line_x = min(line_x, width - padding)

        line_y_end = line_y_start + row_height
        line_thickness = 20

        # Draw the central
        pygame.draw.line(screen, light_blue, (line_x, line_y_start), (line_x, line_y_end), line_thickness)

        # Draw rounded ends
        radius = line_thickness / 2
        pygame.draw.circle(screen, light_blue, (line_x + 1, line_y_start), radius)
        pygame.draw.circle(screen, light_blue, (line_x + 1, line_y_end), radius)

        # Move the line to the next row when it reaches the end of the current row
        if line_x >= width - padding and y_accumulator < (len(rows) - 1) * total_row_height:
            line_x = padding
            line_y_start += total_row_height
            y_accumulator += total_row_height
            if line_y_start >= height:
                screen.fill(black)
                scroll_y += line_y_start
                line_y_start = 0

        if y_accumulator == (len(rows) - 1) * total_row_height:
            if not waiting:
                wait_start_time = pygame.time.get_ticks()
                waiting = True
            else:
                # Check if the waiting period has elapsed
                if pygame.time.get_ticks() - wait_start_time >= wait_duration:
                    # Fill the screen white
                    screen.fill(white)

                    # Create and display the report
                    message = "Música concluída com sucesso!"
                    hits = shared_variables.hits
                    misses = shared_variables.misses
                    precision = hits / len(notes)

                    report_text = (
                        f"{'Música concluída com sucesso!':}\n\n"
                        f"{'='*40}\n"
                        f"{song_info['artist']} - {song_info['title']}\n"
                        f"{'='*40}\n\n"
                        f"Acertos: {hits}\n"
                        f"Erros: {misses}\n"
                        f"Precisão: {precision:.2f}"
                    )

                    report_font = pygame.font.Font(None, 36)
                    text_y = height * 0.1  # Initial y position for the text

                    for i, line in enumerate(report_text.split("\n")):
                        text_surface = report_font.render(line, True, black)
                        text_rect = text_surface.get_rect(right=(width - padding - 10), centery=text_y + text_surface.get_height() // 2)
                        text_rect.centerx = width // 2  # Center horizontally
                        screen.blit(text_surface, text_rect)
                        text_y += text_surface.get_height() + 10  # Add spacing between lines

        pygame.display.flip()

    pygame.quit()
