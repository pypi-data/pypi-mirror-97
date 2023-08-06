"""
Creates Slack Block Kit elements
"""

def header(text):
    d = {}
    d["type"] = "header"
    d["text"] = {
        "type": "plain_text",
        "text": text,
        "emoji": True
    }

    return d

def divider():
    d = {
        "type": "divider"
    }
    return d

def two_columns_mrkdown(col1_text, col2_text):
    d = {
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": col1_text
            },
            {
                "type": "mrkdwn",
                "text": col2_text
            }
        ]
    }

    return d