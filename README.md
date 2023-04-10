# strong-app-fitness


## Local Testing
functions_framework --target=hello_gcs --debug
### Stop local framwork
CTRL-C
### Common Errors

1. The error message "Connection in use: ('0.0.0.0', 8080)" indicates that the port you are trying to use for the Functions Framework is already in use by another process.
[2023-04-09 17:31:24 +0100] [97371] [ERROR] Connection in use: ('0.0.0.0', 8080)
[2023-04-09 17:31:24 +0100] [97371] [ERROR] Retrying in 1 second.


1.1. If you continue to experience this error, you can try running the following command in the terminal to find out which process is using the port:

sudo lsof -i :8080

1.2. To find the name of the process with PID 97116, you can run the following command in the terminal:

ps -p {pid} -o comm=

1.3. To kill a process with a specific PID, you can use the kill command in the terminal.

kill {pid}

1.4. This command will send a signal to the process with PID 97116 to terminate it. If the process does not respond to the signal, you can use the -9 option with the kill command to force the process to terminate:

kill -9 {pid}

This command will send a "SIGKILL" signal to the process with PID 97116, which will immediately terminate it.

Note that killing a process can potentially cause data loss or other unexpected behavior, so you should use this command with caution and only when necessary.

## Deployment
gcloud functions deploy

## Git
### Conventional Commits framwork https://www.conventionalcommits.org/
<<<<<<< HEAD

## Manual Task 

### Create the execrise_type list
INSERT INTO `rifkiamil-strong-00-dev.raw.execrise_type` (exercise, upper_Lower_body, target_area, cardio_intensity)
SELECT
  string_field_0,
  string_field_1,
  string_field_2,
  string_field_3
FROM
  `rifkiamil-strong-00-dev.raw.temp_exercise_type`;
=======
>>>>>>> 9abcd01ee1bb2223d3d5d1f7fba65bcbe57abd07
