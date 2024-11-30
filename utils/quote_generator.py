from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import uuid
from datetime import datetime

class QuoteImageGenerator:
    def __init__(self, app):
        self.app = app
        self.fonts_dir = os.path.join(app.static_folder, 'fonts')
        self.backgrounds_dir = os.path.join(app.static_folder, 'backgrounds')
        self.decorations_dir = os.path.join(app.static_folder, 'decorations')
        self.output_dir = os.path.join(app.static_folder, 'generated')
        
        # Create necessary directories
        os.makedirs(self.fonts_dir, exist_ok=True)
        os.makedirs(self.backgrounds_dir, exist_ok=True)
        os.makedirs(self.decorations_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Default settings
        self.default_font = os.path.join(self.fonts_dir, 'AbyssinicaSIL-Regular.ttf')
        self.default_size = (1200, 1200)  # Square format for social media
        self.default_font_size = 60
        
        # Notebook paper settings
        self.line_spacing = 32
        self.margin_left = 100
        self.line_color = (200, 200, 220)
        
    def create_quote_image(self, text, author=None, style=None, decorations=None, 
                          background_type='notebook', background_value=None,
                          font_name=None, font_size=None, text_color=None,
                          text_alignment='center', watermark=None):
        """
        Create a quote image with the given parameters
        
        :param text: The quote text
        :param author: Optional author name
        :param style: Style preset ('notebook', 'modern', 'minimal', etc.)
        :param decorations: List of decorations to add (paths to decoration images)
        :param background_type: 'notebook', 'color', 'gradient', or 'image'
        :param background_value: Color code, gradient spec, or image path
        :param font_name: Font file name
        :param font_size: Font size to use
        :param text_color: Color for the text
        :param text_alignment: Text alignment ('left', 'center', 'right')
        :param watermark: Optional watermark text or logo
        :return: Path to generated image
        """
        # Create base image based on style
        if background_type == 'notebook':
            img = self._create_notebook_background()
        else:
            img = self._create_background(background_type, background_value)
        
        draw = ImageDraw.Draw(img)
        
        # Set up font
        font_path = os.path.join(self.fonts_dir, font_name) if font_name else self.default_font
        font_size = font_size or self.default_font_size
        try:
            font = ImageFont.truetype(font_path, font_size)
            author_font = ImageFont.truetype(font_path, font_size // 1.5)
        except OSError:
            font = ImageFont.truetype(self.default_font, font_size)
            author_font = ImageFont.truetype(self.default_font, font_size // 1.5)
        
        # Add decorative elements if provided
        if decorations:
            self._add_decorations(img, decorations)
        
        # Calculate text position and wrap text
        max_width = self.default_size[0] - (self.margin_left * 2)
        wrapped_text = self._wrap_text(text, font, max_width)
        
        # Calculate text position based on alignment
        if text_alignment == 'center':
            x = self.default_size[0] // 2
        elif text_alignment == 'right':
            x = self.default_size[0] - self.margin_left
        else:
            x = self.margin_left
        
        y = (self.default_size[1] - (len(wrapped_text) * self.line_spacing)) // 2
        
        # Draw text with style
        text_color = text_color or (0, 0, 0)
        for line in wrapped_text:
            text_bbox = draw.textbbox((0, 0), line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            
            if text_alignment == 'center':
                text_x = x - (text_width // 2)
            elif text_alignment == 'right':
                text_x = x - text_width
            else:
                text_x = x
            
            if background_type == 'notebook':
                # Add slight rotation for handwritten effect
                self._draw_text_with_handwriting_effect(draw, (text_x, y), line, font, text_color)
            else:
                self._draw_text_with_shadow(draw, (text_x, y), line, font, text_color)
            
            y += self.line_spacing
        
        # Add author if provided
        if author:
            author_text = f"- {author}"
            author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
            author_width = author_bbox[2] - author_bbox[0]
            
            if text_alignment == 'center':
                author_x = x - (author_width // 2)
            elif text_alignment == 'right':
                author_x = x - author_width
            else:
                author_x = x
            
            y += self.line_spacing
            self._draw_text_with_shadow(draw, (author_x, y), author_text, author_font, text_color)
        
        # Add watermark if provided
        if watermark:
            self._add_watermark(img, watermark)
        
        # Save image
        filename = f"quote_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path = os.path.join(self.output_dir, filename)
        img.save(output_path, "PNG", quality=95)
        
        return os.path.join('generated', filename)
    
    def _create_notebook_background(self):
        """Create a notebook paper background"""
        img = Image.new('RGB', self.default_size, 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw horizontal lines
        for y in range(40, self.default_size[1] - 40, self.line_spacing):
            draw.line([(40, y), (self.default_size[0] - 40, y)], fill=self.line_color, width=1)
        
        # Draw margin line
        draw.line([(80, 40), (80, self.default_size[1] - 40)], fill=(255, 0, 0, 30), width=1)
        
        # Add paper texture
        noise = Image.effect_noise(self.default_size, 10)
        noise = noise.convert('L')
        noise = ImageEnhance.Contrast(noise).enhance(0.1)
        img = Image.blend(img, noise.convert('RGB'), 0.05)
        
        return img
    
    def _add_decorations(self, img, decorations):
        """Add decorative elements to the image"""
        for decoration in decorations:
            try:
                dec_img = Image.open(os.path.join(self.decorations_dir, decoration['file']))
                dec_img = dec_img.resize(decoration.get('size', (200, 200)))
                if decoration.get('rotation'):
                    dec_img = dec_img.rotate(decoration['rotation'], expand=True)
                img.paste(dec_img, decoration['position'], dec_img if dec_img.mode == 'RGBA' else None)
            except Exception as e:
                print(f"Error adding decoration {decoration['file']}: {str(e)}")
    
    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit within the specified width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line = ' '.join(current_line)
            bbox = font.getbbox(line)
            if bbox[2] > max_width:
                if len(current_line) == 1:
                    lines.append(line)
                    current_line = []
                else:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _draw_text_with_handwriting_effect(self, draw, position, text, font, color):
        """Draw text with a handwriting-like effect"""
        x, y = position
        # Add slight random offset to each character for natural look
        for char in text:
            char_bbox = draw.textbbox((0, 0), char, font=font)
            char_width = char_bbox[2] - char_bbox[0]
            
            # Random slight rotation and position adjustment
            from random import randint
            angle = randint(-2, 2)
            offset_y = randint(-2, 2)
            
            # Create temporary image for the character
            char_img = Image.new('RGBA', (char_width + 10, font.size + 10), (0, 0, 0, 0))
            char_draw = ImageDraw.Draw(char_img)
            char_draw.text((5, 5), char, font=font, fill=color)
            
            # Rotate and paste
            rotated = char_img.rotate(angle, expand=True)
            img_x = x
            img_y = y + offset_y
            draw._image.paste(rotated, (int(img_x), int(img_y)), rotated)
            
            x += char_width
    
    def _draw_text_with_shadow(self, draw, position, text, font, color):
        """Draw text with a subtle shadow effect"""
        x, y = position
        # Draw shadow
        shadow_color = (128, 128, 128)
        draw.text((x+2, y+2), text, font=font, fill=shadow_color)
        # Draw main text
        draw.text((x, y), text, font=font, fill=color)
    
    def _add_watermark(self, img, watermark):
        """Add watermark to the bottom of the image"""
        draw = ImageDraw.Draw(img)
        watermark_font = ImageFont.truetype(self.default_font, 24)
        
        if isinstance(watermark, str):
            # Text watermark
            bbox = watermark_font.getbbox(watermark)
            x = (self.default_size[0] - bbox[2]) // 2
            y = self.default_size[1] - 60
            draw.text((x, y), watermark, font=watermark_font, fill=(128, 128, 128, 128))
        else:
            # Logo watermark
            try:
                logo = Image.open(watermark)
                logo = logo.resize((150, 150))
                x = (self.default_size[0] - 150) // 2
                y = self.default_size[1] - 180
                img.paste(logo, (x, y), logo if logo.mode == 'RGBA' else None)
            except Exception as e:
                print(f"Error adding logo watermark: {str(e)}")
