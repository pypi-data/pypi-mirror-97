import Command from './command.js';
import { sensorPressure } from '../types/sensorTypes.js';

export default class GetDroneTemp extends Command {
  constructor(){
      var sensorPackage = sensorPressure;
      super(sensorPackage, 'getDroneTemp');
  }

  async run(){
    await this.sendBLECommand(this.package);
    const value = await Code.readCharacteristic.readValue();
    var arrayResult = this.removePackageHeader(value.buffer)
    console.log('array result', arrayResult);
    var temperature = ((arrayResult[11] << 32) |(arrayResult[10] << 16) |(arrayResult[9] << 8)  | (arrayResult[8]  & 0xff));
      console.log('temperature', temperature);
    var event = new CustomEvent(this.eventName, { detail: temperature });
    dispatchEvent(event);
  }
}
