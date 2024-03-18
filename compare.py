import os


def get_all_filenames_in_directory(directory):
    # Initialize an empty list to store all filenames
    all_filenames = []

    # Walk through the directory tree and collect filenames
    for root, dirs, files in os.walk(directory):
        for filename in files:
            all_filenames.append(filename)

    return all_filenames


def compare_directories(directory1, directory2):
    # Get list of filenames in each directory
    filenames1 = get_all_filenames_in_directory(directory1)
    filenames2 = get_all_filenames_in_directory(directory2)

    # Compare the filenames
    common_files = set(filenames1) & set(filenames2)
    unique_files1 = set(filenames1) - set(filenames2)
    unique_files2 = set(filenames2) - set(filenames1)

    # Print the comparison results
    print(f"\nFiles unique to {directory1}_{len(filenames1)}")
    print("\n".join(sorted(unique_files1)))
    print(f"\nFiles unique to {directory2}_{len(filenames2)}")
    print("\n".join(sorted(unique_files2)))
    # find_duplicates(filenames1)
    # find_duplicates(filenames2)


def find_duplicates(lst):
    # Initialize an empty set to store unique elements
    seen = set()

    # Initialize an empty list to store duplicate elements
    duplicates = []

    # Iterate over the elements of the list
    for item in lst:
        # If the element is already in the set, it's a duplicate
        if item in seen:
            duplicates.append(item)
        else:
            # Otherwise, add it to the set of seen elements
            seen.add(item)

    print(sorted(duplicates))
    print(len(duplicates))


def main_compare():
    # Example usage:
    directory1 = "Z:\\Cloud Backed Up Files\\Pictures\\_Archive\\_Sorted"
    directory2 = "Z:\\Cloud Backed Up Files\\Pictures\\Family Photos"
    compare_directories(directory1, directory2)
