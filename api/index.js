const express = require("express");
const bodyParser = require("body-parser");
const cors = require('cors');
const path = require('path');
const generateTopologyResponse = require('./topologyResponse');
const generateDeployResponse = require('./deployResponse');

const app = express();

app.use(cors());

const corsOptions = {
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
};

app.use(cors(corsOptions));

app.use(bodyParser.json());

app.post('/api/data', async function (req, res) {
  // Call the function to generate the response based on the request body
  const topologyResponse = await generateTopologyResponse(req.body);

  console.log(req.body);

  // Send the generated response
  res.json(topologyResponse);
});

app.post('/api/deploy', async function (req, res) {
  // Call the function to generate the response based on the request body
  const deployResponse = await generateDeployResponse(req.body);

  console.log(req.body);

  // Send the generated response
  res.json(deployResponse);
});
// // Serve the images using the /test-image route
// app.get('/images/:filename', (req, res) => {
//   const filename = req.params.filename;
//   res.sendFile(path.join(__dirname, `../backend/images/${filename}`));
// });

app.listen(3000, function(){console.log("servers started on port 3000")});
