from io import BytesIO
from PIL import Image, ImageSequence, ImageDraw, ImageFont
from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse
from rich.console import Console

# --- Constants --- #

app = APIRouter()
console = Console()

# --- Routes --- #

@app.get("/sus")
async def ping(top_text: str, bottom_text: str) -> dict:
    gif = generate_sus(top_text, bottom_text)
    gif.seek(0)
    console.log(f'[IMAGES] User generated sussy image with top text "{top_text}" and bottom text "{bottom_text}"')
    return StreamingResponse(gif, media_type="image/png")

# --- Helpers --- #

def generate_sus(top_text: str, bottom_text: str) -> BytesIO:
    im = Image.open("media\gifs\sus.gif")
    W, H = im.size
    frames = []
    transparency = 0
    for frame in ImageSequence.Iterator(im):
        frame = frame.convert("RGBA")
        txt = Image.new('RGBA', frame.size, (255,255,255,0))
        top_size = 25
        bottom_size = 25
        font_top = ImageFont.truetype("media\\fonts\\Oswald-Regular.ttf", top_size)
        font_bottom = ImageFont.truetype("media\\fonts\\Oswald-Regular.ttf", bottom_size)
        d = ImageDraw.Draw(txt)
        w_top, _ = d.textsize(top_text, font=font_top)
        while w_top > W-7:
            top_size -= 1
            font_top = ImageFont.truetype("media\\fonts\\Oswald-Regular.ttf", top_size)
            w_top, _ = d.textsize(top_text, font=font_top)
        w_bottom, _ = d.textsize(bottom_text, font=font_bottom)
        while w_bottom > W-7:
            bottom_size -= 1
            font_bottom = ImageFont.truetype("media\\fonts\\Oswald-Regular.ttf", bottom_size)
            w_bottom, _ = d.textsize(top_text, font=font_bottom)
        d.text(((W-w_top)/2,10), top_text, fill=(0, 0, 0, transparency), font=font_top)
        d.text(((W-w_bottom)/2,150), bottom_text, fill=(0, 0, 0, transparency), font=font_bottom)
        combined = Image.alpha_composite(frame, txt)
        frames.append(combined)
        if transparency < 256: 
            transparency += 8
    b = BytesIO()
    frames[0].save(b, 'GIF', save_all=True, append_images=frames)
    return b

# -------------- #