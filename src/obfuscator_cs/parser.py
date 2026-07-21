import json
import subprocess
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class RoslynASTBridge:
    """
    Interfaces with a compiled Roslyn C# analyzer to extract, modify, and rebuild 
    C# source code into an Abstract Syntax Tree (AST) JSON representation.
    """
    def __init__(self, roslyn_binary_path: str = "./tools/RoslynParser.exe"):
        self.roslyn_binary = roslyn_binary_path

    def parse_source_to_json(self, source_code_path: str) -> Optional[Dict[str, Any]]:
        """Invokes the Roslyn executable to parse C# code into a JSON AST structure."""
        command = [self.roslyn_binary, "--mode", "parse", "--input", source_code_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            ast_json = json.loads(result.stdout)
            logger.info(f"Successfully parsed AST for {source_code_path}")
            return ast_json
        except subprocess.CalledProcessError as e:
            logger.error(f"Roslyn parsing failed: {e.stderr}")
            return None
        except json.JSONDecodeError:
            logger.error("Failed to decode AST JSON from Roslyn output.")
            return None

    def rebuild_source_from_json(self, modified_ast: Dict[str, Any], output_path: str) -> bool:
        """Pipes the obfuscated JSON AST back to Roslyn to emit standard C# code."""
        command = [self.roslyn_binary, "--mode", "emit", "--output", output_path]
        try:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input=json.dumps(modified_ast))
            
            if process.returncode == 0:
                logger.info(f"Successfully emitted obfuscated C# to {output_path}")
                return True
            else:
                logger.error(f"Roslyn emission failed: {stderr}")
                return False
        except Exception as e:
            logger.error(f"IPC Error during source rebuild: {str(e)}")
            return False
