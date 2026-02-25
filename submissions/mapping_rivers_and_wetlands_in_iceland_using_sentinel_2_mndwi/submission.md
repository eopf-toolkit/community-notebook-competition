---
contact_name: "Harsh Shinde"
email_address: "lmfphks8@gmail.com"
notebook_authors: ["Harsh Shinde"]
notebook_title: "Mapping Rivers and Wetlands in Iceland using Sentinel-2 MNDWI"
docker_image_used: "Python" 
makes_use_of_eopf_zarr_sample_service_data: true 
incorporates_one_or_more_eopf_plugins: true
data_sources_used: ["Sentinel-2"] 
had_challenges_working_with_sample_service_data: false 
all_declarations_affirmed: true
---

# Submission

## Abstract (100 words)

This notebook presents a workflow for mapping rivers and wetlands in Iceland using Sentinel-2 Level-2A multispectral imagery. Surface reflectance data are preprocessed using scale and offset correction, spatial resampling, and cloud masking to ensure reliable analysis. The Modified Normalized Difference Water Index (MNDWI) is applied to perform water feature detection by leveraging spectral differences between green and shortwave infrared bands. Threshold-based classification enables the separation of permanent water bodies from seasonal wetlands. The workflow visualizes rivers and wetlands, demonstrating how satellite-based spectral index data can effectively identify and map water bodies.

## AI Disclosure: Describe how you used AI in authoring this notebook (100 words)

AI tools used to support the development of this notebook by assisting with code refinement, documentation clarity. GPT helped improve the structure of Markdown explanations for better readability. It also provided optimization ideas during the workflow design. AI-generated suggestions were reviewed, tested, and adjusted as needed to ensure correctness and alignment with the project’s objectives.

## References: Provide the URLs of all code sources that you used in authoring this notebook

- EOPF 101 Documentation: https://eopf-toolkit.github.io/eopf-101/
- MNDWI Water Index Reference: Xu, H. (2006). Modification of normalised difference water index (NDWI)
- Analyzing and monitoring floods using Python and Sentinel-2 satellite imagery on Creodias: https://creodias.docs.cloudferro.com/en/latest/cuttingedge/Analyzing-and-monitoring-floods-using-Python-and-Sentinel-2-satellite-imagery-on-Creodias.html

## Feedback (If you answered `true` to `had_challenges_working_with_sample_service_data` please provide feedback here!)


## Declarations
By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.

## Notes (optional)
