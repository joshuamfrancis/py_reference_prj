"""Tests for user update endpoints"""
import pytest


class TestUpdateUser:
    """Test user update functionality"""
    
    def test_update_user_name(self, client):
        """Test updating user name"""
        # Create a user
        payload = {"name": "John", "email": "john@example.com"}
        create_response = client.post('/api/users', json=payload)
        user_id = create_response.get_json()['id']
        
        # Update the user
        update_payload = {"name": "Jane"}
        response = client.put(f'/api/users/{user_id}', json=update_payload)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == "Jane"
        assert data['email'] == "john@example.com"  # Email unchanged
    
    def test_update_user_email(self, client):
        """Test updating user email"""
        # Create a user
        payload = {"name": "John", "email": "john@example.com"}
        create_response = client.post('/api/users', json=payload)
        user_id = create_response.get_json()['id']
        
        # Update the email
        update_payload = {"email": "john.doe@example.com"}
        response = client.put(f'/api/users/{user_id}', json=update_payload)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == "john.doe@example.com"
        assert data['name'] == "John"  # Name unchanged
    
    def test_update_user_both_fields(self, client):
        """Test updating both name and email"""
        # Create a user
        payload = {"name": "John", "email": "john@example.com"}
        create_response = client.post('/api/users', json=payload)
        user_id = create_response.get_json()['id']
        
        # Update both fields
        update_payload = {"name": "Jane Doe", "email": "jane@example.com"}
        response = client.put(f'/api/users/{user_id}', json=update_payload)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == "Jane Doe"
        assert data['email'] == "jane@example.com"
    
    def test_update_nonexistent_user(self, client):
        """Test updating a user that doesn't exist"""
        payload = {"name": "John"}
        response = client.put('/api/users/999', json=payload)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_update_user_no_data(self, client):
        """Test updating user with no data"""
        # Create a user
        payload = {"name": "John", "email": "john@example.com"}
        create_response = client.post('/api/users', json=payload)
        user_id = create_response.get_json()['id']
        
        # Try to update with empty data
        response = client.put(f'/api/users/{user_id}', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_update_user_empty_body(self, client):
        """Test updating user with empty body"""
        # Create a user
        payload = {"name": "John", "email": "john@example.com"}
        create_response = client.post('/api/users', json=payload)
        user_id = create_response.get_json()['id']
        
        # Try to update with no body
        response = client.put(f'/api/users/{user_id}')
        
        assert response.status_code == 415
