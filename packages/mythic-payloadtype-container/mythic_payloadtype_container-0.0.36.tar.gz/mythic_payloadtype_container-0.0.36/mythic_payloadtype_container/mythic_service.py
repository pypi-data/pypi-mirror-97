#!/usr/bin/env python3
import aio_pika
import os
import sys
import traceback
import base64
import json
import asyncio
import socket
from . import MythicCommandBase
from . import PayloadBuilder
from pathlib import Path
from importlib import import_module, invalidate_caches

# set the global hostname variable
hostname = ""
output = ""
exchange = None
container_files_path = ""

container_version = "3"


def import_all_agent_functions():
    import glob

    # Get file paths of all modules.
    modules = glob.glob("agent_functions/*.py")
    invalidate_caches()
    for x in modules:
        if not x.endswith("__init__.py") and x[-3:] == ".py":
            module = import_module("agent_functions." + Path(x).stem)
            for el in dir(module):
                if "__" not in el:
                    globals()[el] = getattr(module, el)


async def send_status(message="", command="", status="", username="", reference_id=""):
    global exchange
    # status is success or error
    try:
        message_body = aio_pika.Message(message.encode())
        # Sending the message
        await exchange.publish(
            message_body,
            routing_key="pt.status.{}.{}.{}.{}.{}.{}".format(
                hostname, command, reference_id, status, username, container_version
            ),
        )
    except Exception as e:
        print("Exception in send_status: {}".format(str(e)))


