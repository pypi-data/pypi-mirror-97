# PSU-Infotext
Reusable Django app specifically for PSU's custom-built web applications.  
Provides the ability to include user-editable text in any site using the psu_base plugin.  
Includes:
-  Template tags for editable text
-  WYSIWYG interface for editing the text

## Quick Start

### Dependencies
The following dependency is REQUIRED and must be installed in your app:
- [psu-base](https://pypi.org/project/psu-base/)

### Installation
```shell script
pip install psu-infotext
```

### Configuration
1. Configure [psu-base](https://pypi.org/project/psu-base/) in your Django app
1. Add PSU-Infotext to your INSTALLED_APPS in `settings.py`:
    ```python
    INSTALLED_APPS = [
       ...
       'psu_base',
       'psu_infotext',
    ]
    ```
1. Configure your app's top-level `urls.py` to include Infotext views:
    ```python
    urlpatterns = [
        ...
        path('infotext/', include(('psu_infotext.urls', 'psu_infotext'), namespace='infotext')),
    ]
1. Run migrations: `python manage.py migrate`

## Usage
### Template Tags
The primary purpose of this app is to provide template tags that allow authorized users to 
update text on your site.  For a small amount of text, use the `{%infotext%}` tag.
For a larger amount of text, use the `{%infotext_block%}` tag.  
The following example uses both tags:
```
{% load infotext_taglib %}

<h1>{%infotext code="main_heading" alt="Hello, World!"%}</h1>

{%infotext_block code="example_content"%}
<p>
    This is an example of longer <em>infotext</em><br>
    <ul>
        <li>Bla bla bla</li>
        <li>...</li>
    </ul>
</p>
{%end_infotext_block%}
```

#### Required Attributes:
* **code**: This should uniquely identify the text for the page (url/path)
* **alt**: Alternate (default) text to use when not found in the database  
*(This only applies to the `{%infotext%}` tag. The body of the `{%infotext_block%}` tag is used as the alt text)*

#### Optional Attributes:
* **auto_prefix**: Defaults to True.  When true, the text will be made specific to the page by 
prepending the request path (url) to the **code** attribute.  Set this to False for any text that
is to be displayed on multiple pages (like an error message) to prevent multiple instances of the 
text that may get out-of-sync and display differently on different pages.
* **replacements**: This may be a dict, or string representation of a dict, with the key being the 
text to search for, and the value being the replacement text.

Additional documentation exists in 
[Confluence](https://portlandstate.atlassian.net/wiki/spaces/WDT/pages/713523250/Django+Infotext).