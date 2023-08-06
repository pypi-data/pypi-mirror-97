import pytest

from ampel.ztf.ingest.ZiT0UpperLimitShaper import ZiT0UpperLimitShaper


@pytest.mark.parametrize(
    "uld,expected_id,comment",
    [
        (
            {
                "diffmaglim": 19.024799346923828,
                "fid": 2,
                "jd": 2458089.7405324,
                "pid": 335240532815,
                "programid": 0,
            },
            -3352405322819025,
            "",
        ),
        (
            {
                "diffmaglim": 19.6149997711182,
                "fid": 2,
                "jd": 2459141.8900463,
                "pid": 1387390043915,
                "programid": 0,
                "rcid": None,
            },
            -13873900463919615,
            "pid > 1e12, rcid None",
        ),
        (
            {
                "diffmaglim": 19.6149997711182,
                "fid": 2,
                "jd": 2459141.8900463,
                "pid": 1387390043915,
                "programid": 0,
                "rcid": 57,
            },
            -13873900465719615,
            "pid > 1e12, rcid explicitly set",
        ),
    ],
)
def test_identity(uld, expected_id, comment):
    assert ZiT0UpperLimitShaper().identity(uld) == expected_id, comment
    assert ZiT0UpperLimitShaper().ampelize([uld])[0]["_id"] == expected_id, comment