async def callback(message: aio_pika.IncomingMessage):
    global hostname
    global container_files_path
    with message.process():
        # messages of the form: pt.task.PAYLOAD_TYPE.command
        pieces = message.routing_key.split(".")
        command = pieces[3]
        username = pieces[5]
        reference_id = pieces[4]
        if command == "create_payload_with_code":
            try:
                # pt.task.PAYLOAD_TYPE.create_payload_with_code.UUID
                message_json = json.loads(
                    base64.b64decode(message.body).decode("utf-8"), strict=False
                )
                # go through all the data from rabbitmq to make the proper classes
                c2info_list = []
                for c2 in message_json["c2_profile_parameters"]:
                    params = c2.pop("parameters", None)
                    c2info_list.append(
                        PayloadBuilder.C2ProfileParameters(parameters=params, c2profile=c2)
                    )
                commands = PayloadBuilder.CommandList(message_json["commands"])
                for cls in PayloadBuilder.PayloadType.__subclasses__():
                    agent_builder = cls(
                        uuid=message_json["uuid"],
                        agent_code_path=Path(container_files_path),
                        c2info=c2info_list,
                        selected_os=message_json["selected_os"],
                        commands=commands,
                        wrapped_payload=message_json["wrapped_payload"],
                    )
                try:
                    await agent_builder.set_and_validate_build_parameters(
                        message_json["build_parameters"]
                    )
                    build_resp = await agent_builder.build()
                except Exception as b:
                    resp_message = {
                        "status": "error",
                        "message": "Error in agent creation: "
                        + str(traceback.format_exc()),
                        "payload": "",
                    }
                    await send_status(
                        message=json.dumps(resp_message),
                        command="create_payload_with_code",
                        status="error",
                        reference_id=reference_id,
                        username=username,
                    )
                    return
                # we want to capture the build message as build_resp.get_message()
                # we also want to capture the final values the agent used for creating the payload, so collect them
                build_instances = agent_builder.get_build_instance_values()
                resp_message = {
                    "status": build_resp.get_status().value,
                    "message": build_resp.get_message(),
                    "build_parameter_instances": build_instances,
                    "payload": base64.b64encode(build_resp.get_payload()).decode(
                        "utf-8"
                    ),
                }
                await send_status(
                    message=json.dumps(resp_message),
                    command="create_payload_with_code",
                    reference_id=reference_id,
                    status="success",
                    username=username,
                )

            except Exception as e:
                resp_message = {
                    "status": "error",
                    "message": str(traceback.format_exc()),
                    "payload": "",
                }
                await send_status(
                    message=json.dumps(resp_message),
                    command="create_payload_with_code",
                    status="error",
                    reference_id=reference_id,
                    username=username,
                )
        elif command == "command_transform":
            try:
                # pt.task.PAYLOAD_TYPE.command_transform.taskID
                
                message_json = json.loads(
                    base64.b64decode(message.body).decode("utf-8"), strict=False
                )
                final_task = None
                for cls in MythicCommandBase.CommandBase.__subclasses__():
                    if getattr(cls, "cmd") == message_json["command"]:
                        Command = cls(Path(container_files_path))
                        task = MythicCommandBase.MythicTask(
                            message_json["task"],
                            args=Command.argument_class(message_json["params"]),
                        )
                        await task.args.parse_arguments()
                        await task.args.verify_required_args_have_values()
                        if 'opsec_class' in dir(Command) and Command.opsec_class is not None and callable(Command.opsec_class.opsec_pre):
                            # the opsec_pre function is defined
                            if task.opsec_pre_blocked is None:
                                # this means we haven't run the function to see if it's been blocked or not
                                #   opsec_pre updates task itself
                                await Command.opsec_class().opsec_pre(task)
                                # send the results of the check
                                await send_status(
                                    message=str(task),
                                    command="command_transform",
                                    status="opsec_pre",
                                    reference_id=reference_id,
                                    username=username
                                )
                                if task.opsec_pre_blocked is True:
                                    # the opsec_pre function decided to block the task
                                    if task.opsec_pre_bypassed is False:
                                        # and not provide a bypass
                                        return
                            elif task.opsec_pre_blocked is True and not task.opsec_pre_bypassed:
                                # we already sent our opsec_pre data, we're blocked and not bypassed, just return
                                return
                        final_task = await Command.create_tasking(task)
                        if "opsec_class" in dir(Command) and Command.opsec_class is not None and callable(Command.opsec_class.opsec_post):
                            # the opsec_post function is defined
                            if task.opsec_post_blocked is None:
                                # this means we haven't run the function to see if it's been blocked or not
                                #   opsec_post updates task itself
                                await Command.opsec_class().opsec_post(task)
                                # send the results of the check
                                await send_status(
                                    message=str(task),
                                    command="command_transform",
                                    status="opsec_post",
                                    reference_id=reference_id,
                                    username=username
                                )
                        if task.opsec_post_blocked is True and not task.opsec_post_bypassed:
                            # if we ran our create_tasking, then opsec and we were blocked but not bypassed
                            #   then make sure we report that the tasking status shoudln't be "submitted"
                            await send_status(
                                message=str(final_task),
                                command="command_transform",
                                status="opsec_post",
                                reference_id=reference_id,
                                username=username
                            )
                        else:
                            await send_status(
                                message=str(final_task),
                                command="command_transform",
                                status=final_task.status.value,
                                reference_id=reference_id,
                                username=username
                            )
                        
                        break
                if final_task is None:
                    await send_status(
                        message="Failed to find class where command_name = "
                        + message_json["command"],
                        command="command_transform",
                        status="error",
                        reference_id=reference_id,
                        username=username
                    )
            except Exception as e:
                await send_status(
                    message="[-] Mythic error while creating/running create_tasking: \n"
                    + str(e),
                    command="command_transform",
                    status="error",
                    reference_id=reference_id,
                    username=username
                )
                return
        elif command == "sync_classes":
            await sync_classes(reference_id)
        elif command == "process_container":
            try:
                # pt.task.PAYLOAD_TYPE.command_transform.taskID
                message_json = json.loads(message.body)
                final_task = None
                for cls in MythicCommandBase.CommandBase.__subclasses__():
                    if getattr(cls, "cmd") == message_json["command"]:
                        Command = cls(Path(container_files_path))
                        task = MythicCommandBase.MythicTask(
                            message_json["task"],
                            args=Command.argument_class(message_json["params"]),
                        )
                        await task.args.parse_arguments()
                        agentResponse = MythicCommandBase.AgentResponse(task=task, response=message_json["response"])
                        await Command.process_response(agentResponse)
                        break
            except Exception as e:
                await send_status(
                    message="[-] Mythic error while running process_response: \n"
                    + str(e),
                    command="process_container",
                    status="error",
                    reference_id=reference_id,
                    username=username
                )
                return
        else:
            print("Unknown command: {}".format(command))


