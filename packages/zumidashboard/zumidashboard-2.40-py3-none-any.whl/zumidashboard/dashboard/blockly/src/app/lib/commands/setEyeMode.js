import Command from './command.js';
import { bytesLand } from '../types/flyEventsTypes.js';
import { ledColorRGB } from '../model/data.js';

export default class SetEyeMode extends Command {
  constructor(mode){
    var armModePackage = new Uint8Array(6);
    armModePackage[0] = 0x24;
    armModePackage[1] = mode.eyeCode;
    armModePackage[2] = ledColorRGB.eyeColorR;
    armModePackage[3] = ledColorRGB.eyeColorG;
    armModePackage[4] = ledColorRGB.eyeColorB;
    armModePackage[5] = 100;
      super(armModePackage, 'SetEyeMode');
  }

  async run(){
    await this.sendBLECommand(this.package);
  }
}
