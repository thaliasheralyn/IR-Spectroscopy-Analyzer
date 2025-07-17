IR-Spectroscopy-Analyzer

- Overview
Infrared (IR) Spectroscopy is a powerful analytical chemistry method used to predict chemical structures by examining how molecules absorb infrared electromagnetic waves. It’s commonly used to confirm the existence of functional groups during chemical synthesis. Different functional groups and bonds absorb IR waves at specific wavelengths, producing a unique spectrum for each compound.

- Motivation
Manual interpretation of IR spectra is prone to bias:

1. Picking peaks manually can introduce errors.
2. Overlapping peaks may be hard to distinguish.
3. Constantly referring to tables is time-consuming.
4. Additionally, IR spectroscopy data is typically presented as transmittance, which can introduce significant biases. To improve clarity and accuracy, the raw data is transformed using the following approach:

- Transforms the relationship: Converts transmittance (which decreases in a valley-like shape) into absorbance.
- Enhances clarity: A logarithmic transformation magnifies differences in low transmittance values, making subtle features more visible and easier to analyze.

- This project aims to automate and enhance the analysis of IR spectroscopy data
1. Processing raw transmittance data into absorbance for clearer visualization.
2. Reducing manual effort and bias in peak selection.
3. Making spectrum analysis faster and more reliable for chemists.
