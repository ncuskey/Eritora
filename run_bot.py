#!/usr/bin/env python3
import asyncio
import bot.run

if __name__ == "__main__":
    try:
        asyncio.run(bot.run.main())
    except KeyboardInterrupt:
        pass
