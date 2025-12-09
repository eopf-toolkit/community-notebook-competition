---
contact_name: "Harsh Shinde"
email_address: "lmfphks8@gmail.com"
notebook_authors: ["Harsh Shinde"]
notebook_title: "Ocean Wind Field Classification Using CNNs and Sentinel-1 Level-2 OCN"
docker_image_used: "Python"
makes_use_of_eopf_zarr_sample_service_data: true
incorporates_one_or_more_eopf_plugins: true
data_sources_used: ["Sentinel-1"] 
had_challenges_working_with_sample_service_data: true 
all_declarations_affirmed: true
---

# Submission
  
## Abstract (100 words)
This notebook presents an end-to-end workflow for classifying ocean wind conditions using Sentinel-1 Level-2 Ocean (OCN) data accessed through the EOPF STAC service. We analyze 767 wind-field scenes over the North Sea (1°–8°E, 51°–55°N) from February to October 2025, converting SAR-derived wind speed grids into normalized 128×128 inputs for a Convolutional Neural Network (CNN). The model classifies wind regimes into Calm (≤5 m/s), Moderate (5–12 m/s), and High (>12 m/s) categories. Results demonstrate the effectiveness of CNN-based processing for automated marine wind monitoring, highlighting the utility of Sentinel-1 OCN products for operational ocean applications.

## AI Disclosure: Describe how you used AI in authoring this notebook (100 words)
AI tools were used to support the development of this notebook by assisting with code refinement, documentation clarity, debugging, and model setup. GPT helped improve the structure of Markdown explanations, reorganize sections for better readability, and suggest best practices for working with geospatial data. It also provided optimization ideas during the workflow design. AI-generated suggestions were reviewed, tested, and adjusted as needed to ensure correctness and alignment with the project’s objectives.

## References: Provide the URLs of all code sources that you used in authoring this notebook
- EOPF STAC API: https://stac.core.eopf.eodc.eu
- Sentinel-1 L2 OCN Zarr Product Exploration: https://eopf-sample-service.github.io/eopf-sample-notebooks/sentinel-1-l2-ocn-zarr-product-exploration/
- Sentinel-1 User Guide: https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-1-sar
- How to Plot Wind Speed and Direction in Python: https://www.geodose.com/2023/07/how-to-plot-wind-speed-and-direction-python.html
- Exploration of Sentinel-1 Level-2 Ocean Wind Field (OWI) component: https://github.com/chris010970/s1-ocn/blob/main/notebooks/owi-resample.ipynb

## Feedback (If you answered `true` to `had_challenges_working_with_sample_service_data` please provide feedback here!)
The available Sentinel-1 Level-2 OCN data for this region covered only a short temporal window (2025-02-24 to 2025-10-15). Having a longer time span or multi-year availability along with spatial coverage would make the dataset more versatile for different analysis approaches.

## Declarations
By submitting this notebook:
- I/we agree to abide by the competition rules.
- I/we confirm this submission is my/our own original work.
- I/we grant the European Space Agency and thriveGEO GmbH a non-exclusive license to use, reproduce, modify, and display my/our work for promotional and educational purposes, including featuring it in the EOPF 101 online book.
- I/we confirm that the code submitted may be published under the Apache 2 license.

## Notes (optional)