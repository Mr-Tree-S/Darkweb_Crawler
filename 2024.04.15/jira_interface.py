from jira import JIRA


def get_jira_instance(token):
    jira_server_url = "https://xxxxxx.com"
    jira = JIRA(jira_server_url, token_auth=token)
    return jira

def update_jira_field(issue, new_labels):
    current_labels = issue.get_field("labels")
    print(current_labels)
    if new_labels not in current_labels:
        updated_labels = current_labels + new_labels
        issue.update(fields={"labels": updated_labels})

def create_jira_issue(jira, new_issue_data):
    jira.create_issue(fields=new_issue_data)

""" test

# Setup Jira connection
token = "xxxxx"
jira = get_jira_instance(token)

# Format all post titles into a single description string
description = "Found suspicious entries:\n"

# Define issue data based on the information collected
new_issue_data = {
    'project': 'DEMO',
    'summary': 'LockBit Monitor',
    'description': description,
    'issuetype': 'Incident'
}

# Create the Jira issue
create_jira_issue(jira, new_issue_data)

"""