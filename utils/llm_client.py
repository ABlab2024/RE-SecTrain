import os
import json

class LLMClient:
    def __init__(self, provider, api_key):
        self.provider = provider
        self.api_key = api_key
        self.model = None
        self.client = None

        if provider == "google":
            from google import genai
            self.client = genai.Client(api_key=api_key)
            # Use a modern model compatible with the new SDK
            self.model_name = 'gemini-2.5-flash'
        elif provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        elif provider == "anthropic":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)

    def search_security_issues(self, interest):
        """
        Searches for recent security issues related to the interest.
        """
        prompt = f"Find 3 recent security threats, vulnerabilities, or phishing trends related to '{interest}' in South Korea or globally. Summarize them briefly in Korean. For each item, strictly provide a clickable source link (URL) so users can verify the news. Format the output as Markdown."

        try:
            if self.provider == "google":
                # For Gemini, we use the new google.genai SDK
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                return response.text
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
        except Exception as e:
            return f"Error searching security issues: {str(e)}"

    def generate_phishing_scenario(self, threat_info):
        """
        Generates a phishing email subject and body based on threat info.
        Returns a JSON object with 'subject' and 'body'.
        """
        prompt = f"""
        Based on the following security threat information:
        {threat_info}

        Create a realistic phishing email simulation to train employees.
        The email should appear to be from a legitimate source related to the threat (e.g., IT support, Service Provider).
        The entire content (Subject and Body) must be in Korean.
        
        Return the output strictly as a JSON object with two keys:
        - "subject": The email subject line in Korean.
        - "body": The email body in HTML format in Korean. (Do NOT consist of ```html ... ```, just the raw HTML content).
        
        IMPORTANT: For any call-to-action link (e.g., "Verify Account", "Login", "Download"), use the placeholder "{{TRACKING_LINK}}" as the URL/href. 
        Example: <a href="{{TRACKING_LINK}}">Verify Now</a>
        
        Do not include markdown formatting like ```json or ```.
        """

        try:
            content = ""
            if self.provider == "google":
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config={
                        'response_mime_type': 'application/json'
                    }
                )
                content = response.text
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                content = response.choices[0].message.content
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text

            # Clean up content to ensure valid JSON
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            return json.loads(content)

        except Exception as e:
            return {"subject": "Error Generation", "body": f"Failed to generate scenario: {str(e)}"}

    def generate_vulnerability_report(self, threat_type):
        """
        Generates a detailed vulnerability report including analysis and prevention.
        Returns HTML content.
        """
        prompt = f"""
        Analyze the security threat related to '{threat_type}'. 
        Provide a detailed vulnerability report including:
        1. Threat Analysis (What is it? How does it work?)
        2. Impact (What happens if successful?)
        3. Prevention Methods (Detailed steps to avoid it).
        
        Write in Korean.
        Format the output as HTML suitable for embedding in a div. 
        Use <h2> for main sections, <h3> for subsections, and <ul>/<li> for lists.
        Do NOT include <html>, <head>, or <body> tags. just the inner HTML.
        Make it visually appealing with simple styling classes if needed, but rely on semantic HTML.
        """

        try:
            content = ""
            if self.provider == "google":
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                content = response.text
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.choices[0].message.content
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=1500,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text

            # Clean up markdown code blocks if present
            content = content.strip()
            if content.startswith("```html"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            return content

        except Exception as e:
            return f"<p>Report generation failed: {str(e)}</p>"
