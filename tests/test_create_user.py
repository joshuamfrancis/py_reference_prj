"""Tests for user creation endpoints"""
import pytest


class TestCreateUser:
    """Test user creation functionality"""
    
    def test_create_user_success(self, client):
        """Test successful user creation"""
        payload = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        response = client.post('/api/users', json=payload)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == "John Doe"
        assert data['email'] == "john@example.com"
        assert 'id' in data
        assert 'created_at' in data
    
    def test_create_user_missing_name(self, client):
        """Test user creation with missing name"""
        payload = {
            "email": "john@example.com"
        }
        response = client.post('/api/users', json=payload)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'name' in data['error'].lower()
    
    def test_create_user_missing_email(self, client):
        """Test user creation with missing email"""
        payload = {
            "name": "John Doe"
        }
        response = client.post('/api/users', json=payload)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'email' in data['error'].lower()
    
    def test_create_user_no_data(self, client):
        """Test user creation with no data"""
        response = client.post('/api/users', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_create_user_empty_body(self, client):
        """Test user creation with empty body"""
        response = client.post('/api/users')
        
        assert response.status_code == 415
    
    def test_create_multiple_users(self, client):
        """Test creating multiple users"""
        users_data = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"},
            {"name": "Charlie", "email": "charlie@example.com"}
        ]
        
        user_ids = []
        for user_data in users_data:
            response = client.post('/api/users', json=user_data)
            assert response.status_code == 201
            data = response.get_json()
            user_ids.append(data['id'])
        
        # Verify all IDs are unique
        assert len(set(user_ids)) == 3
