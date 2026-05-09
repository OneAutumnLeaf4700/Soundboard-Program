from unittest.mock import MagicMock, patch

import pytest

from managers.sound_manager import SoundManager


@pytest.fixture
def manager(tmp_path):
    """SoundManager backed by a tmp_path JSON file with AudioPlayer fully mocked."""
    with patch("managers.sound_manager.AudioPlayer") as MockPlayer:
        instance = MockPlayer.return_value
        # The real AudioPlayer is a QObject — give the mock the signal
        # connect interface SoundManager wires to.
        instance.playback_started = MagicMock()
        instance.playback_stopped = MagicMock()
        instance.playback_error = MagicMock()
        # Methods used by play_sound
        instance.load_sound.return_value = True
        instance.play_sound.return_value = True
        instance.get_duration.return_value = 1.5
        instance.format_duration.return_value = "0:01"

        m = SoundManager(data_file=str(tmp_path / "sounds.json"))
        # Expose the underlying mock so tests can configure / assert on it
        m._mock_player = instance
        yield m


def _sample(title="Sound A", file_path="/tmp/a.mp3"):
    return {"title": title, "category": 1, "file_path": file_path, "favorite": False}


class TestSoundCRUD:
    def test_add_sound_emits_signal(self, manager):
        emitted = []
        manager.sound_added.connect(lambda sid, data: emitted.append((sid, data)))
        manager.add_sound("sid1", _sample())
        assert emitted == [("sid1", _sample())]

    def test_get_sound_after_add(self, manager):
        manager.add_sound("sid1", _sample("My sound"))
        got = manager.get_sound("sid1")
        assert got["title"] == "My sound"

    def test_get_all_sounds_returns_dict(self, manager):
        manager.add_sound("sid1", _sample("A"))
        manager.add_sound("sid2", _sample("B"))
        all_sounds = manager.get_all_sounds()
        assert set(all_sounds.keys()) == {"sid1", "sid2"}

    def test_remove_sound_emits_signal(self, manager):
        manager.add_sound("sid1", _sample())
        emitted = []
        manager.sound_removed.connect(emitted.append)
        assert manager.remove_sound("sid1") is True
        assert emitted == ["sid1"]

    def test_remove_sound_returns_false_for_unknown(self, manager):
        assert manager.remove_sound("nope") is False


class TestFavorites:
    def test_add_to_favorites_emits_signals(self, manager):
        manager.add_sound("sid1", _sample())
        added = []
        updated = []
        manager.favorite_added.connect(added.append)
        manager.sound_updated.connect(lambda sid, data: updated.append(sid))
        assert manager.add_to_favorites("sid1") is True
        assert added == ["sid1"]
        assert updated == ["sid1"]

    def test_add_to_favorites_unknown_returns_false(self, manager):
        assert manager.add_to_favorites("not-added") is False

    def test_remove_from_favorites_emits_signals(self, manager):
        manager.add_sound("sid1", _sample())
        manager.add_to_favorites("sid1")
        removed = []
        manager.favorite_removed.connect(removed.append)
        assert manager.remove_from_favorites("sid1") is True
        assert removed == ["sid1"]

    def test_toggle_favorite_returns_new_state(self, manager):
        manager.add_sound("sid1", _sample())
        assert manager.toggle_favorite("sid1") is True
        assert manager.toggle_favorite("sid1") is False

    def test_is_favorite(self, manager):
        manager.add_sound("sid1", _sample())
        assert manager.is_favorite("sid1") is False
        manager.add_to_favorites("sid1")
        assert manager.is_favorite("sid1") is True

    def test_get_favorites_returns_list_of_dicts(self, manager):
        manager.add_sound("sid1", _sample("Fav A"))
        manager.add_to_favorites("sid1")
        favs = manager.get_favorites()
        assert len(favs) == 1
        assert favs[0]["title"] == "Fav A"
        assert favs[0]["id"] == "sid1"


class TestPlay:
    def test_play_sound_returns_false_for_unknown(self, manager):
        assert manager.play_sound("nope") is False

    def test_play_sound_uses_audio_player_when_file_exists(self, manager, tmp_path):
        existing = tmp_path / "a.mp3"
        existing.write_bytes(b"\x00")
        manager.add_sound("sid1", _sample(file_path=str(existing)))
        manager._mock_player.play_sound.return_value = True

        assert manager.play_sound("sid1") is True
        manager._mock_player.play_sound.assert_called_with("sid1")

    def test_play_sound_loads_then_plays_if_first_play_fails(self, manager, tmp_path):
        existing = tmp_path / "a.mp3"
        existing.write_bytes(b"\x00")
        manager.add_sound("sid1", _sample(file_path=str(existing)))
        # First play returns False, so it loads then plays again
        manager._mock_player.play_sound.side_effect = [False, True]
        manager._mock_player.load_sound.return_value = True

        assert manager.play_sound("sid1") is True
        manager._mock_player.load_sound.assert_called_once_with("sid1", str(existing))
        assert manager._mock_player.play_sound.call_count == 2

    def test_play_sound_emits_played_for_sample_without_file(self, manager):
        # Sound metadata exists but file_path doesn't point to a real file
        manager.add_sound("sid1", _sample(file_path="/no/such/path.mp3"))
        played = []
        manager.sound_played.connect(played.append)
        assert manager.play_sound("sid1") is True
        assert played == ["sid1"]
        assert manager.current_playing == "sid1"

    def test_stop_sound_clears_current(self, manager):
        manager.current_playing = "sid1"
        manager.stop_sound()
        manager._mock_player.stop_sound.assert_called_once()
        assert manager.current_playing is None
