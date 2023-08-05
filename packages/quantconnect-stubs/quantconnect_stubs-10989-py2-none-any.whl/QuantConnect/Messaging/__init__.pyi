import typing

import QuantConnect.Interfaces
import QuantConnect.Messaging
import QuantConnect.Notifications
import QuantConnect.Packets
import System

QuantConnect_Messaging_EventMessagingHandler_DebugEventRaised = typing.Any
QuantConnect_Messaging_EventMessagingHandler_SystemDebugEventRaised = typing.Any
QuantConnect_Messaging_EventMessagingHandler_LogEventRaised = typing.Any
QuantConnect_Messaging_EventMessagingHandler_RuntimeErrorEventRaised = typing.Any
QuantConnect_Messaging_EventMessagingHandler_HandledErrorEventRaised = typing.Any
QuantConnect_Messaging_EventMessagingHandler_BacktestResultEventRaised = typing.Any
QuantConnect_Messaging_EventMessagingHandler_ConsumerReadyEventRaised = typing.Any


class StreamingMessageHandler(System.Object, QuantConnect.Interfaces.IMessagingHandler):
    """Message handler that sends messages over tcp using NetMQ."""

    @property
    def HasSubscribers(self) -> bool:
        """
        Gets or sets whether this messaging handler has any current subscribers.
        This is not used in this message handler.  Messages are sent via tcp as they arrive
        """
        ...

    @HasSubscribers.setter
    def HasSubscribers(self, value: bool):
        """
        Gets or sets whether this messaging handler has any current subscribers.
        This is not used in this message handler.  Messages are sent via tcp as they arrive
        """
        ...

    def Initialize(self) -> None:
        """Initialize the messaging system"""
        ...

    def SetAuthentication(self, job: QuantConnect.Packets.AlgorithmNodePacket) -> None:
        """Set the user communication channel"""
        ...

    def SendNotification(self, notification: QuantConnect.Notifications.Notification) -> None:
        """
        Send any notification with a base type of Notification.
        
        :param notification: The notification to be sent.
        """
        ...

    def Send(self, packet: QuantConnect.Packets.Packet) -> None:
        """Send all types of packets"""
        ...

    def Transmit(self, packet: QuantConnect.Packets.Packet) -> None:
        """
        Send a message to the _server using ZeroMQ
        
        :param packet: Packet to transmit
        """
        ...

    def Dispose(self) -> None:
        """Dispose any resources used before destruction"""
        ...


class Messaging(System.Object, QuantConnect.Interfaces.IMessagingHandler):
    """Local/desktop implementation of messaging system for Lean Engine."""

    @property
    def HasSubscribers(self) -> bool:
        """
        This implementation ignores the  flag and
        instead will always write to the log.
        """
        ...

    @HasSubscribers.setter
    def HasSubscribers(self, value: bool):
        """
        This implementation ignores the  flag and
        instead will always write to the log.
        """
        ...

    def Initialize(self) -> None:
        """Initialize the messaging system"""
        ...

    def SetAuthentication(self, job: QuantConnect.Packets.AlgorithmNodePacket) -> None:
        """Set the messaging channel"""
        ...

    def Send(self, packet: QuantConnect.Packets.Packet) -> None:
        """Send a generic base packet without processing"""
        ...

    def SendNotification(self, notification: QuantConnect.Notifications.Notification) -> None:
        """Send any notification with a base type of Notification."""
        ...

    def Dispose(self) -> None:
        """Dispose of any resources"""
        ...


