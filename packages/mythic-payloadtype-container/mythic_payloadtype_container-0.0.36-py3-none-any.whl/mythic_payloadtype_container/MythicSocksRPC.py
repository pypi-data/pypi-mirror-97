from . import MythicBaseRPC


class MythicSocksRPCResponse(MythicBaseRPC.RPCResponse):
    def __init__(self, socks: MythicBaseRPC.RPCResponse):
        super().__init__(socks._raw_resp)


class MythicSocksRPC(MythicBaseRPC.MythicBaseRPC):
    async def start_socks(self, port: int) -> MythicSocksRPCResponse:
        resp = await self.call(
            {
                "action": "control_socks",
                "task_id": self.task_id,
                "start": True,
                "port": port,
            }
        )
        return MythicSocksRPCResponse(resp)

    async def stop_socks(self) -> MythicSocksRPCResponse:
        resp = await self.call(
            {
                "action": "control_socks",
                "stop": True,
                "task_id": self.task_id,
            }
        )
        return MythicSocksRPCResponse(resp)
