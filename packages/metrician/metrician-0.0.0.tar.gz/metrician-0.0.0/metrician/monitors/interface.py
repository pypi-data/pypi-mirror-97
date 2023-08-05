from metrician.interface import BaseInterface
from tensorboardX import GlobalSummaryWriter
class BaseMonitor(BaseInterface):

    def _write_fn(self) -> callable:
        writer = GlobalSummaryWriter.getSummaryWriter()
        return {
            'audio':writer.add_audio,
            'text':writer.add_text,
            'tabular':writer.add_histogram,
            'image':writer.add_image
        }[ self.dtype ]