class EventMessagingHandler(System.Object, QuantConnect.Interfaces.IMessagingHandler):
    """Desktop implementation of messaging system for Lean Engine"""

    @property
    def HasSubscribers(self) -> bool:
        """
        Gets or sets whether this messaging handler has any current subscribers.
        When set to false, messages won't be sent.
        """
        ...

    @HasSubscribers.setter
    def HasSubscribers(self, value: bool):
        """
        Gets or sets whether this messaging handler has any current subscribers.
        When set to false, messages won't be sent.
        """
        ...

    @property
    def DebugEvent(self) -> typing.List[QuantConnect_Messaging_EventMessagingHandler_DebugEventRaised]:
        ...

    @DebugEvent.setter
    def DebugEvent(self, value: typing.List[QuantConnect_Messaging_EventMessagingHandler_DebugEventRaised]):
        ...

    @property
    def SystemDebugEvent(self) -> typing.List[QuantConnect_Messaging_EventMessagingHandler_SystemDebugEventRaised]:
        ...

    @SystemDebugEvent.setter
    def SystemDebugEvent(self, value: typing.List[QuantConnect_Messaging_EventMessagingHandler_SystemDebugEventRaised]):
        ...

    @property
    def LogEvent(self) -> typing.List[QuantConnect_Messaging_EventMessagingHandler_LogEventRaised]:
        ...

    @LogEvent.setter
    def LogEvent(self, value: typing.List[QuantConnect_Messaging_EventMessagingHandler_LogEventRaised]):
        ...

    @property
    def RuntimeErrorEvent(self) -> typing.List[QuantConnect_Messaging_EventMessagingHandler_RuntimeErrorEventRaised]:
        ...

    @RuntimeErrorEvent.setter
    def RuntimeErrorEvent(self, value: typing.List[QuantConnect_Messaging_EventMessagingHandler_RuntimeErrorEventRaised]):
        ...

    @property
    def HandledErrorEvent(self) -> typing.List[QuantConnect_Messaging_EventMessagingHandler_HandledErrorEventRaised]:
        ...

    @HandledErrorEvent.setter
    def HandledErrorEvent(self, value: typing.List[QuantConnect_Messaging_EventMessagingHandler_HandledErrorEventRaised]):
        ...

    @property
    def BacktestResultEvent(self) -> typing.List[QuantConnect_Messaging_EventMessagingHandler_BacktestResultEventRaised]:
        ...

    @BacktestResultEvent.setter
    def BacktestResultEvent(self, value: typing.List[QuantConnect_Messaging_EventMessagingHandler_BacktestResultEventRaised]):
        ...

    @property
    def ConsumerReadyEvent(self) -> typing.List[QuantConnect_Messaging_EventMessagingHandler_ConsumerReadyEventRaised]:
        ...

    @ConsumerReadyEvent.setter
    def ConsumerReadyEvent(self, value: typing.List[QuantConnect_Messaging_EventMessagingHandler_ConsumerReadyEventRaised]):
        ...

    def Initialize(self) -> None:
        """Initialize the Messaging System Plugin."""
        ...

    def LoadingComplete(self) -> None:
        ...

    def SetAuthentication(self, job: QuantConnect.Packets.AlgorithmNodePacket) -> None:
        """Set the user communication channel"""
        ...

    def DebugEventRaised(self, packet: QuantConnect.Packets.DebugPacket) -> None:
        ...

    def SystemDebugEventRaised(self, packet: QuantConnect.Packets.SystemDebugPacket) -> None:
        ...

    def LogEventRaised(self, packet: QuantConnect.Packets.LogPacket) -> None:
        ...

    def RuntimeErrorEventRaised(self, packet: QuantConnect.Packets.RuntimeErrorPacket) -> None:
        ...

    def HandledErrorEventRaised(self, packet: QuantConnect.Packets.HandledErrorPacket) -> None:
        ...

    def BacktestResultEventRaised(self, packet: QuantConnect.Packets.BacktestResultPacket) -> None:
        ...

    def ConsumerReadyEventRaised(self) -> None:
        ...

    def Send(self, packet: QuantConnect.Packets.Packet) -> None:
        """Send any message with a base type of Packet."""
        ...

    def SendNotification(self, notification: QuantConnect.Notifications.Notification) -> None:
        """
        Send any notification with a base type of Notification.
        
        :param notification: The notification to be sent.
        """
        ...

    def SendEnqueuedPackets(self) -> None:
        """Send any message with a base type of Packet that has been enqueued."""
        ...

    def OnDebugEvent(self, packet: QuantConnect.Packets.DebugPacket) -> None:
        """
        Raise a debug event safely
        
        This method is protected.
        """
        ...

    def OnSystemDebugEvent(self, packet: QuantConnect.Packets.SystemDebugPacket) -> None:
        """
        Raise a system debug event safely
        
        This method is protected.
        """
        ...

    def OnConsumerReadyEvent(self) -> None:
        """Handler for consumer ready code."""
        ...

    def OnLogEvent(self, packet: QuantConnect.Packets.LogPacket) -> None:
        """
        Raise a log event safely
        
        This method is protected.
        """
        ...

    def OnHandledErrorEvent(self, packet: QuantConnect.Packets.HandledErrorPacket) -> None:
        """
        Raise a handled error event safely
        
        This method is protected.
        """
        ...

    def OnRuntimeErrorEvent(self, packet: QuantConnect.Packets.RuntimeErrorPacket) -> None:
        """
        Raise runtime error safely
        
        This method is protected.
        """
        ...

    def OnBacktestResultEvent(self, packet: QuantConnect.Packets.BacktestResultPacket) -> None:
        """
        Raise a backtest result event safely.
        
        This method is protected.
        """
        ...

    def Dispose(self) -> None:
        """Dispose of any resources"""
        ...


