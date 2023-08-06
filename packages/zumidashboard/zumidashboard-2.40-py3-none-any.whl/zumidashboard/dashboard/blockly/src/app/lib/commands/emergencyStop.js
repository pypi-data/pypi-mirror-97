import Command from './command.js';
import { bytesEmergencyStop } from '../types/flyEventsTypes.js';

export default class EmergencyStop extends Command {
  constructor(){
      var packageLand = bytesEmergencyStop;
      super(packageLand, '');
  }

  async run(){
    await Code.writeCharacteristic.writeValue(this.package);
  }
}
