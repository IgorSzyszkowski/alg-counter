import pytest

from alg_counter.__main__ import count_algorithms


@pytest.mark.parametrize(
    "scramble, count",
    [
        ("L2 U B2 R2 U B2 R2 D2 R2 U B2 U' F' R2 B2 R B D' L F D'", 11),
        ("R' F' B2 D R' F L' B' U R2 F2 U2 R2 U2 F' L2 F' B' L2 F U2", 10),
        ("D2 B2 L' F2 R2 D2 R F2 R' U2 F2 L' D B' L' D U' L' B2 F' U", 10),
        ("F D R D2 R B U F U B2 U' R2 B2 D F2 D' F2 L2 U' R2", 10),
        ("L2 U L2 F2 D2 L2 B2 D L2 B2 U B2 F D B R' D L R2 U' L B2", 13),
        ("L2 D' B2 U2 L2 R2 F2 U' L2 U' L2 R U' F R2 U' B L2 R D' R'", 11),
        ("D2 L' U2 F2 U' R2 D' R2 U' B2 L2 F2 R2 F R2 D' F R F' U2 F' Rw2 Uw'", 11),
        ("R' B' D' U2 R2 D' R2 B2 D' L2 D2 R2 B2 R2 L' U' L F2 U2 L2 B Fw Uw2", 10),
        ("B' L2 U F2 L2 R2 U' F2 R2 B2 F2 D2 B D2 L' D' F' R B2 L D' Fw", 12),
    ],
)
def test_count_algorithms(scramble: str, count: int):
    assert count == count_algorithms(scramble)
