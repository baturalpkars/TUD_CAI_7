import os
import csv


# Mock function to simulate `_loadBelief`
def test_loadBelief():
    """
    Test the `_loadBelief` method to check if it correctly reads from a CSV file
    and initializes trust values for all team members.
    """
    # Test folder and file path
    test_folder = "test_beliefs"
    test_file_path = os.path.join(test_folder, "allTrustBeliefs.csv")

    # Ensure test folder exists
    os.makedirs(test_folder, exist_ok=True)

    # Create a mock CSV file with sample trust values
    with open(test_file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";", quotechar="'")
        writer.writerow(["name", "competence", "willingness"])  # Header row
        writer.writerow(["human1", "0.6", "0.7"])
        writer.writerow(["human2", "0.4", "0.5"])
        writer.writerow(["invalid_row"])  # Invalid row should be ignored

    # Define test members (including one that is NOT in the CSV file)
    test_members = ["human1", "human2", "human3"]

    # Expected trust values
    expected_output = {
        "human1": {"competence": 0.6, "willingness": 0.7},
        "human2": {"competence": 0.4, "willingness": 0.5},
        "human3": {"competence": 0.5, "willingness": 0.5},  # Not in CSV, should get defaults
    }

    # Function under test (copied from previous response)
    def _loadBelief(members, folder):
        trustBeliefs = {member: {"competence": 0.5, "willingness": 0.5} for member in members}  # Default values

        try:
            with open(folder + "/allTrustBeliefs.csv", "r") as csvfile:
                reader = csv.reader(csvfile, delimiter=";", quotechar="'")
                next(reader)  # Skip header row

                for row in reader:
                    if len(row) < 3:
                        continue  # Skip invalid rows

                    name, competence, willingness = row
                    competence = float(competence)
                    willingness = float(willingness)

                    if name in trustBeliefs:
                        trustBeliefs[name]["competence"] = competence
                        trustBeliefs[name]["willingness"] = willingness

        except FileNotFoundError:
            pass  # If file is missing, return default trust values

        return trustBeliefs

    # Run the function
    result = _loadBelief(test_members, test_folder)

    # Check if result matches expected output
    assert result == expected_output, f"Test Failed! Expected {expected_output}, but got {result}"

    print("✅ Test Passed! _loadBelief works correctly.")

    # Cleanup: Remove the test folder and file after the test
    os.remove(test_file_path)
    os.rmdir(test_folder)


# Run the test
test_loadBelief()
