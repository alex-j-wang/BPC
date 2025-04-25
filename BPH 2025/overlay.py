from PIL import Image
import os

files = [
    # "100000.png",
    # "100001.png",
    # "100010.png",
    # "100011.png",
    # "100100.png",
    # "100101.png",
    # "100110.png",
    # "100111.png",
    # "101000.png",
    # "101001.png",
    # "101010.png",
    # "101011.png",
    # "101100.png",
    # "101101.png",
    # "101110.png",
    # "101111.png",
    # "110000.png",
    # "110001.png",
    # "110010.png",
    # "110011.png",
    # "110100.png",
    # "110101.png",
    # "110110.png",
    # "110111.png",
    # "111000.png",
    # "111001.png",
    # "111010.png",
    # "111011.png",
    # "111100.png",
    # "111101.png",
    # "111110.png",
    # "111111.png"
    "000000.png"
]

layer_to_round = {
    0: "Adventure",
    1: "Reality",
    2: "Comedy",
    3: "Drama",
    4: "Horror",
    5: "Reality",
    6: "Action"
}

round_to_index = {
    "Action": 0,
    "Drama": 1,
    "Comedy": 2,
    "Adventure": 3,
    "Reality": 4,
    "Horror": 5
}

Action = Image.open("input-modified/Action.png").convert("RGBA")
ActionGray = Image.open("input-modified/ActionGray.png").convert("RGBA")
Adventure = Image.open("input-modified/Adventure.png").convert("RGBA")
AdventureGray = Image.open("input-modified/AdventureGray.png").convert("RGBA")
Comedy = Image.open("input-modified/Comedy.png").convert("RGBA")
ComedyGray = Image.open("input-modified/ComedyGray.png").convert("RGBA")
Drama = Image.open("input-modified/Drama.png").convert("RGBA")
DramaGray = Image.open("input-modified/DramaGray.png").convert("RGBA")
Horror = Image.open("input-modified/Horror.png").convert("RGBA")
HorrorGray = Image.open("input-modified/HorrorGray.png").convert("RGBA")
RealityOver = Image.open("input-modified/RealityOver.png").convert("RGBA")
RealityOverGray = Image.open("input-modified/RealityOverGray.png").convert("RGBA")
RealityUnder = Image.open("input-modified/RealityUnder.png").convert("RGBA")
RealityUnderGray = Image.open("input-modified/RealityUnderGray.png").convert("RGBA")

for file in files:
    for layer in range(7):
        bit = file[round_to_index[layer_to_round[layer]]]
        if (layer == 0 and bit == "0"):
            layer_image = AdventureGray
        elif (layer == 0 and bit == "1"):
            layer_image = Adventure
        elif (layer == 1 and bit == "0"):
            layer_image = RealityUnderGray
        elif (layer == 1 and bit == "1"):
            layer_image = RealityUnder
        elif (layer == 2 and bit == "0"):
            layer_image = ComedyGray
        elif (layer == 2 and bit == "1"):
            layer_image = Comedy
        elif (layer == 3 and bit == "0"):
            layer_image = DramaGray
        elif (layer == 3 and bit == "1"):
            layer_image = Drama
        elif (layer == 4 and bit == "0"):
            layer_image = HorrorGray
        elif (layer == 4 and bit == "1"):
            layer_image = Horror
        elif (layer == 5 and bit == "0"):
            layer_image = RealityOverGray
        elif (layer == 5 and bit == "1"):
            layer_image = RealityOver
        elif (layer == 6 and bit == "0"):
            layer_image = ActionGray
        elif (layer == 6 and bit == "1"):
            layer_image = Action

        if layer == 0:
            base = layer_image.copy()
        else:
            base = Image.alpha_composite(base, layer_image)

    print(f"Overlay complete. Saving to output/{file}")
    base.save("output/" + file)
