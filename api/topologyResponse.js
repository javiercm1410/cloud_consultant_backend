const { spawn } = require('child_process');

function generateTopologyResponse(answers) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', [
      '/Users/simon/codes/CloudProject/backend/main.py', answers.cloud_provider, answers.workload, answers.architecture, answers.scale, answers.managed_database, ""
    ]);

    let output = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString().trim(); // Add the trim() method to remove any extra whitespaces
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      // consol.log(output);
      console.log(`child process exited with code ${code}`);

      console.log("Raw output:", output); // Add this line to log the raw output

      try {
        const parsedOutput = JSON.parse(output);
        resolve(parsedOutput);
      } catch (error) {
        console.error("Error parsing JSON:", error);
        console.error("Invalid JSON output:", output);
        reject(error);
      }
      ;
    });
  });
}

module.exports = generateTopologyResponse;
