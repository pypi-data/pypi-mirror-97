import { commandManager } from "../commandManager.js";
import GetBatteryPercentage from "../commands/getBatteryPercentage.js";
import GetBatteryVoltage from "../commands/getBatteryVoltage.js";
import GetHeight from "../commands/getHeight.js";
import GetPressure from "../commands/getPressure.js";
import GetGyroAngles from "../commands/getGyroAngles.js";
import GetOptFlowPosition from "../commands/getOptFlowPosition.js";
import GetDroneTemp from "../commands/getDroneTemp.js";
import GetState from "../commands/getState.js";
import GetTrim from "../commands/getTrim.js";
import GetAccelerometer from "../commands/getAccelerometer.js";

global.getBatteryPercentage = function() {
  var getBatteryPercentage = new GetBatteryPercentage();
  var batteryValue = getBatteryPercentage.getValue();
  commandManager.runCommand(getBatteryPercentage);
  return batteryValue;
};

global.loadCommand = async function(command) {
  if (!global.RUNNING) {
    return;
  } else if (global.RUN_ONLY_DISPLAY_BLOCKS) {
    commandManager.addCommand(command);
    commandManager.runFromStackOnly();
  } else {
    commandManager.addCommand(command);
  }
};

global.getBatteryVoltage = function() {
  var getBatteryVoltage = new GetBatteryVoltage();
  var batteryValue = getBatteryVoltage.getValue();
  commandManager.runCommand(getBatteryVoltage);
  return batteryValue;
};

global.getHeight = function() {
  var getHeight = new GetHeight();
  var height = getHeight.getValue();
  commandManager.runCommand(getHeight);
  return height;
};

global.getGyroAngles = function() {
  var getGyroAngles = new GetGyroAngles();
  var gyroAngles = getGyroAngles.getValue();
  commandManager.runCommand(getGyroAngles);
  return gyroAngles;
};

global.getPressure = function() {
  var getPressure = new GetPressure();
  var pressure = getPressure.getValue();
  getPressure.run();
  return pressure;
};

global.getOptFlowPosition = function() {
  var flowPosition = new GetOptFlowPosition();
  var flowPositionValue = flowPosition.getValue();
  flowPosition.run();
  return flowPositionValue;
};

global.getDroneTemp = function() {
  var droneTemp = new GetDroneTemp();
  var droneTempValue = droneTemp.getValue();
  droneTemp.run();
  return droneTempValue;
};

global.getState = function() {
  var state = new GetState();
  var stateValue = state.getValue();
  state.run();
  return stateValue;
};

global.getTrim = function() {
  var trim = new GetTrim();
  var trimValue = trim.getValue();
  trim.run();
  return trimValue;
};

global.getAccelerometer = function() {
  var accelerometer = new GetAccelerometer();
  var accelerometerValue = accelerometer.getValue();
  accelerometer.run();
  return accelerometerValue;
};

global.getAngularSpeed = function() {
  var accelerometer = new GetAccelerometer();
  var accelerometerValue = accelerometer.getValue();
  accelerometer.run();
  return accelerometerValue;
};

global.plotSensor = async function(fc) {
  var result = await global[fc.value]();
  if (fc.value === "getGyroAngles") {
    result = JSON.stringify(result);
  }
  global.displaySingleValue[fc.value] = result;
  global.blocksSaved[fc.index].setFieldValue(
    global.blocksSaved[fc.index].value + result
  );
  return;
};

global.setWorkspaceInterval = async function(seconds, fc) {
  const intervalTimer = 1300;
  if (fc && fc.index >= 0) {
    global.blocksSaved[fc.index].blockInterval = setInterval(
      async function() {
        if (fc.value) {
          global.loadCommand(fc.value);
          global.blocksSaved[fc.index].setFieldValue(
            fc.labelDescription + global.displayValue[fc.value]
          );
        }
      }.bind(this),
      intervalTimer
    );
  }
};
