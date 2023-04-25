# Linear-Regression-Visualization-Tool
JHU EN.601.664 AI - Final Project

This is a tool for processing Linear Regression with Gradient Descent based on python environment.

How to start:

- If ```ttkbootstrap``` not installed, you can install by : <br />
      - PyPI Installation:  ``` python -m pip install ttkbootstrap ```<br />
      - Github Installation: ```python -m pip install git+https://github.com/israel-dryer/ttkbootstrap```<br />
 
<br />
- Data Manipulate <br />
      -  **Add/Remove**: enter values for *X* and *Y*, then hit the **Add/Remove** button, only one copy of the data point will be removed for one hit of the button if there are multiple data points with the same value <br />
      - **Load/Save**: enter the file name (if same path as the .py file) or full path of the data, then will load/save the data<br />
      - **Clear**: clear all current data<br />

<br />
- Linear Regression<br />
      - Note: the loss function is $L = \frac{1}{n}\sum(y-\hat{y})$
      - **Start**: hit to start the Linear Regression with Gradient Descent based on current data. It will process automatically and generate a gif file to current path, then show the process in loop.
