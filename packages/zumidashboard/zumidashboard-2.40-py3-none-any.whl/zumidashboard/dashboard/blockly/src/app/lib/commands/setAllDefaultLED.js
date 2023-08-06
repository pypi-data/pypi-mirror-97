import Command from './command.js';
import { ledColorRGB } from '../model/data.js';

export default class SetAllDefaultLED extends Command {
  constructor(rValue, gValue, bValue, mode, interval,
              rValue2, gValue2, bValue2, mode2, interval2){
    ledColorRGB.armColorR = rValue;
    ledColorRGB.armColorG = gValue;
    ledColorRGB.armColorB = bValue;

    var AllDefaultColorPackage = new Uint8Array(11);
    AllDefaultColorPackage[0] = 0x2D;
    AllDefaultColorPackage[1] = mode;
    AllDefaultColorPackage[2] = rValue;
    AllDefaultColorPackage[3] = gValue;
    AllDefaultColorPackage[4] = bValue;
    AllDefaultColorPackage[5] = interval;
    AllDefaultColorPackage[6] = mode2;
    AllDefaultColorPackage[7] = rValue2;
    AllDefaultColorPackage[8] = gValue2;
    AllDefaultColorPackage[9] = bValue2;
    AllDefaultColorPackage[10] = interval2;
      super(AllDefaultColorPackage, 'SetAllDefaultLED');
  }

  async run(){
    await this.sendBLECommand(this.package);
  }
}
