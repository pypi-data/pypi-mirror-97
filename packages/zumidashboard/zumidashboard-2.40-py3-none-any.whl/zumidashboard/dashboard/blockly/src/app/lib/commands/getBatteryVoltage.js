import Command from './command.js';
import { sensorBatteryVoltage } from '../types/sensorTypes.js';

export default class GetBatteryVoltage extends Command {
  constructor(){
      var batteryPackage = sensorBatteryVoltage;
      super(batteryPackage, 'batteryVoltage');
  }

  async run(){
    await Code.writeCharacteristic.writeValue(this.package);
    const value = await Code.readCharacteristic.readValue();

    var arrayResult = new Uint8Array(value.buffer);
    var batteryVoltageValue  = ((arrayResult[16] << 8) | (arrayResult[15] & 0XFF));
    console.log('Battery Voltage is ' + arrayResult);
    var event = new CustomEvent(this.eventName, { detail: batteryVoltageValue });
    dispatchEvent(event);
  }
}
