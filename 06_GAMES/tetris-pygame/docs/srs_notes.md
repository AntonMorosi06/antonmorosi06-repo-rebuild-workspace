# SRS notes

This reconstructed baseline includes a small Super Rotation System-inspired wall kick approximation.

When the player rotates a piece, the game tries the target rotation in the current position. If that collides, it tries a small set of horizontal and upward offsets.

The current kick table is intentionally simple:

same position

one cell left

one cell right

two cells left

two cells right

one cell up

This is not a complete official SRS implementation. A future version can add separate kick tables for JLSTZ pieces, I piece and O piece, plus better spawn behavior and T-spin detection.
