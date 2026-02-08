#!/usr/bin/env python3
"""Script to add AI attribution headers to files.

Usage:
    python add_attributions.py --dry-run  # Preview changes
    python add_attributions.py            # Apply changes
"""

import sys
from pathlib import Path

# Standard attribution for Python files
PYTHON_ATTRIBUTION = """
Development notes:
- Developed with AI assistance (Claude/Anthropic) for implementation and refinement
- Code simplified using Anthropic's code-simplifier agent (https://www.anthropic.com/claude-code)
- Core architecture and domain logic by SkinTag team
"""

# Standard attribution for TypeScript files
TYPESCRIPT_ATTRIBUTION = """
 * Development notes:
 * - Developed with AI assistance (Claude/Anthropic)
 * - Core UX design and integration by SkinTag team
"""

# Files to update (high priority)
PYTHON_FILES = [
    "src/model/baseline.py",
    "src/model/classifier.py",
    "src/model/deep_classifier.py",
    "src/model/embeddings.py",
    "src/model/triage.py",
    "src/evaluation/metrics.py",
    "src/data/loader.py",
    "src/data/sampler.py",
    "src/data/taxonomy.py",
    "scripts/train.py",
    "scripts/evaluate.py",
    "scripts/train_all_models.py",
    "run_pipeline.py",
    "app/main.py",
]

TYPESCRIPT_FILES = [
    "webapp-react/src/components/camera/WebcamCapture.tsx",
    "webapp-react/src/components/upload/ImageCropper.tsx",
    "webapp-react/src/App.tsx",
]

# Special cases with custom attribution
SPECIAL_CASES = {
    "src/data/augmentations.py": """
Development notes:
- Developed with AI assistance (Claude/Anthropic)
- Albumentations pipeline structure following: https://albumentations.ai/docs/
- Field condition augmentation strategy from domain expertise
- Code simplified using Anthropic's code-simplifier agent
""",
    "webapp-react/src/components/camera/WebcamCapture.tsx": """
 * Development notes:
 * - Developed with AI assistance (Claude/Anthropic)
 * - MediaPipe hand detection: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
 * - getUserMedia API usage following MDN Web API documentation
""",
    "webapp-react/src/components/upload/ImageCropper.tsx": """
 * Development notes:
 * - Developed with AI assistance (Claude/Anthropic)
 * - Uses react-easy-crop: https://github.com/ValentinH/react-easy-crop
 * - Canvas cropping logic from react-easy-crop examples
""",
}


def add_python_attribution(file_path: Path, attribution: str) -> tuple[str, bool]:
    """Add attribution to Python file after docstring."""
    content = file_path.read_text()

    # Check if already has attribution
    if "Development notes:" in content:
        return content, False

    # Find docstring end
    lines = content.split('\n')
    in_docstring = False
    docstring_end_idx = -1
    quote_style = None

    for i, line in enumerate(lines):
        if not in_docstring:
            if '"""' in line or "'''" in line:
                quote_style = '"""' if '"""' in line else "'''"
                in_docstring = True
                # Check if single-line docstring
                if line.count(quote_style) >= 2:
                    docstring_end_idx = i
                    break
        else:
            if quote_style in line:
                docstring_end_idx = i
                break

    if docstring_end_idx == -1:
        # No docstring found, add at top after shebang/imports
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#!') and not line.startswith('#'):
                docstring_end_idx = i - 1
                break

    # Insert attribution after docstring
    if docstring_end_idx >= 0:
        lines.insert(docstring_end_idx + 1, attribution)
        return '\n'.join(lines), True

    return content, False


def add_typescript_attribution(file_path: Path, attribution: str) -> tuple[str, bool]:
    """Add attribution to TypeScript file after opening comment."""
    content = file_path.read_text()

    # Check if already has attribution
    if "Development notes:" in content:
        return content, False

    lines = content.split('\n')

    # Find first /** comment block
    in_comment = False
    comment_end_idx = -1

    for i, line in enumerate(lines):
        if '/**' in line:
            in_comment = True
        if in_comment and '*/' in line:
            comment_end_idx = i
            break

    # If found, insert before closing */
    if comment_end_idx >= 0:
        lines[comment_end_idx] = attribution + '\n */'
        return '\n'.join(lines), True
    else:
        # No comment found, add at top
        new_content = f"/**\n * [Component/Module description]\n{attribution}\n */\n\n" + content
        return new_content, True


def main():
    dry_run = '--dry-run' in sys.argv
    project_root = Path(__file__).parent

    print("🏷️  Adding AI attribution headers to files...")
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'APPLYING CHANGES'}\n")

    updated = []
    skipped = []

    # Process Python files
    for file_rel in PYTHON_FILES:
        file_path = project_root / file_rel
        if not file_path.exists():
            print(f"⚠️  Not found: {file_rel}")
            continue

        attribution = SPECIAL_CASES.get(file_rel, PYTHON_ATTRIBUTION)
        new_content, changed = add_python_attribution(file_path, attribution)

        if changed:
            if not dry_run:
                file_path.write_text(new_content)
            updated.append(file_rel)
            print(f"✅ Updated: {file_rel}")
        else:
            skipped.append(file_rel)
            print(f"⏭️  Skipped (already has attribution): {file_rel}")

    # Add augmentations.py separately
    aug_file = project_root / "src/data/augmentations.py"
    if aug_file.exists():
        attribution = SPECIAL_CASES["src/data/augmentations.py"]
        new_content, changed = add_python_attribution(aug_file, attribution)
        if changed:
            if not dry_run:
                aug_file.write_text(new_content)
            updated.append("src/data/augmentations.py")
            print(f"✅ Updated: src/data/augmentations.py")

    # Process TypeScript files
    for file_rel in TYPESCRIPT_FILES:
        file_path = project_root / file_rel
        if not file_path.exists():
            print(f"⚠️  Not found: {file_rel}")
            continue

        attribution = SPECIAL_CASES.get(file_rel, TYPESCRIPT_ATTRIBUTION)
        new_content, changed = add_typescript_attribution(file_path, attribution)

        if changed:
            if not dry_run:
                file_path.write_text(new_content)
            updated.append(file_rel)
            print(f"✅ Updated: {file_rel}")
        else:
            skipped.append(file_rel)
            print(f"⏭️  Skipped (already has attribution): {file_rel}")

    print(f"\n📊 Summary:")
    print(f"   Updated: {len(updated)} files")
    print(f"   Skipped: {len(skipped)} files")

    if dry_run:
        print("\n💡 Run without --dry-run to apply changes")
    else:
        print("\n✨ Attribution headers added successfully!")
        print("   Review changes with: git diff")


if __name__ == "__main__":
    main()
