# import pytest

# @pytest.mark.parametrize('post_data', [
#     {'title': 'Test Post 1', 'content': 'This is test post 1.'},
#     {'title': 'Test Post 2', 'content': 'This is test post 2.'},
#     {'title': 'Test Post 3', 'content': 'This is test post 3.'},
#     {'title': 'Test Post 4', 'content': 'This is test post 4.'}
# ])

# def test_add_post(client):
#     global jwt_token
#     response = client.post('/add_post', json={'title': 'Test Post', 'content': 'This is a test post.'}, headers={'Authorization': f'Bearer {jwt_token}'})
#     data = response.get_json()
#     assert response.status_code == 201
#     assert data['message'] == 'Post added successfully!'

