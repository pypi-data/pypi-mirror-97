import Command from './command.js';
import { bytesLand } from '../types/flyEventsTypes.js';
import { ledColorRGB } from '../model/data.js';

export default class SetEyeColor extends Command {
  constructor(rValue, gValue, bValue, eyeMode, interval){
    var armColorPackage = new Uint8Array(6);

    ledColorRGB.eyeColorR = rValue;
    ledColorRGB.eyeColorG = gValue;
    ledColorRGB.eyeColorB = bValue;

    armColorPackage[0] = 0x24;
    armColorPackage[1] = eyeMode;
    armColorPackage[2] = ledColorRGB.eyeColorR;
    armColorPackage[3] = ledColorRGB.eyeColorG;
    armColorPackage[4] = ledColorRGB.eyeColorB;
    armColorPackage[5] = interval;
      super(armColorPackage, 'SetEyeColor');
  }

  async run(){
    await this.sendBLECommand(this.package);
  }
}
