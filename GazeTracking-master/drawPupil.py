import math as m
from PIL import Image


# img = [[1 for x in range(int(width))] for y in range(int(height))]

# image = Image.open('0vWEI.png')
image = Image.open('iris.png')
# data = image.convert('RGB')
pixels = image.load()
width, height = image.size

def showPupil(Ro, Ri):  # for showing data as image
    img = drawPupil(Ro, Ri)
    list_image = [item for sublist in img for item in sublist]
    new_image = Image.new("RGBA", (len(img[0]), len(img)))
    new_image.putdata(list_image)
    return new_image

def drawPupil(Ro, Ri):
    cir = [[0 for x in range(int(Ro * 2))] for y in range(int(Ro * 2))]
    for i in range(int(Ro)):
        # outer_radius = Ro*m.cos(m.asin(i/Ro))
        outer_radius = m.sqrt(Ro*Ro - i*i)
        for j in range(-int(outer_radius),int(outer_radius)):
            if i < Ri:
                # inner_radius = Ri*m.cos(m.asin(i/Ri))
                inner_radius = m.sqrt(Ri*Ri - i*i)
            else:
                inner_radius = -1
            if j < -inner_radius or j > inner_radius:
                # this is the destination
                # solid:
                # cir[int(Ro-i)][int(Ro+j)] = (255,255,255)
                # cir[int(Ro+i)][int(Ro+j)] = (255,255,255)
                # textured:

                x = Ro+j
                y = Ro-i
                # calculate source
                angle = m.atan2(y-Ro,x-Ro)/2
                distance = m.sqrt((y-Ro)*(y-Ro) + (x-Ro)*(x-Ro))
                distance = m.floor((distance-Ri+1)*(height-1)/(Ro-Ri))
            #   if distance >= height:
            #       distance = height-1
                cir[int(y)][int(x)] = pixels[int(width*angle/m.pi) % width, height-distance-1]
                y = Ro+i
                # calculate source
                angle = m.atan2(y-Ro,x-Ro)/2
                distance = m.sqrt((y-Ro)*(y-Ro) + (x-Ro)*(x-Ro))
                distance = m.floor((distance-Ri+1)*(height-1)/(Ro-Ri))
            #   if distance >= height:
            #       distance = height-1
                cir[int(y)][int(x)] = pixels[int(width*angle/m.pi) % width, height-distance-1]
    return cir

