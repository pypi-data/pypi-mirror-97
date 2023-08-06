import Command from './command.js';
import { bytesTakeOff } from '../types/flyEventsTypes.js';

export default class TakeOff extends Command {
  constructor(){
      var packageTakeoff = bytesTakeOff;
      super(packageTakeoff, 'takeOff command');
  }

  async run(){
    await this.sendBLECommand(this.package);
  }
}
