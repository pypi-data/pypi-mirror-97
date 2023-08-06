import Command from './command.js';
import { bytesLand } from '../types/flyEventsTypes.js';
import { ledColorRGB } from '../model/data.js';

export default class SetArmMode extends Command {
  constructor(mode){
    var armModePackage = new Uint8Array(6);
    armModePackage[0] = 0x24;
    armModePackage[1] = mode.armCode;
    armModePackage[2] = ledColorRGB.armColorR;
    armModePackage[3] = ledColorRGB.armColorG;
    armModePackage[4] = ledColorRGB.armColorB;
    armModePackage[5] = 100;
      super(armModePackage, 'SetArmMode');
  }

  async run(){
    await this.sendBLECommand(this.package);
  }
}
