# number of images to generate per font
IMAGES_PER_FONT = 50
# allowlist of fonts to use
FONT_ALLOWLIST = ["Arial",
                  "Arial Black",
                  "Arial Bold Italic",
                  "Arial Bold",
                  "Avenir",
                  "Courier",
                  "Helvetica",
                  "Georgia",
                  "Tahoma",
                  "Tahoma Bold",
                  "Times New Roman",
                  "Times New Roman Bold",
                  "Times New Roman Italic",
                  "Times New Roman Bold Italic",
                  "Trebuchet MS",
                  "Trebuchet MS Bold",
                  "Trebuchet MS Italic",
                  "Trebuchet MS Bold Italic",
                  "Verdana",
                  "Verdana Bold",
                  "Verdana Italic",
                  "Verdana Bold Italic"
                  ]

FONT_EXCEPTS = [
    "mstmc",
    "marlett",
    "SansSerifCollection",
    "segmdl2",
    "Segoelcons",
    "webdings",
    "wingding"
]
# directory where to store the generated images
GEN_IMAGES_DIR = 'generated_images'
# images organized into train and test directories
TRAIN_TEST_IMAGES_DIR = 'train_test_images'
# where to grab the font files from
# macos
# FONT_FILE_DIRS = ['/System/Library/Fonts/', '/System/Library/Fonts/Supplemental/']
# win
FONT_FILE_DIRS = ['C:\\Windows\\Fonts']

# where to grab the Google Fonts, all of which are allowed
GOOGLE_FONTS_DIR = "google_fonts"
