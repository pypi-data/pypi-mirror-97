import GetBatteryPercentage from "./commands/getBatteryPercentage.js";
import GetHeight from "./commands/getHeight.js";
import GetGyroAngles from "./commands/getGyroAngles.js";


const classes = { GetBatteryPercentage, GetHeight, GetGyroAngles};

export default function dynamicClass (name) {
  return classes[name];
}
