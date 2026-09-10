from PIL import Image
import colorsys

image = Image.open("image.png").convert("RGBA")
pixels = image.load()

TRAIT_COLORS = {
    "white":  (255, 255, 255),
    "red":    (255, 84, 0),
    "floating": (110, 255, 163),
    "black":  (51, 50, 50),
    "angel":  (255, 235, 110),
    "alien":  (160, 255, 238),
    "zombie": (184, 113, 255),
    "relic":  (93, 128, 62),
    "aku":    (95, 160, 204),
    "metal":  (0, 0, 0),
}

ORIGINAL_TRAIT_BRIGHTNESS = {
    "white": 1.0,
    "red": 1.0,
    "floating": 1.0,
    "black": 1.0,
    "angel": 1.0,
    "alien": 1.0,
    "zombie": 1.0,
    "relic": 1.0,
    "aku": 1.25,
    "metal": 1.0,
}

NEW_TRAIT_BRIGHTNESS = {
    "white": 1.0,
    "red": 1.0,
    "floating": 1.0,
    "black": 0.1,
    "angel": 1.0,
    "alien": 1.0,
    "zombie": 1.0,
    "relic": 0.70,
    "aku": 1.0,
    "metal": 1.0,
}

original_trait = "relic"
new_trait = "alien"

red, green, blue = TRAIT_COLORS[new_trait]

# Convert the rgb values into hsv
new_hue, new_saturation, _ = colorsys.rgb_to_hsv(
    red / 255,
    green / 255,
    blue / 255
)

# Recolor the image
for y in range(image.height):
    for x in range(image.width):
        r, g, b, a = pixels[x, y]

        # Keep white, hue-shift near-gray pixels to red if black
        if max(r, g, b) - min(r, g, b) <= 10:
            if new_trait == "black":
                _, _, value = colorsys.rgb_to_hsv(
                    r / 255,
                    g / 255,
                    b / 255
                )

                r2, g2, b2 = colorsys.hsv_to_rgb(
                    0.0, 1.0, value
                )

                pixels[x, y] = (
                    int(r2 * 255),
                    int(g2 * 255),
                    int(b2 * 255),
                    a
                )

            continue

        # keep the original brightness
        _, _, value = colorsys.rgb_to_hsv(
            r / 255,
            g / 255,
            b / 255
        )

        # set the brightness based on the original and new trait
        value *= ORIGINAL_TRAIT_BRIGHTNESS.get(original_trait, 1.0)
        value *= NEW_TRAIT_BRIGHTNESS.get(new_trait, 1.0)
        value = min(value, 1.0)

        r2, g2, b2 = colorsys.hsv_to_rgb(
            new_hue,
            new_saturation,
            value
        )

        pixels[x, y] = (
            int(r2 * 255),
            int(g2 * 255),
            int(b2 * 255),
            a
        )

image.save("output.png")