# number of images to generate per font
IMAGES_PER_FONT = 50
# allowlist of fonts to use
FONT_ALLOWLIST = [
    'SF-Pro-Text-RegularItalic',
    'SF-Pro-Text-Bold',
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
# FONT_FILE_DIRS = ['C:\\Windows\\Fonts']
FONT_FILE_DIRS = [
    './fonts',
]

# where to grab the Google Fonts, all of which are allowed
GOOGLE_FONTS_DIR = "google_fonts"
