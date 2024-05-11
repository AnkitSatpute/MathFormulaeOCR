#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from latex2mathml.converter import convert
from xml.etree import ElementTree as ET

def latex_to_mathml(latex_str):
    try:
        mathml_str = convert(latex_str)
        # Remove xmlns attribute
        mathml_str = mathml_str.replace(' xmlns="http://www.w3.org/1998/Math/MathML"', '')
        return mathml_str
    except Exception as e:
        print("Error:", e)
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

        # Start computing depth from the root element
        root_depth = compute_element_depth(mathml_tree)

        return root_depth - 1  # Subtract 1 since we started from depth 1 instead of 0

    except Exception as e:
        print("Error:", e)
        return None

# Example LaTeX string
latex_string = r"\frac{1}{\sqrt{x^2 + \frac{1}{2} \cdot \left(1 + \frac{1}{\sqrt{2}}\right)} + \sqrt{x^2 + \frac{1}{2} \cdot \left(1 + \frac{1}{\sqrt{3}}\right)} + \sqrt{x^2 + \frac{1}{2} \cdot \left(1 + \frac{1}{\sqrt{4}}\right)} + \sqrt{x^2 + \frac{1}{2} \cdot \left(1 + \frac{1}{\sqrt{5}}\right)} + \sqrt{x^2 + \frac{1}{2} \cdot \left(1 + \frac{1}{\sqrt{6}}\right)} + \sqrt{x^2 + \frac{1}{2} \cdot \left(1 + \frac{1}{\sqrt{7}}\right)} + \sqrt{x^2 + \frac{1}{2} \cdot \left(1 + \frac{1}{\sqrt{8}}\right)}}"


# Convert LaTeX to MathML
mathml_string = latex_to_mathml(latex_string)

if mathml_string:
    # Compute and print the maximum depth of the MathML representation
    max_depth = compute_max_depth(mathml_string)
    if max_depth is not None:
        print("Complexity score:", max_depth)
    else:
        print("Failed to compute maximum depth.")
else:
    print("Conversion failed.")

