import Command from './command.js';
import { bytesLand } from '../types/flyEventsTypes.js';

export default class Land extends Command {
  constructor(){
      var packageLand = bytesLand;
      super(packageLand, 'Land');
  }

  async run(){
    await this.sendBLECommand(this.package);
  }
}
