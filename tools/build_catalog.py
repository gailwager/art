"""Regenerates data/catalog.js (and missing thumbnails) from images/ plus the
title/category tables below.

Usage: python3 tools/build_catalog.py   (from anywhere; paths are repo-relative)

To ADD artwork: drop the image in images/, add an entry to ART below (or, for
Instagram mixed-media pieces named mm_<postcode>.jpg, add the title to
MM_TITLES and the caption to data/ig-captions.json; for oil paintings, drop
the image in images/oil_paintings/ and add an entry to OIL), then rerun. NOTE: codes
(e.g. W-07) are assigned alphabetically by title within each category, so
adding a work renumbers later codes in that category — visitors' saved stars
reference codes, so batch additions rather than trickling them in.
"""
import os, json
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.join(ROOT, "images")
OUT = os.path.join(ROOT, "data")
os.makedirs(OUT, exist_ok=True)

# category key -> (code letter, display name, tagline)
CATS = {
    "oil":       ("O", "Oil Paintings", "New work in oils — bears, barns and Colorado light"),
    "wildlife":  ("W", "Wildlife", "Elk, bears, foxes and the wild neighbors of the Rockies"),
    "birds":     ("B", "Birds", "From loons on quiet water to meadowlarks in song"),
    "dogs-cats": ("D", "Dogs & Cats", "Beloved companions, painted with personality"),
    "people":    ("P", "People & Portraits", "Faces, families and moments in watercolor"),
    "flowers":   ("F", "Flowers & Still Life", "Columbines, tulips and treasures from the garden"),
    "landscapes":("L", "Landscapes & Towns", "Colorado high country, village streets and faraway places"),
    "southwest": ("S", "Southwest", "Pueblos and mission churches of New Mexico"),
    "horses":    ("H", "Horses & Farm", "Horses, herds and life on the land"),
    "collage":   ("M", "Mixed Media & Collage", "Recent abstract and collage explorations"),
}

