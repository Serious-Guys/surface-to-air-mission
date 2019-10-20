let express = require('express');
let router = express.Router();

const AirQualityData = require('./data.model');

router.route('/')
  .get(async (req, res) => {
    const [y_start_, x_start_, y_end_, x_end_] = req.query.bounds.split(',').map(el => parseFloat(el, 10));

    const data = await AirQualityData.find({
      x_start: { $gte: x_start_, $lte: x_end_ },
      $and: [{
        $or: [{
          x_start: { $gte: x_start_, $lte: x_end_ },
          x_end: { $gte: x_start_, $lte: x_end_ },
        }],
        $or: [{
          y_start: { $gte: y_start_, $lte: y_end_ },
          y_end: { $gte: y_start_, $lte: y_end_ },
        }]
      }]
    });

    res.json(data);
  })
  .post(async (req, res) => {
    for (let i = -180; i < 179; i += 2) {
      for (let j = -90; j < 89; j += 2) {
        // GENERATE MOCK DATA

        const value = Math.random() * 110 + 60;
        await AirQualityData.create({
          x_start: i,
          x_end: i + 2,
          y_start: j,
          y_end: j + 2,
          value,
          source: 'Simulation',
          timestamp: Date.now(),
        });
      }
    }

    res.sendStatus(200);
  })

module.exports = router;