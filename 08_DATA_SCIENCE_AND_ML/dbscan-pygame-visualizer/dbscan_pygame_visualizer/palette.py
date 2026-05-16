CLUSTER_COLORS = [
    (90, 168, 255),
    (124, 255, 178),
    (255, 184, 107),
    (183, 148, 255),
    (255, 77, 95),
    (120, 225, 255),
    (255, 209, 102),
    (98, 240, 190),
    (240, 140, 255),
    (255, 150, 120),
]

NOISE_COLOR = (98, 110, 128)
CORE_OUTLINE = (255, 255, 255)
BORDER_OUTLINE = (20, 30, 48)
BACKGROUND = (8, 13, 22)
PANEL = (17, 24, 39)
TEXT = (237, 243, 255)
MUTED = (154, 168, 189)
ACCENT = (90, 168, 255)


def color_for_label(label: int | None) -> tuple[int, int, int]:
    if label is None or label < 0:
        return NOISE_COLOR
    return CLUSTER_COLORS[label % len(CLUSTER_COLORS)]