# filename -> (category, title, note)
ART = {
 # Horses & Farm
 "AMISH horse and buggy painting-2.JPG": ("horses", "Amish Horse and Buggy", "Watercolor of a horse and buggy resting by the barn."),
 "COW.JPG": ("horses", "Cows in Pasture", "Watercolor."),
 "Cows.jpg": ("horses", "The Herd", "Watercolor of dairy cows in a green pasture."),
 "cows fenced.JPG": ("horses", "Herefords at the Fence", "Watercolor study of Hereford cattle."),
 "Horses in snow.jpg": ("horses", "Horses in Snow", "A herd on the move through fresh snow."),
 "Horses in snowstorm.jpg": ("horses", "Horses in a Snowstorm", "Watercolor."),
 "Jeannies horses.jpg": ("horses", "Jeannie's Horses", "Commissioned portrait of two horses at pasture."),
 "Mare and Colt.JPG": ("horses", "Mare and Colt", "Watercolor."),
 "horse young.JPG": ("horses", "Young Paint", "A young paint horse in a summer field."),
 "winter stampede.jpg": ("horses", "Winter Stampede", "Appaloosas running through snow."),
 "nacho and applesauce.jpg": ("horses", "Nacho and Applesauce", "A pair of llamas in the winter high country."),
 "JOCKEYS.JPG": ("horses", "The Jockeys", "Watercolor from the racetrack."),
 "colorado spring2.jpg": ("horses", "Colorado Spring", "Horses grazing among the aspens."),
 # Wildlife
 "BUNNY.JPG": ("wildlife", "Cottontail", "Watercolor."),
 "Bears in winter darker.jpg": ("wildlife", "Bears in Winter", "Two brown bears in falling snow."),
 "Bears polar night.jpg": ("wildlife", "Polar Night", "Polar bear mother and cubs under a starry sky."),
 "bears arctic warmth.jpg": ("wildlife", "Arctic Warmth", "A polar bear family huddled against the cold."),
 "bears mother love.jpg": ("wildlife", "Mother's Love", "Polar bear and cub."),
 "bears polar reflections.jpg": ("wildlife", "Polar Reflections", "Polar bears on the ice, mirrored in still water."),
 "bear with snowflakes2.jpg": ("wildlife", "Bear with Snowflakes", "Black bear in a snowfall."),
 "Buffalo.JPG": ("wildlife", "Buffalo", "Watercolor."),
 "buffalo summer.jpg": ("wildlife", "Buffalo in Summer", "Bison grazing in a mountain meadow."),
 "buffalo sunset.jpg": ("wildlife", "Buffalo at Sunset", "Bison and horses in winter light."),
 "ELK-2.JPG": ("wildlife", "Bugling Elk", "A bull elk in full bugle."),
 "Elk painting for John Foster-2.jpg": ("wildlife", "Elk in the Pines", "Commissioned watercolor."),
 "Gail's Elk.jpg": ("wildlife", "Gail's Elk", "A colorful elk in the snow, 1996."),
 "bull elk painting.jpg": ("wildlife", "Bull Elk", "Watercolor."),
 "elk crossing card.jpg": ("wildlife", "Elk Crossing", "Elk fording a mountain river."),
 "new beginnings.jpg": ("wildlife", "New Beginnings", "Elk cow and newborn calf at the water's edge."),
 "Deer.jpg": ("wildlife", "Deer in the Forest", "Watercolor."),
 "deer buck in winter direct scan.jpg": ("wildlife", "Buck in Winter", "Mule deer buck by a woodpile."),
 "moose autumn.jpg": ("wildlife", "Autumn Moose", "Bull moose in fall color."),
 "moose in snow.jpg": ("wildlife", "Moose in Snow", "Watercolor."),
 "FOX.JPG": ("wildlife", "Red Fox", "Watercolor."),
 "FOX2.JPG": ("wildlife", "Fox Study", "Close study of a red fox."),
 "FOX2001.JPG": ("wildlife", "Fox in the Willows", "A fox among red willow branches, 2001."),
 "foxprofile2.jpg": ("wildlife", "Fox Profile", "Watercolor."),
 "wolf darker green 5x7.jpg": ("wildlife", "Wolf", "Watercolor."),
 "Coyote.jpg": ("wildlife", "Coyote in Snow", "Small watercolor study."),
 "coyote2000new.jpg": ("wildlife", "Coyote", "Watercolor, 2000."),
 "cougar painting.jpg": ("wildlife", "Cougar", "Mountain lion in winter."),
 "LEOPARD2.JPG": ("wildlife", "Leopard", "Leopard moving through tall grass."),
 "TIGER.JPG": ("wildlife", "Tiger at the Water", "Tiger wading with its reflection."),
 "lion the king.jpg": ("wildlife", "The King", "Portrait of a lion."),
 "mountain goat.jpg": ("wildlife", "Mountain Goat", "A goat on a rocky summit under the stars."),
 "mountain goats.jpg": ("wildlife", "Mountain Goat Family", "Nanny and kids in the high country."),
 "Lizard.jpg": ("wildlife", "Anole on the Lily", "A green anole sunning on a red daylily."),
 # Birds
 "GROUSE.JPG": ("birds", "Chukar in Winter", "Watercolor."),
 "Geese 2-2.jpg": ("birds", "Geese in Snow", "Canada geese, 1996."),
 "geese january thaw.jpg": ("birds", "January Thaw", "Canada geese in melting snow."),
 "Goose flying.jpg": ("birds", "Taking Flight", "A goose lifting off the water."),
 "Loons2.jpg": ("birds", "Loons", "Loon and chick on quiet water."),
 "OWL.JPG": ("birds", "Long-eared Owl", "Watercolor."),
 "great egret.jpg": ("birds", "Great Egret", "An egret stalking the shallows."),
 "mountain meadowlark.jpg": ("birds", "Meadowlark", "A meadowlark in song."),
 "wood ducks new camera.jpg": ("birds", "Wood Ducks", "A pair of wood ducks on a woodland pond."),
 # Dogs & Cats
 "Annie.jpg": ("dogs-cats", "Annie", "Cocker spaniel portrait."),
 "Barb's Dalmations.jpg": ("dogs-cats", "Barb's Dalmatians", "Dalmatians at play."),
 "Charlie.jpg": ("dogs-cats", "Charlie", "Standard poodle portrait."),
 "Cheryls dogs.jpg": ("dogs-cats", "Cheryl's Goldens", "Two golden retrievers."),
 "Corona.jpg": ("dogs-cats", "Corona", "Portrait of a husky mix."),
 "Dudley and Fraser.jpg": ("dogs-cats", "Dudley and Fraser", "Two yellow labs in the garden."),
 "Golden Retreiver Hunter.jpg": ("dogs-cats", "Hunter", "Golden retriever portrait."),
 "PUPPY.JPG": ("dogs-cats", "Bernese Puppy", "Watercolor."),
 "SCOUT.JPG": ("dogs-cats", "Scout", "German shepherd portrait."),
 "Tasha in summer.jpg": ("dogs-cats", "Tasha in Summer", "Husky resting in summer grass."),
 "Tasha.jpg": ("dogs-cats", "Tasha", "Siberian husky in the snow."),
 "black lab pup.jpg": ("dogs-cats", "Black Lab Pup", "Watercolor."),
 "jake and Lily Kim's black labs.jpg": ("dogs-cats", "Jake and Lily", "Two black labs, painted for Kim."),
 "max and buster.jpg": ("dogs-cats", "Max and Buster", "A cat and dog sharing an afternoon."),
 "puppies at play.jpg": ("dogs-cats", "Puppies at Play", "Lab puppies tugging a rope."),
 "Kitty.jpg": ("dogs-cats", "Kitty", "White cat curled on a celestial quilt."),
 "cat angel.jpg": ("dogs-cats", "Cat at the Window", "Watercolor."),
 "cats himalayan 2.jpg": ("dogs-cats", "Himalayan Cats", "Watercolor."),
 "Rocky and Gracie.jpg": ("dogs-cats", "Rocky and Gracie", "Siamese cats in the sun."),
 # People & Portraits
 "Art's retirement painting.jpg": ("people", "Art's Retirement", "A career in aviation, painted in tribute."),
 "Bluegrass.jpg": ("people", "Bluegrass", "Musicians at a summer jam."),
 "Brook gets air.jpg": ("people", "Brook Gets Air", "Snowboarder catching air."),
 "COWBOY.JPG": ("people", "The Cowboy", "Watercolor portrait."),
 "DROVER.JPG": ("people", "The Drover", "A rider and his horse in falling snow."),
 "Debby.jpg": ("people", "Debby", "Watercolor portrait."),
 "Gail self portrait.jpg": ("people", "Self Portrait", "The artist, by the artist."),
 "Heathers siblings.jpg": ("people", "Heather's Siblings", "Watercolor portrait."),
 "JACKSON.JPG": ("people", "Jackson", "Watercolor portrait."),
 "Kylie.jpg": ("people", "Kylie", "Watercolor portrait."),
 "SKATERS.JPG": ("people", "The Skaters", "Lacing up by the pond."),
 "SOPHIE.JPG": ("people", "Sophie", "Watercolor portrait."),
 "Tor2.JPG": ("people", "Tor", "Watercolor portrait."),
 "Valen.jpg": ("people", "Valen", "A toddler with a dandelion."),
 "charlotte 1.jpg": ("people", "Charlotte", "Watercolor portrait."),
 "charlotte.jpg": ("people", "Charlotte in Profile", "Watercolor portrait."),
 "molly's mom.jpg": ("people", "Molly's Mom", "Double portrait by the lake."),
 "Emily painting.jpg": ("people", "Emily", "Watercolor portrait."),
 "Fishing adventure painting.JPG": ("people", "Fishing Adventure", "Heading out across the water."),
 "fishing the blue.jpg": ("people", "Fishing the Blue", "Fly fishing the Blue River."),
 "Riders in the snow.jpg": ("people", "Riders in the Snow", "Riders winding through winter aspens."),
 "POEM.JPG": ("people", "The Trout — Illustrated Poem", "An illustrated poem with watercolor fish."),
 # Flowers & Still Life
 "Dahlias.jpg": ("flowers", "Dahlias", "Watercolor."),
 "FLOWERS-2.JPG": ("flowers", "Wildflower Bouquet", "Watercolor."),
 "FLOWERS.JPG": ("flowers", "Aspen Gold", "Autumn aspen leaves."),
 "TULIPS~1.JPG": ("flowers", "Tulip Bouquet", "Watercolor."),
 "columbine 3.JPG": ("flowers", "Columbines", "Colorado's state flower in evening light."),
 "columbine.jpg": ("flowers", "Blue Columbines", "Watercolor."),
 "crocus painting high res.jpg": ("flowers", "First of Spring", "Crocus pushing up through the last snow."),
 "daisies and sunflowers.jpg": ("flowers", "Daisies and Sunflowers", "Watercolor."),
 "tulips in bloom.jpg": ("flowers", "Tulips in Bloom", "Watercolor on a dark ground."),
 "poppiesSE.jpg": ("flowers", "Poppies", "Watercolor."),
 "sunflowers.jpg": ("flowers", "Sunflowers", "Watercolor."),
 "sun catcher copy.jpg": ("flowers", "Sun Catcher", "A sunflower turning to the light."),
 "PEARS.JPG": ("flowers", "Pears", "Still life."),
 "still life with peppers.jpg": ("flowers", "Still Life with Peppers", "Sunflowers, peppers and a pitcher."),
 # Landscapes & Towns
 "Aspens in  winter-2.jpg": ("landscapes", "Aspens in Winter", "Winter aspens, 1996."),
 "Bear Creek painting.JPG": ("landscapes", "Bear Creek", "Autumn along Bear Creek."),
 "Breckenridge.jpg": ("landscapes", "Breckenridge", "A storefront sketch in winter."),
 "Corsica.jpg": ("landscapes", "Corsica", "A cottage by the sea."),
 "California Reflections.JPG": ("landscapes", "California Reflections", "Harbor boats and their colors."),
 "KANSAS church.JPG": ("landscapes", "Kansas Church", "A white country church on the plains."),
 "Hydra street.jpg": ("landscapes", "Hydra Street", "A shopping street on the Greek island of Hydra."),
 "Barbara's house.jpg": ("landscapes", "Barbara's House", "House portrait by the shore."),
 "autumn in evergreen (3).jpg": ("landscapes", "Autumn in Evergreen", "Golden aspens in the artist's hometown."),
 "cabin in colorado.jpg": ("landscapes", "Cabin in Colorado", "A log cabin among winter aspens."),
 "cabin in columbine.jpg": ("landscapes", "Cabin in Columbine", "Winter cabin in the trees."),
 "crystal mill.jpg": ("landscapes", "Crystal Mill", "The historic mill near Marble, Colorado."),
 "evergreen lake house.JPG": ("landscapes", "Evergreen Lake House", "The lake house in winter."),
 "yhig print.jpg": ("landscapes", "Yellow House in Georgetown", "A Victorian house with a picket fence."),
 "mountain stream.jpg": ("landscapes", "Mountain Valley", "A stream winding through a high valley."),
 "steamboat  lake.JPG": ("landscapes", "Steamboat Lake", "Sailboats at rest."),
 "swiss windows.jpg": ("landscapes", "Alpine Windows", "Flower boxes on a European street."),
 "tree reflections.jpg": ("landscapes", "Tree Reflections", "Autumn trees mirrored on still water."),
 "winter stream.JPG": ("landscapes", "Winter Stream", "A creek threading through fresh snow."),
 "bloomsbury.jpg": ("landscapes", "Bloomsbury Gift Barn", "The Bloomsbury shop, flowers out front."),
 "flower cart at bloomsbury.jpg": ("landscapes", "Flower Cart at Bloomsbury", "Watercolor."),
 "flower shop.jpg": ("landscapes", "The Flower Shop", "Red windows and spring flowers."),
 # Southwest
 "Pueblo 1.jpg": ("southwest", "Pueblo Village", "Watercolor."),
 "Pueblo 2.jpg": ("southwest", "Pueblo with Ladder", "Taos Pueblo, 1996."),
 "Pueblo print.jpg": ("southwest", "Taos Pueblo", "Watercolor."),
 "Pueblos winter.jpg": ("southwest", "Pueblo Winter", "Adobe walls in snow."),
 "pueblo church 2.jpg": ("southwest", "Ranchos de Taos", "The San Francisco de Asis church."),
 "pueblo church.JPG": ("southwest", "Mission Church", "Adobe mission in winter, 1996."),
 "pueblo in snow.jpg": ("southwest", "Pueblo in Snow", "Watercolor."),
 "St. Francis of Assisi.JPG": ("southwest", "St. Francis of Assisi", "Mission bell towers against a stormy sky."),
}

