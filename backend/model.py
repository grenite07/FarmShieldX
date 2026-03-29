import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v2
from PIL import Image
import io

# 1. Define the classes for the Hackathon Demo
CLASSES = ["Healthy", "Potato Late Blight", "Tomato Yellow Leaf Curl Virus", "Apple Scab"]

# 2. Setup Device and Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = mobilenet_v2(pretrained=False)
model.classifier[1] = torch.nn.Linear(model.last_channel, len(CLASSES))

# Load your fine-tuned weights here (we will mock this to prevent crashing if you don't have the .pth file yet)
# model.load_state_dict(torch.load("../models/mobilenet_v2.pth", map_location=device))
model.eval()
model.to(device)

# 3. Image Transformation Pipeline
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def predict_disease(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = transform(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = model(tensor)
            _, predicted = torch.max(outputs, 1)
            
        return CLASSES[predicted.item()]
    except Exception as e:
        print(f"Error processing image: {e}")
        return "Unknown Condition"