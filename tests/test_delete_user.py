"""Tests for user deletion endpoints"""


class TestDeleteUser:
    """Test user deletion functionality"""

    def test_delete_user_success(self, client):
        """Test successful user deletion"""
        # Create a user
        payload = {"name": "John", "email": "john@example.com"}
        create_response = client.post('/api/users', json=payload)
        user_id = create_response.get_json()['id']

        # Verify user exists
        get_response = client.get(f'/api/users/{user_id}')
        assert get_response.status_code == 200

        # Delete the user
        response = client.delete(f'/api/users/{user_id}')

        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert 'deleted' in data['message'].lower()

    def test_delete_user_not_found(self, client):
        """Test deleting a non-existent user"""
        response = client.delete('/api/users/999')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_delete_user_user_gone(self, client):
        """Test that user is actually deleted"""
        # Create a user
        payload = {"name": "John", "email": "john@example.com"}
        create_response = client.post('/api/users', json=payload)
        user_id = create_response.get_json()['id']

        # Delete the user
        delete_response = client.delete(f'/api/users/{user_id}')
        assert delete_response.status_code == 200

        # Try to retrieve the deleted user
        get_response = client.get(f'/api/users/{user_id}')
        assert get_response.status_code == 404

    def test_delete_multiple_users(self, client):
        """Test deleting multiple users"""
        # Create multiple users
        user_ids = []
        for i in range(3):
            payload = {"name": f"User {i}", "email": f"user{i}@example.com"}
            create_response = client.post('/api/users', json=payload)
            user_ids.append(create_response.get_json()['id'])

        # Delete them one by one
        for user_id in user_ids:
            response = client.delete(f'/api/users/{user_id}')
            assert response.status_code == 200

        # Verify all are deleted
        count_response = client.get('/api/users/count')
        data = count_response.get_json()
        assert data['total_users'] == 0

    def test_delete_same_user_twice(self, client):
        """Test deleting the same user twice"""
        # Create a user
        payload = {"name": "John", "email": "john@example.com"}
        create_response = client.post('/api/users', json=payload)
        user_id = create_response.get_json()['id']

        # Delete once
        response1 = client.delete(f'/api/users/{user_id}')
        assert response1.status_code == 200

        # Try to delete again
        response2 = client.delete(f'/api/users/{user_id}')
        assert response2.status_code == 404
