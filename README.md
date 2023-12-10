# ID2223_lab2
Lab 2 ID2223

Model-centric approach:
  - Disabled the use of reduced precision fp16;
  - Halved the learning rate from 1e-5 to 5e-6
  - Cut down the warmup steps to 50 and the overall steps to 1500 as we noticed very high overfitting after that point

Data-centric approach:
  - One way to improve upon the data would be to either figure out how to participate in the voting that's used to split the dataset into training, validation, test, other and try to influence it so the "other" split is moved into either training or test so we can increase the dataset
  - Another way to get data for this kind of training is to create a type of captcha that requires the user to read a phrase in their native language and collect that data
  - Data rows can be created manually based on complaints from customers (assuming some kind of commercial product that uses this model)
