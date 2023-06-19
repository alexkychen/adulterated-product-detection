# adulterated-product-detection

## Background

Adulteration involves adding impurities or contaminants to a product to lower its quality or deceive consumers. Adulterated products are expected to have lower concentrations of certain compounds compared to their non-adulterated counterparts. Identifying such adulterated products can be challenging, especially when the concentrations of several analytes deviate from the average values but still fall within the normal range observed in non-adulterated counterparts. Traditional threshold-based methods struggle to detect these subtle variations within the normal range, as they primarily rely on identifying outliers or extreme deviations.

To overcome these challenges, I have developed an analytical tool that simulates adulteration scenarios and utilizes the DBSCAN machine learning clustering method (from Python scikit-learn). The tool allows for the construction of a model by using simulated datasets, enabling evaluation, fine-tuning, and improved detection of adulterated products exhibiting deviations within the normal range in real-world scenarios.

## Referenced data simulation

This tool includes a function `generate_ref_data` to generate a referenced dataset representing authentic or non-adulterated product data. This dataset serves as a reference for detecting adulterated samples. Parameters such as sample size, number of analytes, and analyte quantitative boundaries can be customized to simulate real-world data. After generating the referenced data, users can utilize it to create random samples, both adulterated and non-adulterated, for evaluating the performance of their model.

## Adulterated and non-adulterated products simulation

This tool also provides the `generate_random_sample` function, which generates a random sample to be combined with the referenced data for DBSCAN analysis. This function examines the referenced data input and creates either a non-adulterated or adulterated sample based on user specifications. This enables the evaluation of model performance metrics. For generating an adulterated sample, users can set parameters to determine the number of analytes and how their concentrations should be altered to mimic the chemical composition of an adulterated product. This allows for the identification of patterns in model detectability under different adulteration scenarios.






