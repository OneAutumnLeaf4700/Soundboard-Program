from unittest.mock import MagicMock, patch

import pytest

from managers.audio_player import AudioPlayer


@pytest.fixture
def player():
    return AudioPlayer()


class TestLoadSound:
    def test_returns_false_when_file_missing(self, player, tmp_path):
        missing = str(tmp_path / "nope.mp3")
        assert player.load_sound("sid1", missing) is False

    def test_returns_true_and_stores_metadata_on_success(self, player, tmp_path):
        # Stub pydub.AudioSegment.from_file to return an object with __len__
        fake_audio = MagicMock()
        fake_audio.__len__ = MagicMock(return_value=2500)  # 2.5 seconds in ms
        existing_file = tmp_path / "sample.mp3"
        existing_file.write_bytes(b"\x00")  # any contents — just so os.path.exists is True

        with patch("managers.audio_player.AudioSegment.from_file", return_value=fake_audio):
            assert player.load_sound("sid1", str(existing_file)) is True

        meta = player.loaded_sounds["sid1"]
        assert meta["file_path"] == str(existing_file)
        assert meta["duration"] == 2.5

    def test_returns_false_and_emits_error_on_decode_failure(self, player, tmp_path):
        existing_file = tmp_path / "broken.mp3"
        existing_file.write_bytes(b"\x00")
        errors = []
        player.playback_error.connect(lambda sid, msg: errors.append((sid, msg)))

        with patch("managers.audio_player.AudioSegment.from_file", side_effect=RuntimeError("bad codec")):
            assert player.load_sound("sid1", str(existing_file)) is False

        assert errors == [("sid1", "bad codec")]


class TestPlaySound:
    def test_returns_false_when_sound_not_loaded(self, player):
        assert player.play_sound("not-loaded") is False

    def test_plays_loaded_sound_and_updates_current(self, player, mocker):
        # Pre-populate loaded_sounds with a fake audio that has the
        # attributes sounddevice would consume
        fake_audio = MagicMock()
        fake_audio.get_array_of_samples.return_value = [0, 1, 2, 3]
        fake_audio.frame_rate = 44100
        player.loaded_sounds["sid1"] = {"audio": fake_audio, "duration": 1.0}

        sd_play = mocker.patch("managers.audio_player.sd.play")
        np_array = mocker.patch("managers.audio_player.np.array", side_effect=lambda x: x)

        started = []
        player.playback_started.connect(started.append)

        assert player.play_sound("sid1") is True
        sd_play.assert_called_once()
        assert player.current_playing == "sid1"
        assert started == ["sid1"]

    def test_stops_currently_playing_before_starting_new(self, player, mocker):
        fake_audio = MagicMock()
        fake_audio.get_array_of_samples.return_value = []
        fake_audio.frame_rate = 44100
        player.loaded_sounds["sid1"] = {"audio": fake_audio, "duration": 1.0}
        player.loaded_sounds["sid2"] = {"audio": fake_audio, "duration": 1.0}
        player.current_playing = "sid1"

        mocker.patch("managers.audio_player.sd.play")
        sd_stop = mocker.patch("managers.audio_player.sd.stop")
        mocker.patch("managers.audio_player.np.array", side_effect=lambda x: x)

        player.play_sound("sid2")
        sd_stop.assert_called_once()
        assert player.current_playing == "sid2"


class TestStopSound:
    def test_does_nothing_when_not_playing(self, player, mocker):
        sd_stop = mocker.patch("managers.audio_player.sd.stop")
        player.stop_sound()
        sd_stop.assert_not_called()

    def test_emits_stopped_signal(self, player, mocker):
        mocker.patch("managers.audio_player.sd.stop")
        player.current_playing = "sid1"
        stopped = []
        player.playback_stopped.connect(stopped.append)
        player.stop_sound()
        assert stopped == ["sid1"]
        assert player.current_playing is None


class TestDuration:
    def test_get_duration_returns_stored_value(self, player):
        player.loaded_sounds["sid1"] = {"duration": 12.34, "audio": object()}
        assert player.get_duration("sid1") == 12.34

    def test_get_duration_returns_none_for_unknown(self, player):
        assert player.get_duration("nope") is None

    @pytest.mark.parametrize(
        "seconds,expected",
        [
            (0, "0:00"),
            (5, "0:05"),
            (60, "1:00"),
            (65.4, "1:05"),
            (3600, "60:00"),  # No hours rollover
        ],
    )
    def test_format_duration(self, player, seconds, expected):
        assert player.format_duration(seconds) == expected
