# MathFormulaeOCR
Repository of the experiments performed in creating a state-of-the-art Math formula character and layout recognition methods.


## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Results](#results)
6. [Contributing](#contributing)
7. [Acknowledgement](#acknowledgement)

## Introduction

Accurately recognizing and understanding mathematical formulae in scientific documents is a challenging problem in artificial intelligence and machine learning. This repository explores experiments conducted to advance the state-of-the-art in mathematical formulae character and layout recognition.

## Features

- Technique for enhancing the recognition of mathematical formulae.
- Evaluation metrics used to measure the performance of the recognition method.

## Installation

To use the code in this repository, follow these steps:

1. Clone the repository:
    git clone https://github.com/AnkitSatpute/MathFormulaeOCR.git
   
2. Install dependencies:
   pip install -r requirements.txt

## Usage
Place the PDF to be converted to LaTeX in the folder "pdfs", specify the PDF location and the location for LaTeX output, and run the command: 
                python convert_pdf.py --input_folder "PDF location" --output_folder "LaTeX location"

### Evaluation
    Execute the script "Evaluate.py" and enter the locations of detected and ground truth LaTeX files. The evaluation metrics will be computed and printed on the console. 

## Results

| Experiment      | Precision | Recall | F-measure |
|-----------------|-----------|--------|-----------|
| Low complexity  | 57%       | 39%    | 47%       |
| High complexity | 57%       | 37%    | 42%       |



## Contributions
Contributions of any kind are welcome.

## Acknowledgement
Codes taken and modified from 
- https://github.com/facebookresearch/nougat
- https://github.com/lukas-blecher/LaTeX-OCR
- https://github.com/breezedeus/CnSTD



