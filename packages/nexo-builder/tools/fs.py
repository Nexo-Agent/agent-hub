import os
import subprocess
import glob
from typing import Dict, Any, List

class FileSystemTools:
    def get_tools(self) -> Dict[str, Any]:
        return {
            "read_file": {
                "handler": self.read_file,
                "schema": {
                    "name": "read_file",
                    "description": "Read content of a file",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"]
                    }
                }
            },
            "write_file": {
                "handler": self.write_file,
                "schema": {
                    "name": "write_file",
                    "description": "Write content to a file (overwrite)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "content": {"type": "string"}
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            "list_dir": {
                "handler": self.list_dir,
                "schema": {
                    "name": "list_dir",
                    "description": "List files in directory",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"]
                    }
                }
            },
             "search_code": {
                "handler": self.search_code,
                "schema": {
                    "name": "search_code",
                    "description": "Search text in files (grep)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}, "path": {"type": "string", "default": "."}},
                        "required": ["query"]
                    }
                }
            }
        }

    def read_file(self, path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def write_file(self, path: str, content: str) -> str:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing file: {e}"

    def list_dir(self, path: str) -> str:
        try:
            items = os.listdir(path)
            # Add type indicator
            result = []
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    result.append(f"{item}/")
                else:
                    result.append(item)
            return "\n".join(result)
        except Exception as e:
            return f"Error listing directory: {e}"

    def search_code(self, query: str, path: str = ".") -> str:
        try:
            # Simple grep using subprocess
            # -r: recursive, -n: line number, -I: ignore binary
            cmd = ["grep", "-rnI", query, path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # Limit output to first 2000 chars to avoid overflowing context
                return result.stdout[:2000] + ("\n...truncated..." if len(result.stdout) > 2000 else "")
            elif result.returncode == 1:
                return "No matches found."
            else:
                return f"Grep error: {result.stderr}"
        except Exception as e:
            return f"Error searching code: {e}"
