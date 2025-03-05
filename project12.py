{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<h2 style='color:blue' align='center'>Small Image Classification Using Convolutional Neural Network (CNN)</h2>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "In this notebook, we will classify small images cifar10 dataset from tensorflow keras datasets. There are total 10 classes as shown below. We will use CNN for classification"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<img src=\"small_images.jpg\" />"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import tensorflow as tf\n",
    "from tensorflow.keras import datasets, layers, models\n",
    "import matplotlib.pyplot as plt\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<h4 style=\"color:purple\">Load the dataset</h4>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(50000, 32, 32, 3)"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "(X_train, y_train), (X_test,y_test) = datasets.cifar10.load_data()\n",
    "X_train.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(10000, 32, 32, 3)"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X_test.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Here we see there are 50000 training images and 1000 test images"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(50000, 1)"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y_train.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[6],\n",
       "       [9],\n",
       "       [9],\n",
       "       [4],\n",
       "       [1]], dtype=uint8)"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y_train[:5]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "y_train is a 2D array, for our classification having 1D array is good enough. so we will convert this to now 1D array"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "scrolled": True
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([6, 9, 9, 4, 1], dtype=uint8)"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y_train = y_train.reshape(-1,)\n",
    "y_train[:5]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "y_test = y_test.reshape(-1,)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "classes = [\"airplane\",\"automobile\",\"bird\",\"cat\",\"deer\",\"dog\",\"frog\",\"horse\",\"ship\",\"truck\"]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's plot some images to see what they are "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "def plot_sample(X, y, index):\n",
    "    plt.figure(figsize = (15,2))\n",
    "    plt.imshow(X[index])\n",
    "    plt.xlabel(classes[y[index]])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "scrolled": True
   },
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1080x144 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plot_sample(X_train, y_train, 0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1080x144 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plot_sample(X_train, y_train, 1)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Normalize the images to a number from 0 to 1. Image has 3 channels (R,G,B) and each value in the channel can range from 0 to 255. Hence to normalize in 0-->1 range, we need to divide it by 255"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<h4 style=\"color:purple\">Normalizing the training data</h4>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train = X_train / 255.0\n",
    "X_test = X_test / 255.0"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<h4 style=\"color:purple\">Build simple artificial neural network for image classification</h4>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "scrolled": True
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch 1/5\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 1.8074 - accuracy: 0.3561\n",
      "Epoch 2/5\n",
      "1563/1563 [==============================] - 2s 1ms/step - loss: 1.6208 - accuracy: 0.4285\n",
      "Epoch 3/5\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 1.5380 - accuracy: 0.4585\n",
      "Epoch 4/5\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 1.4808 - accuracy: 0.4806\n",
      "Epoch 5/5\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 1.4326 - accuracy: 0.4928\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "<tensorflow.python.keras.callbacks.History at 0x295ab873c10>"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "ann = models.Sequential([\n",
    "        layers.Flatten(input_shape=(32,32,3)),\n",
    "        layers.Dense(3000, activation='relu'),\n",
    "        layers.Dense(1000, activation='relu'),\n",
    "        layers.Dense(10, activation='softmax')    \n",
    "    ])\n",
    "\n",
    "ann.compile(optimizer='SGD',\n",
    "              loss='sparse_categorical_crossentropy',\n",
    "              metrics=['accuracy'])\n",
    "\n",
    "ann.fit(X_train, y_train, epochs=5)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "*You can see that at the end of 5 epochs, accuracy is at around 49%*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Classification Report: \n",
      "               precision    recall  f1-score   support\n",
      "\n",
      "           0       0.63      0.45      0.53      1000\n",
      "           1       0.72      0.46      0.56      1000\n",
      "           2       0.33      0.46      0.39      1000\n",
      "           3       0.36      0.25      0.29      1000\n",
      "           4       0.44      0.37      0.40      1000\n",
      "           5       0.34      0.46      0.39      1000\n",
      "           6       0.56      0.47      0.51      1000\n",
      "           7       0.39      0.67      0.50      1000\n",
      "           8       0.64      0.60      0.62      1000\n",
      "           9       0.59      0.53      0.55      1000\n",
      "\n",
      "    accuracy                           0.47     10000\n",
      "   macro avg       0.50      0.47      0.47     10000\n",
      "weighted avg       0.50      0.47      0.47     10000\n",
      "\n"
     ]
    }
   ],
   "source": [
    "from sklearn.metrics import confusion_matrix , classification_report\n",
    "import numpy as np\n",
    "y_pred = ann.predict(X_test)\n",
    "y_pred_classes = [np.argmax(element) for element in y_pred]\n",
    "\n",
    "print(\"Classification Report: \\n\", classification_report(y_test, y_pred_classes))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<h4 style=\"color:purple\">Now let us build a convolutional neural network to train our images</h4>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "cnn = models.Sequential([\n",
    "    layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(32, 32, 3)),\n",
    "    layers.MaxPooling2D((2, 2)),\n",
    "    \n",
    "    layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),\n",
    "    layers.MaxPooling2D((2, 2)),\n",
    "    \n",
    "    layers.Flatten(),\n",
    "    layers.Dense(64, activation='relu'),\n",
    "    layers.Dense(10, activation='softmax')\n",
    "])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "cnn.compile(optimizer='adam',\n",
    "              loss='sparse_categorical_crossentropy',\n",
    "              metrics=['accuracy'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {
    "scrolled": False
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch 1/10\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 1.4407 - accuracy: 0.4810\n",
      "Epoch 2/10\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 1.1084 - accuracy: 0.6109\n",
      "Epoch 3/10\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 0.9895 - accuracy: 0.6574\n",
      "Epoch 4/10\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 0.9071 - accuracy: 0.6870\n",
      "Epoch 5/10\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 0.8416 - accuracy: 0.7097\n",
      "Epoch 6/10\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 0.7847 - accuracy: 0.7262\n",
      "Epoch 7/10\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 0.7350 - accuracy: 0.7448\n",
      "Epoch 8/10\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 0.6941 - accuracy: 0.7574\n",
      "Epoch 9/10\n",
      "1563/1563 [==============================] - 2s 1ms/step - loss: 0.6516 - accuracy: 0.7731\n",
      "Epoch 10/10\n",
      "1563/1563 [==============================] - 2s 2ms/step - loss: 0.6187 - accuracy: 0.7836\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "<tensorflow.python.keras.callbacks.History at 0x296555783d0>"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cnn.fit(X_train, y_train, epochs=10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "*With CNN, at the end 5 epochs, accuracy was at around 70% which is a significant improvement over ANN. CNN's are best for image classification and gives superb accuracy. Also computation is much less compared to simple ANN as maxpooling reduces the image dimensions while still preserving the features*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {
    "scrolled": True
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "313/313 [==============================] - 0s 1ms/step - loss: 0.9022 - accuracy: 0.7028\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[0.9021560549736023, 0.7027999758720398]"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cnn.evaluate(X_test,y_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[4.3996371e-04, 3.4844263e-05, 1.5558505e-03, 8.8400185e-01,\n",
       "        1.9452239e-04, 3.5314459e-02, 7.2777577e-02, 6.9044131e-06,\n",
       "        5.6417785e-03, 3.2224660e-05],\n",
       "       [8.1062522e-03, 5.0841425e-02, 1.2453231e-07, 5.3348430e-07,\n",
       "        9.1728407e-07, 1.0009186e-08, 2.8985988e-07, 1.7532484e-09,\n",
       "        9.4089705e-01, 1.5346886e-04],\n",
       "       [1.7055811e-02, 1.1841061e-01, 4.6799007e-05, 2.7727904e-02,\n",
       "        1.0848254e-03, 1.0896578e-03, 1.3575243e-04, 2.8652203e-04,\n",
       "        7.8895986e-01, 4.5202184e-02],\n",
       "       [3.1300801e-01, 1.1591638e-02, 1.1511055e-02, 3.9592334e-03,\n",
       "        7.7280165e-03, 5.6289224e-05, 2.3531138e-04, 9.4204297e-06,\n",
       "        6.5178138e-01, 1.1968113e-04],\n",
       "       [1.3230885e-05, 2.1221960e-05, 9.2594400e-02, 3.3585075e-02,\n",
       "        4.4722903e-01, 4.1028224e-03, 4.2241842e-01, 2.8064171e-05,\n",
       "        6.6392668e-06, 1.0745022e-06]], dtype=float32)"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y_pred = cnn.predict(X_test)\n",
    "y_pred[:5]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[3, 8, 8, 8, 4]"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y_classes = [np.argmax(element) for element in y_pred]\n",
    "y_classes[:5]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([3, 8, 8, 0, 6], dtype=uint8)"
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y_test[:5]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAI4AAACcCAYAAACp45OYAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjMuMCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy86wFpkAAAACXBIWXMAAAsTAAALEwEAmpwYAAAWp0lEQVR4nO1da2wc13X+zszscpfkkqIoiZIs2ZSth2VbjhPLrosqgJvWhRsUSH80aFygTdGgaYu2aYD+SBD0+aOAg6JFfxT54bZBXLRoaiBFGxRGjcCNYxuwHT1cyw/ZkmBZkWzqLVJ8LXdn5vTHDveec7gkV0NpRXrvBwi6s/funbvDM/e8zyVmhofH9SK41QvwWJvwhOORC55wPHLBE45HLnjC8cgFTzgeubAiwiGix4noPSI6SURfv1GL8lj9oLx2HCIKARwH8BiAswAOAniCmd+5ccvzWK2IVvDdhwGcZOb3AYCIvgvgcwAWJZxKpZ+Hh4cBAEHUo/oCcptfGOiNMBHEnSZJs02kiV5ekbm3nJ9kL13Hi7PIUF6sAwCRXYnqXaKHFx221Msu76faC5/IovOnSbXZPn7i/UvMvNHeZyWEcxuAM+L6LICfWuoLw8PD+JM//RoAoH/DbtVXDovN9kClX/VNzjlimb52udkOglSNS8XDjgzxlQWhlkLxswPzR5AP0XQladKyL5Wf23VE+hEHQehutQRRyZeC7O8099Pfc3P29LjfXAz0iwp211QMVdfM5WPN9qO/+PnTre6zEhmn1a9e8CoQ0ZeJ6BARHZqcnFrB7TxWE1ay45wFsF1cbwPwkR3EzE8BeAoA7hgd5ZRLAIA4HFLj6oW+ZjsJ9Y4TFMSOM+uIj5NpNa5QcO051m9lXby11ci9L4ZjolZ323QQ6jdxdma22Q5FX0HeGECtVndzBHXVx2lNzK/f22LR7bpxnIjv6DU2xMts/WZHGxpyz7WnXBHr0O90Kq6pR68/mdLPvxVWsuMcBLCLiHYQURHAFwB8fwXzeawh5N5xmDkmoj8A8ByAEMC3mfntG7Yyj1WNlbAqMPOzAJ69QWvxWENYEeFcLwiMgGMAQGJkkIRS0a6qvlLFLXP4jpFmO5i4qsb1zzj5p1ad0/P3l5rtdHBds10pahl/fn0AEBjNrDbn5JMkdestlbSgJDV8qzovpi7b+8V1t47UyDhSLSlGWj4pl8timJBjoGWtFIloG4llSRNCttZlR3h4tIAnHI9c6CirYoSI0VARAxRVXxq6/XiOtRocius+oT8P9OptOj1ysNmuXdI2oy337Wm26aJjW3PUp8b1h26bnpzV6n5JbP097O4dDBvzgVDHjcaNuV5376iu2VhYF/fuc2yxZ2JCjYu239Nsz6wbVH1p7Nh8Erj5Sql+3iRYaJDovjBZfj/xO45HLnjC8cgFTzgeudBRGaeBBt8lofYCQMBOLkhi4wcQggIJ2aJKFTWskDp5hTZsUn0zk05mqJ863mzHVFbjUieCYLpgnIlCLy7W3RprZ7RMhrobR9C6dFWYBcKq7ovcEjG32f3O2XNX1LgKOWc1DW5QfdJMUBduhUKgVexU+DHCQP/OyDp+W8DvOB654AnHIxc6q44zkGSBWGmit2mWNJzqrbIm2FoSue8NThrP80ZnVS5vukP1xSxU2qL72bxhsxo3WxCxNOcuqz4Ij/h0ybE4HhlWwwqp+y1VEzvTV3HstDY5o/rmhCkgKjsVOZzWlvRo2LFhKujnmIg4m4rgTqFhmTE5VkiBNms0XI9Lw+84HrngCccjFzqvVWXbZ2LDLSV7MuSciDjjArl2z8kTalz18EvNdvyQdnJChE4y9zbbRcPuqnDso39sXPWFIhQz7ROxz6wtr0ndzVkZXqf6Ch8K9jelrduFEaElnnHjogFtma5ePOrW1Kv70t3OqlwVgWEBaVZVjAVbjE3stnWqtoDfcTxywROORy54wvHIhc4GchGhEDZUv8CofFI9T43lMhL03X/Veazjszo2fqDgZJDJj86pvlrJeZEZznpL5y6ocX1bhbo8YPO2nFpcnnIyVHF8Uo2riqCp+NKY6itWnXk4vqa93j1XBprt+qyTQbh8pxo3fsplJRXLWsapbHFmiFBYwdlYh+eEpz8mTQa1BZFjC+F3HI9c8ITjkQsdZVUBEXqKjf2TQ2OtTIX6nJpYXHE9VXC0PrX/E2rcQPRgsz0zqdlHPZR5ROJn1/QWXii7/X06qam+QMTi1kWwUyEw+VdFkc4MjVlhWpiZ0mvsE/euijl6+jU7Wl9xuVOJiTmeKotrYQUv1/UeEYvfYh436m3UE/A7jkcueMLxyAVPOB650FkZJwjQ19fwKsclbaavJy4vG6Tljlioh1R0XunyiA7Uvjbt3AUXJ7Q5n4Rnuzbj1OWiVUXH3Ryxsb33FJ38cE24SEoF8xgDd20rS8zNSFlOS0ATsy4KoCaG9UZ6HZVtLmU/tJqzzAmX+4JNnYJK/lJ9aRs+h2V3HCL6NhFdIKK3xGfriegHRHQi+39oqTk8Pn5oh1V9B8Dj5rOvA3iemXcBeD679ugiLMuqmPlFIho1H38OwKNZ+2kALwD42nJzERGiTJ0uV3pV35RI340iTc+J2H4j4eUNWKvLKdw1hTqmORIqs2QQ9ZoOpiqLkiVRoB9PIRKlTcR8SazvJdOPYxNAVSgLNTjRenBRmBpkMFgh1iytxrLSlp6/lAi2k4h12apb4gO7eyys3rUQeYXjEWYeA4Ds/03LjPf4mOGma1WyIte1a+M3+3YeHUJereo8EW1h5jEi2gLgwmIDZUWuXbv3cDGrN1cs6VunIla2XCipvpjcljt5TVSMMBWzSoPrm+2RPp06I6OTdBUHvS2H4l0KSb9Xxai9x8XCYWtZVSIs2Gy0l0BcFyVDNeuYC+LFuhAJDTQRFSlsZQxK3W8JDWcKbd5yC+Tdcb4P4ItZ+4sA/ivnPB5rFO2o4/8G4BUAe4joLBF9CcCTAB4johNo1Dl+8uYu02O1oR2t6olFun7uBq/FYw2hwxW5gCgLKApJq9Il4S0fv6BTXq9MuWCoi2Nnm+2his5nuu+efc12oaRTe2XgUl2oqYHJ4ZIyTmDSZmXFLCkz2KpbiTIZWD148TLegcxvUvObVGExR0BazpNzFEInNxashi1zA4ysmAQ3Tx336HJ4wvHIhY7nVc1v8ZHZHlPBBiZNENbFiy5+ePzqh8328aM/VuPefeOVZnvnzntU3+jOvc320AaXKgyzLSepsLayfq/kyFAFb+k5ImFhtmpwKtRleS6FnScUc9iwKskalzrXQZkF2MZPi7uStnxXa/q6FfyO45ELnnA8csETjkcu3IKKXA1IHg4ApZJzM9y9527Vt3Pvbc32zKSTd94+ckSNe/3Qq832Sy/q03KOvdMMJ8LuvQ8027v27FXj1g2ta7aLRf14wnAxuWaJCtZGQqmLwK401nnrEtJznhiVPlUuk/ZAVsYRanxgogDi1Aere9wkeMLxyIUOsypuqqOByUVicZ6UtdiGwqq8btjF2x54VIcB7dy5o9l++UcvqL5Tp5waP/26C7SyoR777ne5Wtu3b1d9kThZLxHnSSUmZTYVKv2CYxcFy7BHQ0rNnaSV2rzfqiKMOW9CqudqXQvUcfe91LBCyxpbwe84HrngCccjFzrMqgiUsajApKUEkWMfhdA6DYUlVmgwQUGn2OzafX+zncb6nRgb+16zffWSq3JxYk5XjDj/4XvN9l27tHa39143/6aRLc12ZM5njOtuXXUTjyyPW2LjoKTFnIvGyblUTDDLPiEO2KlZ8rsFxx/ZYpIL4Xccj1zwhOORC55wPHKh45bj+VIhoeGroVBNizb2SarugjezoXt5bPO27aOqb3TUXR887wLDYlNx8+KFcde+pCt+HTvmqn3u2LGz2b7rrl1q3MiIs3RXKjpNGaIwddWUWElq4uwFUTHUesCl5dg6x5kWS981qr/KzdIIb2JelUeXwxOORy50uHgkEGZbaWi3VKm2knH+ycAl5VC0OqaoIFHSuVmViivMqNRewzIlW7BHI01edeljr18SztY3Dqpx64ddDYbNm7X1efOWUbFGzcaGh52Kv3HEnTFBJvEpFSp9bKphyAobynJsHhWJFGO252r44pEeNwuecDxywROORy50Vh1nBvG8jGO6hMxDrPm2CkKixeUTqcLOmoqe5845FXxszMkn1ya026IggrUqfboUS5+Qm3oj973EBJ1/KHK/TnzwvuqrVv+32Y7NMc3DG7Y22/v2uWD7XTu1nLRxo4sKGDBHK/aUnSwnC4HDyC2xXLJJQK/dCHWciLYT0Q+J6BgRvU1Ef5R97qtydTHaYVUxgD9m5r0AHgHw+0R0D3xVrq5GO7njYwDmiyhNEtExALchT1UuApDl8KQmrpXFyb+2aKPQHEGhsKia7VceH/jGkcOqb+rqxWZ7vagGdnbsoho3MOi2+kKkVfo0dgUuB/pFDlRBe7mLkZu/0NOn+sLAnUVxZVx75k9/8E6zPTHu2N2RQ/rPVCy6dW3frs952Lrl9mZ7y1bH4raO3K7G9fU7BkFlkz8WmFOYW+C6hOOspNsnAbwGX5Wrq9E24RBRP4DvAfgqM1+7ju81K3JNmDfMY+2iLcIhogIaRPOvzPwf2cfns2pcWKoqFzM/xcz7mXn/4LrBVkM81iCWlXGokfz8TwCOMfPfiq75qlxPos2qXMwp6nEj0k96sgGAYreUwOQyS0mG4fqsSj8lVPDqrD6Tc89ulz/1qQf2N9uHj76lxr12yLkPJqZ0RdIkdqVZNm1xqvOBAwfUuKjkZIQPTuv8rldfdfnt9+7V+e0Dg+7FOn/OmQzOnz+vxtXrbh2bRSQiAOzYMerWK1wJ05N6t5dB9IVIy2HV2uL5XvNox47zMwB+HcCbRPR/2WffQINgnskqdP0EwOfbmMvjY4J2tKqXsXjCoK/K1aXoeCDXvPd5Yb6Ra9qgbVkEM6XFiz6Xe50a/OlHNU3L3CSZH7X7gYfVuPsefKjZNic8IhA33DDsqoHdeeddalwkzqkY3XW/6tt6+x633rKuGjYoWJX00l+5clmNkyxo08bNqk8GjoWiSmqQanE2EeeD1c3zTk2+Vyt4X5VHLnjC8ciFjrKqNE0xO9uwvobXtBMyYnEskDmjIRaFnuNYBCoZ56KsdmVjceNEFpV270vNBEJtvd2lEdszB0lcB6Ja16mf6GKXszXhsDUpupVBN39qLN9XJ9waI8Fm+gZG1TiIeOErE7Oq66Pzbi3SOt8TaGeu8AeD+jUZVK9WsRz8juORC55wPHLBE45HLnRUxpmanMSLL/4QADARH1V9fcKjnMxpi21dyAJ1caRzkmgLp1Rh66baVSJkGammVudMblMig9W117sgcsTXr3MBVP396/R6RYCWLW4lq5DaiqS6ALcs1K3lk0gEkQUmCEt+T8W/mfhzEsdXUq+eI6jqiIFW8DuORy54wvHIhQ7nVQUoFRosqR7qeN5QnJ/U0zOg+lJREkXmCtnKXdIaLatizd+7OU7ENKdsnK3COsymMhWJsiRSiw+gzQeRONZxbk47W5V6bizfMh25XhfOXHN+lKxmthS7k6iZGGwW81c1R0ZPqC3VreB3HI9c8ITjkQuecDxyoeN5VWkWyDU1fVV19YqzlWzRy0TQtyyNVqtrtT2Ohak80DIOC1lGBkKlsX4EsVDHk9jkd5FUs8WZUeb1Y3ZyzVxVuwSkmyS1lUBVCRepP+t1SFluwVmboi3nD+talouFjDOzTp9funl7P5aD33E8csETjkcudJRV1eqzOHPmbQDAyXNahe0VFUQjU14kURuwq2iVGJU7Td12XCgGi/ZJT3liw2vF1m/VYFnQOliiVEooAsWsB7xWE2zSlBeRAWyyKiuRrgIqvd722EVlLRaf12Ge6ZAzh2zdp8+zGNQhyC3hdxyPXPCE45ELHdaqCAE3tKeCdf4Jy7Etlii1GQSyqoXefuVxjaEpwC139IDFvUyRanX6rgnykq+ZZEH2CKVErLdu1piKcynYBDXLn82SFdrqHUqrMmc5RO46Fu3K1hE1btu+3c12RDrld/z4m1gOfsfxyAVPOB654AnHIxc6bjmOszTapKYtqnVRWiOOtaoOIf/IUwBTw/sDGchl5JNUyBpSDU5NvlGx4NZhxAc1h1Sd7bhEWmmtyi3WaI/QlvIVCVkOxoNfEDe0xyDWe51ZY2iPK4Fy26iu6lUVacXvv6tLwpTqU1gO7VTkKhHRj4nojawi119mn/uKXF2MdljVHIDPMPMnADwA4HEiegS+IldXo53ccQYwv3cVsn+MvBW5st05LJgAJKGfFyLLI8S1yGcKYc57kusmW4DS9faIClpDA3qjlGm+SWKsrakMrhLz9eiYYBmQZc+Wkmp8Ytjp5KRjEdJ8IFV4ALgmAoijDXr9t+92avbQkIuL/vDdk2rc5ZOn3BzGAl8yf5tWaLc+TphVqrgA4AfM7CtydTnaIhxmTpj5AQDbADxMRPe1ewNZkas6t3zdFY+1getSx5l5HA2W9DhyVOQq9Sx/ZJ/H2kA7Fbk2Aqgz8zgRlQH8PIBvIkdFLjAQzp+VWdNqaoo5MUzvTKHwiMu2DWKSAeoLj2YWgewi52pmRgdx61xv63kWanzdySfVupW1WudHZZ1iQt2VyN8t12vU9somJ9ds3L1D9QVize8dfK3ZnrugA9BDEVAWmkg0G2DWCu3YcbYAeJoaIf4BgGeY+b+J6BX4ilxdi3a0qqNolKi1n1+Gr8jVtSDrib6pNyO6COA0gA0ALnXsxqsfq/l53MHMG+2HHSWc5k2JDjHz/uVHdgfW4vPwTk6PXPCE45ELt4pwnrpF912tWHPP45bIOB5rH55VeeRCRwmHiB4noveI6CQRdV0YxsfptMGOsarM8nwcwGMAzgI4COAJZn5nyS9+jJD59LYw8xEiqgA4DOCXAfwmgCvM/GT2Qg0x89IhKrcYndxxHgZwkpnfZ+YagO+iEdPTNWDmMWY+krUnAcjTBp/Ohj2NBjGtanSScG4DcEZcn80+60qs9dMGO0k4rcLKulKly3va4GpCJwnnLAAZar8NwEcdvP+qwEpOG1xN6CThHASwi4h2EFERwBfQiOnpGrRx2iDQbmzTLUanveOfBfB3aISsf5uZ/6pjN18FIKIDAF4C8CZclNg30JBzngFwO7LYJma+0nKSVQJvOfbIBW859sgFTzgeueAJxyMXPOF45IInHI9c8IQjQETPEtG66/zOd4joV27SklYtOn7u+GoGM3/WfpYZ7YhtXdguR9fuOET0n0R0OIuL+XL22QdEtIGIRrOYmW8BOAJgOxFNEdHfENERIno+y3C1c/4ZER0koreI6KmM6EBELxDRN7M6Q8eJ6NPZ5yER/XX2naNE9DudfAYrQdcSDoDfYuYHAewH8BUiGjb9ewD8MzN/kplPA+gDcISZPwXgRwD+vMWcf8/MDzHzfQDKAH5J9EXM/DCAr4rvfgnABDM/BOAhAL9NRDqnd5WimwnnK0T0BoBX0XC+7jL9p5n5VXGdAvj3rP0vAA60mPNnieg1InoTwGcA3Cv65h2ahwGMZu1fAPAbWQmZ1wAMt1jHqkRXyjhE9CgaxRN+mplniOgFACUzbHqZaZSvhohKAL4FYD8znyGivzBzzldVSOCeOwH4Q2Z+7jp/wi1Ht+44gwCuZkRzN4BH2vhOAGBee/o1AC+b/nkiuZTF27SjaT0H4PeyUAsQ0W4iauMkhVuPrtxxAPwPgN8loqMA3kODXS2HaQD3EtFhABMAflV2ZmVg/gENz/cHaISRLId/RINtHckE6YtYA2GjgPeOtw0immLm5U8A6xJ0K6vyWCH8juORC37H8cgFTzgeueAJxyMXPOF45IInHI9c8ITjkQv/D1ySmnqgIQWbAAAAAElFTkSuQmCC\n",
      "text/plain": [
       "<Figure size 1080x144 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plot_sample(X_test, y_test,3)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'ship'"
      ]
     },
     "execution_count": 23,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "classes[y_classes[3]]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'ship'"
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "classes[y_classes[3]]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<h3 style='color:purple'>Exercise</h3>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Use CNN to do handwritten digits classification using MNIST dataset. You can use this notebook as a reference:\n",
    "https://github.com/codebasics/deep-learning-keras-tf-tutorial/blob/main/1_digits_recognition/digits_recognition_neural_network.ipynb\n",
    "\n",
    "Above we used ANN for digits classification. You need to modify this code to use CNN instead. Check how accuracy improves fast with CNN and figure out how CNN can be a better choice for doing image classification compared to ANN. Once you have worked on this problem on your own, you can check my solution by clicking on this link: [Solution](https://github.com/codebasics/deep-learning-keras-tf-tutorial/blob/main/16_cnn_cifar10_small_image_classification/cnn_mnist_exercise_solution.ipynb)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}