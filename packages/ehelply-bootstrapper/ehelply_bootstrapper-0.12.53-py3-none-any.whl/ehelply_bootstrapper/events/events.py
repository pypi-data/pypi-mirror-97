from typing import Dict, List, Union, Type
from pydantic import BaseModel


class Event(BaseModel):
    """
    The Event class represents some event that is triggered.

    This class is a BASE CLASS and is MEANT to be overridden. Create a new Event class based on this one for each
        type of event.
    """
    name: str


class EventListener:
    """
    EventListener handles triggered events.

    You should override this class and create a new class based on this class for EACH event type that can be triggered.

    Return EventResponses for what the Controller should do as a result of the event.
    The EventResponse name is the function to call on the controller. And the EventResponse parameters are the values
        to pass to the function.
    """
    def __init__(self, event_name: str, event_model):
        self.event_name = event_name
        self.event_model = event_model

    def verify(self, event: Event) -> bool:
        """
        Verifies that an incoming event matches the event model that this listener is expecting.

        DON'T OVERRIDE
        """
        if isinstance(event, self.event_model):
            return True
        return False

    async def trigger(self, event: Event):
        """
        Event handler function

        MUST BE OVERRIDEN
        """
        pass


class EventController:
    """
    EventController will register n listeners.

    Then, when an Event is triggered, it will run through the listeners in order. Each Listener will return a list of
        EventResponses. These EventResponses then trigger a function on the controller
    """
    def __init__(self):
        self.listeners: Dict[str, List[EventListener]] = {}
        self.events: Dict[str, Type[Event]] = {}

    def register_listener(self, listener: EventListener):
        """
        Register a new EventListener
        """
        if listener.event_name in self.listeners:
            self.listeners[listener.event_name].append(listener)
        else:
            self.listeners[listener.event_name] = [listener]

    def register_event(self, action: str, event: Type[Event]):
        """
        Register a new Event and attach some action string to it

        This is optional and only required to trigger an action

        Triggering manually created events is allowed, possible, and encouraged. In those cases, registering events
            is not necessary

        Registering events opens the possibility to trigger events via action strings.
        """
        self.events[action] = event

    async def trigger_action(self, action: str, **parameters):
        """
        Trigger an action
        """
        if action not in self.events:
            return None

        event: Event = self.events[action](**parameters)

        await self.trigger_event(event)

    async def trigger_event(self, event: Event):
        """
        Trigger a new Event

        Loops through all of the EventListeners that are registered to listen to that event name in order.

        Then, after each EventListener is processed, it will trigger the EventResponses
        """
        for listener in self.listeners[event.name]:
            if listener.verify(event):
                await listener.trigger(event)
