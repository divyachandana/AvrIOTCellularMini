# AvrIOTCellularMini


**Running the Python Server**
Open Terminal or Command Prompt: Navigate to the folder containing your server Python script (server.py).

**Run the Server**: Execute the Python server script by running the command:

```python server.py```
This will start the Flask server, listening for incoming HTTP requests from your AVR-IoT Cellular Mini device.

**Training the Machine Learning Model**
**Prepare Your Data**: Ensure your dataset is ready and accessible in the same directory as your training script or specify the path to it within the script.

Open a New Terminal or Command Prompt Window: Navigate to the folder containing your training Python script (train.py).

**Run the Training Script**: Execute the training script by running the command:

```python train.py```
This script will train your machine learning model using the provided dataset and save the trained model to a file (e.g., model.pkl).

**Running the Arduino Code on AVR DB Series Board**
Open the Arduino IDE: Launch the Arduino Integrated Development Environment (IDE) on your computer.

Load the .ino File: Navigate to File > Open, then find and select the .ino file you wish to upload. This will open the file in the IDE.

**Configure the IDE for AVR DB Series**:

**Select the Board**: Go to Tools > Board: "<current board>" > and select "AVR DB-series" from the list. If you do not see the AVR DB-series option, you may need to install or update the board definitions in your Arduino IDE by going to Tools > Board > Boards Manager..., searching for "DxCore" (which supports AVR DB-series), and installing or updating it.
Choose the Correct Serial Port: Go to Tools > Port and select the port that your AVR DB-series board is connected to. If unsure, disconnect your device, open the menu to note the available ports, reconnect your device, and select the newly appeared port.
Upload the Code: Press the Upload button (the right arrow icon) within the IDE. This action compiles the Arduino sketch and uploads it to your AVR DB-series board. Wait for the process to complete, indicating that your device is now running the uploaded sketch.

**Monitor the Output (Optional)**: To view debug output or messages from your device, open the Serial Monitor within the Arduino IDE by clicking the magnifying glass icon in the upper-right corner. Ensure the baud rate in the Serial Monitor matches the baud rate specified in your sketch (e.g., Serial.begin(115200);).


