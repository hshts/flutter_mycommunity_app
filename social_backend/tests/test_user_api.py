import json


def test_user_login_email(client):
    resp = client.post('/user/login', json={'email': 'test@example.com', 'password': '123'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'data' in data
    assert data['data']['email'] == 'test@example.com'


def test_send_mobile_otp(client):
    resp = client.get('/user/sendMobileOTP?mobile=13800138000')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['data'] is True


def test_follow_and_unfollow(client, auth_headers):
    # 先创建两个用户
    client.post('/user/login', json={'email': 'a@x.com'})
    client.post('/user/login', json={'email': 'b@x.com'})

    # 关注
    resp = client.post('/user/follwerCommunity', headers=auth_headers, json={'uid': 1, 'followed': 2, 'token': 't'})
    assert resp.status_code == 200
    assert resp.get_json()['data'] is True

    # 获取关注列表
    resp = client.post('/user/getFollow', json={'uid': 1})
    assert resp.status_code == 200
    assert 2 in resp.get_json()['data']

    # 取消关注
    resp = client.post('/user/cleanfollwerCommunity', headers=auth_headers, json={'uid': 1, 'followed': 2, 'token': 't'})
    assert resp.status_code == 200
    assert resp.get_json()['data'] is True
