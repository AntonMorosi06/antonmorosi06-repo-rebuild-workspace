BACKGROUND = (8, 13, 22)
PANEL = (17, 24, 39)
TEXT = (237, 243, 255)
MUTED = (154, 168, 189)
GRID = (28, 38, 56)
EDGE = (70, 92, 130)
ACCENT = (90, 168, 255)

CLUSTER_COLORS = [
    (90, 168, 255),
    (124, 255, 178),
    (255, 184, 107),
    (183, 148, 255),
    (255, 77, 95),
    (120, 225, 255),
    (255, 209, 102),
    (98, 240, 190),
]


def color_for_label(label: int) -> tuple[int, int, int]:
    return CLUSTER_COLORS[label % len(CLUSTER_COLORS)]
