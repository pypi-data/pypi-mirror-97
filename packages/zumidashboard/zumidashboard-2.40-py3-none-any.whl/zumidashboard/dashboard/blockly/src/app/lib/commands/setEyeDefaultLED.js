import Command from './command.js';
import { ledColorRGB } from '../model/data.js';

export default class SetEyeDefaultLED extends Command {
  constructor(rValue, gValue, bValue, armMode, interval){
    ledColorRGB.armColorR = rValue;
    ledColorRGB.armColorG = gValue;
    ledColorRGB.armColorB = bValue;

    var eyeColorPackage = new Uint8Array(6);
    eyeColorPackage[0] = 0x2C;
    eyeColorPackage[1] = armMode;
    eyeColorPackage[2] = rValue;
    eyeColorPackage[3] = gValue;
    eyeColorPackage[4] = bValue;
    eyeColorPackage[5] = interval;
      super(eyeColorPackage, 'SetEyeDefaultLED');
  }

  async run(){
    await this.sendBLECommand(this.package);
  }
}
