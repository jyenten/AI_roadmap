import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

print("=== Day 22: Custom Image Classifier ===")


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"using device: {device}")

script_dir = os.path.dirname(os.path.abspath(__file__))

train_dir = os.path.join(script_dir, "training_set", "training_set")
test_dir = os.path.join(script_dir, "test_set", "test_set")

transform_train = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])

transform_test = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])

train_dataset = datasets.ImageFolder(root=train_dir, transform=transform_train)
test_dataset = datasets.ImageFolder(root=test_dir, transform=transform_test)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)


print(f"Classes: {train_dataset.classes}")
print(f"Training samples: {len(train_dataset)}")
print(f"Test samples: {len(test_dataset)}")

model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

for param in model.parameters():
    param.requires_grad = False

num_features = model.fc.in_features
model.fc = nn.Sequential(
    nn.Linear(num_features, 256),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(256, 2)
)

model = model.to(device)

trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Trainable parameters: {trainable_params}")

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

def train_epoch(model, loader, croiterion, optimizer):
    model.train()
    total_loss = 0
    correct = 0

    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        predicted = outputs.argmax(dim=1)
        correct += (predicted == labels).sum().item()

    return total_loss / len(loader), correct / len(loader.dataset)

def evaluate(model, loader, criterion):
    model.eval()
    total_loss = 0
    correct = 0

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            predicted = outputs.argmax(dim=1)
            correct += (predicted == labels).sum().item()

    return total_loss / len(loader), correct / len(loader.dataset)

train_losses = []
test_losses = []
train_accuracies = []
test_accuracies = []

for epoch in range(5):
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer)
    test_loss, test_acc = evaluate(model, test_loader, criterion)

    train_losses.append(train_loss)
    test_losses.append(test_loss)
    train_accuracies.append(train_acc)
    test_accuracies.append(test_acc)

    print(f"Epoch {epoch+1}/5 - Train Loss: {train_loss:.4f}, Train acc: {train_acc:.4f}, Test Acc: {test_acc:.4f}")

model_path = os.path.join(script_dir, "cat_dog_model.pth")
torch.save(model.state_dict(), model_path)
print(f"Model save to: {model_path}")

loaded_model = models.resnet18(weights=None)
num_features = loaded_model.fc.in_features
loaded_model.fc = nn.Sequential(
    nn.Linear(num_features, 256),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(256, 2)
    )
loaded_model.load_state_dict(torch.load(model_path, map_location=device))
loaded_model = loaded_model.to(device)
loaded_model.eval()

print("Model loaded successfully")

test_images, test_labels = next(iter(test_loader))
test_images = test_images.to(device)

all_images = []
all_labels = []

for test_images, test_labels in test_loader:
    all_images.append(test_images)
    all_labels.append(test_labels)
    if len(torch.cat(all_labels).unique()) == 2:
        break

all_images = torch.cat(all_images)
all_labels = torch.cat(all_labels)

indices_cats = (all_labels == 0).nonzero(as_tuple=False)[0][:3]
indices_dogs = (all_labels == 1).nonzero(as_tuple=False)[0][:3]
indices = torch.cat([indices_cats, indices_dogs])

sample_images = all_images[indices].to(device)
sample_labels = all_labels[indices]


with torch.no_grad():
    outputs = loaded_model(sample_images)
    predicted = outputs.argmax(dim=1)

classes = train_dataset.classes
for i in range(len(indices)):
    actual = classes[sample_labels[i].item()]
    pred = classes[predicted[i].cpu().item()]
    status = "✓" if actual == pred else "✗"
    print(f"{status} Actual: {actual}, Predicted: {pred}")


class_names = ["kočka", "pes"]   # index 0 = kočka, 1 = pes

cat_idx = torch.where(all_labels == 0)[0][:3]   # první 3 kočky
dog_idx = torch.where(all_labels == 1)[0][:3]   # první 3 psi
indices = torch.cat([cat_idx, dog_idx])

sample_images = all_images[indices].to(device)
sample_labels = all_labels[indices]

print("indices:", indices)              # ČEKÁME 6 hodnot
print("len indices:", len(indices))     # ČEKÁME 6
print("sample_labels:", sample_labels)  # ČEKÁME tensor([0, 0, 0, 1, 1, 1])

model.eval()
with torch.no_grad():
    outputs = model(sample_images)              # syrové skóre modelu
    _, preds = torch.max(outputs, dim=1)         # index nejvyššího skóre = třída

for i in range(len(indices)):
    skutecnost = class_names[sample_labels[i].item()]
    predpoved  = class_names[preds[i].item()]
    znacka = "✓" if skutecnost == predpoved else "✗"
    print(f"{znacka} Skutečnost: {skutecnost}, Předpověď: {predpoved}")

