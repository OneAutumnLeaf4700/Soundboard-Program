import json

import pytest

from models.sound_model import SoundModel


@pytest.fixture
def model(tmp_path):
    return SoundModel(data_file=str(tmp_path / "data" / "sounds.json"))


def _sample(title="Sound A", category=1, file_path="/tmp/sound_a.mp3"):
    return {
        "title": title,
        "category": category,
        "file_path": file_path,
        "favorite": False,
    }


class TestInit:
    def test_creates_data_directory(self, tmp_path):
        path = tmp_path / "nested" / "dir" / "sounds.json"
        SoundModel(data_file=str(path))
        assert path.parent.is_dir()

    def test_starts_empty(self, model):
        assert model.get_all_sounds() == {}
        assert model.get_favorites() == []

    def test_loads_existing_data(self, tmp_path):
        path = tmp_path / "sounds.json"
        path.write_text(json.dumps({
            "sounds": {"sid1": _sample("Pre-existing")},
            "favorites": ["sid1"],
        }))
        m = SoundModel(data_file=str(path))
        assert "sid1" in m.get_all_sounds()
        assert m.is_favorite("sid1")

    def test_handles_corrupt_json_without_raising(self, tmp_path, caplog):
        path = tmp_path / "sounds.json"
        path.write_text("{ this is not valid json")
        m = SoundModel(data_file=str(path))  # Should not raise
        # Logged the error but starts empty
        assert m.get_all_sounds() == {}


class TestAddRemove:
    def test_add_sound_persists_to_disk(self, model):
        model.add_sound("sid1", _sample("Sound A"))
        assert model.get_sound("sid1") == _sample("Sound A")
        # Reload to confirm save
        reloaded = SoundModel(data_file=model.data_file)
        assert reloaded.get_sound("sid1") == _sample("Sound A")

    def test_add_sound_overwrites_existing(self, model):
        model.add_sound("sid1", _sample("First"))
        model.add_sound("sid1", _sample("Second"))
        assert model.get_sound("sid1")["title"] == "Second"

    def test_remove_sound_returns_true_on_success(self, model):
        model.add_sound("sid1", _sample())
        assert model.remove_sound("sid1") is True
        assert model.get_sound("sid1") is None

    def test_remove_sound_returns_false_for_unknown_id(self, model):
        assert model.remove_sound("nope") is False

    def test_remove_sound_also_drops_from_favorites(self, model):
        model.add_sound("sid1", _sample())
        model.add_to_favorites("sid1")
        assert model.is_favorite("sid1")
        model.remove_sound("sid1")
        assert not model.is_favorite("sid1")


class TestFavorites:
    def test_add_to_favorites_returns_true_on_success(self, model):
        model.add_sound("sid1", _sample())
        assert model.add_to_favorites("sid1") is True
        assert model.is_favorite("sid1")

    def test_add_to_favorites_rejects_unknown_sound(self, model):
        assert model.add_to_favorites("not-added") is False

    def test_add_to_favorites_idempotent(self, model):
        model.add_sound("sid1", _sample())
        model.add_to_favorites("sid1")
        # Second add returns False because it's already there
        assert model.add_to_favorites("sid1") is False
        assert model.favorites.count("sid1") == 1

    def test_remove_from_favorites(self, model):
        model.add_sound("sid1", _sample())
        model.add_to_favorites("sid1")
        assert model.remove_from_favorites("sid1") is True
        assert not model.is_favorite("sid1")

    def test_remove_from_favorites_unknown_id(self, model):
        assert model.remove_from_favorites("nope") is False

    def test_toggle_favorite_round_trip(self, model):
        model.add_sound("sid1", _sample())
        assert model.toggle_favorite("sid1") is True
        assert model.is_favorite("sid1")
        assert model.toggle_favorite("sid1") is False
        assert not model.is_favorite("sid1")

    def test_get_favorites_returns_list_with_ids(self, model):
        model.add_sound("sid1", _sample("First"))
        model.add_sound("sid2", _sample("Second"))
        model.add_to_favorites("sid1")
        favs = model.get_favorites()
        assert len(favs) == 1
        assert favs[0]["id"] == "sid1"
        assert favs[0]["title"] == "First"

    def test_get_favorites_skips_orphaned_ids(self, model):
        # Manually corrupt: id in favorites but not in sounds
        model.favorites.append("orphan-id")
        favs = model.get_favorites()
        assert favs == []


class TestPersistence:
    def test_round_trip_through_disk(self, tmp_path):
        path = str(tmp_path / "sounds.json")
        m1 = SoundModel(data_file=path)
        m1.add_sound("sid1", _sample("Persisted"))
        m1.add_to_favorites("sid1")
        # New instance reads the same file
        m2 = SoundModel(data_file=path)
        assert m2.get_sound("sid1")["title"] == "Persisted"
        assert m2.is_favorite("sid1")

    def test_save_failure_is_non_fatal(self, model, monkeypatch):
        # Force open() to raise IOError on write
        original_open = open

        def boom(path, mode="r", *args, **kwargs):
            if "w" in mode:
                raise IOError("disk full")
            return original_open(path, mode, *args, **kwargs)

        monkeypatch.setattr("builtins.open", boom)
        # Should log but not raise
        model.add_sound("sid1", _sample())
