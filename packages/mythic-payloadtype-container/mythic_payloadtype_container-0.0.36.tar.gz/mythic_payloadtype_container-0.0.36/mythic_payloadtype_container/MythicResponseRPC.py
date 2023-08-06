from . import MythicBaseRPC
import base64


class MythicResponseRPCResponse(MythicBaseRPC.RPCResponse):
    def __init__(self, resp: MythicBaseRPC.RPCResponse):
        super().__init__(resp._raw_resp)


class MythicResponseRPC(MythicBaseRPC.MythicBaseRPC):
    async def user_output(self, user_output: str) -> MythicResponseRPCResponse:
        resp = await self.call(
            {
                "action": "user_output",
                "user_output": user_output,
                "task_id": self.task_id,
            }
        )
        return MythicResponseRPCResponse(resp)

    async def update_callback(self, callback_info: dict) -> MythicResponseRPCResponse:
        resp = await self.call(
            {
                "action": "task_update_callback",
                "callback_info": callback_info,
                "task_id": self.task_id,
            }
        )
        return MythicResponseRPCResponse(resp)

    async def register_artifact(
        self, artifact_instance: str, artifact_type: str, host: str = None
    ) -> MythicResponseRPCResponse:
        resp = await self.call(
            {
                "action": "register_artifact",
                "task_id": self.task_id,
                "host": host,
                "artifact_instance": artifact_instance,
                "artifact": artifact_type,
            }
        )
        return MythicResponseRPCResponse(resp)

    async def tokens_on_host(
        self, host: str = None, add: list = [], remove: list = []
    ) -> MythicResponseRPCResponse:
        resp = await self.call(
            {
                "action": "rpc_tokens",
                "task_id": self.task_id,
                "host": host,
                "add": add,
                "remove": remove,
            }
        )
        return MythicResponseRPCResponse(resp)

    async def logon_sessions_on_host(
        self, host: str = None, add: list = [], remove: list = []
    ) -> MythicResponseRPCResponse:
        resp = await self.call(
            {
                "action": "rpc_logon_sessions",
                "task_id": self.task_id,
                "host": host,
                "add": add,
                "remove": remove,
            }
        )
        return MythicResponseRPCResponse(resp)

    async def callback_tokens(
        self, host: str = None, add: list = [], remove: list = []
    ) -> MythicResponseRPCResponse:
        resp = await self.call(
            {
                "action": "rpc_callback_tokens",
                "task_id": self.task_id,
                "host": host,
                "add": add,
                "remove": remove,
            }
        )
        return MythicResponseRPCResponse(resp)

    async def authentication_packages_on_host(
        self, host: str = None, add: list = [], remove: list = []
    ) -> MythicResponseRPCResponse:
        resp = await self.call(
            {
                "action": "rpc_authentication_packages",
                "task_id": self.task_id,
                "host": host,
                "add": add,
                "remove": remove,
            }
        )
        return MythicResponseRPCResponse(resp)

    async def create_processes(
        self, host: str = None, add: list = [], remove: list = []
    ) -> MythicResponseRPCResponse:
        resp = await self.call(
            {
                "action": "create_processes",
                "task_id": self.task_id,
                "host": host,
                "add": add,
                "remove": remove,
            }
        )
        return MythicResponseRPCResponse(resp)

    async def get_running_job_contexts(
        self, host: str = None
    ) -> MythicResponseRPCResponse:
        resp = await self.call(
            {
                "action": "get_security_context_of_running_jobs_on_host",
                "task_id": self.task_id,
                "host": host,
            }
        )
        return MythicResponseRPCResponse(resp)

    async def register_keystrokes(
        self, keystrokes: list = []
    ) -> MythicResponseRPCResponse:
        # keystrokes list entries are dictionaries with three components:
        #  "window_title", "user", and "keystrokes"
        #  window_title and user can be left out or blank and will be replaced with "UNKNOWN"
        #  however, "keystrokes" must always be present
        resp = await self.call(
            {
                "action": "register_keystrokes",
                "task_id": self.task_id,
                "keystrokes": keystrokes,
            }
        )
        return MythicResponseRPCResponse(resp)

    async def register_credentials(
        self, credentials: list = []
    ) -> MythicResponseRPCResponse:
        # credentials list entries are dictionaries with the following components:
        #   "credential_type" - one of ["plaintext", "certificate", "hash", "key", "ticket", "cookie", "hex"]
        #   "realm" - the realm or domain for the credential
        #   "credential" - the value of the actual credential
        #   "account" - the user the account is for
        #   "comment" - any comment you want to specify about the credential as you save it
        
        resp = await self.call(
            {
                "action": "register_credentials",
                "task_id": self.task_id,
                "credentials": credentials,
            }
        )
        return MythicResponseRPCResponse(resp)

    async def search_database(self, table: str, search: dict) -> MythicResponseRPCResponse:
        # the search is a dictionary where the key is the element and the value is the regular expression for our match
        #   ex: {"name": ".*Slack.*"}
        resp = await self.call(
            {
                "action": "search_database",
                "task_id": self.task_id,
                "table": table,
                "search": search
            }
        )
        return MythicResponseRPCResponse(resp)