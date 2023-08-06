# Terra Nanotech Auth Templates

Template Overrides for Alliance Auth

```shell
pip install tnnt-templates
```

In `local.py` right after `INSTALLED_APPS`:

```python
# TN-NT Auth Templates
INSTALLED_APPS.insert(0, "tnnt_templates")

if "tnnt_templates" in INSTALLED_APPS:
    TEMPLATES[0]["OPTIONS"]["context_processors"].append(
        "tnnt_templates.context_processors.tnnt_settings"
    )

    TNNT_TEMPLATE_ENTITY_ID = 08154711  #  replace with your corp/alliance ID
    TNNT_TEMPLATE_ENTITY_TYPE = "corporation"  # default: "alliance"
    TNNT_TEMPLATE_ENTITY_NAME = "My Awesome Corp/Alliance"  # your corp/alliance name

    # the URLs are shown in the user menu
    TNNT_TEMPLATE_URLS_OWN_WEBSITES = [
        {
            "name": "Website",
            "url": "https://webseite.com/",
            "new_tab": True,
        },
        {
            "name": "Forums",
            "url": "https://forum.website.com/",
            "new_tab": True,
        },
    ]

    TNNT_TEMPLATE_URLS_OTHER_WEBSITES = [
        {
            "name": "Website",
            "url": "https://website.com/",
            "new_tab": True,
        },
    ]
```

**Important**

If you are using `AA-GDPR`, the template stuff needs to be **after** the `AA_GDPR`
entry, like this:

```python
# GDPR Compliance
INSTALLED_APPS.insert(0, "aagdpr")
AVOID_CDN = True


# TN-NT Auth Templates
INSTALLED_APPS.insert(0, "tnnt_templates")
```
