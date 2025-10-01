def test_read_main(anon_client):
    response = anon_client.get("/")
    assert response.status_code == 200


def test_login_response_401(anon_client):
    payload = {
        "username": "testtest",
        "password": "testtest"
    }
    respone = anon_client.post("users/login", json=payload)
    assert respone.status_code == 401

def test_register_response_201(anon_client):
    payload = {
        "username": "testtest1",
        "password": "testtest",
        "password_confirm": "testtest"
    }
    respone = anon_client.post("users/register", json=payload)
    assert respone.status_code == 201


def test_login_response_200(anon_client):
    payload = {
        "username": "usertest",
        "password": "12345sa3b89"
    }
    respone = anon_client.post("users/login", json=payload)
    assert respone.status_code == 200
    assert respone.json()["detail"] == "Logged in successfully"
    assert respone.json()["access_token"] is not None
    assert respone.json()["refresh_token"] is not None

def test_login_ivalid_password_response_401(anon_client):
    payload = {
        "username": "usertest",
        "password": "testtest"
    }
    respone = anon_client.post("users/login", json=payload)
    assert respone.status_code == 401
    assert respone.json()["detail"] == "Incorrect username or password"


def test_login_ivalid_username_response_401(anon_client):
    payload = {
        "username": "usertest1",
        "password": "12345sa3b89"
    }
    respone = anon_client.post("users/login", json=payload)
    assert respone.status_code == 401
    assert respone.json()["detail"] == "Incorrect username or password"

def test_register_password_confirm_response_422(anon_client):
    payload = {
        "username": "usertest1",
        "password": "12345sa3b89",
        "password_confirm": "12345sa3b891"
    }
    respone = anon_client.post("users/register", json=payload)
    assert respone.status_code == 422
    # Check that the validation error contains the password mismatch message
    error_detail = respone.json()["detail"]
    assert any("Passwords do not match" in str(err) for err in error_detail)

    

