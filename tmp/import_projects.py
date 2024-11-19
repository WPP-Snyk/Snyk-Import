import json
import os
import subprocess

# File path for import-projects.json
json_file = 'import-projects.json'

# Function to read the existing JSON and append the new target
def update_json_file(orgId, integrationId, owner, repo_name, branch_name):
    # Load the existing data from the JSON file if it exists
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
    else:
        data = {"targets": []}  # Initialize a new structure if the file doesn't exist

    # New target to be added
    new_target = {
        "orgId": orgId,
        "integrationId": integrationId,
        "target": {
            "name": repo_name,
            "owner": owner,
            "branch": branch_name
        }
    }

    # Append the new target
    data["targets"].append(new_target)

    # Write the updated data back to the JSON file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f'Updated {json_file} with the new target:')
    print(json.dumps(new_target, indent=4))

# Function to create a PR in the GitHub repository
def create_pr(branch_name, repo_name="Snyk-WPP/Snyk-Import"):
    # Stage the changes
    subprocess.run(["git", "add", json_file])

    # Commit the changes
    commit_message = f"Add new import target for {branch_name}"
    subprocess.run(["git", "commit", "-m", commit_message])

    # Create a new branch
    subprocess.run(["git", "checkout", "-b", branch_name])

    # Push the branch
    subprocess.run(["git", "push", "origin", branch_name])

    # Use the GitHub CLI (gh) to create a PR
    subprocess.run(["gh", "pr", "create", "--title", commit_message, "--body", "Adding new import target", "--repo", repo_name])

# Main function to ask for inputs and update the JSON
def main():
    # Predefined orgId and integrationId
    orgId = "e0587f5d-e98d-4169-add8-989ec4b1e4e1"
    integrationId = "6ed0fc33-1d7c-4732-a2f3-d29f841dd2cb"

    # Ask for the organization (GitHub owner)
    org_choice = input("Enter the GitHub Org (owner) name: ").strip()

    # Ask for the repository name
    repo_choice = input("Enter the repository name you want to import: ").strip()

    # Ask for the branch name
    branch_choice = input("Enter the branch name you want to import: ").strip()

    # Update the JSON file with the provided details
    update_json_file(orgId, integrationId, org_choice, repo_choice, branch_choice)

    # Ask for a new branch name to open a PR
    pr_branch_name = input("Enter the name of the new branch for the PR: ").strip()

    # Create a PR with the changes
    create_pr(pr_branch_name)

# Run the program
if __name__ == "__main__":
    main()
