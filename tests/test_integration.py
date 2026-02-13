"""Integration tests for complete workflows"""


class TestIntegration:
    """Test complete user management workflows"""

    def test_full_user_lifecycle(self, client):
        """Test complete user lifecycle: create, read, update, delete"""
        # Create
        create_payload = {"name": "John Doe", "email": "john@example.com"}
        create_response = client.post('/api/users', json=create_payload)
        assert create_response.status_code == 201
        user = create_response.get_json()
        user_id = user['id']

        # Read
        get_response = client.get(f'/api/users/{user_id}')
        assert get_response.status_code == 200
        assert get_response.get_json()['name'] == "John Doe"

        # Update
        update_payload = {"name": "Jane Doe", "email": "jane@example.com"}
        update_response = client.put(
            f'/api/users/{user_id}',
            json=update_payload)
        assert update_response.status_code == 200
        updated_user = update_response.get_json()
        assert updated_user['name'] == "Jane Doe"

        # Delete
        delete_response = client.delete(f'/api/users/{user_id}')
        assert delete_response.status_code == 200

        # Verify deletion
        final_get = client.get(f'/api/users/{user_id}')
        assert final_get.status_code == 404

    def test_user_list_consistency(self, client):
        """Test that user lists are consistent across operations"""
        # Verify initial count
        count_response = client.get('/api/users/count')
        initial_count = count_response.get_json()['total_users']
        assert initial_count == 0

        # Create 3 users
        for i in range(3):
            payload = {"name": f"User {i}", "email": f"user{i}@example.com"}
            client.post('/api/users', json=payload)

        # Check count
        count_response = client.get('/api/users/count')
        assert count_response.get_json()['total_users'] == 3

        # Check list
        list_response = client.get('/api/users')
        assert len(list_response.get_json()) == 3

        # Delete one
        users = list_response.get_json()
        client.delete(f'/api/users/{users[0]["id"]}')

        # Verify count decreased
        count_response = client.get('/api/users/count')
        assert count_response.get_json()['total_users'] == 2

    def test_concurrent_user_operations(self, client):
        """Test multiple user operations in sequence"""
        # Create multiple users
        user_ids = []
        for i in range(5):
            payload = {"name": f"User {i}", "email": f"user{i}@example.com"}
            response = client.post('/api/users', json=payload)
            user_ids.append(response.get_json()['id'])

        # Update some
        for user_id in user_ids[:2]:
            payload = {"name": "Updated"}
            response = client.put(f'/api/users/{user_id}', json=payload)
            assert response.status_code == 200

        # Delete some
        for user_id in user_ids[2:4]:
            response = client.delete(f'/api/users/{user_id}')
            assert response.status_code == 200

        # Get all and verify
        all_users = client.get('/api/users').get_json()
        assert len(all_users) == 3
