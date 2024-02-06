import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn import datasets

def load_dataset(dataset_name):
    if dataset_name == "Iris":
        data = datasets.load_iris()
    elif dataset_name == "Breast Cancer":
        data = datasets.load_breast_cancer()
    elif dataset_name == "Wine":
        data = datasets.load_wine()
    elif dataset_name == "Digits":
        data = datasets.load_digits()
    elif dataset_name == "Diabetes":
        data = datasets.load_diabetes()
    else:
        raise ValueError("Invalid dataset name")
    
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, tuple):
        return data[0], data[1]
    else:
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df["target"] = data.target
        return df

# Sidebar for user input
dataset_name = st.sidebar.selectbox("Choose Dataset", ("Iris", "Breast Cancer", "Wine", "Digits", "Diabetes"))
test_size = st.sidebar.slider("Select Test Size", 0.1, 0.5, 0.2)
n_neighbors = st.sidebar.slider("Select Number of Neighbors (k)", 1, 20, 5)

# Load the selected dataset
data = load_dataset(dataset_name)

# Handle NaN values
data.dropna(inplace=True) 

# Split the data into features and target variable
if isinstance(data, pd.DataFrame):
    X = data.drop("target", axis=1)
    y = data["target"]
else:
    X, y = data

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

# Train the kNN model
knn_model = KNeighborsClassifier(n_neighbors=n_neighbors)
knn_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = knn_model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Display evaluation metrics
st.title("k-Nearest Neighbors (kNN) Streamlit App")
# Display the dataset as a table
st.subheader("Dataset")
if isinstance(data, pd.DataFrame):
    st.write(data)
elif isinstance(data, tuple):
    X_df = pd.DataFrame(data[0], columns=data.feature_names)
    y_df = pd.DataFrame(data[1], columns=["target"])
    st.write(X_df.join(y_df))
else:
    st.write(data)
st.write(f"Dataset: {dataset_name}")
st.write(f"Number of Neighbors (k): {n_neighbors}")
st.write(f"Test Size: {test_size}")
st.write("Accuracy:", accuracy)

# Plot graph between k values and accuracy
k_values = list(range(1, 21))  # Range of k values
accuracies = []

for k in k_values:
    knn_model = KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(X_train, y_train)
    y_pred = knn_model.predict(X_test)
    accuracies.append(accuracy_score(y_test, y_pred))

# Plot graph
fig, ax = plt.subplots()
ax.plot(k_values, accuracies)
ax.set_title("Accuracy vs. Number of Neighbors (k)")
ax.set_xlabel("Number of Neighbors (k)")
ax.set_ylabel("Accuracy")
st.pyplot(fig)
