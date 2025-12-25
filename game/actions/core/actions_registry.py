from collections import defaultdict

# Global tool storage (simple by design)
TOOLS = {}
TOOLS_BY_TAG = defaultdict(list)


def register_tool_metadata(metadata: dict):
    name = metadata["tool_name"]

    if name in TOOLS:
        raise ValueError(f"Tool '{name}' already registered")

    if not metadata["tags"]:
        raise ValueError(f"Tool '{name}' must have at least one tag")

    TOOLS[name] = metadata

    for tag in metadata["tags"]:
        TOOLS_BY_TAG[tag].append(name)


def get_tools_by_tags(tags=None):
    if not tags:
        return dict(TOOLS)

    allowed = set()
    for tag in tags:
        allowed.update(TOOLS_BY_TAG.get(tag, []))

    return {name: TOOLS[name] for name in allowed}
