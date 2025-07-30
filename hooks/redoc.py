import re
import json
import yaml
from pathlib import Path


def on_page_markdown(markdown, page, config, files):
    """Process custom Redoc syntax in markdown."""

    # Pattern to match [REDOC(path/to/openapi.yaml)]
    pattern = r"\[REDOC\((.*?)\)\]"

    # Check if the page contains REDOC tag
    if re.search(pattern, markdown):
        # Set the template for this page
        page.meta["template"] = "full-width.html"

    def replace_redoc(match):
        spec_path = match.group(1)

        # Resolve the path relative to the docs directory
        docs_dir = Path(config["docs_dir"])
        current_page_dir = Path(page.file.src_path).parent

        # Try to resolve the path relative to the current page first
        full_path = docs_dir / current_page_dir / spec_path
        if not full_path.exists():
            # Try relative to docs root
            full_path = docs_dir / spec_path

        # Read and parse the OpenAPI spec
        try:
            with open(full_path, "r") as f:
                if spec_path.endswith(".yaml") or spec_path.endswith(".yml"):
                    spec_data = yaml.safe_load(f)
                else:
                    spec_data = json.load(f)

            # Convert to JSON string for embedding
            spec_json = json.dumps(spec_data)

            # Generate the Redoc HTML with embedded spec
            redoc_html = f"""
<div id="redoc-container"></div>

<script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
<script>
  // Embedded OpenAPI specification
  const spec = {spec_json};

  // Initialize Redoc with the embedded spec
  Redoc.init(spec, {{
    scrollYOffset: 50
  }}, document.getElementById('redoc-container'));
</script>

<style>
  /* Basic Redoc container styling */
  #redoc-container {{
    min-height: 100%;
    background-color: white;
  }}

  /* Ensure Redoc wrapper has white background */
  .redoc-wrap {{
    background-color: white;
  }}
</style>
"""
        except Exception as e:
            # Fallback to spec-url if reading fails
            print(f"Warning: Could not read OpenAPI spec at {full_path}: {e}")
            redoc_html = f'''
<div id="redoc-container">
  <redoc spec-url="{spec_path}"></redoc>
</div>

<script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>

<style>
  /* Basic Redoc container styling */
  #redoc-container {{
    min-height: 100%;
    background-color: white;
  }}

  /* Ensure Redoc wrapper has white background */
  .redoc-wrap {{
    background-color: white;
  }}
</style>
'''

        return redoc_html

    # Replace all occurrences
    markdown = re.sub(pattern, replace_redoc, markdown)

    return markdown
