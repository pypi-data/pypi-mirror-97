import Command from './command.js';
import { ledColorRGB } from '../model/data.js';

export default class ResetDefaultLED extends Command {
  constructor(){
    ledColorRGB.armColorR = 255;
    ledColorRGB.armColorG = 0;
    ledColorRGB.armColorB = 0;

    var resetDefaultColorPackage = new Uint8Array(11);
    resetDefaultColorPackage[0] = 0x2D;
    resetDefaultColorPackage[1] = Mode.SOLID;
    resetDefaultColorPackage[2] = 255;
    resetDefaultColorPackage[3] = 0;
    resetDefaultColorPackage[4] = 0;
    resetDefaultColorPackage[5] = 100;
    resetDefaultColorPackage[6] = Mode.SOLID+0x30;
    resetDefaultColorPackage[7] = 255;
    resetDefaultColorPackage[8] = 0;
    resetDefaultColorPackage[9] = 0;
    resetDefaultColorPackage[10] = 100;
      super(resetDefaultColorPackage, 'ResetDefaultLED');
  }

  async run(){
    await this.sendBLECommand(this.package);
  }
}
