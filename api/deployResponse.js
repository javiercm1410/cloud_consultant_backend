const { spawn } = require('child_process');

function generateTopologyResponse(answers) {
  return new Promise((resolve, reject) => {

    let pythonProcess;

    if (answers.cloud_provider === 'GCP' && answers.architecture === 'Container-based') {
      pythonProcess = spawn('python3', [
        "/Users/simon/codes/CloudProject/backend/gcp_container_mysql_deploy.py",
        "/Users/simon/codes/CloudProject/backend/deployment_templates/gcp",
        answers.access_key, answers.database_password, answers.database_name,
        answers.database_version, answers.env_database, answers.container_repository,
        answers.container_port
      ]);
    } else if (answers.cloud_provider === 'AWS' && answers.architecture === 'Classic-three-tier') {
      pythonProcess = spawn('python3', [
        "/Users/simon/codes/CloudProject/backend/aws_three_tier_mysql_deploy.py",
        "/Users/simon/codes/CloudProject/backend/deployment_templates/aws/three-tier-arch-mysql",
        answers.access_key, answers.database_name, answers.database_password,
        answers.deploy_command_front, answers.deploy_command_back, answers.backend_port,
        answers.workload
      ]);
        }

    let output = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString().trim(); // Add the trim() method to remove any extra whitespaces
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      reject(`Python script error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      // consol.log(output);
      console.log(`child process exited with code ${code}`);

      console.log("Raw output:", output); // Add this line to log the raw output

      try {
        // const parsedOutput = JSON.parse(output);
        resolve(output);
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