async def sync_classes(reference_id: str = ""):
    try:
        commands = {}
        payload_type = {}
        import_all_agent_functions()
        for cls in PayloadBuilder.PayloadType.__subclasses__():
            payload_type = cls(agent_code_path=Path(container_files_path)).to_json()
            break
        for cls in MythicCommandBase.CommandBase.__subclasses__():
            commands[cls.cmd] = cls(Path(container_files_path)).to_json()
        payload_type["commands"] = commands
        await send_status(json.dumps(payload_type), command="sync_classes", status="success", username="", reference_id=reference_id)
    except Exception as e:
        print(str(traceback.format_exc()))
        sys.stdout.flush()
        await send_status(
            message="Error while syncing info: " + str(traceback.format_exc()),
            command="sync_classes",
            status="error",
            username="",
            reference_id=reference_id
        )
        sys.exit(1)


async def heartbeat():
    config_file = open("rabbitmq_config.json", "rb")
    main_config = json.loads(config_file.read().decode("utf-8"))
    config_file.close()
    if main_config["name"] == "hostname":
        hostname = socket.gethostname()
    else:
        hostname = main_config["name"]
    while True:
        try:
            connection = await aio_pika.connect_robust(
                host=main_config["host"],
                login=main_config["username"],
                password=main_config["password"],
                virtualhost=main_config["virtual_host"],
            )
            channel = await connection.channel()
            # declare our heartbeat exchange that everybody will publish to, but only the mythic server will are about
            exchange = await channel.declare_exchange(
                "mythic_traffic", aio_pika.ExchangeType.TOPIC
            )
        except Exception as e:
            print(str(e))
            await asyncio.sleep(2)
            continue
        while True:
            try:
                # routing key is ignored for fanout, it'll go to anybody that's listening, which will only be the server
                await exchange.publish(
                    aio_pika.Message("heartbeat".encode()),
                    routing_key="pt.heartbeat.{}.{}".format(hostname, container_version),
                )
                await asyncio.sleep(10)
            except Exception as e:
                print(str(e))
                # if we get an exception here, break out to the bigger loop and try to connect again
                break


async def mythic_service():
    global hostname
    global exchange
    global container_files_path
    connection = None
    config_file = open("rabbitmq_config.json", "rb")
    main_config = json.loads(config_file.read().decode("utf-8"))
    config_file.close()
    if main_config["name"] == "hostname":
        hostname = socket.gethostname()
    else:
        hostname = main_config["name"]
    container_files_path = os.path.abspath(main_config["container_files_path"])
    if not os.path.exists(container_files_path):
        os.makedirs(container_files_path)
    while connection is None:
        try:
            connection = await aio_pika.connect_robust(
                host=main_config["host"],
                login=main_config["username"],
                password=main_config["password"],
                virtualhost=main_config["virtual_host"],
            )
        except Exception as e:
            await asyncio.sleep(1)
    try:
        channel = await connection.channel()
        # declare our exchange
        exchange = await channel.declare_exchange(
            "mythic_traffic", aio_pika.ExchangeType.TOPIC
        )
        # get a random queue that only the mythic server will use to listen on to catch all heartbeats
        queue = await channel.declare_queue("", exclusive=True)
        # bind the queue to the exchange so we can actually catch messages
        await queue.bind(
            exchange="mythic_traffic", routing_key="pt.task.{}.#".format(hostname)
        )
        # just want to handle one message at a time so we can clean up and be ready
        await channel.set_qos(prefetch_count=100)
        print(" [*] Waiting for messages in mythic_service with version {}.".format(container_version))
        task = queue.consume(callback)
        await sync_classes()
        result = await asyncio.wait_for(task, None)
    except Exception as e:
        print(str(e))


# start our service
def start_service_and_heartbeat():
    loop = asyncio.get_event_loop()
    asyncio.gather(heartbeat(), mythic_service())
    loop.run_forever()
