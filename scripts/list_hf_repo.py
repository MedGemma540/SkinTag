"""List files in HuggingFace repo."""
from huggingface_hub import list_repo_tree, list_repo_refs
repo = "skintaglabs/siglip-skin-lesion-classifier"

print("=== BRANCHES/TAGS ===")
refs = list_repo_refs(repo, repo_type="model")
for b in refs.branches:
    print(f"  branch: {b.name} ({b.ref})")
for t in refs.tags:
    print(f"  tag: {t.name} ({t.ref})")

print("\n=== FILES (main) ===")
files = list(list_repo_tree(repo, repo_type="model", recursive=True))
for f in files:
    size = getattr(f, "size", None)
    if size:
        if size > 1_000_000:
            print(f"  {size/1_000_000:>10.1f} MB  {f.path}")
        else:
            print(f"  {size/1_000:>10.1f} KB  {f.path}")
    else:
        print(f"  [dir]          {f.path}")
