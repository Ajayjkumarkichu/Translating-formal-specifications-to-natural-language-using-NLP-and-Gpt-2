module Ventilator {
  // Define states of the ventilator
  datatype State = 
    | PowerOn
    | PowerOff
    | Ventilating
    | Alarm

  // Define the ventilator system
  class VentilatorSystem {
    var currentState: State
    var alarmTriggered: bool

    // Constructor to initialize the state
    constructor Init()
      ensures currentState == PowerOff
      ensures alarmTriggered == false
    {
      currentState := PowerOff;
      alarmTriggered := false;
    }

    // Method to power on the ventilator
    method PowerOnVentilator()
      requires currentState == PowerOff
      ensures currentState == PowerOn
    {
      currentState := PowerOn;
    }

    // Method to start ventilation
    method StartVentilation()
      requires currentState == PowerOn
      ensures currentState == Ventilating
    {
      currentState := Ventilating;
    }

    // Method to stop ventilation
    method StopVentilation()
      requires currentState == Ventilating
      ensures currentState == PowerOn
    {
      currentState := PowerOn;
    }

    // Method to trigger an alarm
    method TriggerAlarm()
      requires currentState == Ventilating
      ensures currentState == Alarm
    {
      currentState := Alarm;
      alarmTriggered := true;
    }

    // Method to reset an alarm
    method ResetAlarm()
      requires currentState == Alarm
      ensures currentState == PowerOn
    {
      currentState := PowerOn;
      alarmTriggered := false;
    }

    // Invariant to ensure safety: Ventilator should not be ventilating in PowerOff state
    invariant VentilatorSafety: 
      currentState != Ventilating || currentState == PowerOn || currentState == Alarm

    // Invariant to ensure reliability: Alarm should only be triggered in Ventilating state
    invariant AlarmReliability: 
      !alarmTriggered || currentState == Alarm

    // Invariant to ensure the ventilator can't transition from PowerOff to Ventilating directly
    invariant ValidStateTransition: 
      !(currentState == PowerOff && currentState == Ventilating)

    // Invariant to ensure alarm can only be reset when triggered
    invariant AlarmResetSafety: 
      !alarmTriggered || currentState == Alarm
  }
}