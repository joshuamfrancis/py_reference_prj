"""Tests for user retrieval endpoints"""


class TestGetUsers:
    """Test user retrieval functionality"""

    def test_get_all_users_empty(self, client):
        """Test getting all users when none exist"""
        response = client.get('/api/users')

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_all_users(self, client):
        """Test getting all users"""
        # Create a few users first
        for i in range(3):
            payload = {"name": f"User {i}", "email": f"user{i}@example.com"}
            client.post('/api/users', json=payload)

        response = client.get('/api/users')

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 3

        # Verify structure
        for user in data:
            assert 'id' in user
            assert 'name' in user
            assert 'email' in user
            assert 'created_at' in user

    def test_get_user_by_id(self, client):
        """Test getting a specific user by ID"""
        # Create a user
        payload = {"name": "John", "email": "john@example.com"}
        create_response = client.post('/api/users', json=payload)
        user_id = create_response.get_json()['id']

        # Retrieve the user
        response = client.get(f'/api/users/{user_id}')

        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == user_id
        assert data['name'] == "John"
        assert data['email'] == "john@example.com"

    def test_get_user_not_found(self, client):
        """Test retrieving non-existent user"""
        response = client.get('/api/users/999')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'not found' in data['error'].lower()

    def test_get_user_invalid_id(self, client):
        """Test retrieving user with invalid ID format"""
        response = client.get('/api/users/invalid')

        assert response.status_code == 404

    def test_count_users(self, client):
        """Test counting users"""
        # Create some users
        for i in range(5):
            payload = {"name": f"User {i}", "email": f"user{i}@example.com"}
            client.post('/api/users', json=payload)

        response = client.get('/api/users/count')

        assert response.status_code == 200
        data = response.get_json()
        assert data['total_users'] == 5
