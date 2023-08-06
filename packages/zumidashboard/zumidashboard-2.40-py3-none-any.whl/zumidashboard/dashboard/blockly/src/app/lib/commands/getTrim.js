import Command from './command.js';
import { trimData } from '../types/sensorTypes.js';

export default class GetTrim extends Command {
  constructor(){
      var trimPackage = trimData;
      super(trimPackage, 'getTrim');
  }

  async run(){
    await this.sendBLECommand(this.package);
    const value = await Code.readCharacteristic.readValue();
    var arrayResult = this.removePackageHeader(value.buffer)
    var trimAllRoll		=	((arrayResult[1] <<	8) | (arrayResult[0]	&	0xff));
    var trimAllPitch		=	((arrayResult[3] <<	8) | (arrayResult[2]	&	0xff));;
    var trimAllYaw		=	((arrayResult[5] <<	8) | (arrayResult[4]	&	0xff));;
    var trimAllThrottle		=	((arrayResult[7] <<	8) | (arrayResult[6]	&	0xff));

    console.log('trim raw data', arrayResult);

    var trimData = {roll: trimAllRoll,
                    pitch: trimAllPitch,
                    yaw: trimAllYaw,
                    throttle: trimAllThrottle};

    console.log('trim data:', trimData);
    
    var event = new CustomEvent(this.eventName, { detail: trimData });
    dispatchEvent(event);
  }
}
