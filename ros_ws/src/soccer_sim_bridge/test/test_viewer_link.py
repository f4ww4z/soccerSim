import numpy as np
import pytest

from soccer_sim_bridge.viewer_link import TEXT_BYTES, _State

pytestmark = pytest.mark.ros


def _pair(tmp_path, nq=7, n_sliders=3):
    path = str(tmp_path / "state.bin")
    return _State(path, nq, n_sliders, create=True), _State(path, nq, n_sliders, create=False)


def test_pose_goes_sim_to_viewer(tmp_path):
    sim, viewer = _pair(tmp_path)
    sim.qpos[:] = np.arange(7)
    assert viewer.qpos.tolist() == list(range(7))


def test_sliders_go_viewer_to_sim(tmp_path):
    sim, viewer = _pair(tmp_path)
    viewer.sliders[:] = [1.0, 2.0, 3.0]
    assert sim.sliders.tolist() == [1.0, 2.0, 3.0]
    assert sim.qpos.tolist() == [0.0] * 7  # the two regions don't overlap


def test_overlay_text_round_trips_and_shrinks(tmp_path):
    sim, viewer = _pair(tmp_path)
    sim.set_text("brain decision\nball speed", "retreat\n3.2 m/s")
    assert viewer.get_text() == ("brain decision\nball speed", "retreat\n3.2 m/s")
    sim.set_text("a", "b")
    assert viewer.get_text() == ("a", "b")


def test_overlay_text_is_truncated_not_overflowed(tmp_path):
    sim, viewer = _pair(tmp_path)
    sim.set_text("x" * (2 * TEXT_BYTES), "y")
    left, right = viewer.get_text()
    assert len(left) == TEXT_BYTES and right == ""
    assert sim.sliders.tolist() == [0.0] * 3  # text never spills into the numeric regions
