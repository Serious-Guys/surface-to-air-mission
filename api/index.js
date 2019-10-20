const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const mongoose = require('mongoose');
const airQualityController = require('./src/data.controller');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// CONNECT TO MONGO

const db = 'mongodb://localhost:27017/surfaceair';

const connect = async ({ host }) => {
  try {
    await mongoose.connect(
      host,
      {
        useCreateIndex: true,
        useNewUrlParser: true,
        useUnifiedTopology: true,
      }
    );
    console.log(`Successfully connected to ${db}`);
  } catch(e) {
    console.log('Error connecting to database: ', error);
    process.exit(1);
  }
}

connect({ host: db });

mongoose.connection.on('disconnected', connect);

// API ROUTES

app.use('/api/airquality', airQualityController)

app.listen(3001, '0.0.0.0', () => console.log('Listening on 3001'));