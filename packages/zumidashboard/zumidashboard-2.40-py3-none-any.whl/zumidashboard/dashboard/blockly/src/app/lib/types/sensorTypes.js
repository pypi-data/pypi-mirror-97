//Generic
var SensorArray = function (payload){
  var sensorType = new Uint8Array(3);
  sensorType[0] = 17;
  sensorType[1] = 144;
  sensorType[2] = payload;
  return sensorType;
}

//Set last bit use by different sensors
exports.droneState = SensorArray(0x31);

exports.trimData = SensorArray(0x35);

exports.sensorAngles = SensorArray(50);

exports.sensorAccelerometer = SensorArray(0x50);

exports.sensorOptFlow = SensorArray(0x52);

exports.sensorBattery = SensorArray(49);

exports.sensorBatteryVoltage = SensorArray(84);

exports.sensorHeight = SensorArray(87);

exports.sensorPressure = SensorArray(81);

exports.sensorAngularSpeed = SensorArray(80);
