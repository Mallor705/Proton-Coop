import logging
import sys
from pathlib import Path
from functools import lru_cache

class Logger:
    """Custom logger for Linux-Coop, with optimized console and file output."""
    def __init__(self, name: str, log_dir: Path):
        """Initializes the logger, creating log directory and configuring handlers."""
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self._handlers_setup = False
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Configures logger handlers in an optimized way, avoiding duplication."""
        if self.logger.hasHandlers() or self._handlers_setup:
            return
            
        # Optimized formatter
        formatter = logging.Formatter('%(asctime)s - %(message)s', 
                                    datefmt='%Y-%m-%d %H:%M:%S')
        
        # Console handler with buffer
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)
        
        # Optimized file handler
        log_file = self.log_dir / f"{self.logger.name}.log"
        file_handler = logging.FileHandler(
            log_file, 
            mode='a', 
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        
        self._handlers_setup = True
    
    @lru_cache(maxsize=128)
    def _should_log(self, level: int) -> bool:
        """Cache for log level check."""
        return self.logger.isEnabledFor(level)
    
    def info(self, message: str):
        """Logs an informational message in an optimized way."""
        if self._should_log(logging.INFO):
            self.logger.info(message)
    
    def error(self, message: str):
        """Logs an error message in an optimized way."""
        if self._should_log(logging.ERROR):
            self.logger.error(message)

    def warning(self, message: str):
        """Logs a warning message in an optimized way."""
        if self._should_log(logging.WARNING):
            self.logger.warning(message)
    
    def flush(self):
        """Forces flushing of handlers to ensure logs are written."""
        for handler in self.logger.handlers:
            if hasattr(handler, 'flush'):
                handler.flush()