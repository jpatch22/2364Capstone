import torch
import torch.nn as nn

class ImageClassifier(nn.Module):
    def __init__(self, height, width, num_classes):
        super().__init__()
        
        # Define convolutional layers
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.relu = nn.ReLU()
        
        # Calculate the size of the feature map after convolution and pooling
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.feature_size = self._get_conv_output_size(height, width)
        
        # Define fully connected layers
        self.fc1 = nn.Linear(128 * self.feature_size * self.feature_size, 512)
        self.fc2 = nn.Linear(512, num_classes)
        
        
        # Define dropout layer
        self.dropout = nn.Dropout(p=0.5)
        
    def forward(self, x):
        # Convolutional layers with ReLU activation and max pooling
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        
        # Flatten the input for fully connected layers
        x = x.view(-1, 128 * self.feature_size * self.feature_size)
        
        # Fully connected layers with ReLU activation and dropout
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        
        return x
    
    def _get_conv_output_size(self, height, width):
        # Function to compute the size of the feature map after convolution and pooling
        print("entering func")
        print("self", self.relu)
        x = torch.randn(1, 3, height, width)
        x = self.pool(self.relu(self.conv1(x)))
        print("after")
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        return x.size(2)  # Assuming square feature maps