# Oil Paintings — images live in images/oil_paintings/.
# filename -> (title, note); titles/sizes from Gail's list, untitled studies
# are given descriptive names.
OIL = {
 "IMG_0209.jpeg": ("Early Morning Frolic", "Two paint horses at play in the morning light. Oil, 24″ × 20″."),
 "IMG_0212.jpeg": ("Snowmelt in Spring", "A creek finding its way through the last of the snow. Oil, 14″ × 11″."),
 "IMG_0213.jpeg": ("Mama Bear", "Black bear portrait. Oil, 25″ × 25″."),
 "IMG_0214.jpeg": ("Five Island Lobster", "The lobster shack at Five Islands, Maine. Oil, 16″ × 13″."),
 "IMG_0215.jpeg": ("Niko", "Bernese mountain dog puppy portrait. Oil, 11″ × 14″."),
 "IMG_0216.jpeg": ("Peaceful Afternoon in Evergreen", "A red barn in the green hills. Oil, 15″ × 12″."),
 "IMG_0217.jpeg": ("Bluebird", "A bluebird perched on barbed wire. Oil, 12″ × 15″."),
 "IMG_0218.jpeg": ("Black Lab", "Black lab portrait. Oil, 12″ × 15″."),
 "IMG_0219.jpeg": ("Sunrise on Snowbird Lane", "Winter sunrise over the valley. Oil, 17″ × 14″."),
 "IMG_0220.jpeg": ("Old Mine in Nevadaville", "The old mine buildings at Nevadaville, Colorado. Oil, 17″ × 14″."),
 "IMG_0221.jpeg": ("Evergreen Lake", "Quiet water and willows at Evergreen Lake, Colorado. Oil, 17″ × 15″."),
 "IMG_0222.jpeg": ("Mr. Fox", "Red fox portrait. Oil, 17″ × 15″."),
 "IMG_0223.jpeg": ("Autumn on Squaw Pass", "Golden aspens against the September sky. Oil, 17″ × 15″."),
 "IMG_0224.jpeg": ("Beautiful Day on the Colorado Plains", "A weathered grain elevator under big clouds. Oil, 12″ × 15″."),
 "IMG_0225.jpeg": ("Buffalo", "A bull bison in winter grass. Oil, 17″ × 15″."),
 "IMG_0230.jpeg": ("Red Barn in the Foothills", "Horses at the fence below the mountains. Oil study."),
 "IMG_0231.jpeg": ("The CP Barn", "An old barn wearing its painted brand. Oil study."),
 "IMG_0233.jpeg": ("The Old Homestead", "A weathered barn in the dry grass. Oil study."),
 "IMG_0235.jpeg": ("High Country Barn", "A red barn at the edge of the pines, aspens alongside. Oil study."),
 "IMG_0236.jpeg": ("Late Winter Barn", "Snow lingering on the roof, bare aspens behind. Oil study."),
 "IMG_0237.jpeg": ("Cabin 1000", "Old cabins in the dry hills. Oil study."),
 "IMG_0238.jpeg": ("Early Spring", "A bare tree beside the path, waiting for the season to turn. Oil study."),
 "IMG_0239.jpeg": ("The Chestnut", "Portrait of a chestnut horse. Oil study."),
}
for _f, (_t, _n) in OIL.items():
    ART["oil_paintings/" + _f] = ("oil", _t, _n)

