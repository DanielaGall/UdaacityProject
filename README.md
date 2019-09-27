{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "Plagiarism Project, Machine Learning Deployment\n",
    "\n",
    "This repository contains code and associated files for deploying a plagiarism detector using AWS SageMaker.\n",
    "Project Overview\n",
    "\n",
    "In this project, you will be tasked with building a plagiarism detector that examines a text file and performs binary classification; labeling that file as either plagiarized or not, depending on how similar that text file is to a provided source text. Detecting plagiarism is an active area of research; the task is non-trivial and the differences between paraphrased answers and original work are often not so obvious.\n",
    "\n",
    "This project will be broken down into three main notebooks:\n",
    "\n",
    "Notebook 1: Data Exploration\n",
    "\n",
    "    Load in the corpus of plagiarism text data.\n",
    "    Explore the existing data features and the data distribution.\n",
    "    This first notebook is not required in your final project submission.\n",
    "\n",
    "Notebook 2: Feature Engineering\n",
    "\n",
    "    Clean and pre-process the text data.\n",
    "    Define features for comparing the similarity of an answer text and a source text, and extract similarity features.\n",
    "    Select \"good\" features, by analyzing the correlations between different features.\n",
    "    Create train/test .csv files that hold the relevant features and class labels for train/test data points.\n",
    "\n",
    "Notebook 3: Train and Deploy Your Model in SageMaker\n",
    "\n",
    "    Upload your train/test feature data to S3.\n",
    "    Define a binary classification model and a training script.\n",
    "    Train your model and deploy it using SageMaker.\n",
    "    Evaluate your deployed classifier.\n",
    "\n",
    "Please see the README in the root directory for instructions on setting up a SageMaker notebook and downloading the project files (as well as the other notebooks)."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "conda_python3",
   "language": "python",
   "name": "conda_python3"
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
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
