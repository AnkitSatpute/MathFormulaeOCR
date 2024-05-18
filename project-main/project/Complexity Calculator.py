#!/usr/bin/env python
# coding: utf-8

# In[7]:


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
            # Base case: if element has no children, return 1
            if len(element) == 0:
                return 1
            else:
                # Recursively compute depth of children
                children_depths = [compute_element_depth(child) for child in element]
                # Return 1 plus the maximum depth of children
                return 1 + max(children_depths)

        # Computing depth from the root element
        root_depth = compute_element_depth(mathml_tree)

        return root_depth - 1  # Subtract 1 since we started from depth 1 instead of 0

    except Exception as e:
        return None

def process_latex_files(directory):
    try:
        # Ensure the provided directory exists
        if not os.path.isdir(directory):
            print(f"The directory '{directory}' does not exist.")
            return
        
        # Initialize the frequency distribution for file complexities and error counts
        file_complexity_distribution = defaultdict(int)
        conversion_error_count = 0

        # Iterate through all .tex files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".tex"):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    latex_strings = file.readlines()

                # Initialize variables to calculate total complexity and count
                total_complexity_score = 0
                count = 0
                file_has_error = False

                # Process each LaTeX string in the file
                for latex_str in latex_strings:
                    latex_str = latex_str.strip()
                    if latex_str:
                        mathml_str = latex_to_mathml(latex_str)
                        if mathml_str:
                            complexity_score = compute_max_depth(mathml_str)
                            if complexity_score is not None:
                                total_complexity_score += complexity_score
                                count += 1
                        else:
                            file_has_error = True

                # Check if the file had a conversion error
                if file_has_error:
                    conversion_error_count += 1

                # Calculate the average complexity score for the file and update the distribution
                if count > 0:
                    average_complexity_score = total_complexity_score / count
                    file_complexity_distribution[round(average_complexity_score, 2)] += 1

        # Print the frequency distribution of the file complexities
        print("File Complexity Frequency Distribution:")
        for complexity, frequency in sorted(file_complexity_distribution.items()):
            print(f"Complexity: {complexity}, Frequency: {frequency}")
        
        # Print the count of files with conversion errors
        print(f"\nNumber of files with conversion errors: {conversion_error_count}")

    except Exception as e:
        print("Error processing LaTeX files:", e)

if __name__ == "__main__":
    directory = input("Enter the directory containing the .tex files:\n")
    process_latex_files(directory)


# In[ ]:




