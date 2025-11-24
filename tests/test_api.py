from urllib.parse import quote

from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic sanity check for a known activity
    assert "Chess Club" in data


def test_signup_duplicate_and_unregister():
    activity = "Chess Club"
    email = "teststudent@example.com"

    # Ensure email not present to start
    if email in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_unreg = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")
    assert resp_unreg.status_code == 200
    assert email not in app_module.activities[activity]["participants"]
