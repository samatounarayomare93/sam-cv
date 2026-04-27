import logging
import os
import re
from typing import Optional

class CVTailor:
    """Dynamically tailors Sam's CV content to match specific job requirements."""
    
    def __init__(self, base_cv_path: str):
        self.base_cv_path = base_cv_path
        self.base_content = self._load_base_cv()

    def _load_base_cv(self) -> str:
        if os.path.exists(self.base_cv_path):
            try:
                with open(self.base_cv_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                logging.error(f"Failed to load base CV: {e}")
        return ""

    def tailor_cv(self, job_title: str, competitive_advantage: str, keywords: list = None) -> str:
        """
        Injects a dynamic 'Competitive Advantage' section AND hidden ATS keywords.
        """
        if not self.base_content:
            return ""

        # Sector 2: American ATS Bypass (Hidden Layer)
        hidden_layer = ""
        if keywords:
            kw_str = ", ".join(keywords)
            hidden_layer = f"""
            <div id="ats-bypass-layer" style="color: #ffffff; font-size: 1px; line-height: 1px; opacity: 0.01; position: absolute; left: -9999px;">
                {kw_str}
            </div>
            """

        # Sector 1: Sovereign Fit Summary
        tailored_section = f"""
        <div class="tailored-fit" style="background: #f8f9fa; border-left: 5px solid #007bff; padding: 15px; margin-bottom: 20px; border-radius: 4px;">
            <h3 style="color: #007bff; margin-top: 0; font-family: 'Inter', sans-serif;">🎯 Why I am the Perfect Match for {job_title}</h3>
            <p style="font-style: italic; color: #333; line-height: 1.5;">
                {competitive_advantage}
            </p>
        </div>
        """

        merged_content = self.base_content
        # Inject tailored section
        if "<h2>" in merged_content:
            merged_content = merged_content.replace("<h2>", tailored_section + "<h2>", 1)
        elif "<h3>" in merged_content:
            merged_content = merged_content.replace("<h3>", tailored_section + "<h3>", 1)
        
        # Inject hidden layer at the end of body
        if "</body>" in merged_content:
            merged_content = merged_content.replace("</body>", hidden_layer + "</body>")
        else:
            merged_content += hidden_layer
            
        return merged_content

def get_tailored_cv_path(job_id: str, job_title: str, advantage: str, keywords: list = None) -> str:
    """Helper to generate and save a tailored CV for a specific strike."""
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Sam_Cordahi_CV.html")
    tailor = CVTailor(base_path)
    content = tailor.tailor_cv(job_title, advantage, keywords)
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "core", "temp_cvs")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, f"CV_{job_id}.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return file_path
