import os
from collections import defaultdict
from latex2mathml.converter import convert
from xml.etree import ElementTree as ET

def latex_to_mathml(latex_str):
    try:
        mathml_str = convert(latex_str)
        # Remove xmlns attribute
        mathml_str = mathml_str.replace(' xmlns="http://www.w3.org/1998/Math/MathML"', '')
        return mathml_str
    except Exception as e:
        return None

def compute_max_depth(mathml_str):
    try:
        # Parse the MathML string
        mathml_tree = ET.fromstring(mathml_str)

        # Recursive function to compute the depth of an element
        def compute_element_depth(element):
            # Base case: if element has no children, return 0 (since we start counting from the root itself)
            if len(element) == 0:
                return 0
            else:
                # Recursively compute depth of children
                children_depths = [compute_element_depth(child) for child in element]
                # Return 1 plus the maximum depth of children
                return 1 + max(children_depths)

        # Computing depth from the root element
        root_depth = compute_element_depth(mathml_tree)

        return root_depth + 1  # Add 1 to account for the root node

    except Exception as e:
        return None

def process_latex_files(directory):
    try:
        if not os.path.isdir(directory):
            print(f"The directory '{directory}' does not exist.")
            return
        
        # Folders for low and high complexity formulae
        low_complexity_folder = os.path.join(directory, 'low_complexity')
        high_complexity_folder = os.path.join(directory, 'high_complexity')
        os.makedirs(low_complexity_folder, exist_ok=True)
        os.makedirs(high_complexity_folder, exist_ok=True)

        # Frequency distribution for file complexities and error counts
        file_complexity_distribution = defaultdict(int)
        conversion_error_count = 0
        for filename in os.listdir(directory):
            if filename.endswith(".tex"):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    latex_strings = file.readlines()

                # To process each LaTeX string in the file:
                for latex_str in latex_strings:
                    latex_str = latex_str.strip()
                    if latex_str:
                        mathml_str = latex_to_mathml(latex_str)
                        if mathml_str:
                            complexity_score = compute_max_depth(mathml_str)
                            if complexity_score is not None:
                                # Complexity category 
                                target_folder = low_complexity_folder if complexity_score <= 6 else high_complexity_folder
                                target_path = os.path.join(target_folder, filename)
                                with open(target_path, 'a', encoding='utf-8') as target_file:
                                    target_file.write(latex_str + '\n')
                                file_complexity_distribution[complexity_score] += 1
                        else:
                            conversion_error_count += 1

        # Frequency distribution of the formulae complexities
        print("Expression Complexity Frequency Distribution:")
        for complexity, frequency in sorted(file_complexity_distribution.items()):
            print(f"Complexity: {complexity}, Frequency: {frequency}")
        
        # Count of files with conversion errors
        print(f"\nNumber of expressions with conversion errors: {conversion_error_count}")

    except Exception as e:
        print("Error processing LaTeX files:", e)

if __name__ == "__main__":
    directory = input("Enter the directory containing the .tex files:\n")
    process_latex_files(directory)
