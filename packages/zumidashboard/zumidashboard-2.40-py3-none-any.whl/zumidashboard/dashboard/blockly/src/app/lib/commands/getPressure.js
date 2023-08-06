import Command from './command.js';
import { sensorPressure } from '../types/sensorTypes.js';

export default class GetPressure extends Command {
  constructor(){
      var sensorPackage = sensorPressure;
      super(sensorPackage, 'getPressure');
  }

  async run(){
    await Code.writeCharacteristic.writeValue(this.package);
    const value = await Code.readCharacteristic.readValue();

    var arrayResult = new Uint8Array(value.buffer);

    let pressureValue = arrayResult[7] & 0xFF;
    var event = new CustomEvent(this.eventName, { detail: pressureValue });
    dispatchEvent(event);
  }
}
