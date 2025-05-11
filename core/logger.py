from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>", level="INFO")
logger.add("logs/lookup.log", rotation="500 KB", level="DEBUG", backtrace=True, diagnose=True)

