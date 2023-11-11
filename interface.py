import pygame


def generate_tab_interface(notes, song_info, width=1800, height=900, string_spacing=25, time_resolution=5, padding=20):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"{song_info['artist']} - {song_info['title']}")

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)
    white = (255, 255, 255)
    black = (0, 0, 0)

    row_height = string_spacing * 6  # Height of each row (four strings)
    empty_row_height = string_spacing  # Height of the empty row
    current_row = 0
    content_height = len(notes) * string_spacing

    # Store the contents of each row
    rows = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Create a new row if needed
        if current_row >= len(rows):
            row = pygame.Surface((width, row_height + empty_row_height))
            row.fill(white)  # Fill with white background
            rows.append(row)

        for note in notes:
            time = note['time']
            string = note['string']
            fret = note['fret']
            x_position = (time // time_resolution) - (current_row * width) + padding

            if x_position >= width - padding:
                current_row += 1
                if current_row >= len(rows):
                    row = pygame.Surface((width, row_height + empty_row_height))
                    row.fill(white)
                    rows.append(row)
                x_position = (time // time_resolution) - (current_row * width) + padding

            y_position = (string_spacing * (string - 1)) + 5

            text = font.render(str(fret), True, black)
            rows[current_row].blit(text, (x_position, y_position))

        # Blit each row (and empty row) onto the main screen
        for i, row in enumerate(rows):
            row_y_position = i * (row_height + empty_row_height)
            screen.blit(row, (0, row_y_position))

            # Draw white rectangle to fill the gap between rows
            pygame.draw.rect(screen, white, (0, row_y_position + row_height, width, empty_row_height))

        # Draw lines for each string in all previous rows and the current row
        for row_offset in range(current_row + 1):
            for i in range(1, 5):
                y = i * string_spacing + (current_row - row_offset) * (row_height + empty_row_height)
                if y < content_height:
                    pygame.draw.line(screen, black, (padding, y), (width - padding, y), 2)

        # Add string labels at the start of each row
        labels = ["G", "D", "A", "E"]
        for i, label in enumerate(labels):
            y = i * string_spacing
            for row_offset in range(current_row + 1):
                row_y_position = row_offset * (row_height + empty_row_height) + 5
                screen.blit(font.render(label, True, black), (0, y + row_y_position))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
