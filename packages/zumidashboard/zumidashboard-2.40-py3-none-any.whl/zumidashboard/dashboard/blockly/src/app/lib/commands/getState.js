import Command from './command.js';
import { droneState } from '../types/sensorTypes.js';

export default class GetState extends Command {
  constructor(){
      var statePackage = droneState;
      super(statePackage, 'getState');
  }

  async run(){
    await this.sendBLECommand(this.package);
    const value = await Code.readCharacteristic.readValue();
    var arrayResult = this.removePackageHeader(value.buffer)
    var droneState = arrayResult[2];
    console.log('drone State', droneState);
    var event = new CustomEvent(this.eventName, { detail: droneState });
    dispatchEvent(event);
  }
}
