import pytest
import requests

import atoti as tt


@pytest.mark.legacy_app
def test_legacy_url_returns_content():
    with tt.create_session() as session:
        legacy_url = f"{session.url}/legacy/"
        res = requests.get(legacy_url)
        assert res.status_code == 200