# Mixed Media & Collage — titles from Gail's own Instagram captions;
# untitled pieces are given descriptive names.
MM_TITLES = {
 "DbJvXumR0Lz": "BFFs", "DYbIRA6Mzml": "Spring Showers", "DYYQ-6xRms4": "Life at the Top",
 "DYV0Pu3RQmp": "On the Move", "DYNPfWCxicv": "I Am You and You Are Me",
 "DYNN3Icx7BK": "Be Not Divided", "DXcgX2iEeJw": "Lullabies at Twilight",
 "DXazFXgDFl7": "New Found Freedom", "DXH9LckESfg": "Really for Real",
 "DXAohv7EUM7": "There Must Be a Way", "DW-F_2vkc4l": "Hesitation",
 "DW9E2kfiQKZ": "Back to Basics", "DW9C4KeiaOb": "In Search of Authenticity",
 "DWsKJzbEcp5": "Finding the Path", "DWHUgPyEdIr": "A Stitch in Time",
 "DV7GZjSEQN_": "Lost", "DV315mdkfiP": "A Quiet Prayer", "DV150j5jVQd": "5 Things",
 "DV13SyXDcQ-": "A Trip Around the Universe", "DTqyxKjEaFD": "Celebrate",
 "DThRBt_DWTd": "Searching the Deep", "DThOVxHDcgf": "Drifting",
 "DTehYO3DGKE": "Dream the Impossible", "DTedot8jMLn": "Winter's Edge",
 "DOe5gbcjAX1": "Love Life, Play Well", "DOcr15QDCbN": "Evergreen Rodeo",
 "DOaBjeRDEas": "Simple Joys", "DMqrvjBOLXK": "Cairn", "DMie3uSOVuk": "The View from Above",
 "DLRDDe0uGjr": "Oasis", "DKGmLKTO-_F": "Botanics", "DJ-0WxXuc42": "Birds of a Feather",
 "DJ5V8Kiudbi": "Finding Possibilities", "DJxTYSQOpcd": "Who Doesn't Love the Beach",
 "DJsYWZuOefd": "Lost in the Grid", "DIaR2EUO1XY": "The Journey",
 "DISfSw_uDJT": "Be Mindful, Be Joyful, Be Grateful", "DH39mZCS5Qr": "Searching for Ancient Treasure",
 "DHzeDnJu_K7": "Life in the Tropics", "DHxGC5Hu5Pl": "Land's End",
 "DHwCKJ1Oeic": "Searching for Beauty", "DHsFawEuJ23": "Charms",
 "DHphVgUO0Po": "Love and Loss", "DHm1BpTuK2O": "Finding Focus",
 "DHkFCnIu8X1": "Ahhh… Music", "DHhqhurulMF": "Finding a World Within",
 "DHerzR4uMPy": "All-in-All", "DHcCxHIufA3": "For the Love of Dancing",
 "DHZ7MdWuEuL": "Pure Joy", "DHXWw-su29g": "At Loose Ends",
 "DHUbH7YOSNj": "Finding Pathways", "DHRlsBIuWZq": "Heading Upwards",
 "DHPpn11Og3m": "Staying Connected", "DHNGi_Fusls": "Oceanography",
 "DBHIo5qOyiC": "The Crow", "DBEWfa_Oy9P": "Fragments", "DA_wWsuSMF0": "Night Bouquet",
 "DAFPzhvOQst": "Autumn Dance", "DACzgesOVj9": "Postcard from Colorado II",
 "DAAPLSZuFkZ": "Postcard from Colorado", "C_9lv2lun8y": "Rings of Copper",
 "C_69DLYuixn": "Tangled Ribbons", "C_4SW37OYPU": "Puzzle in Neutrals",
 "C_1nVMKurPt": "The Vortex", "C_zSBQPu358": "Sunshine and Shadow",
 "C_yFvz5uJmZ": "Looking for Clues", "C_wMklxudTM": "Windy Day",
 "C_rmvRtObJt": "City Blocks", "C_o8injuuk4": "Bird's Eye View of the 'Hood",
 "C_mg7wAOS3a": "On the Rocks", "C_juW8yu7ZJ": "Colorado Aspens III",
 "C_gmyJky8EY": "Colorado Aspens II", "C_eUygMu6A-": "Colorado Aspens I",
 "C_byaawO_i6": "Mission at Moonrise", "C_Zd8uuO46h": "The Paint",
 "C_XCsvfOC68": "Buffalo and Calf", "C_UVaiNOZUa": "Hillside Sheep",
 "C_RvwVMu2MO": "Elk at Dusk", "C_PQtb8OpTj": "Chestnut",
 "C_Mm8J3Oaqr": "Love Songs", "C_KJXBXu1N_": "Nocturne", "C_HT7qSOgsy": "I Love You",
 "C_EN5SAy6AI": "Mellow Moon", "C-4OlC7OCdr": "-", "C-4NJt2umU_": "Violet Rhythms",
 "C-wVu62uIei": "Confetti", "C-MddjNM1wk": "Turquoise Moons",
}

