import httpx
import asyncio
from supabase import create_client
import os

import logging

logging.basicConfig(filename="planificateur.log", level=logging.info,
                    format='%(asctime)s %(levelname)s %(message)s')
