import os
import subprocess
from datetime import datetime, timedelta

def parse_grid(file_path, start_date):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    commit_dates = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line.strip().split()):
            if char == '*':
                # Calculate the date for this position
                commit_date = start_date + timedelta(weeks=j, days=i)
                commit_dates.append(commit_date)
    return commit_dates

def make_empty_commit_on_date(commit_date):
    # Set the GIT_AUTHOR_DATE and GIT_COMMITTER_DATE environment variables
    env = os.environ.copy()
    date_str = commit_date.strftime('%a %b %d %H:%M:%S %Y %z')
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str

    # Create an empty commit with the specified date
    commit_message = f"Empty commit for {commit_date.strftime('%Y-%m-%d')}"
    subprocess.run(['git', 'commit', '--allow-empty', '--date', date_str, '-m', commit_message], check=True, env=env)

def main():
    # Prompt the user to enter the desired year
    year_input = input("Enter the year for the contribution graph (e.g., 2021): ")

    # Validate the user input
    try:
        year = int(year_input)
        if year < 1900 or year > 2100:
            raise ValueError("Year out of range. Please enter a year between 1900 and 2100.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    # Prompt the user to enter the file path
    file_path = input("Enter the path to your test.txt file: ")

    # Validate the file path
    if not os.path.isfile(file_path):
        print(f"Error: The file at {file_path} does not exist.")
        return

    # Set the starting date to the first Sunday of the specified year
    start_date = datetime(year, 1, 1)
    while start_date.weekday() != 6:  # 6 corresponds to Sunday
        start_date += timedelta(days=1)

    # Parse the grid and get commit dates
    commit_dates = parse_grid(file_path, start_date)

    # Make empty commits on the specified dates
    for commit_date in commit_dates:
        make_empty_commit_on_date(commit_date)
        print(f"Made empty commit for {commit_date.strftime('%Y-%m-%d')}")

if __name__ == '__main__':
    main()
