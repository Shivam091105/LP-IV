
from PIL import Image, ImageDraw, ImageFont
import random
import string

# Generate a random CAPTCHA
captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# Create a white image
image = Image.new("RGB", (200, 70), "white")
draw = ImageDraw.Draw(image)

# Draw CAPTCHA text
try:
    font = ImageFont.truetype("arial.ttf", 35)
except OSError:
    font = ImageFont.load_default()

draw.text((35, 15), captcha, fill="black", font=font)

# Add distortion lines
for _ in range(6):
    x1, y1 = random.randint(0, 200), random.randint(0, 70)
    x2, y2 = random.randint(0, 200), random.randint(0, 70)
    draw.line((x1, y1, x2, y2), fill="gray", width=2)

# Add noise dots
for _ in range(100):
    x, y = random.randint(0, 199), random.randint(0, 69)
    draw.point((x, y), fill="gray")

# Save and display the CAPTCHA
image.save("captcha.png")
image.show()

# Verify user input
user_input = input("Enter the CAPTCHA shown in the image: ").strip()

if user_input.upper() == captcha:
    print("CAPTCHA verified! Access granted.")
else:
    print("Incorrect CAPTCHA! Access denied.")
