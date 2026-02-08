# Code Attribution Templates

Use these templates at the top of files that used AI assistance or external code.

## Python Files

### Template 1: AI-Assisted Development (General)
```python
"""
[Original docstring description]

Development notes:
- Developed with AI assistance (Claude/Anthropic) for planning, implementation, and refinement
- Code simplified using Anthropic's code-simplifier agent
- Core architecture and domain logic by SkinTag team
"""
```

### Template 2: AI + External Libraries
```python
"""
[Original docstring description]

Development notes:
- Developed with AI assistance (Claude/Anthropic)
- Code simplified using Anthropic's code-simplifier agent
- Uses external libraries: [library names]
  - [Library]: https://github.com/...
- Core implementation by SkinTag team
"""
```

### Template 3: Adapted from External Source
```python
"""
[Original docstring description]

Development notes:
- Initial implementation adapted from: [URL or paper citation]
- Modified and extended with AI assistance (Claude/Anthropic)
- Code simplified using Anthropic's code-simplifier agent
"""
```

## TypeScript/React Files

### Template 1: AI-Assisted React Component
```typescript
/**
 * [Component description]
 *
 * Development notes:
 * - Developed with AI assistance (Claude/Anthropic)
 * - Uses external library: [library-name] (https://...)
 * - Core UX design by SkinTag team
 */
```

### Template 2: MediaPipe Integration
```typescript
/**
 * [Component description]
 *
 * Development notes:
 * - Developed with AI assistance (Claude/Anthropic)
 * - MediaPipe integration following: https://developers.google.com/mediapipe
 * - Hand detection logic adapted from MediaPipe documentation examples
 */
```

---

## Recommended Attribution by File Type

### For src/model/* files:
Use Template 1 (AI-Assisted Development)

### For src/data/augmentations.py:
```python
"""
Augmentation pipelines for robustness to imaging conditions.

Development notes:
- Developed with AI assistance (Claude/Anthropic)
- Albumentations pipeline structure following: https://albumentations.ai/docs/
- Field condition augmentation strategy from domain expertise and literature review
- Code simplified using Anthropic's code-simplifier agent
"""
```

### For webapp-react/src/components/camera/WebcamCapture.tsx:
```typescript
/**
 * Real-time webcam capture with MediaPipe hand detection
 *
 * Development notes:
 * - Developed with AI assistance (Claude/Anthropic)
 * - MediaPipe hand detection: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
 * - getUserMedia API usage following MDN documentation
 */
```

### For webapp-react/src/components/upload/ImageCropper.tsx:
```typescript
/**
 * Image cropper component for lesion focusing
 *
 * Development notes:
 * - Developed with AI assistance (Claude/Anthropic)
 * - Uses react-easy-crop: https://github.com/ValentinH/react-easy-crop
 * - Canvas cropping logic from react-easy-crop examples
 */
```

---

## Quick Reference: External Libraries to Credit

### Python:
- SigLIP base model: https://huggingface.co/google/siglip-so400m-patch14-384
- Albumentations: https://albumentations.ai/
- Transformers: https://huggingface.co/docs/transformers
- XGBoost: https://xgboost.readthedocs.io/

### TypeScript/React:
- react-easy-crop: https://github.com/ValentinH/react-easy-crop
- MediaPipe: https://developers.google.com/mediapipe
- Radix UI: https://www.radix-ui.com/
- Lucide icons: https://lucide.dev/

---

## Honest & Appropriate Attribution

Since you used AI extensively, this is an honest statement that satisfies the rubric:

```
Development notes:
- Developed collaboratively with AI assistance (Claude/Anthropic) for implementation,
  debugging, and code refinement
- Code simplified and optimized using Anthropic's code-simplifier agent
- Architecture, domain logic, and ML strategy designed by SkinTag team
- External libraries and frameworks credited in dependencies
```
