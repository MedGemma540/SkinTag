# SkinTag Mobile Deployment Report

**Generated:** 2026-02-04
**Branch:** `feature/mobile-app`
**Status:** Phase 2B Complete

---

## Executive Summary

Two lightweight mobile models were successfully trained via knowledge distillation from the fine-tuned SigLIP teacher model. Both models achieve performance comparable to the teacher while being **50-70x smaller** and suitable for on-device inference.

| Model | Accuracy | F1 Macro | F1 Malignant | Size | Reduction |
|-------|----------|----------|--------------|------|-----------|
| **SigLIP (Teacher)** | 92.30% | 0.887 | 0.824 | ~3.4 GB | - |
| **MobileNetV3-Large** | 92.44% | 0.884 | 0.816 | 12.5 MB | **272x** |
| **EfficientNet-B0** | 92.65% | 0.887 | 0.820 | 16.8 MB | **202x** |

---

## 1. Dataset Summary

- **Total samples:** 47,277 images from 5 datasets
- **Test samples:** 9,456 (20% holdout)
- **Class distribution:** Benign=37,397, Malignant=9,880
- **Datasets:** HAM10000, DDI, Fitzpatrick17k, PAD-UFES, BCN20000

---

## 2. Model Comparison

### Performance Metrics

| Model | Parameters | Size (MB) | Accuracy | F1 Macro | F1 Malignant | AUC |
|-------|------------|-----------|----------|----------|--------------|-----|
| SigLIP (Teacher) | 878M | 3,351 | 92.30% | 0.8874 | 0.8242 | ~0.96 |
| MobileNetV3-Large | 3.2M | 12.5 | 92.44% | 0.8841 | 0.8158 | 0.9592 |
| EfficientNet-B0 | 4.3M | 16.8 | 92.65% | 0.8871 | 0.8203 | 0.9597 |

### Key Findings

1. **EfficientNet-B0 is the top performer** with the highest accuracy (92.65%) and F1 scores
2. **MobileNetV3-Large offers the best size/performance trade-off** at only 12.5 MB
3. Both distilled models **match or exceed teacher performance** on the test set
4. **AUC scores >0.95** indicate excellent discrimination between benign and malignant

### Accuracy Gap Analysis

| Student Model | Teacher F1 | Student F1 | Gap |
|---------------|------------|------------|-----|
| MobileNetV3-Large | 0.8874 | 0.8841 | -0.003 (0.4%) |
| EfficientNet-B0 | 0.8874 | 0.8871 | -0.000 (0.0%) |

**Result:** Knowledge distillation was highly successful - both students achieved within 0.4% of teacher performance.

---

## 3. Model Exports

### ONNX Format (Universal)

| Model | Export Path | Size |
|-------|-------------|------|
| MobileNetV3-Large | `models/mobilenet_distilled/exports/model.onnx` | 12.3 MB |
| EfficientNet-B0 | `models/efficientnet_distilled/exports/model.onnx` | 16.6 MB |

### iOS (Core ML)

- **Status:** ONNX exported, ready for Core ML conversion on macOS
- **Recommended model:** MobileNetV3-Large for size, EfficientNet-B0 for accuracy
- **Export format:** Core ML (.mlmodel) with FP16 quantization
- **Expected size:** ~6-10 MB after FP16 quantization
- **Target inference:** <50ms on iPhone 12+

### Android (TFLite)

- **Status:** ONNX exported, ready for TFLite conversion
- **Recommended model:** MobileNetV3-Large for size, EfficientNet-B0 for accuracy
- **Export format:** TFLite with FP16 or INT8 quantization
- **Expected size:** ~5-15 MB after quantization
- **Target inference:** <100ms on mid-range devices

---

## 4. Mobile App Infrastructure

### iOS App (SwiftUI)

Location: `mobile/ios/SkinTag/`

**Features:**
- Camera capture with AVFoundation
- Core ML inference service
- Medical disclaimer views
- Results display with triage tiers
- Standardized color theme matching web app

### Flutter Cross-Platform App

Location: `mobile/flutter/skin_tag/`

**Features:**
- TFLite inference service
- Camera integration
- Disclaimer and results screens
- Matching color theme

---

## 5. Recommended Deployment Strategy

### For iOS (Primary)

1. Use **MobileNetV3-Large** for optimal size/battery trade-off
2. Export with FP16 quantization (~6 MB)
3. Target iOS 15+ for best Core ML support

### For Android

1. Use **EfficientNet-B0** for best accuracy
2. Export with FP16 quantization (~8 MB)
3. Target Android 8+ (API 26) for Neural Networks API support

### For Resource-Constrained Devices

1. Use **MobileNetV3-Large with INT8 quantization** (~3-4 MB)
2. May have slight accuracy reduction but fastest inference

---

## 6. Clinical Deployment Notes

### Target Use Cases

1. **Dermatology Clinic Triage:** Quick screening to prioritize patients
2. **Remote/Rural Healthcare:** Offline screening where specialists are unavailable
3. **Medical Education:** Training tool for students and technicians

### Important Limitations

- This is a **screening tool only**, not a diagnostic device
- All positive results should be verified by a qualified dermatologist
- Model performance may vary across skin types and lighting conditions
- Not FDA cleared or CE marked for clinical diagnosis

### Triage Tiers

| Risk Level | Probability Range | Recommended Action |
|------------|-------------------|-------------------|
| Low | 0-30% | Routine monitoring |
| Moderate | 30-60% | Schedule dermatology consult |
| High | 60-100% | Urgent dermatology referral |

---

## 7. Preprocessing Requirements

For both models, images must be preprocessed as follows:

```python
# Image preprocessing
1. Resize to 224x224 pixels
2. Convert to RGB (3 channels)
3. Normalize with ImageNet statistics:
   - mean = [0.485, 0.456, 0.406]
   - std = [0.229, 0.224, 0.225]
```

### iOS (Core ML)

```swift
let config = MLModelConfiguration()
config.computeUnits = .cpuAndNeuralEngine
```

### Android (TFLite)

```kotlin
val options = Interpreter.Options()
options.setNumThreads(4)
```

---

## 8. Files Generated

| File | Description |
|------|-------------|
| `models/mobilenet_distilled/mobilenet_v3_large.pt` | PyTorch model (12.5 MB) |
| `models/mobilenet_distilled/exports/model.onnx` | ONNX format (12.3 MB) |
| `models/mobilenet_distilled/config.json` | Model configuration |
| `models/mobilenet_distilled/training_history.json` | Training metrics |
| `models/efficientnet_distilled/efficientnet_b0.pt` | PyTorch model (16.8 MB) |
| `models/efficientnet_distilled/exports/model.onnx` | ONNX format (16.6 MB) |
| `models/efficientnet_distilled/config.json` | Model configuration |
| `mobile/ios/SkinTag/` | Complete iOS SwiftUI app |
| `mobile/flutter/skin_tag/` | Complete Flutter app |

---

## 9. Conclusion

Phase 2B mobile development is **complete**. Two high-performing mobile models have been trained and exported:

- **MobileNetV3-Large** (12.5 MB): Best for size-constrained deployments
- **EfficientNet-B0** (16.8 MB): Best for maximum accuracy

Both models achieve **>92% accuracy** and **>0.81 F1 malignant**, matching the teacher model performance while being suitable for on-device inference. The mobile app infrastructure (iOS and Flutter) is ready for integration with the exported models.

### Next Steps

1. Convert ONNX to Core ML on macOS machine
2. Convert ONNX to TFLite
3. Integrate models with iOS/Flutter apps
4. Test on physical devices
5. Gather user feedback
