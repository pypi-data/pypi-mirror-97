#  tgcalls - Python binding for tgcalls (c++ lib by Telegram)
#  pytgcalls - library connecting python binding for tgcalls and pyrogram
#  Copyright (C) 2020-2021 Il`ya (Marshal) <https://github.com/MarshalX>
#
#  This file is part of tgcalls and pytgcalls.
#
#  tgcalls and pytgcalls is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  tgcalls and pytgcalls is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License v3
#  along with tgcalls. If not, see <http://www.gnu.org/licenses/>.

import asyncio
import json
from typing import Callable, List, Union

import pyrogram
from pyrogram import raw
from pyrogram.errors import BadRequest
from pyrogram.handlers import RawUpdateHandler
from pyrogram.raw import functions, types
from pyrogram.raw.types import InputPeerChannel, InputPeerChat

import tgcalls

uint_ssrcs = lambda ssrcs: ssrcs if ssrcs >= 0 else ssrcs + 2 ** 32
int_ssrcs = lambda ssrcs: ssrcs if ssrcs < 2**31 else ssrcs - 2 ** 32


def parse_call_participant(participant_data):
    native_participant = tgcalls.GroupParticipantDescription()

    native_participant.audioSsrc = uint_ssrcs(participant_data.source)
    native_participant.isRemoved = participant_data.left

    return native_participant


