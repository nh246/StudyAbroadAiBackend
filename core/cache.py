# In-memory cache for user profiles
# This will be replaced with a database later

from typing import Dict, Optional
from threading import Lock

class UserProfileCache:
    """Thread-safe in-memory storage for user profiles"""
    
    def __init__(self):
        self._cache: Dict[int, dict] = {}
        self._lock = Lock()
        self._next_id = 1
    
    def save_profile(self, profile_data: dict) -> int:
        """Save a user profile and return the user_id"""
        with self._lock:
            user_id = self._next_id
            self._cache[user_id] = profile_data
            self._next_id += 1
            return user_id
    
    def get_profile(self, user_id: int) -> Optional[dict]:
        """Retrieve a user profile by ID"""
        with self._lock:
            return self._cache.get(user_id)
    
    def update_profile(self, user_id: int, profile_data: dict) -> bool:
        """Update an existing profile"""
        with self._lock:
            if user_id in self._cache:
                self._cache[user_id] = profile_data
                return True
            return False
    
    def get_all_profiles(self) -> Dict[int, dict]:
        """Get all profiles (for debugging)"""
        with self._lock:
            return self._cache.copy()
    
    def clear(self):
        """Clear all profiles"""
        with self._lock:
            self._cache.clear()
            self._next_id = 1


# Singleton instance
profile_cache = UserProfileCache()
