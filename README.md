# MathFormulaeOCR
Repository of the experiments performed in creating a state-of-the-art Math formula character and layout recognition method.


## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Evaluation](#evaluation)
4. [Results](#results)
5. [Contributions](#contributions)
6. [Acknowledgement](#acknowledgement)


## Installation

To use the code in this repository, follow these steps:

1. Clone the repository:
    git clone https://github.com/AnkitSatpute/MathFormulaeOCR.git
   
2. Install dependencies:
   pip install -r requirements.txt

## Usage
Place the PDF to be converted to LaTeX in the folder "pdfs", specify the PDF location and the location for LaTeX output, and run the command: 
                python convert_pdf.py --input_folder "PDF location" --output_folder "LaTeX location"

# Evaluation
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



