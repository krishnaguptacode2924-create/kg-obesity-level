def KG_Obesity_Predict(feature_dictionary):

    import pandas as pd
    import joblib as jb

    model  = jb.load("KG_Obesity_Artifact/KG_Obesity_Predictor.joblib")
    target = jb.load("KG_Obesity_Artifact/KG_Encoder_Obesity_Level.joblib")
    mtrans = jb.load("KG_Obesity_Artifact/KG_Encoder_MTRANS.joblib")
    calc   = jb.load("KG_Obesity_Artifact/KG_Encoder_CALC.joblib")
    caec   = jb.load("KG_Obesity_Artifact/KG_Encoder_CAEC.joblib")

    df = pd.DataFrame([feature_dictionary])

    # For Female feature, transform Male/Female to 0/1
    df["Female"] = df["Female"].map({"Female": 1, "Male": 0})

    # For Family_History feature, transform No/Yes to 0/1
    df["Family_History"] = df["Family_History"].map({"Yes": 1, "No": 0})

    # For FAVC feature, transform No/Yes to 0/1
    df["FAVC"] = df["FAVC"].map({"Yes": 1, "No": 0})

    # For SMOKE feature, transform No/Yes to 0/1
    df["SMOKE"] = df["SMOKE"].map({"Yes": 1, "No": 0})

    # For SCC feature, transform No/Yes to 0/1
    df["SCC"] = df["SCC"].map({"Yes": 1, "No": 0})

    # For MTRANS feature, encode input using encoder
    df['MTRANS'] = mtrans.transform(df['MTRANS'])

    # For CALC feature, encode input using encoder
    df['CALC'] = calc.transform(df['CALC'])

    # For CAEC feature, encode input using encoder
    df['CAEC'] = caec.transform(df['CAEC'])

    # For BMI feature, combine Weight and Height inputs
    df['BMI'] = df['Weight'] / (df['Height'] ** 2)
    df = df[
        [
            'Female', 'Age', 'BMI', 'Family_History', 
            'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE',
            'CH2O', 'SCC', 'FAF', 'TUE', 'CALC', 'MTRANS'
            ]
            ]

    prediction = model.predict(df)   
    label = target.inverse_transform(prediction)      
    result = label[0].replace("_", " ")

    probabilities = model.predict_proba(df)[0]
    confidence = round(float(max(probabilities) * 100), 2)

    return {
        "Prediction": result,
        "Confidence_score": confidence
    }
