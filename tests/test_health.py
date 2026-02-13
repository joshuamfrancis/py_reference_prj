"""Tests for health and status endpoints"""


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_health_check_returns_json(self, client):
        """Test that health check returns JSON"""
        response = client.get('/api/health')

        assert response.content_type == 'application/json'

    def test_count_users_initially_zero(self, client):
        """Test that count is zero when no users exist"""
        response = client.get('/api/users/count')

        assert response.status_code == 200
        data = response.get_json()
        assert data['total_users'] == 0
