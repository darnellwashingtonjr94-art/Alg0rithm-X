import subprocess
import json
import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class LighthouseAuditor:
    """
    Executes Lighthouse audits on target URLs via headless Chromium/Puppeteer.
    Requires Node.js and the lighthouse CLI installed globally.
    """
    def __init__(self, lighthouse_path: str = "lighthouse"):
        self.lighthouse_path = lighthouse_path

    def run_audit(self, target_url: str, output_dir: str = "./reports") -> Optional[Dict[str, Any]]:
        """
        Runs a performance and SEO audit, returning the parsed JSON results.
        """
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, "audit_report.json")

        command = [
            self.lighthouse_path,
            target_url,
            "--output=json",
            f"--output-path={report_path}",
            "--quiet",
            "--chrome-flags='--headless --no-sandbox --disable-gpu'"
        ]

        try:
            logger.info(f"Starting Lighthouse audit for: {target_url}")
            subprocess.run(command, check=True)
            
            with open(report_path, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
                
            categories = report_data.get('categories', {})
            scores = {
                'performance': categories.get('performance', {}).get('score', 0) * 100,
                'accessibility': categories.get('accessibility', {}).get('score', 0) * 100,
                'best_practices': categories.get('best-practices', {}).get('score', 0) * 100,
                'seo': categories.get('seo', {}).get('score', 0) * 100,
            }
            
            logger.info(f"Audit Complete. Scores: {scores}")
            return scores

        except subprocess.CalledProcessError as e:
            logger.error(f"Lighthouse CLI failed: {e}")
            return None
        except FileNotFoundError:
            logger.error("Lighthouse JSON output not found.")
            return None
