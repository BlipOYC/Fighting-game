
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Slider Test")
clock = pygame.time.Clock()


class Slider:
    def __init__(self, min_val, max_val, width, height, center,
                 filled_color, unfilled_color, knob_color, touch_color, font_color):

        pos = (0, 0)
        self.val_range = (min_val, max_val)
        self.min_val = min_val
        self.max_val = max_val
        self.slider_val = min_val
        self.slider = pygame.Rect(*pos, width, height)
        self.slider.center = center
        self.filled_color = filled_color
        self.unfilled_color = unfilled_color
        self.is_active = False
        self.font = pygame.font.Font(None, 30)
        self.font_color = font_color

        self.knob_color = {
            True: touch_color,
            False: knob_color
        }

        self.knob_height = height + 14
        self.knob = pygame.Rect(pos[0], pos[1] - 7, 10, self.knob_height)
        self.knob.center = center

        self.filled_slider = pygame.Rect(
            self.slider.x,
            self.slider.y,
            self.knob.centerx - self.slider.x,
            height
        )


    def update_slider(self, mouse_pos, mouse_state):
        if self.knob.collidepoint(mouse_pos) and mouse_state[0] and not self.is_active:
            self.is_active = True

        if not self.knob.collidepoint(mouse_pos) and mouse_state[0] and self.is_active:
            self.knob.centerx = mouse_pos[0]
        elif not (self.knob.collidepoint(mouse_pos) and mouse_state[0]) and self.is_active:
            self.is_active = False

        self.knob.centerx = mouse_pos[0] if self.is_active else self.knob.centerx

        if self.knob.x < self.slider.x:
            self.knob.centerx = self.slider.x
        elif self.knob.x > self.slider.right:
            self.knob.x = self.slider.right

        self.filled_slider.width = self.knob.x - self.slider.x

        self.slider_val = max(
            min(
                int(
                    ((self.val_range[1] - self.val_range[0]) / self.slider.w)
                    * (self.knob.centerx - self.slider.x)),
                self.max_val
            ),
            self.min_val
        )

    def draw(self, screen):
        pygame.draw.rect(
            screen, self.unfilled_color, self.slider, border_radius=7
        )
        pygame.draw.rect(
            screen, self.knob_color[self.is_active],
            self.knob, border_radius=5
        )
        pygame.draw.rect(
            screen, self.filled_color,
            self.filled_slider, border_radius=7
        )


# Create the slider
slider = Slider(
    min_val=0,
    max_val=100,
    width=400,
    height=10,
    center=(400, 300),
    filled_color=(50, 150, 255),
    unfilled_color=(100, 100, 100),
    knob_color=(255, 255, 255),
    touch_color=(255, 100, 100),
    font_color=(255, 255, 255)
)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_state = pygame.mouse.get_pressed()

    slider.update_slider(mouse_pos, mouse_state)

    screen.fill((30, 30, 30))
    slider.draw(screen)

    # Display current value
    text = slider.font.render(
        f"Value: {slider.slider_val}",
        True,
        slider.font_color
    )
    screen.blit(text, (350, 340))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()