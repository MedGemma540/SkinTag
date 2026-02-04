# Mobile App Testing & Update Guide

## Overview

The mobile apps (iOS SwiftUI and Flutter) need to be updated to match the new clinical triage system from the web app, then tested on physical devices.

---

## Current Status

| Component | iOS | Flutter | Web (Reference) |
|-----------|-----|---------|-----------------|
| Triage tiers | 3 (low/moderate/high) | 3 (low/moderate/high) | **4 (urgent/priority/routine/monitor)** |
| Thresholds | 0.3/0.7 | 0.3/0.7 | **0.15 (clinical)** |
| Condition display | No | No | **Yes, with tooltips** |
| Clinical guidance | No | No | **Yes** |
| Treatment callout | No | No | **Yes** |

---

## Updates Required

### 1. Triage System (Both Platforms)

**Current 3-tier:**
```
low (< 30%) → moderate (30-70%) → high (> 70%)
```

**New 4-tier clinical:**
```
monitor (< 15%) → routine (15-30%) → priority (30-60%) → urgent (> 60%)
```

### 2. Files to Update

#### iOS (Swift)
- `mobile/ios/SkinTag/SkinTag/Models/TriageResult.swift` - Add 4-tier enum
- `mobile/ios/SkinTag/SkinTag/Theme/Colors.swift` - Add routine blue color
- `mobile/ios/SkinTag/SkinTag/Views/ResultsView.swift` - Update UI

#### Flutter (Dart)
- `mobile/flutter/skin_tag/lib/models/triage_result.dart` - Add 4-tier enum
- `mobile/flutter/skin_tag/lib/theme/app_theme.dart` - Add routine blue
- `mobile/flutter/skin_tag/lib/screens/results_screen.dart` - Update UI

### 3. New Color Scheme

| Tier | Color | Hex |
|------|-------|-----|
| URGENT | Red | #dc2626 |
| PRIORITY | Orange | #ea580c |
| ROUTINE | Blue | #1a56db |
| MONITOR | Green | #16a34a |

### 4. Clinical Guidance Tooltips

Add condition guidance dictionary matching web app:
- Melanoma → URGENT
- SCC → URGENT
- BCC → PRIORITY
- Actinic Keratosis → PRIORITY
- Non-Neoplastic → ROUTINE
- Benign lesions → MONITOR

---

## Testing Checklist

### Prerequisites

#### iOS
- [ ] macOS with Xcode 15+
- [ ] iOS 15+ device or simulator
- [ ] Apple Developer account (for device testing)
- [ ] Core ML model converted from ONNX (see below)

#### Flutter
- [ ] Flutter SDK installed (3.0+)
- [ ] Android Studio or VS Code with Flutter extension
- [ ] Android device/emulator or iOS device/simulator
- [ ] TFLite model converted from ONNX (see below)

### Model Conversion

#### For iOS (Core ML)
```bash
# On macOS only
pip install coremltools

# Convert ONNX to Core ML
python -c "
import coremltools as ct
import onnx

# Load ONNX
onnx_model = onnx.load('models/mobilenet_distilled/exports/model.onnx')

# Convert
mlmodel = ct.converters.onnx.convert(
    model=onnx_model,
    minimum_deployment_target=ct.target.iOS15,
)

# Save
mlmodel.save('mobile/ios/SkinTag/SkinTag/SkinTagModel.mlpackage')
"
```

#### For Android (TFLite)
```bash
pip install tensorflow onnx-tf

python -c "
import onnx
from onnx_tf.backend import prepare
import tensorflow as tf

# ONNX → TF SavedModel
onnx_model = onnx.load('models/mobilenet_distilled/exports/model.onnx')
tf_rep = prepare(onnx_model)
tf_rep.export_graph('models/tf_savedmodel')

# TF → TFLite
converter = tf.lite.TFLiteConverter.from_saved_model('models/tf_savedmodel')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open('mobile/flutter/skin_tag/assets/model.tflite', 'wb') as f:
    f.write(tflite_model)
"
```

### Build & Run

#### iOS
```bash
cd mobile/ios/SkinTag

# Open in Xcode
open SkinTag.xcodeproj

# Or build from command line
xcodebuild -scheme SkinTag -destination 'platform=iOS Simulator,name=iPhone 15'
```

#### Flutter
```bash
cd mobile/flutter/skin_tag

# Get dependencies
flutter pub get

# Run on connected device
flutter run

# Build APK
flutter build apk --release

# Build iOS (on macOS)
flutter build ios --release
```

### Functional Tests

#### Camera & Upload
- [ ] Camera permission request works
- [ ] Camera preview displays correctly
- [ ] Photo capture works
- [ ] Gallery upload works (if implemented)
- [ ] Image preview shows before analysis

#### Analysis
- [ ] Loading indicator shows during inference
- [ ] Model inference completes (< 1 second)
- [ ] Results display correctly
- [ ] Risk score percentage accurate
- [ ] Triage tier determined correctly

#### Clinical Triage (After Update)
- [ ] URGENT tier shows at > 60% malignancy
- [ ] PRIORITY tier shows at 30-60%
- [ ] ROUTINE tier shows at 15-30%
- [ ] MONITOR tier shows at < 15%
- [ ] Correct colors for each tier
- [ ] Clinical guidance text is correct
- [ ] Timeframe displayed (e.g., "Within 2 weeks")

#### UI/UX
- [ ] Matches web app design language
- [ ] Responsive on different screen sizes
- [ ] Dark mode supported (if applicable)
- [ ] Disclaimer visible and readable
- [ ] "Find a Dermatologist" button works

### Performance Tests

- [ ] Cold start < 3 seconds
- [ ] Inference time < 500ms on modern device
- [ ] Memory usage < 200MB
- [ ] Battery impact acceptable
- [ ] Works offline (after model loaded)

### Edge Cases

- [ ] Handles camera denial gracefully
- [ ] Handles blurry images
- [ ] Handles non-skin images (general error)
- [ ] Works in low light (warns user)
- [ ] Portrait and landscape orientations

---

## Quick Commands

### Check Flutter setup
```bash
flutter doctor
```

### Run Flutter tests
```bash
cd mobile/flutter/skin_tag
flutter test
```

### Check iOS build
```bash
cd mobile/ios/SkinTag
xcodebuild -list
```

### Verify ONNX models exist
```bash
ls -la models/mobilenet_distilled/exports/model.onnx
ls -la models/efficientnet_distilled/exports/model.onnx
```

---

## Known Issues

1. **Core ML conversion requires macOS** - Cannot convert on Windows/Linux
2. **TFLite conversion may fail on Python 3.14** - Use Python 3.11
3. **ONNX Runtime not available for Python 3.14** - Verification skipped

---

## Next Steps After Testing

1. Update both apps with 4-tier clinical system
2. Add condition display with tooltips
3. Test on physical devices across screen sizes
4. Submit to App Store / Play Store (if applicable)
5. Create TestFlight / internal testing builds
