# Importing necessary libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import tensorflow as tf
from tensorflow.keras import layers
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Step 1: Data Creation and Preprocessing
# ----------------------------------------

# Creating a synthetic dataset using sklearn
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, weights=[0.9, 0.1], random_state=42)

# Splitting the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Handling imbalanced data using SMOTE
smote = SMOTE(random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)

# Normalizing the data
scaler = StandardScaler()
X_train_sm = scaler.fit_transform(X_train_sm)
X_test = scaler.transform(X_test)

# Step 2: Data Visualization using Seaborn and Matplotlib
# -------------------------------------------------------

# Plotting the class distribution
sns.countplot(x=y_train_sm)
plt.title('Class Distribution After SMOTE')
plt.show()

# Plotting feature distributions
plt.figure(figsize=(12, 6))
sns.histplot(X_train_sm[:, 0], kde=True)
plt.title('Feature Distribution')
plt.show()

# Step 3: Training a Random Forest Classifier using Scikit-learn
# --------------------------------------------------------------

# Training a random forest classifier
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train_sm, y_train_sm)

# Making predictions
y_pred_rf = rf_model.predict(X_test)

# Evaluating the model
print("Random Forest Accuracy:", accuracy_score(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

# Step 4: Building a Neural Network with TensorFlow/Keras
# -------------------------------------------------------

# Building a simple neural network using Keras
model = tf.keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_train_sm.shape[1],)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compiling the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Training the model
model.fit(X_train_sm, y_train_sm, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Evaluating the model
loss, accuracy = model.evaluate(X_test, y_test)
print("Keras Model Accuracy:", accuracy)

# Step 5: Building a Neural Network with PyTorch
# ----------------------------------------------

# Converting data to PyTorch tensors
X_train_torch = torch.tensor(X_train_sm, dtype=torch.float32)
y_train_torch = torch.tensor(y_train_sm, dtype=torch.float32).view(-1, 1)
X_test_torch = torch.tensor(X_test, dtype=torch.float32)
y_test_torch = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

# Creating a simple neural network model
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(X_train_sm.shape[1], 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        return x

# Initializing the model, loss function, and optimizer
model_torch = SimpleNN()
criterion = nn.BCELoss()
optimizer = optim.Adam(model_torch.parameters(), lr=0.001)

# Training the model
num_epochs = 10
for epoch in range(num_epochs):
    model_torch.train()
    optimizer.zero_grad()
    outputs = model_torch(X_train_torch)
    loss = criterion(outputs, y_train_torch)
    loss.backward()
    optimizer.step()

    print(f'Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}')

# Evaluating the model
model_torch.eval()
with torch.no_grad():
    y_pred_torch = model_torch(X_test_torch)
    y_pred_torch = (y_pred_torch > 0.5).float()
    accuracy_torch = (y_pred_torch == y_test_torch).float().mean()
    print("PyTorch Model Accuracy:", accuracy_torch.item())
