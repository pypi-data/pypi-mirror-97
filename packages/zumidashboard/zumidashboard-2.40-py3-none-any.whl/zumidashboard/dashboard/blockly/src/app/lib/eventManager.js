class EventManager {
  constructor() {
    this.events = {};
  }

  addEvent(eventObject, eventType){
     this.events[eventType] = eventObject;
     this.events[eventType].run();
  }

  removeEvent (evenType){
    var event = this.events[evenType];
    if(event && event.intervalId){
      delete this.events[evenType];
      clearInterval(event.intervalId);
    }
  }
  removeAllEvents (){
    if(!this.events) {
      return;
    }

    for (var key in this.events) {
      if(key && this.events[key] && this.events[key].intervalId){
        clearInterval(this.events[key].intervalId);
      }
    }
  }
}

export let eventManager =  new EventManager();