class GroupCallNative:
    SEND_ACTION_UPDATE_EACH = 0.45

    def __init__(
            self,
            client: pyrogram.Client,
            enable_logs_to_console: bool,
            path_to_log_file: str
    ):
        self.client = client

        self.native_instance = self.__setup_native_instance()

        self.me = None
        self.group_call = None

        self.chat_peer = None
        self.full_chat = None

        self.my_ssrc = None

        self.enable_action = True
        self.enable_logs_to_console = enable_logs_to_console
        self.path_to_log_file = path_to_log_file

        self.is_connected = False

        self.update_to_handler = {
            types.UpdateGroupCallParticipants: self._process_group_call_participants_update,
            types.UpdateGroupCall: self._process_group_call_update,
        }

        self._update_handler = RawUpdateHandler(self._process_update)
        self.client.add_handler(self._update_handler, -1)

    def __setup_native_instance(self):
        native_instance = tgcalls.NativeInstance()
        native_instance.setEmitJoinPayloadCallback(self.__emit_join_payload_callback)

        return native_instance

    async def _process_group_call_participants_update(self, update):
        ssrcs_to_remove = []
        for participant in update.participants:
            ssrcs = uint_ssrcs(participant.source)

            if participant.left:
                ssrcs_to_remove.append(ssrcs)
            elif participant.user_id == self.me.id and ssrcs != self.my_ssrc:
                await self.reconnect()

        if ssrcs_to_remove:
            self.native_instance.removeSsrcs(ssrcs_to_remove)

    async def _process_group_call_update(self, update):
        if update.call.params:
            await self.__set_join_response_payload(json.loads(update.call.params.data))

    async def _process_update(self, _, update, users, chats):
        if type(update) not in self.update_to_handler.keys():
            raise pyrogram.ContinuePropagation

        if not self.group_call or not update.call or update.call.id != self.group_call.id:
            raise pyrogram.ContinuePropagation
        self.group_call = update.call

        await self.update_to_handler[type(update)](update)

    async def get_me(self):
        self.me = await self.client.get_me()

        return self.me

    async def check_group_call(self) -> bool:
        if not self.group_call or not self.my_ssrc:
            return False

        try:
            in_group_call = (await (self.client.send(functions.phone.CheckGroupCall(
                call=self.group_call,
                source=int_ssrcs(self.my_ssrc)
            ))))
        except BadRequest as e:
            if e.x != '[400 GROUPCALL_JOIN_MISSING]':
                raise e

            in_group_call = False

        return in_group_call

    async def get_group_participants(self):
        return (await (self.client.send(functions.phone.GetGroupCall(
            call=self.full_chat.call
        )))).participants

    async def leave_current_group_call(self):
        if not self.full_chat.call or not self.my_ssrc:
            return

        response = await self.client.send(functions.phone.LeaveGroupCall(
            call=self.full_chat.call,
            source=int_ssrcs(self.my_ssrc)
        ))
        await self.client.handle_updates(response)

    async def get_group_call(self, group: Union[str, int, InputPeerChannel, InputPeerChat]):
        self.chat_peer = group
        if type(group) not in [InputPeerChannel, InputPeerChat]:
            self.chat_peer = await self.client.resolve_peer(group)

        if isinstance(self.chat_peer, InputPeerChannel):
            self.full_chat = (await (self.client.send(functions.channels.GetFullChannel(
                channel=self.chat_peer
            )))).full_chat
        elif isinstance(self.chat_peer, InputPeerChat):
            self.full_chat = (await (self.client.send(functions.messages.GetFullChat(
                chat_id=self.chat_peer.chat_id
            )))).full_chat

        if self.full_chat is None:
            raise RuntimeError(f'Can\'t get full chat by {group}')

        self.group_call = self.full_chat.call

        return self.group_call

    async def stop(self):
        await self.leave_current_group_call()
        self.native_instance.stopGroupCall()
        self.client.remove_handler(self._update_handler, -1)

        while self.is_connected:
            await asyncio.sleep(1)

        # TODO
        # del self.native_instance
        # self.native_instance = self.__setup_native_instance()

    async def start(self):
        raise NotImplementedError()

    async def reconnect(self):
        await self.stop()
        await self.start()

    async def _start_group_call(
            self,
            use_file_audio_device: bool,
            get_input_filename_callback: Callable,
            get_output_filename_callback: Callable
    ):
        self.native_instance.startGroupCall(
            self.enable_logs_to_console,
            self.path_to_log_file,

            use_file_audio_device,

            self.__network_state_updated_callback,
            self.__participant_descriptions_required_callback,
            get_input_filename_callback,
            get_output_filename_callback
        )

    def set_is_mute(self, is_muted: bool):
        self.native_instance.setIsMuted(is_muted)

    def restart_playout(self):
        self.native_instance.reinitAudioInputDevice()

    def restart_recording(self):
        self.native_instance.reinitAudioOutputDevice()

    def __participant_descriptions_required_callback(self, ssrcs_list: List[int]):
        def _(future):
            filtered_participants = [p for p in future.result() if p.source in ssrcs_list]
            participants = [parse_call_participant(p) for p in filtered_participants]
            self.native_instance.addParticipants(participants)

        call_participants = asyncio.ensure_future(self.get_group_participants(), loop=self.client.loop)
        call_participants.add_done_callback(_)

    def __network_state_updated_callback(self, state: bool):
        self.is_connected = state

        if self.is_connected:
            self.set_is_mute(False)
            if self.enable_action:
                self.__start_status_worker()

    async def audio_levels_updated_callback(self):
        pass  # TODO

    def __start_status_worker(self):
        async def worker():
            while self.is_connected:
                await self.send_speaking_group_call_action()
                await asyncio.sleep(self.SEND_ACTION_UPDATE_EACH)

        asyncio.ensure_future(worker(), loop=self.client.loop)

    async def send_speaking_group_call_action(self):
        await self.client.send(
            raw.functions.messages.SetTyping(
                peer=self.chat_peer,
                action=raw.types.SpeakingInGroupCallAction()
            )
        )

    async def __set_join_response_payload(self, params):
        params = params['transport']

        candidates = []
        for row_candidates in params.get('candidates', []):
            candidate = tgcalls.GroupJoinResponseCandidate()
            for key, value in row_candidates.items():
                setattr(candidate, key, value)

            candidates.append(candidate)

        fingerprints = []
        for row_fingerprint in params.get('fingerprints', []):
            fingerprint = tgcalls.GroupJoinPayloadFingerprint()
            for key, value in row_fingerprint.items():
                setattr(fingerprint, key, value)

            fingerprints.append(fingerprint)

        payload = tgcalls.GroupJoinResponsePayload()
        payload.ufrag = params.get('ufrag')
        payload.pwd = params.get('pwd')
        payload.fingerprints = fingerprints
        payload.candidates = candidates

        participants = [parse_call_participant(p) for p in await self.get_group_participants()]

        # TODO video payload
        self.native_instance.setJoinResponsePayload(payload, participants)

    def __emit_join_payload_callback(self, payload):
        if self.group_call is None:
            return

        self.my_ssrc = payload.ssrc

        fingerprints = [{
            'hash': f.hash,
            'setup': f.setup,
            'fingerprint': f.fingerprint
        } for f in payload.fingerprints]

        params = {
            'ufrag': payload.ufrag,
            'pwd': payload.pwd,
            'fingerprints': fingerprints,
            'ssrc': payload.ssrc
        }

        async def _():
            response = await self.client.send(functions.phone.JoinGroupCall(
                call=self.group_call,
                params=types.DataJSON(data=json.dumps(params)),
                muted=True
            ))
            await self.client.handle_updates(response)

        asyncio.ensure_future(_(), loop=self.client.loop)
