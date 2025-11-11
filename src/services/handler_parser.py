import json
import subprocess
from pathlib import Path
from ..core.logger import Logger
import shutil
from ..core.config import Config

class HandlerParser:
    """
    This service is responsible for parsing and interpreting handler.js files
    by executing a Node.js script.
    """

    def __init__(self, logger: Logger):
        self.logger = logger
        self.node_executable = shutil.which('node')
        self.parser_script_path = Config.APP_DIR / "src" / "services" / "handler_parser.js"

    def parse_handler(self, handler_js_path: Path) -> dict:
        """
        Parses the content of a handler.js file and returns a dictionary
        with the extracted information.
        """
        if not self.node_executable:
            self.logger.error("Node.js executable not found. Please install Node.js.")
            return {}

        if not self.parser_script_path.exists():
            self.logger.error(f"Handler parser script not found at {self.parser_script_path}")
            return {}

        command = [self.node_executable, str(self.parser_script_path), str(handler_js_path)]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error executing handler_parser.js: {e}")
            self.logger.error(f"Stderr: {e.stderr}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON output from handler_parser.js: {e}")
            return {}
