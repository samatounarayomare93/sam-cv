module.exports = {
  apps: [
    {
      name: "Project-Chronos",
      script: "run.py",
      interpreter: ".venv/Scripts/python.exe", // Or .venv/bin/python on Linux
      watch: false,
      autorestart: true,
      max_memory_restart: "1G",
      env: {
        NODE_ENV: "production",
        NODE_NAME: "SOVEREIGN-MASTER"
      },
      log_date_format: "YYYY-MM-DD HH:mm:ss",
      error_file: "logs/pm2_error.log",
      out_file: "logs/pm2_out.log"
    }
  ]
};
