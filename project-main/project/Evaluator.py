#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import numpy as np
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import json
import Levenshtein

# Download NLTK WordNet resource (if not already downloaded)
try:
    nltk.data.find('corpora/wordnet.zip')
except LookupError:
    print("Downloading NLTK WordNet resource...")
    nltk.download('wordnet')

def extract_text_from_latex(latex_file):
    """
    Extract text from a LaTeX file.
    """
    with open(latex_file, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def separate_text_and_math(latex_content):
    """
    Separate plain text and math expressions in a LaTeX document.
    """
    text_parts = []
    math_parts = []
    # Extended regex to include more LaTeX math environments and specific macros
    parts = re.split(
        r'(\$.*?\$|\$\$.*?\$\$|\\\(.*?\\\)|\\\[.*?\\\]|\\begin\{.*?\}.*?\\end\{.*?\}|\\mathrm\{.*?\}|'
        r'\\mathbb\{.*?\}|\\mathcal\{.*?\}|\\mathsf\{.*?\}|\\mathit\{.*?\}|\\mathfrak\{.*?\}|\\mathbf\{.*?\}|'
        r'\\left\{.*?\\right\}|\\left\(.*?\\right\)|\\left\[.*?\\right\]|\\frac\{.*?\}\{.*?\}|\\sqrt\{.*?\}|'
        r'\\sum|\\prod|\\int|\\lim|\\sin|\\cos|\\tan|\\log|\\ln|\\exp|\\alpha|\\beta|\\gamma|\\delta|'
        r'\\epsilon|\\zeta|\\eta|\\theta|\\iota|\\kappa|\\lambda|\\mu|\\nu|\\xi|\\pi|\\rho|\\sigma|\\tau|'
        r'\\upsilon|\\phi|\\chi|\\psi|\\omega|\\Gamma|\\Delta|\\Theta|\\Lambda|\\Xi|\\Pi|\\Sigma|\\Upsilon|'
        r'\\Phi|\\Psi|\\Omega)', latex_content, flags=re.DOTALL)
    
    for part in parts:
        if re.match(
            r'^\$.*\$$|^\$\$.*\$\$$|^\\\(.*\\\)$|^\\\[.*\\\]$|^\\begin\{.*\}.*\\end\{.*\}$|^\\mathrm\{.*\}$|'
            r'^\\mathbb\{.*\}$|^\\mathcal\{.*\}$|^\\mathsf\{.*\}$|^\\mathit\{.*\}$|^\\mathfrak\{.*\}$|^\\mathbf\{.*\}$|'
            r'^\\left\{.*\\right\}$|^\\left\(.*\\right\}$|^\\left\[.*\\right\]$|^\\frac\{.*\}\{.*\}$|^\\sqrt\{.*\}$|'
            r'^\\sum$|^\\prod$|^\\int$|^\\lim$|^\\sin$|^\\cos$|^\\tan$|^\\log$|^\\ln$|^\\exp$|^\\alpha$|^\\beta$|'
            r'^\\gamma$|^\\delta$|^\\epsilon$|^\\zeta$|^\\eta$|^\\theta$|^\\iota$|^\\kappa$|^\\lambda$|^\\mu$|'
            r'^\\nu$|^\\xi$|^\\pi$|^\\rho$|^\\sigma$|^\\tau$|^\\upsilon$|^\\phi$|^\\chi$|^\\psi$|^\\omega$|'
            r'^\\Gamma$|^\\Delta$|^\\Theta$|^\\Lambda$|^\\Xi$|^\\Pi$|^\\Sigma$|^\\Upsilon$|^\\Phi$|^\\Psi$|^\\Omega$', 
            part, flags=re.DOTALL):
            math_parts.append(part)
        else:
            text_parts.append(part)
    return ' '.join(text_parts), ' '.join(math_parts)

def compute_metrics(pred, gt, minlen=4):
    metrics = {}
    if len(pred) < minlen or len(gt) < minlen:
        return metrics
    metrics["edit_dist"] = Levenshtein.distance(pred, gt) / max(len(pred), len(gt))
    reference = gt.split()
    hypothesis = pred.split()
    metrics["bleu"] = sentence_bleu([reference], hypothesis, smoothing_function=SmoothingFunction().method1)
    try:
        from nltk.translate.meteor_score import meteor_score
        metrics["meteor"] = meteor_score([reference], hypothesis)
    except ImportError:
        metrics["meteor"] = np.nan
    reference = set(reference)
    hypothesis = set(hypothesis)
    metrics["precision"] = len(reference.intersection(hypothesis)) / len(hypothesis)
    metrics["recall"] = len(reference.intersection(hypothesis)) / len(reference)
    metrics["f_measure"] = 2 * metrics["precision"] * metrics["recall"] / (metrics["precision"] + metrics["recall"])
    return metrics

def get_input():
    predicted_text_path = input("Enter path to predicted LaTeX file: ")
    ground_truth_text_path = input("Enter path to ground truth LaTeX file: ")
    
    # Extract text from LaTeX files
    predicted_text = extract_text_from_latex(predicted_text_path)
    ground_truth_text = extract_text_from_latex(ground_truth_text_path)
    
    return predicted_text, ground_truth_text

if __name__ == "__main__":
    predicted_text, ground_truth_text = get_input()
    
    # Separate text and math
    pred_text, pred_math = separate_text_and_math(predicted_text)
    gt_text, gt_math = separate_text_and_math(ground_truth_text)
    
    # Calculate metrics for text
    text_metrics = compute_metrics(pred_text, gt_text)
    
    # Calculate metrics for math
    math_metrics = {}
    if pred_math and gt_math:
        math_metrics = compute_metrics(pred_math, gt_math)
    
    # Combine metrics
    metrics = {"text": text_metrics, "math": math_metrics}
    
    # Display results
    print("Metrics:")
    for category, category_metrics in metrics.items():
        print(f"{category} metrics:")
        for metric, value in category_metrics.items():
            print(f"  {metric}: {value}")
    

