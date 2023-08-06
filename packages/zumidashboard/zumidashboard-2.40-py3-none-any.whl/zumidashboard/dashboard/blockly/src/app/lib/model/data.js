import '../../constants/consts.js';

let ledMode = {
  'eye': global.HOLD.eyeCode,
  'arms': global.HOLD.armCode,
}

let ledColorRGB = {
  'eyeColorR': 255,
  'eyeColorG': 0,
  'eyeColorB': 0,
  'armColorR': 255,
  'armColorG': 0,
  'armColorB': 0
}

let flyVars = {
  'yaw': 0,
  'roll': 0,
  'pitch': 0,
  'throttle': 0
}

exports.dataLedMode = ledMode;
exports.flyVariables = flyVars;
exports.ledColorRGB = ledColorRGB;
