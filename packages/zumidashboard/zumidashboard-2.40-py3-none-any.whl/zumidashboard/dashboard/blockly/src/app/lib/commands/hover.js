import Command from './command.js';
import { bytesHover } from '../types/flyEventsTypes.js';

export default class Hover extends Command {
  constructor(){
      var packageHover = bytesHover;
      super(packageHover, 'hover command');
  }

  async run(){
    await this.sendBLECommand(this.package);
  }
}
