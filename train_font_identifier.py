import os

import torch
import torch.nn as nn
import torch.optim as optim
# from datasets import load_dataset
from torchvision import datasets, models, transforms
from tqdm import tqdm
from util.image_util import filter_main
from consts import TRAIN_TEST_IMAGES_DIR
import argparse

# Transformations for the image data
data_transforms = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),  # Convert images to grayscale with 3 channels
    transforms.RandomCrop((224, 224)),  # Resize images to the expected input size of the model
    transforms.ToTensor(),  # Convert images to PyTorch tensors
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize with ImageNet stats
])

# 过滤异常image大小
for x in ['train', 'test']:
    font_file_path = os.path.join(TRAIN_TEST_IMAGES_DIR, x)
    filter_main(font_file_path)

# Create datasets
image_datasets = {
    x: datasets.ImageFolder(os.path.join(TRAIN_TEST_IMAGES_DIR, x), data_transforms)
    for x in ['train', 'test']
}

# 加载中文字体数据集
# ds = load_dataset("poorguys/chinese_fonts_common_512x512")

# Create dataloaders
dataloaders = {
    'train': torch.utils.data.DataLoader(image_datasets['train'], batch_size=4, shuffle=True, drop_last=True),
    # 'train': torch.utils.data.DataLoader(ds['image'], batch_size=4, shuffle=True),
    'test': torch.utils.data.DataLoader(image_datasets['test'], batch_size=4, shuffle=True, drop_last=True)
}

# Define the model
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Modify the last fully connected layer to match the number of font classes you have
num_classes = len(image_datasets['train'].classes)
model.fc = nn.Linear(model.fc.in_features, num_classes)

# Define the loss function
criterion = torch.nn.CrossEntropyLoss()

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
if torch.cuda.is_available():
    print("Using GPU")
    model = model.cuda()
    criterion = criterion.cuda()
optimizer = optim.Adam(model.parameters())


# Function to perform a training step with progress bar
def train_step(model, data_loader, criterion, optimizer):
    model.train()
    total_loss = 0
    progress_bar = tqdm(data_loader, desc='Training', leave=True)
    for inputs, targets in progress_bar:
        if torch.cuda.is_available():
            inputs, targets = inputs.cuda(), targets.cuda()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        progress_bar.set_postfix(loss=loss.item())
    progress_bar.close()
    return total_loss / len(data_loader)


# Function to perform a validation step with progress bar
def validate(model, data_loader, criterion):
    model.eval()
    total_loss = 0
    correct = 0
    progress_bar = tqdm(data_loader, desc='Validation', leave=False)
    with torch.no_grad():
        for inputs, targets in progress_bar:
            if torch.cuda.is_available():
                inputs, targets = inputs.cuda(), targets.cuda()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            total_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == targets).sum().item()
            progress_bar.set_postfix(loss=loss.item())
    progress_bar.close()
    return total_loss / len(data_loader), correct / len(data_loader.dataset)


# Save the model to disk
def main():
    parser = argparse.ArgumentParser(description="Train a font identifier model.")
    parser.add_argument('--checkpoint', type=str, default=None, help="Path to a checkpoint file to resume training.")
    args = parser.parse_args()

    # Load checkpoint if provided
    if args.checkpoint and os.path.exists(args.checkpoint):
        print(f"Loading checkpoint from {args.checkpoint}")
        model.load_state_dict(torch.load(args.checkpoint))
        print("Checkpoint loaded successfully.")
    print(image_datasets['train'].classes)

    # Training loop with progress bar for epochs
    num_epochs = 50  # Replace with the number of epochs you'd like to train for
    for epoch in range(num_epochs):
        print(f"Epoch {epoch + 1}/{num_epochs}")
        train_loss = train_step(model, dataloaders["train"], criterion, optimizer)
        val_loss, val_accuracy = validate(model, dataloaders["test"], criterion)
        print(f"Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.4f}")

    # Save the model to disk
    torch.save(model.state_dict(), 'font_identifier_model.pth')
    print("Model saved to 'font_identifier_model.pth'.")

if __name__ == "__main__":
    main()
