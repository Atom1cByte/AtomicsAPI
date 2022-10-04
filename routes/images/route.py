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
        font = ImageFont.truetype("media\\fonts\\Oswald-Regular.ttf", 25)
        d = ImageDraw.Draw(txt)
        w_top, _ = d.textsize(top_text, font=font)
        if w_top > W:
            font = ImageFont.truetype("media\\fonts\\Oswald-Regular.ttf", W-15/len(top_text))
            w_top, _ = d.textsize(top_text, font=font)
        w_bottom, _ = d.textsize(bottom_text, font=font)
        if w_bottom > W:
            font = ImageFont.truetype("media\\fonts\\Oswald-Regular.ttf", W-15/len(top_text))
            w_bottom, _ = d.textsize(top_text, font=font)
        d.text(((W-w_top)/2,10), top_text, fill=(0, 0, 0, transparency), font=font)
        d.text(((W-w_bottom)/2,150), bottom_text, fill=(0, 0, 0, transparency), font=font)
        combined = Image.alpha_composite(frame, txt)
        frames.append(combined)
        if transparency < 256: 
            transparency += 8
    b = BytesIO()
    frames[0].save(b, 'GIF', save_all=True, append_images=frames)
    return b

# -------------- #