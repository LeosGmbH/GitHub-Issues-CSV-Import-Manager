import csv
import requests

GITHUB_TOKEN = input("Enter your GitHub Personal Access Token: ")
REPO_OWNER = input("Enter your GitHub username or organization name: ")
REPO_NAME = input("Enter the repository name: ")
DELETE = input("Delete Files or Add Files? Enter 'delete' or 'add': ")
CSV_FILE = "issues.csv"

rest_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues'
graphql_url = 'https://api.github.com/graphql'

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_existing_issues():
    print("ℹ️ Fetching existing issues from GitHub...")
    all_issues = {}
    page = 1
    while True:
        params = {'state': 'open', 'per_page': 100, 'page': page}
        response = requests.get(rest_url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"❌ Error fetching issues: {response.status_code} - {response.text}")
            return {}

        issues = response.json()
        if not issues:
            break

        for issue in issues:
            all_issues[issue['title']] = issue['node_id'] 
        
        if len(issues) < 100:
            break
        page += 1
        
    print(f"✅ {len(all_issues)} issues found.")
    return all_issues

def delete_github_issue(issue_node_id, title):
    query = """
    mutation DeleteIssue($issueId: ID!) {
      deleteIssue(input: {issueId: $issueId}) {
        clientMutationId
      }
    }
    """
    variables = {"issueId": issue_node_id}
    
    graphql_data = {
        'query': query,
        'variables': variables
    }

    response = requests.post(graphql_url, json=graphql_data, headers=headers)
    
    if response.status_code == 200:
        if 'errors' in response.json():
            error_message = response.json()['errors'][0]['message']
            print(f'❌ Error deleting (GraphQL): {title} | {error_message}')
        else:
            print(f'💥 PERMANENTLY DELETED: {title} (Node ID: {issue_node_id})')
    else:
        print(f'❌ Failed to send GraphQL request: {title} | {response.status_code} - {response.text}')

def create_issue(title, body, labels, milestone_id):
    label_list = [l.strip() for l in labels.split(',')] if labels else []

    data = {
        'title': title, 
        'body': body,
        'labels': label_list
    }

    if milestone_id:
        try:
            data['milestone'] = int(milestone_id)
        except ValueError:
            print(f"⚠️ Milestone ID '{milestone_id}' is not a valid number. It will be ignored.")
            
    response = requests.post(rest_url, json=data, headers=headers)
    
    if response.status_code == 201:
        print(f'✅ Created: {title}')
    else:
        print(f'❌ Failed: {title} | {response.status_code} - {response.text}')

def delete_issues_from_csv(csv_file):
    existing_issues = get_existing_issues()
    issues_to_delete_count = 0

    if not existing_issues:
        print("ℹ️ No issues found for comparison or error during fetch.")
        return

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            csv_title = row['title'].strip()
            
            if csv_title in existing_issues:
                issue_node_id = existing_issues[csv_title]
                delete_github_issue(issue_node_id, csv_title)
                issues_to_delete_count += 1
    
    print(f"\n--- Deletion process complete ---\n{issues_to_delete_count} issues have been permanently deleted.")

def import_issues(csv_file):
    print("ℹ️ Starting issue import...")
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            create_issue(
                row['title'], 
                row['body'], 
                row.get('labels', ''),  
                row.get('milestone', '') 
            )
    print("\n--- Import complete ---")

if __name__ == '__main__':
    if DELETE.lower() == 'delete':
        delete_issues_from_csv(CSV_FILE)
    
    elif DELETE.lower() == 'add':
        import_issues(CSV_FILE)
        
    else:
        print("❌ Invalid input. Please enter 'delete' or 'add'.")