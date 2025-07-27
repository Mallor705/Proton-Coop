from typing import Dict, Optional, Any
from pathlib import Path
import time

class ProfileCache:
    """External cache for profiles and path validations."""
    
    def __init__(self):
        self._path_cache: Dict[str, bool] = {}
        self._profile_cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, float] = {}
        self._cache_ttl = 300  # 5 minutes TTL
    
    def check_path_exists(self, path: Path) -> bool:
        """Checks if a path exists with caching."""
        path_str = str(path)
        current_time = time.time()
        
        # Check if cache entry exists and is not expired
        if (path_str in self._path_cache and 
            path_str in self._cache_timestamps and
            current_time - self._cache_timestamps[path_str] < self._cache_ttl):
            return self._path_cache[path_str]
        
        # Cache miss or expired, check filesystem
        exists = path.exists()
        self._path_cache[path_str] = exists
        self._cache_timestamps[path_str] = current_time
        return exists
    
    def get_profile(self, profile_key: str) -> Optional[Any]:
        """Retrieves a profile from the cache."""
        current_time = time.time()
        
        if (profile_key in self._profile_cache and
            profile_key in self._cache_timestamps and
            current_time - self._cache_timestamps[profile_key] < self._cache_ttl):
            return self._profile_cache[profile_key]
        return None
    
    def set_profile(self, profile_key: str, profile: Any) -> None:
        """Stores a profile in the cache."""
        self._profile_cache[profile_key] = profile
        self._cache_timestamps[profile_key] = time.time()

    def invalidate_profile(self, profile_key: str) -> None:
        """Invalidates a specific profile entry from the cache."""
        self._profile_cache.pop(profile_key, None)
        self._cache_timestamps.pop(profile_key, None)

    def clear_expired(self) -> None:
        """Removes expired entries from the cache."""
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self._cache_timestamps.items()
            if current_time - timestamp >= self._cache_ttl
        ]
        
        for key in expired_keys:
            self._path_cache.pop(key, None)
            self._profile_cache.pop(key, None)
            self._cache_timestamps.pop(key, None)

# Global cache instance
_global_cache = ProfileCache()

def get_cache() -> ProfileCache:
    """Returns the global cache instance."""
    return _global_cache