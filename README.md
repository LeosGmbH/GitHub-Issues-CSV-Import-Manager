# GitHub-Issues-CSV-Import-Manager
A versatile Python script to bulk-manage GitHub Issues using a CSV file. It supports importing new issues (add mode) and permanently deleting existing issues by title (delete mode) via the GitHub REST and GraphQL APIs.

## ✨ Features

- **Dual Mode Operation**: Add new issues or permanently delete existing ones
- **Bulk Processing**: Handle multiple issues in a single operation
- **Comprehensive Metadata**: Support for titles, descriptions, labels, and milestones
- **GraphQL Integration**: Secure issue deletion through GitHub's GraphQL API
- **Detailed Logging**: Clear status updates and error messages

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install requests
   ```

2. **Prepare Your CSV**
   Create a CSV file with the following structure:
   ```csv
   title,body,labels,milestone
   "Login bug","Cannot login","bug",1
   "Add button","Need a button","enhancement,ui,feature",2
   "Fix text","Text is wrong","bug,ui",1
   ```

3. **Run the Script**
   ```bash
   python issue_manager.py
   ```
   Follow the interactive prompts to configure your operation.

## 📋 CSV Format Reference

| Column    | Required | Description                                      |
|-----------|----------|--------------------------------------------------|
| title     | Yes      | Issue title                                      |
| body      | No       | Detailed issue description                       |
| labels    | No       | Comma-separated list of labels (e.g., "bug,UI") |
| milestone | No       | Milestone ID (must be a number)                  |

## 🔧 Usage Modes

### Adding Issues
1. Set up your CSV file with issue details
2. Run the script and select 'add' mode
3. Enter your GitHub credentials when prompted

### Deleting Issues
1. Create a CSV file with 'title' column matching issues to delete
2. Run the script and select 'delete' mode
3. The script will find and remove matching issues

## 🔒 Authentication

1. Generate a [Personal Access Token](https://github.com/settings/tokens) with these scopes:
   - `repo` (for private repositories)
   - `public_repo` (for public repositories)

## ⚠️ Important Notes

- **Deletion is permanent**: Issues deleted using this tool cannot be recovered
- **Rate Limits**: GitHub enforces API rate limits (5,000 requests/hour for authenticated users)
- **CSV Encoding**: Save your CSV file with UTF-8 encoding to handle special characters

## 🐛 Troubleshooting

### Common Issues
- **401 Unauthorized**: Verify your access token has the correct permissions
- **404 Not Found**: Check repository name and owner
- **Validation Failed**: Ensure milestone IDs are valid numbers
- **CSV Errors**: Verify file path and encoding

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
