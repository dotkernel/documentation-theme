#!/usr/bin/env python3
import sys
import yaml

if len(sys.argv) < 3:
    print("Missing required arguments to update_mkdocs_yml.py.\n")
    print("Usage:\n")
    print("  update_mkdocs_yml.py <SITE_URL> <DOCS_DIR>\n")
    exit(1)

site_url = sys.argv[1]
docs_dir = sys.argv[2]

with open("mkdocs.yml") as f:
    mkdocs = yaml.load(f, Loader=yaml.SafeLoader)

mkdocs["site_url"] = site_url
mkdocs["edit_uri"] = 'edit/main/{}/'.format(docs_dir)
mkdocs["markdown_extensions"] = [
        {
            "markdown.extensions.codehilite": {
                "use_pygments": False
            }
        },
        "markdown.extensions.attr_list",
        "markdown.extensions.md_in_html",
        "markdown.extensions.def_list",
        "pymdownx.superfences",
        "pymdownx.tabbed",
        {
            "pymdownx.snippets": {
                "url_download": True,
                "base_path": [
                    "docs/snippets"
                ]
            }
        },
        {
            "toc": {
                "toc_depth": 2
            }
        },
        "callouts"
    ]

mkdocs["theme"] = {
        "name": None,
        "custom_dir": "documentation-theme/theme",
        "static_templates": [
            "pages/404.html"
        ]
    }

mkdocs["extra"]["dotkernel_blog_url"] = "https://www.dotkernel.com/blog/"
mkdocs["extra"]["dotkernel_rss_url"] = "https://www.dotkernel.com/feed/"
mkdocs["extra"]["docs_api_url"] = "https://docs.dotkernel.org/api/"
mkdocs["extra"]["docs_admin_url"] = "https://docs.dotkernel.org/admin/"
mkdocs["extra"]["docs_frontend_url"] = "https://docs.dotkernel.org/frontend/"
mkdocs["extra"]["docs_packages_url"] = "https://docs.dotkernel.org/packages/"

# Remove any trailing slashes from the end of the repo_url
mkdocs["repo_url"] = mkdocs["repo_url"].rstrip("/")
mkdocs["extra"]["repo_name"] = mkdocs["repo_url"].replace("https://github.com/", "")
mkdocs["extra"]["base_url"] = "https://docs.dotkernel.org/"

if mkdocs["extra"]["project"] == "DotKernel Frontend":
    mkdocs["extra"]["project_url"] = mkdocs["extra"]["docs_frontend_url"]
elif mkdocs["extra"]["project"] == "DotKernel Admin":
    mkdocs["extra"]["project_url"] = mkdocs["extra"]["docs_admin_url"]
elif (mkdocs["extra"]["project"] == "DotKernel API"):
    mkdocs["extra"]["project_url"] = mkdocs["extra"]["docs_api_url"]
elif mkdocs["extra"]["project"] == "Packages":
    mkdocs["extra"]["project_url"] = mkdocs["extra"]["docs_packages_url"]

mkdocs["extra"]["projects"] = [
    {
        "name": "API",
        "description": "DotKernel API",
        "docs_url": mkdocs["extra"]["docs_api_url"],
    },
    {
        "name": "Admin",
        "description": "DotKernel Admin application",
        "docs_url": mkdocs["extra"]["docs_admin_url"],
    },
    {
        "name": "Frontend",
        "description": "DotKernel Frontend application",
        "docs_url": mkdocs["extra"]["docs_frontend_url"],
    },
    {
        "name": "Packages",
        "description": "DotKernel packages",
        "docs_url": mkdocs["extra"]["docs_packages_url"],
    },
]

# If plugins are set, check if search exists
# https://www.mkdocs.org/user-guide/configuration/#plugins
if "plugins" in mkdocs and not "search" in mkdocs["plugins"]:
    mkdocs["plugins"].append("search")

with open("mkdocs.yml", "w") as f:
    yaml.dump(mkdocs, f, default_flow_style=False)
