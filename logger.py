import logging

ARCHIVO_LOG = "software_fj.log"

logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

log = logging.getLogger("SoftwareFJ")