import re as _re
def _clean_caption(cap):
    cap = _re.sub(r"#\S+", "", cap)              # strip hashtags
    cap = cap.replace("\n", " ")
    cap = _re.sub(r"\s+", " ", cap).strip(" .…")
    if len(cap) > 180:
        cap = cap[:180].rsplit(" ", 1)[0] + "…"
    return cap if cap else "Acrylic mixed media."

_caps_path = os.path.join(OUT, "ig-captions.json")
try:
    _caps = json.load(open(_caps_path))
except Exception:
    _caps = {}

for _f in os.listdir(REPO):
    if _f.startswith("mm_") and _f.endswith(".jpg"):
        _code = _f[3:-4]
        _title = MM_TITLES.get(_code, "Untitled")
        ART[_f] = ("collage", _title, _clean_caption(_caps.get(_code, "")))

files = sorted(f for f in os.listdir(REPO) if os.path.isfile(os.path.join(REPO, f)) and not f.startswith("."))
_oildir = os.path.join(REPO, "oil_paintings")
if os.path.isdir(_oildir):
    files += sorted("oil_paintings/" + f for f in os.listdir(_oildir)
                    if f.lower().endswith((".jpg", ".jpeg", ".png")) and not f.startswith("."))
unknown = [f for f in files if f not in ART]
missing = [f for f in ART if f not in files]
if unknown:
    print("UNCLASSIFIED:", unknown)
