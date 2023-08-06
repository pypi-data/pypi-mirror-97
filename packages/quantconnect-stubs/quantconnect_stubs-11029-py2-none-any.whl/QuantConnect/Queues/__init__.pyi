import QuantConnect.Interfaces
import QuantConnect.Packets
import QuantConnect.Queues
import System


class JobQueue(System.Object, QuantConnect.Interfaces.IJobQueueHandler):
    """Implementation of local/desktop job request:"""

    def Initialize(self, api: QuantConnect.Interfaces.IApi) -> None:
        """Initialize the job queue:"""
        ...

    def NextJob(self, location: str) -> QuantConnect.Packets.AlgorithmNodePacket:
        """Desktop/Local Get Next Task - Get task from the Algorithm folder of VS Solution."""
        ...

    def AcknowledgeJob(self, job: QuantConnect.Packets.AlgorithmNodePacket) -> None:
        """Desktop/Local acknowledge the task processed. Nothing to do."""
        ...


