const mongoose = require('mongoose');

const AirQualityDataSchema = new mongoose.Schema({
  x_start: Number,
  x_end: Number,
  y_start: Number,
  y_end: Number,
  value: Number,
  source: String,
  timestamp: Date,
});

module.exports = mongoose.model('AirQualityData', AirQualityDataSchema);