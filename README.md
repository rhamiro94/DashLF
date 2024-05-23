# Render deployment of Mercado Argentino de Valores Dashboard

In this repository, you will find a simple example of how to deploy a Dashboard using Python´s Dash framework on Render.

## Objetive

The main objective of this repo is to show you an easy way to deploy a Dash app on the web using data collected from another repo you may find [here](https://github.com/rhamiro94/LocalFinance) An easy way to visualize and track an important financial market in Argentina called MAV that  shows the financing of Small Caps companies.

## Guide

This repo has a requirements file where we specify the libraries we are going to use in our main file called app.py that shows the structure of the app.
We also have a CSV file that provides the data that we show in our app and that can be actualized by running the cargacsv.py file that can be found in this repo. 
This last file takes data from a local PostgreSQL database that is daily updated. So basically it's a Python script that uses a PostgreSQL connection to store its data into a CSV file.

## Conclusion and link to the app

In conclusion, this repo shows a series of scripts to connect, update, and deploy data into the web using Render.
You can find the link to the app [here](https://dashlf.onrender.com/)
