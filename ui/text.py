import pygame
from pygame.locals import Color
from PIL import Image, ImageFont, ImageDraw

class Text:
    """Create a text object."""

    def __init__(self, text, pos, font = None, size = 24, color = 'black', **options):
        self.text = text
        self.pos = pos
        self.font_name = font
        self.font_size = size
        self.font_color = Color(color)
        self.set_font()
        self.render()

    def set_font(self):
        """Set the Font object from name and size."""
        font_path = pygame.font.match_font(self.font_name)
        self.font = pygame.font.Font(font_path, self.font_size)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.font_color)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self, screen):
        """Draw the text image to the screen."""
        screen.blit(self.img, self.rect)

        
class EmojiText:
    def __init__(self, text, pos, font_name, size=20, color='black'):
        self.text = text
        self.pos = pos
        self.font_path = pygame.font.match_font(font_name)
        self.font_size = size
        self.color = Color(color)[:3]
        self.image = self.render_text()

    def render_text(self):
        font = ImageFont.truetype(self.font_path, self.font_size)
        size = font.getbbox(self.text)[2:]
        # Create a new image with a transparent background
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), self.text, font=font, fill=self.color)
        # Convert PIL image to Pygame image
        mode = image.mode
        data = image.tobytes()
        pygame_image = pygame.image.fromstring(data, size, mode)
        return pygame.transform.scale_by(pygame_image, 0.4)

    def draw(self, screen):
        screen.blit(self.image, self.pos)