if missing:
    print("MISSING:", missing)

# assign codes: sort by title within category
order = ["collage", "oil", "wildlife", "birds", "horses", "dogs-cats", "people", "flowers", "landscapes", "southwest"]
items = []
for cat in order:
    letter = CATS[cat][0]
    members = sorted([(t, f, n) for f, (c, t, n) in ART.items() if c == cat and f in files])
    for i, (title, fname, note) in enumerate(members, 1):
        w, h = Image.open(os.path.join(REPO, fname)).size
        items.append({
            "code": f"{letter}-{i:02d}",
            "title": title,
            "cat": cat,
            "file": fname,
            "note": note,
            "w": w, "h": h,
        })

# generate any missing 600px thumbnails (gallery grids use images/thumbs/)
THUMBS = os.path.join(REPO, "thumbs")
os.makedirs(THUMBS, exist_ok=True)
made = 0
for it in items:
    tpath = os.path.join(THUMBS, os.path.splitext(it["file"])[0] + ".jpg")
    if not os.path.exists(tpath):
        os.makedirs(os.path.dirname(tpath), exist_ok=True)
        im = Image.open(os.path.join(REPO, it["file"])).convert("RGB")
        im.thumbnail((600, 600))
        im.save(tpath, quality=82, optimize=True)
        made += 1
if made:
    print(f"generated {made} missing thumbnails")

catalog = {
    "categories": [{"key": k, "letter": CATS[k][0], "name": CATS[k][1], "tag": CATS[k][2]} for k in order],
    "artworks": items,
}
with open(os.path.join(OUT, "catalog.js"), "w") as f:
    f.write("// Generated catalog of Gail Wager's artwork\nconst CATALOG = ")
    json.dump(catalog, f, indent=1)
    f.write(";\n")
print(f"catalog: {len(items)} artworks in {len(order)} categories")
for k in order:
    print(" ", CATS[k][0], CATS[k][1], sum(1 for it in items if it['cat']==k))
