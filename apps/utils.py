import torch
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image, UnidentifiedImageError
import json
import torch
import numpy as np
import cv2

# ─── CONFIG ──────────────────────────────────────────────────────
MODEL_PATH = "models/waste_model.pth"
CLASS_PATH = "models/classes.json"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ─── MODEL LOADING ───────────────────────────────────────────────
def load_model():
    with open(CLASS_PATH, "r") as f:
        classes = json.load(f)
    model = models.efficientnet_b0(weights=None)
    num_features = model.classifier[1].in_features
    model.classifier[1] = torch.nn.Linear(num_features, len(classes))
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()
    return model, classes

# ─── PREPROCESSING ───────────────────────────────────────────────
def preprocess_image(image: Image.Image) -> torch.Tensor:
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

# ─── PREDICTION ──────────────────────────────────────────────────
def predict(model, class_names: list, image: Image.Image):
    """
    Returns:
        top_class  (str)   — predicted class name
        top_conf   (float) — confidence of top prediction (0–1)
        all_probs  (dict)  — {class_name: probability} for all classes
    """
    img_tensor = preprocess_image(image).to(device)
    with torch.no_grad():
        outputs = model(img_tensor)
        probs   = F.softmax(outputs, dim=1)[0]

    all_probs  = {class_names[i]: probs[i].item() for i in range(len(class_names))}
    top_idx    = probs.argmax().item()
    top_class  = class_names[top_idx]
    top_conf   = probs[top_idx].item()

    return top_class, top_conf, all_probs

# ─── DISPOSAL GUIDANCE ───────────────────────────────────────────
def get_disposal(class_name: str):
    """Returns (label, icon, css_class)"""
    if class_name in ["cardboard", "paper", "plastic"]:
        return "Blue Bin",         "🔵", "disposal-blue"
    elif class_name in ["glass", "metal"]:
        return "Recycling Centre", "♻️",  "disposal-green"
    else:
        return "General Waste",    "🗑️",  "disposal-yellow"

# ─── SAFE IMAGE OPEN ─────────────────────────────────────────────
def safe_open_image(file) -> tuple:
    """
    Returns (image, error_message).
    image is None if opening failed.
    """
    try:
        img = Image.open(file).convert("RGB")
        return img, None
    except UnidentifiedImageError:
        return None, f"'{file.name}' is not a recognised image format."
    except Exception as e:
        return None, f"Could not open '{file.name}': {e}"

# ─── CONFIDENCE LEVEL ────────────────────────────────────────────
LOW_CONF_THRESHOLD = 0.60

def confidence_level(conf: float) -> str:
    """Returns 'high', 'medium', or 'low'."""
    if conf >= 0.85:
        return "high"
    elif conf >= LOW_CONF_THRESHOLD:
        return "medium"
    else:
        return "low"
    

def generate_gradcam(model, image, class_idx):
    model.eval()

    gradients = []
    activations = []

    def backward_hook(module, grad_in, grad_out):
        gradients.append(grad_out[0])

    def forward_hook(module, inp, out):
        activations.append(out)

    # 👇 EfficientNet last conv layer
    target_layer = model.features[-1]

    fh = target_layer.register_forward_hook(forward_hook)
    bh = target_layer.register_full_backward_hook(backward_hook)

    # preprocess
    img_tensor = preprocess_image(image).to(device)

    output = model(img_tensor)
    model.zero_grad()

    score = output[0, class_idx]
    score.backward()

    grads = gradients[0]
    acts = activations[0]

    weights = torch.mean(grads, dim=(2, 3), keepdim=True)
    cam = torch.sum(weights * acts, dim=1).squeeze()

    cam = torch.relu(cam)
    cam = cam.detach().cpu().numpy()

    cam = cv2.resize(cam, (224, 224))
    cam = (cam - cam.min()) / (cam.max() + 1e-8)

    fh.remove()
    bh.remove()

    return cam


# Add this function to utils.py (or modify existing overlay_gradcam)
def overlay_gradcam(image, cam, alpha=0.4):
    import numpy as np
    import cv2

    img = np.array(image.resize((224, 224)))

    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    overlay = heatmap * alpha + img * (1 - alpha)
    overlay = np.clip(overlay, 0, 255).astype(np.uint8)

    return overlay
