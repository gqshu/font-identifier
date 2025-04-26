import os
import sys
import torch
from torchvision import models, transforms
from PIL import Image
from collections import Counter
from consts import TRAIN_TEST_IMAGES_DIR

# Define the same transformations used during training, excluding random cropping
base_transforms = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),  # Convert images to grayscale with 3 channels
    transforms.ToTensor(),  # Convert images to PyTorch tensors
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize with ImageNet stats
])

def load_model(model_path, num_classes):
    """Load the trained model."""
    model = models.resnet18(weights=None)  # Initialize ResNet18 without pretrained weights
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)  # Adjust the final layer
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu')))
    model.eval()
    if torch.cuda.is_available():
        model = model.cuda()
    return model

def predict_with_majority(model, image_path, class_names, k=5, crop_size=(224, 224)):
    """Perform inference on an image using K random crops and take the majority result."""
    image = Image.open(image_path).convert('RGB')  # Open the image
    predictions = []
    # Resize the image while preserving aspect ratio
    if image.width < crop_size[0] or image.height < crop_size[1]:
        scale_factor = max(crop_size[0] / image.height, crop_size[1] / image.width)
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        resize_transform = transforms.Resize((new_height, new_width))
        image = resize_transform(image)

    for _ in range(k):
        # Apply random cropping
        random_crop_transform = transforms.Compose([
            transforms.RandomCrop(crop_size),
            base_transforms
        ])
        cropped_image = random_crop_transform(image).unsqueeze(0)  # Add batch dimension
        if torch.cuda.is_available():
            cropped_image = cropped_image.cuda()

        # Perform inference
        with torch.no_grad():
            outputs = model(cropped_image)
            _, predicted = torch.max(outputs, 1)
            predictions.append(class_names[predicted.item()])

    # Take the majority vote
    majority_label = Counter(predictions).most_common(1)[0][0]
    return majority_label

def main():
    if len(sys.argv) < 3:
        print("Usage: python predict.py <model_path> <input_dir_or_file>")
        sys.exit(1)

    model_path = sys.argv[1]
    input_path = sys.argv[2]

    # Load the class names (replace with your actual class names)
    class_names = os.listdir(os.path.join(TRAIN_TEST_IMAGES_DIR, "train"))  # Update this path if needed

    # Load the model
    num_classes = len(class_names)
    model = load_model(model_path, num_classes)

    # Check if input is a directory or a file
    if os.path.isdir(input_path):
        # Iterate through all files in the directory
        for file_name in os.listdir(input_path):
            file_path = os.path.join(input_path, file_name)
            if os.path.isfile(file_path):
                label = predict_with_majority(model, file_path, class_names, k=5)
                print(f"{file_name}: {label}")
    elif os.path.isfile(input_path):
        # Perform inference on a single file
        label = predict_with_majority(model, input_path, class_names, k=5)
        print(f"{os.path.basename(input_path)}: {label}")
    else:
        print(f"Invalid input path: {input_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()