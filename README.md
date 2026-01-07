# Satellite Imagery Based Property Valuation

This file contains instructions on how to setup project and run the code.

Clone the repository (training the model requires high GPU Power so use some external GPU or Kaggle)
<ol>
<li> Downloading images using data_fetcher.py:
In this file enter the API Key, csv file path, output folder name, & image parameters like zoom level and size(by default set to 20 and 640 x 640 respectively). You can use any API of your choice. This file uses Google Map Static API. Images will take some time to download approx 2000 images / h. The file also tracks which image couldn't be saved in the terminal.</li>

<li> Preprocessing the data using preprocessing.ipynb:
Enter the csv file path that contains your data. Run each cell one by one. This notebook not only analyses the existing data but all engineers new features that give better results in prediction. New data file gets saved.</li>

<li> Prediction using model_training.ipynb:
Enter the csv file path and image file path. 
Run all the cells.<br>
To use xgboost model use: <br>         
                                    df = pd.read_csv('file.csv') <br>    
                                    exclude_cols = ['id','date']<br>
                                    feature_cols = [col for col in testing_data.columns if col not in exclude_cols]<br>
                                    X = df[feature_cols_pros].values<br>
                                    X_scaled = scaler_pros.transform(X)<br>
                                    y_pred= xgb_model_pros.predict(X_scaled)

To use hybrid model use: <br>           
                                    df = pd.read_csv('file.csv')<br>
                                    exclude_cols = ['id','date']<br>
                                    feature_cols = [col for col in testing_data.columns if col not in exclude_cols]<br>
                                    X = df[feature_cols_pros].values<br>
                                    X_scaled = scaler_pros.transform(X)<br>
                                    id = X['id']<br>
                                    y = np.zeros(X.shape[0])<br>
                                    gen = multimodal_generator(id, X_scaled, y, BATCH_SIZE=16)<br>
                                    steps = len(ids) // BATCH_SIZE<br>
                                    y_pred = cnn_model_pros.predict(gen, steps=steps, verbose=1).flatten()<br>

This file also compares the performance of both models : Xgboost and Hybrid and showcases training history of hybrid model & Grad-CAM visualisation.</li>
</ol>

