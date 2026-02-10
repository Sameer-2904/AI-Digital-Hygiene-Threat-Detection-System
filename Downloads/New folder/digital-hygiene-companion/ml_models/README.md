# ML Models Directory

This directory is reserved for trained machine learning models that can enhance detection accuracy.

## Planned Models

### 1. Phishing Email Classifier
- **Type**: Text Classification (Logistic Regression, Random Forest, or Neural Network)
- **Features**: Email content, headers, metadata
- **Training Data**: Public phishing datasets
- **Performance Target**: >95% accuracy

### 2. URL Maliciousness Predictor
- **Type**: Binary Classification
- **Features**: Domain characteristics, URL structure, content
- **Training Data**: URLhaus, PhishTank, Alexa Top Sites
- **Performance Target**: >90% accuracy

### 3. Social Engineering Pattern Detector
- **Type**: Sequence Classification / NLP
- **Features**: Text features, linguistic patterns
- **Training Data**: Labeled social engineering examples
- **Performance Target**: >85% accuracy

### 4. Credential Theft Attempt Classifier
- **Type**: Text Classification
- **Features**: Keywords, urgency indicators, requests
- **Training Data**: Phishing emails, legitimate communications
- **Performance Target**: >90% accuracy

## Current Implementation

The current version uses **rule-based and heuristic detection** without trained ML models. This approach:

### Advantages
- ✅ No external dependencies needed
- ✅ Transparent, interpretable decisions
- ✅ Works offline
- ✅ Fast inference
- ✅ Easy to understand and modify

### Limitations
- ⚠️ May have higher false positives
- ⚠️ Cannot adapt to new threats automatically
- ⚠️ Limited to predefined patterns

## Future Enhancements

### Phase 2: ML Integration
1. Collect labeled training data
2. Train multiple models
3. Implement model serving
4. Add periodic retraining

### Phase 3: Advanced AI
1. Large Language Models (LLMs) for context understanding
2. Ensemble methods combining multiple detectors
3. Anomaly detection for unknown threats
4. Behavioral analysis

## Installing Models

Once models are trained:

```bash
# Download models
python download_models.py

# Models will be stored in this directory
```

## Model Format

Preferred formats for portability:
- `.joblib` for scikit-learn models
- `.pkl` for any Python objects
- `.h5` or `.pb` for TensorFlow models
- `.pth` for PyTorch models

## Privacy Note

All models will be:
- Kept local on the user's device
- Never sent to external servers
- Queryable only offline or on the device
- Transparent about their operation

---

See main README.md for more information about the digital hygiene companion project.
