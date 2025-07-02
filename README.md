# Floor Plan Object Detection and Inpainting

This project transforms 2D floor plans into detailed, photorealistic 3D renderings using deep learning. It combines **object detection** and **image inpainting** to enable users to visualize floor plans and customize them based on personal design preferences.

---

## 🚀 Project Overview

People often struggle to interpret 2D floor plans and visualize real-world spaces. This project:
- Detects and labels objects (doors, windows, furniture) in floor plan images using YOLOv11.
- Generates 3D scene reconstructions from 2D layouts.
- Enables text-guided customization (e.g., changing wallpaper, furniture) using **Stable Diffusion inpainting**.

---

## 📂 Project Structure

- `in_painting/`: Stable Diffusion inpainting pipelines for text-guided floor plan customization.
- `object_detection/`: YOLO-based object detection models for identifying floor plan elements.
- `segmentation/`: Preprocessing and floor plan segmentation scripts, including FastAPI orchestration.

---

## 🔍 Key Components

### 🖼️ Object Detection
- **Model:** YOLOv11
- **Performance:**
  - mAP@50: **0.74**
  - Precision: **0.769**
- **Benchmark:** Significantly outperforms Faster R-CNN.

### 🏠 Floor Plan to 3D Render
- Extracts wall and object placements from SVG files.
- Manual lighting adjustments to enhance realism.
- Supports inpainting customization via text prompts.

### 🎨 Inpainting with Stable Diffusion
- Users can input prompts like: `"glossy bright red wallpaper and a blue bed"`.
- **Key Hyperparameters:**
  - **Strength:** Controls how much of the original image is altered.
  - **Guidance:** Controls how closely the model follows the prompt.
  - **Inference Steps:** Typically set to 120 for high detail.

### 📊 Evaluation Metrics
- **PSNR:** Pixel-level fidelity
- **SSIM:** Structural similarity
- **LPIPS:** Perceptual similarity
- **CLIP Similarity:** Semantic alignment

---

## ⚙️ System Architecture

- Modular Python files orchestrated via **FastAPI**.
- End-to-end deployment using **Docker**.
- User interface built with **Streamlit**.
- Cloud-ready deployment (AWS, GCP supported).

---

## 🔁 Model Maintenance

| Stage                | Metric                  | Monitoring Frequency |
|----------------------|-------------------------|----------------------|
| Object Detection     | Accuracy, IoU           | Weekly               |
| 3D Layout Generation | Layout quality          | Visual inspection    |
| Inpainting           | User satisfaction score | Weekly               |

- If significant performance drops occur, or if new floor plan styles emerge, the system will trigger **parameter updates and retraining.**

---

## 🛠️ Technologies Used

- YOLOv11
- Stable Diffusion (Inpainting & Img2Img)
- FastAPI
- Streamlit
- Docker
- AWS / GCP

---

## 👥 Contributors

- Ankit Agrawal
- Brandt Buchda
- Halleluya Mengesha
- Hira Stanley
- Ultra Partihuttakorn
