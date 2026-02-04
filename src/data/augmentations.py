"""Augmentation pipelines for robustness to imaging conditions.

Includes realistic field condition augmentations for smartphone-captured images,
as would be encountered when deployed by non-specialist technicians in the field.
"""

import albumentations as A
from albumentations.pytorch import ToTensorV2


def get_dermoscope_removal_pipeline(p: float = 0.5):
    """Placeholder for dermoscope artifact removal."""
    return A.Compose([])


def get_dermoscope_addition_pipeline(p: float = 0.5):
    """Placeholder for dermoscope artifact addition."""
    return A.Compose([])


def get_field_condition_augmentation(severity: str = "moderate"):
    """Augmentations simulating real-world smartphone capture conditions.

    Designed for deployment by non-specialist technicians in field settings.

    Includes:
    - Motion blur (shaky hands)
    - Focus blur (autofocus issues)
    - Low light noise
    - Overexposure/underexposure
    - Color cast (different lighting)
    - Compression artifacts (messaging apps)
    - Shadow from hand/phone

    Args:
        severity: "light", "moderate", or "heavy"

    Returns:
        Albumentations Compose pipeline
    """
    if severity == "light":
        blur_limit, noise_var, brightness = 3, 30, 0.2
    elif severity == "heavy":
        blur_limit, noise_var, brightness = 9, 80, 0.4
    else:  # moderate
        blur_limit, noise_var, brightness = 5, 50, 0.3

    return A.Compose([
        # Motion blur (shaky hands during capture)
        A.OneOf([
            A.MotionBlur(blur_limit=blur_limit, p=1.0),
            A.GaussianBlur(blur_limit=blur_limit, p=1.0),
            A.MedianBlur(blur_limit=blur_limit, p=1.0),
        ], p=0.3),

        # Focus issues (out-of-focus areas)
        A.OneOf([
            A.Defocus(radius=(1, 3), alias_blur=(0.1, 0.3), p=1.0),
            A.ZoomBlur(max_factor=1.05, p=1.0),
        ], p=0.2),

        # Lighting variations (indoor/outdoor, different bulbs)
        A.OneOf([
            A.RandomBrightnessContrast(
                brightness_limit=brightness,
                contrast_limit=brightness,
                p=1.0
            ),
            A.RandomGamma(gamma_limit=(60, 140), p=1.0),
            A.RandomToneCurve(scale=0.2, p=1.0),
        ], p=0.5),

        # Color cast (fluorescent lights, sunlight, etc.)
        A.OneOf([
            A.HueSaturationValue(
                hue_shift_limit=15,
                sat_shift_limit=20,
                val_shift_limit=15,
                p=1.0
            ),
            A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=1.0),
            A.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.15, hue=0.05, p=1.0),
        ], p=0.4),

        # Sensor noise (low light, older phones)
        A.OneOf([
            A.GaussNoise(var_limit=(10, noise_var), p=1.0),
            A.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.5), p=1.0),
            A.MultiplicativeNoise(multiplier=(0.9, 1.1), p=1.0),
        ], p=0.4),

        # Compression (WhatsApp, social media sharing)
        A.OneOf([
            A.ImageCompression(quality_lower=40, quality_upper=90, p=1.0),
            A.Downscale(scale_min=0.4, scale_max=0.8, p=1.0),
        ], p=0.3),

        # Shadow from hand/phone (partial occlusion)
        A.RandomShadow(
            shadow_roi=(0, 0.5, 1, 1),
            num_shadows_limit=(1, 2),
            shadow_dimension=5,
            p=0.15
        ),

        # Glare/specular highlights (flash, sunlight reflection)
        A.RandomSunFlare(
            flare_roi=(0, 0, 1, 0.5),
            angle_range=(0, 1),
            num_flare_circles_range=(1, 3),
            src_radius=100,
            p=0.1
        ),
    ])


def get_skin_tone_augmentation(p: float = 0.5):
    """Augmentation to improve robustness across Fitzpatrick skin types.

    Subtly varies skin tone characteristics to reduce bias toward
    lighter skin types that may be overrepresented in training data.
    """
    return A.Compose([
        A.HueSaturationValue(
            hue_shift_limit=8,
            sat_shift_limit=15,
            val_shift_limit=10,
            p=p
        ),
        A.RandomGamma(gamma_limit=(85, 115), p=p * 0.5),
    ])


def get_lighting_augmentation():
    """Simulate lighting and exposure variations (different exam rooms, cameras)."""
    return A.Compose([
        A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=0.7),
        A.RandomGamma(gamma_limit=(70, 130), p=0.5),
        A.CLAHE(clip_limit=4.0, p=0.3),
    ])


def get_noise_augmentation():
    """Simulate sensor noise (low-light capture, older cameras)."""
    return A.Compose([
        A.GaussNoise(var_limit=(10, 50), p=0.5),
        A.ISONoise(p=0.3),
    ])


def get_compression_augmentation():
    """Simulate compression artifacts (telemedicine, image uploads)."""
    return A.Compose([
        A.ImageCompression(quality_lower=50, quality_upper=95, p=0.5),
        A.Downscale(scale_min=0.5, scale_max=0.9, p=0.3),
    ])


def get_domain_bridging_augmentation(source_domain: str, p: float = 0.5):
    """Get domain-bridging augmentation based on source imaging domain.

    Randomly adds or removes dermoscope artifacts so the model cannot rely
    on imaging source as a classification signal.

    Args:
        source_domain: "dermoscopic", "clinical", or "smartphone"
        p: probability of applying the augmentation

    Returns:
        Albumentations Compose pipeline
    """
    if source_domain == "dermoscopic":
        # Remove dermoscope artifacts to look more like phone photos
        return get_dermoscope_removal_pipeline(p=p)
    elif source_domain in ("clinical", "smartphone"):
        # Add dermoscope artifacts to break the domain-pathology correlation
        return get_dermoscope_addition_pipeline(p=p)
    else:
        return A.Compose([])  # No-op for unknown domains


def get_training_transform(image_size: int = 448, domain: str = None):
    """Full training augmentation pipeline for robustness.

    Args:
        image_size: Target image size
        domain: If provided, includes domain-bridging augmentations
    """
    transforms = [
        A.Resize(image_size, image_size),
        # Geometric (orientation-invariant lesions)
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.Rotate(limit=30, p=0.5),
    ]

    # Domain bridging (applied before standard augmentations)
    if domain is not None:
        bridging = get_domain_bridging_augmentation(domain, p=0.4)
        transforms.append(bridging)

    transforms.extend([
        # Lighting variation
        A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=0.5),
        A.RandomGamma(gamma_limit=(80, 120), p=0.3),
        # Sensor noise
        A.GaussNoise(var_limit=(10, 50), p=0.3),
        # Compression artifacts
        A.ImageCompression(quality_lower=70, quality_upper=100, p=0.3),
        # Normalize for model
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

    return A.Compose(transforms)


def get_eval_transform(image_size: int = 448):
    """Evaluation transform (no augmentation)."""
    return A.Compose([
        A.Resize(image_size, image_size),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])
