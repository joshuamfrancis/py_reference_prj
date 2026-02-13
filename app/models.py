"""Data models and in-memory storage"""
from datetime import datetime
from typing import List, Dict, Optional


class User:
    """User model"""
    
    def __init__(self, user_id: int, name: str, email: str):
        self.id = user_id
        self.name = name
        self.email = email
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at
        }


class UserStore:
    """In-memory user storage"""
    
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.next_id = 1
    
    def create_user(self, name: str, email: str) -> User:
        """Create a new user"""
        user = User(self.next_id, name, email)
        self.users[self.next_id] = user
        self.next_id += 1
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return list(self.users.values())
    
    def update_user(self, user_id: int, name: str = None, email: str = None) -> Optional[User]:
        """Update user information"""
        user = self.users.get(user_id)
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    def clear_all(self):
        """Clear all users (for testing)"""
        self.users.clear()
        self.next_id = 1


# Global store instance
user_store = UserStore()
