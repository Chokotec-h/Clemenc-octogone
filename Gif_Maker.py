
from PIL import Image

from DATA.assets.animations import *


def create_image_with_text(char,animation,frame):
    img = Image.open(animations[char][animation][0])
    img = img.crop((animations[char][animation][1][frame][0],0,animations[char][animation][1][frame][0]+animations[char][animation][1][frame][2],animations[char][animation][1][frame][1]+animations[char][animation][1][frame][3]))    #Récupére la moitié gauche de l'image
    img = img.resize((animations[char][animation][1][frame][2]*2, (animations[char][animation][1][frame][1]+animations[char][animation][1][frame][3])*2))
    return img
# Create the frames
def convert_to_gif(char,animation):
    width = []
    height = []
    for _,y,w,h in animations[char][animation][1] :
        width.append(w)
        height.append(y+h)
    frames = [Image.new("RGBA",(max(width)*2,max(height)*2))]
    for frame in range(len(animations[char][animation][1])*animations[char][animation][-2]):
        new_frame = create_image_with_text(char,animation,frame//animations[char][animation][-2])
        frames.append(new_frame)
    frames[0].paste(frames[1])
    frames[0].save(f'./GIF/{char}_{animation}.gif', format='GIF',
               append_images=frames[1:], save_all=True, duration=300/animations[char][animation][-2], loop=0)

def convert_all(char):
    for a in animations[char]:
        convert_to_gif("Kebab",a)

convert_all("Kebab")